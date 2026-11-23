# R39 — executed isolated checks

Environment: Node v24.22.3; built-in assert, vm, TypeScript stripping and crypto. No npm installs, network calls, secrets or payments in the harness. Six input source files were fetched read-only from pinned GitHub and their Git blob SHA-1 values verified before extraction.

Observed successful output (16 groups, exit 0):

```json
{"source_blob_hashes_verified":6,"assertion_groups":16,"baseline_groups":6,"candidate_groups":10,"node":"v24.22.3","zod":false,"react":false,"rpc":false,"upstream_suite":false}
```

This executes extracted mapper functions, enum tables and the actual FormData helper/field whitelist. The lookup-boundary assertion uses the extracted table, not the full async update function. Candidate split/encode functions are newly written pure-data proposals, not an upstream patch. No real Zod schema, React renderer, RPC server, deployment or preflight was run. The VM isolates reviewed snippets; it is not a security claim about arbitrary code.

## Reproduction inputs

Pinned commit: 234423bc0548032be5beb7cdb2583bd0a5b72a88.

Save this optional read-only fetch script alongside the harness to reconstruct r39_sources.json. This urllib script is documentation, not the fetch path executed in this round; connector reads supplied the actual inputs. The harness checks every source hash, so changed content fails closed.

```python
import json, urllib.request, urllib.parse
manifest = json.loads("{\"apps/web-admin/lib/webhooks.ts\":\"1d9da544fc3a7982c53620bccacb03957647e104\",\"apps/web-admin/lib/api-keys.ts\":\"7cc3f59f9eaed1c166d3df6eeec42edb3eb15725\",\"packages/utils/src/form-data.ts\":\"8bc58bbe615fb084b9a8a559927db68095a129d7\",\"proto/publira/admin/v1/webhook.proto\":\"e6df46bea3f51394b7c5317870183c7844ec2e13\",\"proto/publira/admin/v1/api_key.proto\":\"45a3b62ba078a7ec08d4695e1d590eca6694ad9a\",\"apps/web-admin/app/[tenant_id]/[locale]/(protected)/integrations/api-keys-and-webhooks/_lib/form-schemas.ts\":\"a9d19b5217e8aef5c96dd3956036adbf9433c5f4\"}")
base = "https://raw.githubusercontent.com/publira/publira/234423bc0548032be5beb7cdb2583bd0a5b72a88/"
result = {}
for path, sha in manifest.items():
    with urllib.request.urlopen(base + urllib.parse.quote(path, safe="/"), timeout=30) as r:
        content = r.read().decode("utf-8")
    result[path] = {"content": content, "sha": sha}
with open("r39_sources.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False)
```

## Exact executed harness: r39_test.mjs

Run `node r39_test.mjs` beside r39_sources.json. Node may emit an experimental TypeScript stripping warning.

```javascript
import assert from "node:assert/strict";
import fs from "node:fs";
import vm from "node:vm";
import { stripTypeScriptTypes } from "node:module";
import { createHash } from "node:crypto";
const src=JSON.parse(fs.readFileSync(new URL("./r39_sources.json",import.meta.url)));
for(const [path,r] of Object.entries(src)){
 const b=Buffer.from(r.content);
 assert.equal(createHash("sha1").update(Buffer.from("blob "+b.length+"\0")).update(b).digest("hex"),r.sha,path);
}
const w=src["apps/web-admin/lib/webhooks.ts"].content;
const a=src["apps/web-admin/lib/api-keys.ts"].content;
const f=src["packages/utils/src/form-data.ts"].content;
const schemas=src["apps/web-admin/app/[tenant_id]/[locale]/(protected)/integrations/api-keys-and-webhooks/_lib/form-schemas.ts"].content;
function cut(s,start,end){const i=s.indexOf(start);assert(i>=0);const j=s.indexOf(end,i);assert(j>i);return s.slice(i,j);}
function enumFrom(path,prefix){
 return Object.fromEntries([...src[path].content.matchAll(new RegExp(prefix+"([A-Z_]+) = (\\d+);","g"))].map(m=>[m[1],+m[2]]));
}
const WebhookEventType=enumFrom("proto/publira/admin/v1/webhook.proto","WEBHOOK_EVENT_TYPE_");
const ApiKeyScope=enumFrom("proto/publira/admin/v1/api_key.proto","API_KEY_SCOPE_");
const code=[
 cut(w,"const eventValues:","const statusValues:"),
 cut(w,"const isSubscribableEvent","/** What the console shows"),
 cut(w,"const toWebhookEndpointItem","const toWebhookDeliveryItem"),
 cut(a,"const scopeValues:","/** What the console shows"),
 cut(a,"const toApiKeyItem","const listApiKeysForSession"),
 f.replace(/export /g,""),
 cut(schemas,"export const webhookEndpointFormFields","export const webhookEndpointIdFormFields").replace("export ",""),
 "globalThis.result={toWebhookEndpointItem,toApiKeyItem,eventValues,rpcEventTypes,toFormDataInput,webhookEndpointFormFields};"
].join("\n");
const ctx=vm.createContext({WebhookEventType,ApiKeyScope,FormData,File});
vm.runInContext(stripTypeScriptTypes(code,{mode:"strip"}),ctx);
const api=ctx.result;
const plain=x=>JSON.parse(JSON.stringify(x));
let groups=0;function check(name,fn){fn();groups++;console.log("PASS",name);}
check("baseline mixed event drops 99",()=>assert.deepEqual(plain(api.toWebhookEndpointItem({eventTypes:[1,99]}).eventTypes),["purchase.completed"]));
check("baseline unknown-only subscription disappears",()=>assert.deepEqual(plain(api.toWebhookEndpointItem({eventTypes:[99]}).eventTypes),[]));
check("baseline unknown key scope disappears",()=>assert.deepEqual(plain(api.toApiKeyItem({scopes:[1,99]}).scopes),["catalog"]));
check("baseline known TEST excluded",()=>assert.deepEqual(plain(api.toWebhookEndpointItem({eventTypes:[6,1]}).eventTypes),["purchase.completed"]));
check("mapper-only preservation cannot use existing RPC lookup",()=>assert.deepEqual(["purchase.completed",99].map(v=>api.rpcEventTypes[v]),[1,undefined]));
check("existing FormData field whitelist drops a separate unknown channel",()=>{
 const fd=new FormData(); fd.append("event_types","purchase.completed");fd.append("unknown_event_types","99");
 const parsed=api.toFormDataInput(fd,api.webhookEndpointFormFields);
 assert.deepEqual(plain(parsed),{eventTypes:["purchase.completed"]});
});
const known=Object.fromEntries(Object.entries(api.rpcEventTypes));
const namedCodes=new Set([0,...Object.values(WebhookEventType)]);
// Candidate pure data contract, not integrated React/Zod/RPC code.
function split(codes){
 return codes.reduce((out,n)=>{
  const label=api.eventValues[n];
  if(label && label!=="webhook.test")out.known.push(label);
  else if(!namedCodes.has(n) && Number.isInteger(n) && n>=-2147483648 && n<=2147483647)out.unknown.push(n);
  return out;
 },{known:[],unknown:[]});
}
function encode(selected,preserved){
 const codes=selected.map(v=>{if(!Object.hasOwn(known,v))throw Error("unknown selection");return known[v]});
 for(const token of preserved){
  if(typeof token!=="string" || !/^-?(0|[1-9][0-9]*)$/.test(token))throw Error("invalid numeric token");
  const n=Number(token);
  if(!Number.isInteger(n)||n < -2147483648 || n>2147483647 || namedCodes.has(n))throw Error("invalid preserved event");
  codes.push(n);
 }
 if(!codes.length)throw Error("empty");
 return [...new Set(codes)];
}
check("candidate mixed roundtrip",()=>{const x=split([1,99]);assert.deepEqual(encode(x.known,x.unknown.map(String)),[1,99]);});
check("candidate unknown-only roundtrip",()=>{const x=split([99]);assert.deepEqual(encode(x.known,x.unknown.map(String)),[99]);});
check("candidate known deselection preserves unknown",()=>assert.deepEqual(encode([],["99"]),[99]));
check("candidate deduplicates",()=>assert.deepEqual(encode(["purchase.completed","purchase.completed"],["99","99"]),[1,99]));
check("candidate valid int32 boundaries",()=>assert.deepEqual(encode([],["-2147483648","2147483647"]),[-2147483648,2147483647]));
check("candidate malformed tokens fail closed",()=>{for(const t of ["","1e3","0x63","99.5","NaN","Infinity"," 99","99 ","01","2147483648","-2147483649"])assert.throws(()=>encode([],[t]));});
check("candidate known/reserved codes refused in opaque channel",()=>{for(const n of [0,1,6,7,12])assert.throws(()=>encode([],[String(n)]));});
check("candidate invalid known choice refused",()=>assert.throws(()=>encode(["__proto__"],["99"])));
check("candidate truly empty subscription refused",()=>assert.throws(()=>encode([],[])));
check("candidate does not promote TEST or unspecified",()=>assert.deepEqual(split([0,6,99]),{known:[],unknown:[99]}));
console.log(JSON.stringify({source_blob_hashes_verified:Object.keys(src).length,assertion_groups:groups,baseline_groups:6,candidate_groups:10,node:process.version,zod:false,react:false,rpc:false,upstream_suite:false}));

```

## Native checks still required

Use actual form rendering, field whitelist, Zod schema and server action with a mocked RPC boundary to assert exact numeric request payloads. Cover URL/enabled-only changes, mixed and unknown-only subscriptions, known-event deselection, numeric validation, TEST/UNSPECIFIED exclusion, unknown-scope display, and unchanged create allowlists. Server authorization and event validation remain authoritative. Replace the existing drop-unknown API-key expectation. Run repository preflight and old/new release-pair scenarios separately; none is implied by these 16 isolated groups.
