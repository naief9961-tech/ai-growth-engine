#!/usr/bin/env python3
import json,re,urllib.parse,urllib.request,uuid,time,statistics,os

R="https://api.a2a-registry.org/public/agents"
I=[
"MCP server timeout",
"MCP server timeout error",
"MCP server request timeout",
"MCP timeout while loading tools",
"MCP tool server timeout"
]
def get(u,body=None,h=None):
 d=None if body is None else json.dumps(body).encode()
 x={"User-Agent":"OpenWorld-A2A-Proof/1.0","Accept":"application/json"}
 if h:x.update(h)
 if d:x["Content-Type"]="application/json"
 t=time.perf_counter()
 q=urllib.request.Request(u,data=d,headers=x,method="POST" if d else "GET")
 with urllib.request.urlopen(q,timeout=20) as z:o=json.load(z)
 return o,(time.perf_counter()-t)*1000
def tok(s):return set(re.findall(r"[a-z0-9]+",str(s).lower()))
def score(c,q):
 qt=tok(q); b=0
 for s in c.get("skills",[]) or []:
  ex=s.get("examples") or []
  st=tok(" ".join([s.get("name",""),s.get("description","")," ".join(s.get("tags") or [])," ".join(ex)]))
  v=20*len(qt&st)
  if q.lower() in " ".join(ex).lower():v+=1000
  if "mcp" in qt and "mcp" in st:v+=100
  if "timeout" in qt and "timeout" in st:v+=100
  b=max(b,v)
 return b
out=[]
for n,q in enumerate(I,1):
 t0=time.perf_counter()
 a,rm=get(R+"?"+urllib.parse.urlencode({"q":q}))
 rows=a.get("agents") or a.get("items") or a.get("data") or []
 cc=[]
 for x in rows[:15]:
  u=x.get("manifestUrl")
  if not u:continue
  try:c,cm=get(u)
  except:continue
  cc.append((score(c,q),u,c,cm))
 if not cc:raise SystemExit("no candidates")
 cc.sort(key=lambda x:x[0],reverse=True)
 sc,u,c,cm=cc[0]
 it=next((x for x in c.get("supportedInterfaces",[]) if str(x.get("protocolBinding","")).upper()=="JSONRPC"),None)
 if not it:raise SystemExit("no JSONRPC interface")
 b={"jsonrpc":"2.0","id":n,"method":"SendMessage","params":{"message":{"messageId":str(uuid.uuid4()),"role":"ROLE_USER","parts":[{"text":q}]}}}
 r,im=get(it["url"],b,{"A2A-Version":"1.0"})
 m=(r.get("result") or {}).get("message") or r.get("message") or {}
 d=next((p.get("data") for p in m.get("parts",[]) if isinstance(p,dict) and isinstance(p.get("data"),dict)),{})
 if m.get("role")!="ROLE_AGENT" or not (d.get("matches") or []):raise SystemExit("invocation failed")
 out.append({"round":n,"intent":q,"candidates":len(rows),"selected":{"name":c.get("name"),"manifestUrl":u,"score":sc,"endpoint":it["url"]},"timingMs":{"registry":round(rm,3),"card":round(cm,3),"invoke":round(im,3),"e2e":round((time.perf_counter()-t0)*1000,3)}})
vals=[x["timingMs"]["e2e"] for x in out]
res={"runType":"P4 Open-World A2A Proof","runner":{"runId":os.getenv("GITHUB_RUN_ID"),"os":os.getenv("RUNNER_OS")},"rounds":out,"p50Ms":round(statistics.median(vals),3),"maxMs":round(max(vals),3),"pass":len(out)==5}
open("p4-openworld-result.json","w").write(json.dumps(res,indent=2))
print(json.dumps(res,indent=2))
