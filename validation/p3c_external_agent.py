#!/usr/bin/env python3
import json, math, os, re, statistics, sys, time, urllib.request, uuid

BASE = "https://naifgravity.com"
CARD = BASE + "/.well-known/agent-card.json"
COMMERCE = BASE + "/.well-known/naif-agent.json"
A2A = BASE + "/a2a/v1/message:send"
UA = "NAIF-P3C-GitHubActions-ExternalAgent/1.0"

INTENTS = [
    "MCP server timeout",
    "API returns HTTP 500 internal server error",
    "API returns HTTP 502 Bad Gateway",
    "API returns HTTP 401 authentication required",
    "API returns HTTP 403 forbidden",
]

def req_json(url, method="GET", body=None, accept="application/json"):
    data = None if body is None else json.dumps(body).encode()
    headers = {
        "User-Agent": UA,
        "Accept": accept,
    }
    if data is not None:
        headers["Content-Type"] = "application/json"
    if "/a2a/" in url:
        headers["A2A-Version"] = "1.0"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    t0 = time.perf_counter_ns()
    with urllib.request.urlopen(request, timeout=20) as response:
        payload = json.load(response)
        status = response.status
    ms = (time.perf_counter_ns() - t0) / 1_000_000
    return status, payload, round(ms, 3)

def words(value):
    return set(re.findall(r"[a-z0-9]+", str(value).lower()))

def select_skill(card, intent):
    iw = words(intent)
    best = None
    for skill in card.get("skills", []):
        corpus = " ".join([
            skill.get("id", ""),
            skill.get("name", ""),
            skill.get("description", ""),
            " ".join(skill.get("tags", []) or []),
            " ".join(skill.get("examples", []) or []),
        ])
        sw = words(corpus)
        score = len(iw & sw)
        row = (score, skill.get("id", ""), skill.get("name", ""))
        if best is None or row > best:
            best = row
    return {"score": best[0], "id": best[1], "name": best[2]} if best else None

def first_data(message):
    for part in message.get("parts", []):
        if isinstance(part, dict) and isinstance(part.get("data"), dict):
            return part["data"]
    return {}

def percentile_nearest(values, p):
    xs = sorted(values)
    return xs[max(0, math.ceil(p * len(xs)) - 1)]

results = []
for i, intent in enumerate(INTENTS, 1):
    round_start = time.perf_counter_ns()

    s, card, card_ms = req_json(CARD)
    if s != 200:
        raise RuntimeError(f"round {i}: agent card HTTP {s}")
    selected = select_skill(card, intent)
    if not selected or selected["score"] < 1:
        raise RuntimeError(f"round {i}: no card skill selected")
    discovery_ms = (time.perf_counter_ns() - round_start) / 1_000_000

    s, commerce, commerce_ms = req_json(COMMERCE)
    if s != 200 or not commerce.get("probe"):
        raise RuntimeError(f"round {i}: commerce manifest missing probe")

    message_id = str(uuid.uuid4())
    a2a_body = {
        "message": {
            "messageId": message_id,
            "role": "ROLE_USER",
            "parts": [{"text": intent}],
        }
    }
    s, a2a, a2a_ms = req_json(
        A2A, method="POST", body=a2a_body, accept="application/a2a+json"
    )
    if s != 200 or a2a.get("message", {}).get("role") != "ROLE_AGENT":
        raise RuntimeError(f"round {i}: invalid A2A response")

    resolved = first_data(a2a["message"])
    matches = resolved.get("matches") or []
    if not matches:
        raise RuntimeError(f"round {i}: no FixGraph match for {intent!r}")
    product_id = (
        ((matches[0].get("repairPacket") or {}).get("paidFix") or {}).get("productId")
    )
    if not product_id:
        raise RuntimeError(f"round {i}: matched record has no productId")

    catalog_url = BASE + commerce.get("catalog", "/api/agent/catalog")
    s, catalog, catalog_ms = req_json(catalog_url)
    product_ids = {p.get("id") for p in catalog.get("products", [])}
    if product_id not in product_ids:
        raise RuntimeError(f"round {i}: matched product absent from public catalog: {product_id}")

    probe_url = BASE + commerce["probe"]
    probe_body = {
        "productId": product_id,
        "source": f"p3c-gha-r{i}",
        "input": {
            "message": intent,
            "selectedSkill": selected["id"],
            "externalAgentProof": True,
        },
    }
    s, probe, probe_ms = req_json(probe_url, method="POST", body=probe_body)
    if s != 200 or not probe.get("probeId"):
        raise RuntimeError(f"round {i}: free probe failed")
    safety = {
        "quoteCreated": probe.get("quoteCreated"),
        "automaticCheckout": probe.get("automaticCheckout"),
        "automaticPayment": probe.get("automaticPayment"),
        "automaticExecution": probe.get("automaticExecution"),
    }
    if any(v is not False for v in safety.values()):
        raise RuntimeError(f"round {i}: unsafe probe flags: {safety}")

    e2e_ms = (time.perf_counter_ns() - round_start) / 1_000_000
    results.append({
        "round": i,
        "intent": intent,
        "selectedSkill": selected,
        "productId": product_id,
        "messageId": message_id,
        "probeId": probe["probeId"],
        "timingMs": {
            "cardFetch": card_ms,
            "discovery": round(discovery_ms, 3),
            "commerceManifest": commerce_ms,
            "a2aResolve": a2a_ms,
            "catalog": catalog_ms,
            "freeProbe": probe_ms,
            "endToEnd": round(e2e_ms, 3),
        },
        "safety": safety,
        "rawInputStored": resolved.get("rawInputStored"),
        "autoExecution": resolved.get("autoExecution"),
    })

e2e = [r["timingMs"]["endToEnd"] for r in results]
p50 = round(statistics.median(e2e), 3)
p95 = round(percentile_nearest(e2e, 0.95), 3)
summary = {
    "runType": "NAIF P3-C External Agent Discovery + Free Probe Proof",
    "proofScope": "known-origin public A2A Agent Card discovery/selection/invocation from an external GitHub-hosted runner; not open-world registry discovery",
    "runner": {
        "environment": "GitHub Actions hosted runner",
        "os": os.getenv("RUNNER_OS"),
        "arch": os.getenv("RUNNER_ARCH"),
        "runId": os.getenv("GITHUB_RUN_ID"),
        "sha": os.getenv("GITHUB_SHA"),
        "ref": os.getenv("GITHUB_REF"),
    },
    "roundCount": len(results),
    "criteria": {"p50MsLt": 30000, "p95MsLt": 60000},
    "metrics": {
        "p50EndToEndMs": p50,
        "p95EndToEndMs": p95,
        "minEndToEndMs": round(min(e2e), 3),
        "maxEndToEndMs": round(max(e2e), 3),
    },
    "safety": {
        "realPayment": False,
        "quoteEndpointCalled": False,
        "checkoutEndpointCalled": False,
        "paymentEndpointCalled": False,
        "productionExecutionRequested": False,
    },
    "rounds": results,
}
summary["pass"] = (
    summary["roundCount"] >= 5
    and p50 < 30000
    and p95 < 60000
    and all(r["rawInputStored"] is False and r["autoExecution"] is False for r in results)
)
with open("p3c-result.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)
print(json.dumps(summary, indent=2))
sys.exit(0 if summary["pass"] else 1)
