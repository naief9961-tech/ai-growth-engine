# R29 — isolated checks and candidate diff

Source SHA: `dddefb9bcd7c57d2b9605a8f41c7ea03ad6e0bec`. Runtime: Node v24.22.1. Five assertion groups passed with exit code 0 on 2026-11-09. Synthetic data only; no network or secrets.

## Reproduction

Obtain the pinned [viking-skills.ts](https://github.com/shpaw415/open-bot/blob/dddefb9bcd7c57d2b9605a8f41c7ea03ad6e0bec/apps/control/src/viking-skills.ts) and [http-error.ts](https://github.com/shpaw415/open-bot/blob/dddefb9bcd7c57d2b9605a8f41c7ea03ad6e0bec/apps/control/src/http-error.ts). Put them side by side as baseline.ts and http-error.ts. In baseline.ts only adjust the import from "./http-error" to "./http-error.ts" for Node module resolution. Copy baseline.ts to candidate.ts and apply the diff below. Save the harness as probe.ts next to them.

Run:
```sh
node --experimental-transform-types --disable-warning=ExperimentalWarning probe.ts
```

The baseline business logic is unmodified. Candidate changes only the post-success confirmation deadline and read timeout plumbing; it is not an upstream patch or an end-to-end save budget solution. Clock and fetch are injected/mocked; the final stalled-read case uses a real abort timer and a synthetic pending fetch.

## Actual output
```text
1 PASS: immediate success unchanged in baseline/candidate
2 PASS: expired post-success budget: baseline starts GET, candidate returns unconfirmed without GET
3 PASS: remaining 10ms: baseline sets 20000ms, candidate sets 10ms
4 PASS: insufficient poll budget: baseline starts second read, candidate stops
5 PASS: signal-aware stalled read aborts and candidate retains unconfirmed success
LIMIT: mocked fetch/clock, no network, CLI, router, OpenViking or deployment test; candidate only bounds post-success confirmation.
```

## Candidate diff (review only)
```diff
--- baseline.ts
+++ candidate.ts
@@ -145,7 +145,7 @@
     options.postRetryDelayMs ?? DEFAULT_POST_RETRY_DELAY_MS
   const root = baseUrl.replace(/\/$/, "")
 
-  async function call(path: string, init?: RequestInit) {
+  async function call(path: string, init?: RequestInit, timeoutMs = 20_000) {
     let response: Response
     try {
       response = await fetchImpl(`${root}${path}`, {
@@ -159,7 +159,7 @@
         // are fs-backed. The budget is only a safety net for a loaded
         // OpenViking — 20 s keeps one wedged call from stacking into the
         // minute-scale hangs seen in the field.
-        signal: AbortSignal.timeout(20_000),
+        signal: AbortSignal.timeout(Math.max(1, Math.min(20_000, timeoutMs))),
       })
     } catch (error) {
       const message = error instanceof Error ? error.message : "request failed"
@@ -190,11 +190,13 @@
     return unwrapVikingResult(body)
   }
 
-  async function get(name: string): Promise<SkillDetail> {
+  async function get(name: string, timeoutMs = 20_000): Promise<SkillDetail> {
     const nameError = skillNameError(name)
     if (nameError) throw new HttpError(400, nameError, "skill_name")
     const result = await call(
       `/api/v1/skills/${encodeURIComponent(name)}?include_content=true&include_files=false`,
+      undefined,
+      timeoutMs,
     )
     const content =
       isRecord(result) && typeof result.content === "string"
@@ -307,19 +309,22 @@
   // 2026-11-07: the 502 here read as "save failed" and triggered the exact
   // blind retries that made things worse).
   async function confirmSave(input: SkillDetail, deadline: number) {
-    // skillBody() trims the stored body, while manifest bodies typically end
-    // with a newline — compare normalized or every newline-terminated skill
-    // "fails" the confirm forever (the 2026-10-15 install outage).
     const want = input.body.trim()
     for (let attempt = 0; attempt < confirmAttempts; attempt++) {
-      if (attempt > 0) await sleep(confirmPollDelayMs)
+      let remaining = deadline - Date.now()
+      if (remaining <= 0) return false
+      if (attempt > 0) {
+        if (confirmPollDelayMs >= remaining) return false
+        await sleep(confirmPollDelayMs)
+        remaining = deadline - Date.now()
+        if (remaining <= 0) return false
+      }
       try {
-        const saved = await get(input.name)
+        const saved = await get(input.name, remaining)
         if (saved.body === want) return true
       } catch {
-        // not visible yet — poll again
+        // POST already succeeded; failed read-back does not undo the write.
       }
-      if (Date.now() >= deadline) return false
     }
     return false
   }

```

## Complete harness
```ts
import assert from 'node:assert/strict';
import { createVikingSkills as baseline } from './baseline.ts';
import { createVikingSkills as candidate } from './candidate.ts';
const realNow=Date.now, realTimeout=AbortSignal.timeout;
const input={name:'synthetic-skill',description:'synthetic',body:'new body'};
const ok=x=>Response.json({status:'ok',result:x});
async function probe(factory,mode) {
 let now=0,posted=false,reads=0,timeouts=[],trace=[],aborted=false;
 Date.now=()=>now;
 AbortSignal.timeout=ms=>{timeouts.push(ms);return realTimeout(ms)};
 const fake=async(url,init)=>{
   const method=init.method||'GET'; trace.push(method+' '+new URL(url).pathname);
   if(url.endsWith('/validate')) return ok({valid:true});
   if(method==='DELETE') return ok({});
   if(method==='POST'){posted=true;if(mode==='expired')now=30;if(mode==='remaining')now=15;return ok({});}
   if(!posted)return ok({description:'old',content:'old body'});
   reads++;
   if(mode==='poll'&&reads===1){now=24;return ok({content:'old body'});}
   if(mode==='stalled')return new Promise((resolve,reject)=>{
     const timer=setTimeout(()=>resolve(ok({content:input.body})),100);
     init.signal.addEventListener('abort',()=>{aborted=true;clearTimeout(timer);reject(init.signal.reason)},{once:true});
   });
   return ok({content:input.body});
 };
 try {
   const service=factory('https://synthetic.invalid','synthetic',fake,{saveBudgetMs:mode==='stalled'?10:25,confirmAttempts:2,confirmPollDelayMs:5});
   const result=await service.save(input);
   return {result,reads,timeouts,trace,aborted};
 } finally {Date.now=realNow;AbortSignal.timeout=realTimeout;}
}
let outputs=[];
for(const fn of [baseline,candidate])assert.deepEqual((await probe(fn,'fast')).result,{confirmed:true});
outputs.push('1 PASS: immediate success unchanged in baseline/candidate');
let before=await probe(baseline,'expired'),after=await probe(candidate,'expired');
assert.equal(before.reads,1);assert.equal(after.reads,0);assert.deepEqual(after.result,{confirmed:false});
outputs.push('2 PASS: expired post-success budget: baseline starts GET, candidate returns unconfirmed without GET');
before=await probe(baseline,'remaining');after=await probe(candidate,'remaining');
assert.equal(before.timeouts.at(-1),20000);assert.equal(after.timeouts.at(-1),10);
outputs.push('3 PASS: remaining 10ms: baseline sets 20000ms, candidate sets 10ms');
before=await probe(baseline,'poll');after=await probe(candidate,'poll');
assert.equal(before.reads,2);assert.equal(after.reads,1);assert.deepEqual(after.result,{confirmed:false});
outputs.push('4 PASS: insufficient poll budget: baseline starts second read, candidate stops');
after=await probe(candidate,'stalled');
assert.equal(after.aborted,true);assert.deepEqual(after.result,{confirmed:false});
outputs.push('5 PASS: signal-aware stalled read aborts and candidate retains unconfirmed success');
console.log(outputs.join('\n'));
console.log('LIMIT: mocked fetch/clock, no network, CLI, router, OpenViking or deployment test; candidate only bounds post-success confirmation.');

```

## Remaining validation

Run project-native regression tests before adoption, including response-body stalls, missing/new skill snapshot timings, exhausted pre-write budget, write-outcome ambiguity, replace/rollback and rename, control route startup, CLI with and without group assignment, and actual deployed revision. Real OpenViking read-back/indexing was not exercised. Confirmation must compare the intended persistence contract; this candidate preserves the current body-only comparison rather than expanding it.
