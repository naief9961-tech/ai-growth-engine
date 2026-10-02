#!/usr/bin/env python3
import json, os, re, statistics, time, urllib.parse, urllib.request, uuid

REGISTRY = "https://api.a2a-registry.org/public/agents"
INTENTS = [
    "MCP server timeout",
    "MCP server timeout error",
    "MCP server request timeout",
    "MCP timeout while loading tools",
    "MCP tool server timeout",
]

def fetch(url, body=None, extra=None):
    data = None if body is None else json.dumps(body).encode()
    headers = {"User-Agent":"OpenWorld-A2A-Proof/1.1","Accept":"application/json"}
    if extra:
        headers.update(extra)
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=20) as resp:
        out = json.load(resp)
    return out, round((time.perf_counter()-t0)*1000, 3)

def tokens(value):
    return set(re.findall(r"[a-z0-9]+", str(value).lower()))

def card_score(card, intent):
    qt = tokens(intent)
    best = 0
    for skill in card.get("skills", []) or []:
        examples = skill.get("examples") or []
        blob = " ".join([
            skill.get("name",""), skill.get("description",""),
            " ".join(skill.get("tags") or []), " ".join(examples)
        ])
        st = tokens(blob)
        overlap = len(qt & st)
        score = 20 * overlap
        if intent.lower() in " ".join(examples).lower():
            score += 1000
        for example in examples:
            et = tokens(example)
            if not et:
                continue
            shared = len(qt & et)
            query_coverage = shared / max(1, len(qt))
            example_coverage = shared / max(1, len(et))
            score = max(score, int(600 * query_coverage + 400 * example_coverage))
            if et <= qt:
                score = max(score, 800 + 25 * len(et))
        if "mcp" in qt and "mcp" in st:
            score += 100
        if "timeout" in qt and "timeout" in st:
            score += 100
        best = max(best, score)
    return best

rounds = []
for number, intent in enumerate(INTENTS, 1):
    t0 = time.perf_counter()
    try:
        reg, registry_ms = fetch(REGISTRY + "?" + urllib.parse.urlencode({"q":intent}))
        rows = reg.get("agents") or reg.get("items") or reg.get("data") or []
        candidates = []
        for row in rows[:15]:
            manifest = row.get("manifestUrl")
            if not manifest:
                continue
            try:
                card, card_ms = fetch(manifest)
            except Exception:
                continue
            candidates.append((card_score(card,intent), manifest, card, card_ms))
        if not candidates:
            raise RuntimeError("no readable candidates")
        candidates.sort(key=lambda x:x[0], reverse=True)
        top3 = [{"score":x[0],"name":x[2].get("name"),"manifestUrl":x[1]} for x in candidates[:3]]
        score, manifest, card, card_ms = candidates[0]
        print("ROUND",number,"INTENT",intent,"TOP3",json.dumps(top3))
        print("ROUND",number,"SELECTED",card.get("name"),manifest,"SCORE",score)
        iface = next((x for x in card.get("supportedInterfaces",[]) if str(x.get("protocolBinding","")).upper()=="JSONRPC"), None)
        if not iface or not iface.get("url"):
            raise RuntimeError("selected agent has no JSONRPC interface")
        payload = {"jsonrpc":"2.0","id":number,"method":"SendMessage","params":{"message":{
            "messageId":str(uuid.uuid4()),"role":"ROLE_USER","parts":[{"text":intent}]
        }}}
        response, invoke_ms = fetch(iface["url"], payload, {"A2A-Version":"1.0"})
        message = (response.get("result") or {}).get("message") or response.get("message") or {}
        texts = [p.get("text") for p in message.get("parts",[]) if isinstance(p,dict) and isinstance(p.get("text"),str)]
        ok = not response.get("error") and message.get("role")=="ROLE_AGENT" and any(x.strip() for x in texts)
        print("ROUND",number,"ROLE",message.get("role"),"TEXT",json.dumps(texts)[:1200],"OK",ok)
        if not ok:
            raise RuntimeError("invalid A2A response")
        rounds.append({
            "round":number,"intent":intent,"status":"PASS","registryCandidates":len(rows),"top3":top3,
            "selected":{"name":card.get("name"),"manifestUrl":manifest,"score":score,"endpoint":iface["url"]},
            "replyText":texts,
            "timingMs":{"registry":registry_ms,"card":card_ms,"invoke":invoke_ms,"e2e":round((time.perf_counter()-t0)*1000,3)}
        })
    except Exception as exc:
        rounds.append({"round":number,"intent":intent,"status":"FAIL","reason":repr(exc),"timingMs":{"e2e":round((time.perf_counter()-t0)*1000,3)}})
        print("ROUND",number,"FAIL",repr(exc))
        break

vals = [r["timingMs"]["e2e"] for r in rounds if r.get("status")=="PASS"]
result = {
    "runType":"P4 Open-World A2A Proof",
    "proofScope":"Public-registry search from natural intent; target identity/domain/CID/peer ID are not selection inputs.",
    "runner":{"runId":os.getenv("GITHUB_RUN_ID"),"os":os.getenv("RUNNER_OS"),"arch":os.getenv("RUNNER_ARCH"),"ref":os.getenv("GITHUB_REF")},
    "rounds":rounds,
    "p50Ms":round(statistics.median(vals),3) if vals else None,
    "maxMs":round(max(vals),3) if vals else None,
}
result["pass"] = len(rounds)==5 and all(r.get("status")=="PASS" for r in rounds)
with open("p4-openworld-result.json","w") as fh:
    json.dump(result,fh,indent=2)
print(json.dumps(result,indent=2))
raise SystemExit(0 if result["pass"] else 1)
