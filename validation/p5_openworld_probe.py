#!/usr/bin/env python3
import json, os, re, statistics, time, urllib.parse, urllib.request, uuid

REGISTRY="https://api.a2a-registry.org/public/agents"
INTENTS=[
 "MCP server timeout",
 "MCP server timeout error",
 "MCP server request timeout",
 "MCP timeout while loading tools",
 "MCP tool server timeout",
]

def fetch(url, body=None, extra=None):
    data=None if body is None else json.dumps(body).encode()
    h={"User-Agent":"OpenWorld-P5-Proof/1.0","Accept":"application/json"}
    if extra: h.update(extra)
    if data is not None: h["Content-Type"]="application/json"
    req=urllib.request.Request(url,data=data,headers=h,method="POST" if data else "GET")
    t=time.perf_counter()
    with urllib.request.urlopen(req,timeout=20) as r:
        out=json.load(r)
    return out, round((time.perf_counter()-t)*1000,3)

def toks(v):
    return set(re.findall(r"[a-z0-9]+",str(v).lower()))

def card_score(card,intent):
    q=toks(intent); best=0
    for s in card.get("skills",[]) or []:
        ex=s.get("examples") or []
        blob=" ".join([s.get("name",""),s.get("description","")," ".join(s.get("tags") or [])," ".join(ex)])
        st=toks(blob); v=20*len(q&st)
        if intent.lower() in " ".join(ex).lower(): v+=1000
        for e in ex:
            et=toks(e)
            if et:
                sh=len(q&et)
                v=max(v,int(600*sh/max(1,len(q))+400*sh/max(1,len(et))))
                if et<=q: v=max(v,800+25*len(et))
        if "mcp" in q and "mcp" in st: v+=100
        if "timeout" in q and "timeout" in st: v+=100
        best=max(best,v)
    return best

def product_score(p,intent):
    q=toks(intent)
    blob=" ".join(str(p.get(k,"")) for k in ("id","name","input","output","demo"))
    pt=toks(blob); v=20*len(q&pt)
    if "mcp" in q and "mcp" in pt: v+=150
    if "timeout" in q and ({"health","endpoint","debug","diagnostic"} & pt): v+=80
    return v

def urls_from(texts):
    out=[]
    for t in texts:
        for u in re.findall(r"https?://[^\s]+",t):
            u=u.rstrip(".,;:)]}")
            if u not in out: out.append(u)
    return out

rounds=[]
for n,intent in enumerate(INTENTS,1):
    start=time.perf_counter()
    reg,reg_ms=fetch(REGISTRY+"?"+urllib.parse.urlencode({"q":intent}))
    rows=reg.get("agents") or reg.get("items") or reg.get("data") or []
    cand=[]
    for row in rows[:15]:
        manifest=row.get("manifestUrl")
        if not manifest: continue
        try: card,card_ms=fetch(manifest)
        except Exception: continue
        cand.append((card_score(card,intent),manifest,card,card_ms))
    if not cand: raise RuntimeError("no readable registry candidates")
    cand.sort(key=lambda x:x[0],reverse=True)
    score,manifest,card,card_ms=cand[0]
    iface=next((x for x in card.get("supportedInterfaces",[]) if str(x.get("protocolBinding","")).upper()=="JSONRPC"),None)
    if not iface or not iface.get("url"): raise RuntimeError("selected agent has no JSONRPC A2A interface")

    payload={"jsonrpc":"2.0","id":n,"method":"SendMessage","params":{"message":{
      "messageId":str(uuid.uuid4()),"role":"ROLE_USER","parts":[{"text":intent}]
    }}}
    a2a,a2a_ms=fetch(iface["url"],payload,{"A2A-Version":"1.0"})
    msg=(a2a.get("result") or {}).get("message") or a2a.get("message") or {}
    texts=[p.get("text") for p in msg.get("parts",[]) if isinstance(p,dict) and isinstance(p.get("text"),str)]
    if a2a.get("error") or msg.get("role")!="ROLE_AGENT" or not texts:
        raise RuntimeError("invalid A2A response")

    links=urls_from(texts)
    catalog_url=next((u for u in links if "catalog" in u.lower()),None)
    probe_url=next((u for u in links if "probe" in u.lower()),None)
    if not catalog_url or not probe_url:
        raise RuntimeError("A2A reply did not expose machine-readable catalog/probe links")

    catalog,catalog_ms=fetch(catalog_url)
    products=[p for p in (catalog.get("products") or []) if p.get("id") and p.get("machineCheckout") is False]
    if not products: raise RuntimeError("no safe catalog products")
    ranked=sorted(products,key=lambda p:(product_score(p,intent),-float(p.get("price") or 0)),reverse=True)
    product=ranked[0]
    if product_score(product,intent)<=0: raise RuntimeError("no relevant product")

    body={"productId":product["id"],"source":f"p5-ow-gha-r{n}","input":{
      "message":intent,"externalOpenWorldProof":True
    }}
    probe,probe_ms=fetch(probe_url,body)
    if not probe.get("probeId"): raise RuntimeError("free probe did not return probeId")
    safety={
      "quoteCreated":probe.get("quoteCreated"),
      "automaticCheckout":probe.get("automaticCheckout"),
      "automaticPayment":probe.get("automaticPayment"),
      "automaticExecution":probe.get("automaticExecution"),
    }
    if any(v is not False for v in safety.values()):
        raise RuntimeError("unsafe probe flags")

    rounds.append({
      "round":n,"intent":intent,"status":"PASS","registryCandidates":len(rows),
      "selectedAgent":{"name":card.get("name"),"manifestUrl":manifest,"score":score,"endpoint":iface["url"]},
      "selectedProduct":{"id":product["id"],"name":product.get("name"),"score":product_score(product,intent)},
      "probeId":probe["probeId"],"safety":safety,
      "timingMs":{"registry":reg_ms,"card":card_ms,"a2a":a2a_ms,"catalog":catalog_ms,"probe":probe_ms,
                  "e2e":round((time.perf_counter()-start)*1000,3)}
    })

vals=[x["timingMs"]["e2e"] for x in rounds]
res={
 "runType":"P5 Open-World Discovery to Free Probe Proof",
 "proofScope":"Natural-intent public-registry discovery; target identity/domain/product/probe endpoint are not discovery inputs.",
 "runner":{"runId":os.getenv("GITHUB_RUN_ID"),"os":os.getenv("RUNNER_OS"),"arch":os.getenv("RUNNER_ARCH"),"ref":os.getenv("GITHUB_REF")},
 "rounds":rounds,
 "p50Ms":round(statistics.median(vals),3),
 "maxMs":round(max(vals),3),
 "safety":{"quoteCalled":False,"checkoutCalled":False,"paymentCalled":False,"executionRequested":False},
 "pass":len(rounds)==5
}
open("p5-openworld-probe-result.json","w").write(json.dumps(res,indent=2))
print(json.dumps(res,indent=2))
