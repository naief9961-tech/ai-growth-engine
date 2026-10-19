# R7 isolated evidence and reproduction

Executed on 2026-10-19, Node v24.19.0, exit 0. Eight groups passed; results in RESULTS.json. No installation or external test request. Executed source files: pinned client, schema-store and boot source, Git blob hashes verified in the harness.

## Scope

- Cockpit: extracts the actual fetchWithDeadline and postToServer functions; the injected fetch increments a synthetic effect counter, then simulates a response parse failure or nested ECONNRESET. Baseline replays twice; a local candidate policy returns unknownOutcome after one attempt. Typed ECONNREFUSED and explicit 401 still retry once; absent new option preserves defaults.
- Hyde: executes the full SchemaStore class after built-in Node TypeScript stripping. Imports replaced by a gated synthetic fetchSource, registry helper, parser stubs and logger; no filesystem/network read. Deferred promises force reverse completion without sleeps. The exact boot redacted expression is checked against source, then compared with registry-filter projection. Missing-first-load and failed-refresh-last-good boundaries pass.
- These are dependency-isolated control-flow checks. Synthetic counters are not persisted decisions. Parser stubs do not prove schema validation. No real MCP runtime, database, providers, Vitest, upstream full suite or typecheck.
- Node emitted its standard experimental stripTypeScriptTypes warning; this did not fail the checks.

## Run in an isolated temporary directory

Copy EVIDENCE.json and save the following as fetch_sources.py. It reads three pinned public source files only; the Node harness validates their exact Git blob hashes. Sources are not vendored; upstream licenses apply.

```python
import json, urllib.request
from pathlib import Path

manifest = json.loads(Path("EVIDENCE.json").read_text())["sources"]
wanted = {"src/client/server-connection.js", "src/schema-store.ts", "src/boot.ts"}
sources = {}
for source in manifest:
    if source["path"] not in wanted:
        continue
    url = "https://raw.githubusercontent.com/{repository}/{commit}/{path}".format(**source)
    with urllib.request.urlopen(url, timeout=20) as response:
        content = response.read().decode("utf-8")
    sources[source["path"]] = dict(source, content=content, sha=source["blob_sha"])
Path("sources.json").write_text(json.dumps(sources), encoding="utf-8")
```

Save the following as checks.mjs, then run:

```sh
python3 fetch_sources.py
node checks.mjs > results.json
```

```js
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import { createHash } from 'node:crypto';
import { stripTypeScriptTypes } from 'node:module';
const sources=JSON.parse(fs.readFileSync(new URL('./sources.json',import.meta.url)));
for(const s of Object.values(sources)){
 const b=Buffer.from(s.content);
 assert.equal(createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex'),s.sha);
}
const results=[];
const source=sources['src/client/server-connection.js'].content;
const deadline=source.slice(source.indexOf('async function fetchWithDeadline('),source.indexOf('async function canConnectToPort('));
const post=source.slice(source.indexOf('async function postToServer('),source.indexOf('module.exports ='));
function getPost(patched){
 let code=post;
 if(patched) code=code.replace("      if (attempt > 0) return { ok: false, status: null, json: null };",
 "      if (options.retryAfterAmbiguousFailure === false && error?.cause?.code !== 'ECONNREFUSED') return { ok: false, status: null, json: null, unknownOutcome: true };\n      if (attempt > 0) return { ok: false, status: null, json: null };");
 return vm.runInNewContext(deadline+'\n'+code+'\npostToServer',{AbortController,setTimeout,clearTimeout,process:{env:{}},fsp:{},HOOK_TIMEOUT_MS:1000});
}
const info={port:12345,secret:'synthetic-placeholder'};
async function scenario(mode,patched,optOut=true){
 let attempts=0,effects=0;
 const fn=getPost(patched);
 const result=await fn('/api/sessions/synthetic/plan',{kind:'add_decision'},{
 homeDir:'unused',initialInfo:info,ensure:false,readServerInfo:async()=>info,
 retryAfterTimeout:false,...(optOut?{retryAfterAmbiguousFailure:false}:{}),
 fetchImpl:async()=>{
 attempts++;
 if(mode==='refused'&&attempts===1)throw new TypeError('fetch failed',{cause:{code:'ECONNREFUSED'}});
 if(mode==='401'&&attempts===1)return{ok:false,status:401};
 effects++;
 if(mode==='socket'&&attempts===1)throw new TypeError('fetch failed',{cause:{code:'ECONNRESET'}});
 return {ok:true,status:200,json:async()=>{if(mode==='json'&&attempts===1) return JSON.parse('{truncated');return{accepted:true}}};
 }});
 return {attempts,effects,ok:result.ok,unknownOutcome:result.unknownOutcome===true};
}
for(const mode of ['json','socket']){
 const before=await scenario(mode,false);assert.equal(before.effects,2);assert.equal(before.ok,true);
 const after=await scenario(mode,true);assert.equal(after.effects,1);assert.equal(after.unknownOutcome,true);
 results.push({case:'cockpit '+mode,before,after,passed:true});
}
for(const mode of ['refused','401']){
 const after=await scenario(mode,true);assert.equal(after.attempts,2);assert.equal(after.effects,1);assert.equal(after.ok,true);
 results.push({case:'cockpit '+mode+' recovery',after,passed:true});
}
const compatible=await scenario('json',true,false);assert.equal(compatible.effects,2);
results.push({case:'cockpit default retry compatibility',observed:compatible,passed:true});
const ts=sources['src/schema-store.ts'].content.replace(/^import .*;\n/gm,'').replace(/^export /gm,'');
let gates=new Map();
const registry={apps:new Map(['shop','crm'].map(name=>[name,{repo:name,logSchemaPath:'log',redactedSchemaPath:'redacted'}]))};
const appNames=r=>[...r.apps.keys()];
const SchemaStore=vm.runInNewContext(stripTypeScriptTypes(ts)+'\nSchemaStore',{
 fetch:()=>{throw Error('network forbidden')},AbortSignal,SCHEMA_DIR:'unused',console,
 appNames,fetchSource:({repo,path})=>new Promise((resolve,reject)=>gates.set(repo+':'+path,{resolve,reject})),
 parseLogSchemaText:(_app,text)=>({fields:{synthetic:text}}),parseRedactedSchemaText:text=>text,
 describeSource:({repo,path})=>repo+'/'+path
});
const boot=sources['src/boot.ts'].content;
assert.ok(boot.includes('redacted: [...schemas.redactedSchemas.keys()]'));
const original=schemas=>[...schemas.redactedSchemas.keys()];
const candidate=schemas=>appNames(registry).filter(app=>schemas.redactedSchemas.has(app));
const store=new SchemaStore({registry,token:'synthetic-unused',log:()=>{},warn:()=>{}});
let refresh=store.refresh();
assert.equal(gates.size,4);
for(const kind of ['log','redacted'])gates.get('crm:'+kind).resolve('first');
await new Promise(resolve=>setImmediate(resolve));
for(const kind of ['log','redacted'])gates.get('shop:'+kind).resolve('second');
await refresh;
assert.deepEqual(original(store),['crm','shop']);
assert.deepEqual(candidate(store),['shop','crm']);
results.push({case:'hyde reversed completion with parallel reads',before:original(store),after:candidate(store),passed:true});
gates=new Map();refresh=store.refresh();for(const g of gates.values())g.reject(Error('synthetic unavailable'));await refresh;
assert.deepEqual(candidate(store),['shop','crm']);
assert.deepEqual(original(store),['crm','shop']);
results.push({case:'hyde last-good refresh and live map preserved',passed:true});
gates=new Map();const partial=new SchemaStore({registry,token:'synthetic-unused',log:()=>{},warn:()=>{}});
refresh=partial.refresh();
for(const [key,g] of gates)key.startsWith('shop:')?g.reject(Error('synthetic missing')):g.resolve('present');
await refresh;assert.deepEqual(candidate(partial),['crm']);
results.push({case:'hyde absent app is not reported ready',passed:true});
console.log(JSON.stringify({runtime:process.version,scope:'Source-extracted control-flow checks with synthetic fetch/parser boundaries; no live server, upstream suite, persistence or full MCP runtime.',results},null,2));
```

## Integration regressions still needed upstream

Cockpit: exercise the MCP tool entry with a write persisted before response loss; verify only one operation and a user-facing unknown-outcome message, including already-applied updates. Cover postPlan, postPullRequest, postCrossReviewSkip and diagnostic classification. Retain timeout, 401, typed refused-connection and default retry controls. Do not claim a synthetic counter proves real provider/process behavior.

Hyde: drive boot with deferred readers in both completion orders; verify registry-order report plus absence after failed first load and last-good preservation. Compare live-map membership without insertion-order assumptions, including the existing log-map assertion, unless a separate ordered-store contract is chosen. Run Vitest and typecheck; neither was run here.
