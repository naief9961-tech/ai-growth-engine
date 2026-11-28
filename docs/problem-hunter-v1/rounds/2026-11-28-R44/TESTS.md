# R44 — executed isolated evidence

Date: 2026-11-28. Target: https://github.com/IndianOpinion/mcp/issues/27
Source commit: `b46fa71e8ea583bc9b1fc1322b7dd19748e3bc50`. tools.js blob: `4480c18d97e5ad71e5280944e1eb0df67ef42ec4`.
Git blob SHA-1 was verified against the transferred original source before execution.

## Result and limits

Node24.22.3, Zod4.6.7 installed locally with --ignore-scripts --no-audit --no-fund. No service/payment expenditure, credentials, live account or live REST request.
12 groups passed: nine paired shape fixtures + authentication, 404, exported schema/unchanged independent contract.
Three URL-less valid variants fail baseline validation and pass candidate. Numeric URLs/missing outlets remain rejected. Baseline missing-URL text contains <undefined>; candidate removes it and includes supplied headline.
Authentication/404 use the original wrapper and ApiError class with a stubbed client. global fetch throws to prevent test network access.

Not run: MCP SDK client/server or transport, upstream npm test, private source, deployment. This is evidence of the public handler/schema boundary, not the whole system.
Initial harness import failed because version.js was not yet copied; after fetching that dependency from the same commit the recorded regression command passed. No product-code change was needed for this setup error.

## Candidate changes

Only get_breaking_event's source shape changes from `{outlet: str, url: str}` to `{outlet: str, headline: str.optional(), url: str.optional()}`.
Only its source text map changes to:
```js
...(r.sources || []).map((s) =>
  `- ${s.outlet}${s.headline ? `: ${s.headline}` : ''}${s.url ? ` <${s.url}>` : ''}`
),
```
get_brief retains its separate required URL schema. Null URL was not added to the contract: only omission is accepted by this change. Other malformed shapes retain validation failure.

## Reproduction layout

Place exact source files tools.js, render.js, client.js and version.js from the pinned SHA in baseline/ and candidate/, with package.json `{"type":"module"}` in each. Apply only the two changes above to candidate/tools.js. Install zod4.6.7 in the parent isolated directory, then run `node regression.mjs`.
Source file links and blob hashes are in ledger.json. No repository-wide install or upstream application execution was performed.

## Executed regression.mjs

```js
import assert from 'node:assert/strict';
import {writeFile} from 'node:fs/promises';
import {z} from 'zod';
import * as baseline from './baseline/tools.js';
import * as candidate from './candidate/tools.js';
import {ApiError as BaselineError} from './baseline/client.js';
import {ApiError as CandidateError} from './candidate/client.js';
const originalLog=console.log;
console.log=()=>{};
globalThis.fetch=()=>{throw Error('Network forbidden in regression');};
const base={event_id:7,post_id:8,headline:'Synthetic event',decided_at:'2026-11-28T00:00:00Z',url:'https://example.invalid/event',md_url:null,scores:{breaking:0.5,new_event:0.5,high_stakes:0.5,confirmed:0.5},composites:{min:0.5,mean:0.5,geo:0.5,breaking:0.5},your_score:0.5,would_send:false};
async function call(module,payload,kind='bearer',error){
 const registered=new Map();let calls=[];
 module.registerTools({registerTool:(n,c,f)=>registered.set(n,{c,f})},{site:'https://example.invalid',api:'https://example.invalid/api',auth:{kind},client:{call:async(...args)=>{calls.push(args);if(error)throw error;return payload;}}});
 const tool=registered.get('get_breaking_event');
 const r=await tool.f({event_id:7});
 return {r,calls,schema:tool.c.outputSchema};
}
const fixtures=[
 ['missing URL',{sources:[{outlet:'example.invalid',headline:'Synthetic headline'}]},false,true],
 ['legacy URL',{sources:[{outlet:'example.invalid',url:'https://example.invalid/source'}]},true,true],
 ['headline and URL',{sources:[{outlet:'example.invalid',headline:'Synthetic headline',url:'https://example.invalid/source'}]},true,true],
 ['mixed sources',{sources:[{outlet:'a.invalid',headline:'First'},{outlet:'b.invalid',url:'https://b.invalid/source'}]},false,true],
 ['empty sources',{sources:[]},true,true],
 ['absent sources',{},true,true],
 ['future fields preserved',{sources:[{outlet:'example.invalid',headline:'News',future:{id:1}}],future:true},false,true],
 ['wrong URL type',{sources:[{outlet:'example.invalid',url:42}]},false,false],
 ['missing outlet',{sources:[{headline:'Synthetic headline'}]},false,false],
];
let results=[];
for(const [name,extra,oldValid,newValid] of fixtures){
 const payload={...base,...extra};
 for(const [variant,module,expected] of [['baseline',baseline,oldValid],['candidate',candidate,newValid]]){
  const {r,calls,schema}=await call(module,payload);
  assert.equal(schema.safeParse(r.structuredContent).success,expected,name+' '+variant);
  assert.deepEqual(calls,[['GET','/agent/breaking/7',{auth:true}]]);
  assert.deepEqual(r.structuredContent,payload,'pass-through preserved');
  if(variant==='candidate'&&expected){
   const text=r.content[0].text;
   assert.ok(!text.includes('<undefined>'));
   for(const s of extra.sources||[]){if(s.headline)assert.ok(text.includes(s.headline));if(s.url)assert.ok(text.includes(`<${s.url}>`));}
  }
  if(variant==='baseline'&&name==='missing URL')assert.ok(r.content[0].text.includes('<undefined>'));
 }
 results.push({name,baselineValid:oldValid,candidateValid:newValid,passed:true});
}
for(const [module,ErrorType] of [[baseline,BaselineError],[candidate,CandidateError]]){
 const missing=await call(module,base,'anonymous');
 assert.equal(missing.r.isError,true);assert.equal(missing.calls.length,0);
 const absent=await call(module,base,'bearer',new ErrorType(404,{error:'not_found',message:'Synthetic event missing.'}));
 assert.equal(absent.r.isError,true);assert.match(absent.r.content[0].text,/Check the event_id/);
}
results.push({name:'authentication guard unchanged',passed:true},{name:'404 error path unchanged',passed:true});
const before=z.toJSONSchema(baseline.OUTPUT_SCHEMAS.get_breaking_event),after=z.toJSONSchema(candidate.OUTPUT_SCHEMAS.get_breaking_event);
assert.ok(before.properties.sources.items.required.includes('url'));
assert.ok(!after.properties.sources.items.required.includes('url'));
assert.ok(after.properties.sources.items.required.includes('outlet'));
assert.deepEqual(z.toJSONSchema(baseline.OUTPUT_SCHEMAS.get_brief),z.toJSONSchema(candidate.OUTPUT_SCHEMAS.get_brief));
results.push({name:'exported JSON Schema and independent get_brief contract',passed:true});
await writeFile(new URL('./results.json',import.meta.url),JSON.stringify({node:process.version,zod:'4.6.7',groups:results.length,results,limits:'Real pinned tools.js handler registration and Zod validation; stubbed client, no SDK transport/server, upstream npm suite or live REST execution.'},null,2)+'\n');
console.log=originalLog;
console.log(JSON.stringify({passed:results.length,pairedFixtures:fixtures.length,baselineFailuresReproduced:3,node:process.version,zod:'4.6.7'}));

```

## Before accepting upstream

Add the URL-less and mixed-source REST fixtures to test/stub-rest.mjs and SDK callTool checks alongside test/mcp.test.mjs/test/fixes.test.mjs. Assert source text, structured fields and successful output validation; preserve URL-present compatibility, no-auth and not_found controls. Run the repository suite in its intended environment. The maintainer must validate the private deployment separately.
