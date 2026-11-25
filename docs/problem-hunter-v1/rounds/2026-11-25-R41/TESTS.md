# R41 JavaScript isolated evidence — executed, not an application fix

**Follow-up 2026-11-25:** native isolated Go tests now executed; see [six Go groups, original failures and candidate results](GO-TESTS.md). The JavaScript results below are unchanged.

Runtime: Node24.22.3. Command actually run: `node r41/check.mjs`; exit0, eight assertion groups. Input: exact apply function extracted from web/src/app/events.ts at 8caff896859499b86398c1e3e75c964c40dca6f3 (blob ebb409b4c5755857f705340b0616aa65e194e206). TypeScript stripped with Node's built-in experimental stripTypeScriptTypes. No dependency installation or network in test.

| Group | Observation |
|---|---|
|1 baseline | running → cancelled → late log leaves no running request |
|2 baseline | running → cancelled → late request/running resurrects it |
|3 paired | duplicate pre-ready count2 becomes1 |
|4 paired | running+cancelled pre-ready count2 becomes0 |
|5 paired | terminal-only pre-ready count1 becomes0 |
|6 candidate control | terminating a preserves b |
|7 candidate reconnect | empty authoritative snapshot clears stale item |
|8 limitation | snapshot-only patch still permits late live resurrection |

There are8 groups, including3 paired groups (11 group executions). Stubs: QueryClient setQueryData in-memory Map, refreshRequests no-op, mergeLogs uses incoming. No React/EventSource/WebView2 or Go hub test. At the initial run the Go command failed before any test; the guard was then uncompiled. This limitation is superseded for the isolated hub fixture by GO-TESTS.md; full application compilation remains untested. No upstream suite, provider/API/OAuth/customer data or full OOXML-style validation claim.

Reproduction: fetch the pinned source through GitHub, verify its Git blob SHA, and extract text from `function apply(` up to (excluding) `// useAdminEvents` into apply.ts. Save the harness below as check.mjs next to it and run `node check.mjs`. The harness exercises only that reviewed function, not upstream entrypoints. No source is vendored here.

```js
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import { stripTypeScriptTypes } from 'node:module';

const original = fs.readFileSync(new URL('./apply.ts', import.meta.url), 'utf8');
const candidate = original.replace('snapshot.running.push(record)', `snapshot.running = snapshot.running.filter((item) => item.id !== record.id)
        if (record.state === 'running') snapshot.running.push(record)`);
function fixture(source) {
  const cache = new Map();
  const client = {setQueryData(key, value) { const k=JSON.stringify(key); cache.set(k,typeof value==='function'?value(cache.get(k)):value); }};
  const context = {logsKey:['logs'], runningKey:['requests-running'], connectionKey:['events','connection'],maxLogs:2000,refreshRequests:()=>{}, mergeLogs:(_, incoming)=>incoming};
  vm.createContext(context);
  vm.runInContext(stripTypeScriptTypes(source)+';globalThis.applyFn=apply;',context);
  return {send:(event,snapshot)=>context.applyFn(client,event,snapshot),running:()=>cache.get('["requests-running"]')||[]};
}
const event = (state,id='synthetic-1')=>({type:'request',data:{id,state}});
const results=[];
{
 const f=fixture(original); f.send(event('running')); f.send(event('cancelled'));
 assert.equal(f.running().length,0);
 f.send({type:'log',data:{event:'request.progress',request_id:'synthetic-1',message:'synthetic late attempt'}});
 assert.equal(f.running().length,0); results.push('source: late log does not resurrect cancelled request');
}
{
 const f=fixture(original); f.send(event('running'));f.send(event('cancelled'));f.send(event('running'));
 assert.equal(f.running().length,1); results.push('source: a late type=request running event DOES resurrect it');
}
for (const [name,states,oldCount,newCount] of [
 ['duplicate pre-ready',['running','running'],2,1],
 ['terminal pre-ready',['running','cancelled'],2,0],
 ['terminal-only pre-ready',['failed'],1,0],
]) {
 for(const [source,count] of [[original,oldCount],[candidate,newCount]]) {
  const f=fixture(source),snapshot={logs:[],running:[]};
  for(const s of states) f.send(event(s),snapshot);
  f.send({type:'ready'},snapshot);assert.equal(f.running().length,count);
 }
 results.push('paired: '+name);
}
{
 const f=fixture(candidate);f.send(event('running','a'));f.send(event('running','b'));f.send(event('completed','a'));
 assert.equal(f.running().length,1);assert.equal(f.running()[0].id,'b');results.push('candidate: terminal update preserves unrelated running request');
}
{
 const f=fixture(candidate);f.send(event('running'));f.send({type:'ready'},{logs:[],running:[]});
 assert.equal(f.running().length,0);results.push('candidate: empty authoritative reconnect snapshot clears stale state');
}
{
 const f=fixture(candidate);f.send(event('cancelled'));f.send(event('running'));
 assert.equal(f.running().length,1);results.push('limit: snapshot-only change does not fix a late live running event');
}
console.log(JSON.stringify({groups:results.length,results,limits:'Actual apply extracted; mocked QueryClient/refresh/log merge. No React/EventSource, Go hub, WebView2, OAuth, provider or upstream integration execution.'},null,2));

```

The proposed backend guard now has native deterministic scheduling tests and race-detector coverage in the isolated fixture; full application tests remain required. Frontend snapshot tests include sequences that the current atomic subscribe/ready implementation should normally prevent; they establish defensive reducer behavior, not the incident's cause.
