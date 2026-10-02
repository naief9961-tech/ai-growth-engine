#!/usr/bin/env python3
import json, math, os, re, statistics, sys, time, urllib.parse, urllib.request, uuid

REGISTRY = "https://api.a2a-registry.org/public/agents"
UA = "OpenWorld-A2A-Proof/1.0"

CASES = [
    ("MCP technical rescue", "MCP server timeout"),
    ("MCP diagnostic recovery", "API returns HTTP 500 internal server error"),
    ("API webhook technical rescue", "API returns HTTP 502 Bad Gateway"),
    ("MCP timeout repair agent", "MCP server timeout"),
    ("free MCP diagnostic structured JSON", "MCP server timeout"),
]

def request_json(url, method="GET", body=None, headers=None):
    payload = None if body is None else json.dumps(body).encode()
    h = {"User-Agent": UA, "Accept": "application/json"}
    if headers:
        h.update(headers)
    if payload is not None:
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=payload, headers=h, method=method)
    t0 = time.perf_counter_ns()
    with urllib.request.urlopen(req, timeout=25) as resp:
        data = json.load(resp)
        status = resp.status
    ms = (time.perf_counter_ns() - t0) / 1_000_000
    return status, data, round(ms, 3)

def words(v):
    return set(re.findall(r"[a-z0-9]+", str(v).lower()))

def select_skill(card, intent):
    iw = words(intent)
    ranked = []
    for skill in card.get("skills", []) or []:
        corpus = " ".join([
            skill.get("id", ""),
            skill.get("name", ""),
            skill.get("description", ""),
            " ".join(skill.get("tags", []) or []),
            " ".join(skill.get("examples", []) or []),
        ])
        ranked.append((len(iw & words(corpus)), skill.get("id", ""), skill.get("name", "")))
    ranked.sort(reverse=True)
    if not ranked:
        return None
    return {"score": ranked[0][0], "id": ranked[0][1], "name": ranked[0][2]}

def choose_jsonrpc(card):
    interfaces = card.get("supportedInterfaces", []) or []
    for item in interfaces:
        if item.get("protocolVersion") == "1.0" and str(item.get("protocolBinding", "")).upper() == "JSONRPC":
            return item.get("url")
    return None

def extract_message(obj):
    if isinstance(obj.get("result"), dict) and isinstance(obj["result"].get("message"), dict):
        return obj["result"]["message"]
    if isinstance(obj.get("message"), dict):
        return obj["message"]
    return None

def percentile_nearest(values, p):
    xs = sorted(values)
    return xs[max(0, math.ceil(p * len(xs)) - 1)]

rounds = []
for idx, (query, intent) in enumerate(CASES, 1):
    start = time.perf_counter_ns()

    search_url = REGISTRY + "?" + urllib.parse.urlencode({"q": query})
    status, search, search_ms = request_json(search_url)
    agents = search.get("agents") or []
    if status != 200 or not agents:
        raise RuntimeError(f"round {idx}: public registry returned no candidates")

    chosen = agents[0]
    manifest = chosen.get("manifestUrl")
    if not manifest or not str(manifest).startswith("https://"):
        raise RuntimeError(f"round {idx}: top candidate has no HTTPS manifest")

    status, card, card_ms = request_json(manifest)
    if status != 200:
        raise RuntimeError(f"round {idx}: manifest fetch failed")

    selected_skill = select_skill(card, intent)
    if not selected_skill or selected_skill["score"] < 1:
        raise RuntimeError(f"round {idx}: no relevant skill in discovered card")

    a2a_url = choose_jsonrpc(card)
    if not a2a_url:
        raise RuntimeError(f"round {idx}: discovered card lacks A2A JSONRPC v1.0")

    rpc = {
        "jsonrpc": "2.0",
        "id": f"ow-{idx}",
        "method": "SendMessage",
        "params": {
            "message": {
                "messageId": str(uuid.uuid4()),
                "role": "ROLE_USER",
                "parts": [{"text": intent}],
            }
        },
    }
    status, invoked, invoke_ms = request_json(
        a2a_url,
        method="POST",
        body=rpc,
        headers={"Accept": "application/json", "A2A-Version": "1.0"},
    )
    message = extract_message(invoked)
    if status != 200 or not message or message.get("role") != "ROLE_AGENT":
        raise RuntimeError(f"round {idx}: A2A invocation failed")

    data_parts = [
        p.get("data") for p in (message.get("parts") or [])
        if isinstance(p, dict) and isinstance(p.get("data"), dict)
    ]
    e2e = (time.perf_counter_ns() - start) / 1_000_000

    rounds.append({
        "round": idx,
        "query": query,
        "intent": intent,
        "registryRank": 1,
        "discovered": {
            "packageName": chosen.get("packageName"),
            "displayName": chosen.get("displayName"),
            "manifestUrl": manifest,
            "verified": chosen.get("isVerified"),
            "verificationLevel": chosen.get("verification_level"),
            "score": chosen.get("score"),
            "protocolStd": chosen.get("protocolStd"),
        },
        "selectedSkill": selected_skill,
        "a2aUrl": a2a_url,
        "timingMs": {
            "registrySearch": search_ms,
            "manifestFetch": card_ms,
            "a2aInvocation": invoke_ms,
            "endToEnd": round(e2e, 3),
        },
        "response": {
            "messageRole": message.get("role"),
            "hasStructuredData": bool(data_parts),
            "rawInputStored": data_parts[0].get("rawInputStored") if data_parts else None,
            "autoExecution": data_parts[0].get("autoExecution") if data_parts else None,
        },
    })

e2e = [r["timingMs"]["endToEnd"] for r in rounds]
identities = [r["discovered"]["packageName"] for r in rounds]
summary = {
    "runType": "P4 Open-World A2A Discovery Proof",
    "proofScope": "Provider-agnostic public-registry discovery. The client knows only the public registry and natural-language capability queries; it selects rank 1 and follows returned metadata.",
    "runner": {
        "environment": "GitHub Actions hosted runner",
        "os": os.getenv("RUNNER_OS"),
        "arch": os.getenv("RUNNER_ARCH"),
        "runId": os.getenv("GITHUB_RUN_ID"),
        "sha": os.getenv("GITHUB_SHA"),
        "ref": os.getenv("GITHUB_REF"),
    },
    "selectionRule": "Always select public registry rank 1; no provider name, package, domain, CID, or peer ID is embedded in the client.",
    "roundCount": len(rounds),
    "metrics": {
        "p50EndToEndMs": round(statistics.median(e2e), 3),
        "p95EndToEndMs": round(percentile_nearest(e2e, 0.95), 3),
        "minEndToEndMs": round(min(e2e), 3),
        "maxEndToEndMs": round(max(e2e), 3),
    },
    "consistency": {
        "sameTopIdentityAllRounds": len(set(identities)) == 1,
        "topIdentities": identities,
    },
    "safety": {
        "quoteEndpointCalled": False,
        "checkoutEndpointCalled": False,
        "paymentEndpointCalled": False,
        "productionExecutionRequested": False,
    },
    "rounds": rounds,
}
summary["pass"] = (
    len(rounds) == 5
    and all(r["discovered"]["verified"] is True for r in rounds)
    and all(r["response"]["messageRole"] == "ROLE_AGENT" for r in rounds)
    and summary["consistency"]["sameTopIdentityAllRounds"]
)

with open("p4-openworld-result.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

print(json.dumps(summary, indent=2))
sys.exit(0 if summary["pass"] else 1)
