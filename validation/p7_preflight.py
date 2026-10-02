#!/usr/bin/env python3
import json, urllib.request, os
UA="NAIF-P7-Preflight/1.0"
def get(url):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=20) as r:return json.load(r)
policy=get("https://naifgravity.com/api/commerce/policy")
catalog=get("https://naifgravity.com/api/agent/catalog")
eligible=[p for p in catalog.get("products",[]) if p.get("machineCheckout") is True]
eligible.sort(key=lambda p: float(p.get("price") or 1e9))
out={
  "runner":{"runId":os.getenv("GITHUB_RUN_ID"),"os":os.getenv("RUNNER_OS"),"arch":os.getenv("RUNNER_ARCH")},
  "policy":policy,
  "eligibleCount":len(eligible),
  "cheapest":[{"id":p.get("id"),"name":p.get("name"),"price":p.get("price"),"currency":p.get("currency"),"endpoints":p.get("endpoints")} for p in eligible[:10]]
}
print(json.dumps(out,indent=2))
open("p7-preflight.json","w").write(json.dumps(out,indent=2))
