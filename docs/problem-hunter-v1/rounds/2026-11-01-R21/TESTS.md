# Local test, 1 November

Node 24 with --experimental-transform-types. Pin 01fefec9556c0ad6e8a0b6c76eb06770b3317106; use the two linked implementation files in REPORT. For each run concatenate the following setup, full webhookJson.ts, webhook.ts with only import lines removed, then the harness below. Use .mts. Provider/validator unchanged for baseline; interpolation is identity because fixtures contain no variables. axios.post records arguments in memory. No authentication, live HTTP, framework build or upstream suite. For the candidate replace both occurrences of /json/i.test(contentType) with `(/^(application\/json|[^/;\s]+\/[^/;\s]+\+json)$/i.test(contentType.split(';',1)[0].trim()))`. EXPECTED below is the two parameterized plain-text entries on baseline and [] on candidate. Baseline: both falsely rejected, four controls accepted; candidate: six accepted with expected payload shapes. No claim of complete parser or transport validation.

```ts
import assert from 'node:assert/strict';
let posted=[];const axios={post:async (...a)=>posted.push(a)}, logger={error(){},info(){}}, interpolateTemplate=(s)=>s;
// insert the two pinned source files here
const cases=[['text/plain; profile="json"',false],['text/plain; note="JSON debug"',false],['text/plain',false],['application/json; charset=utf-8',true],['application/problem+json',true],['',true]];let wrong=[];for (const [type,json] of cases){const headers=JSON.stringify(type?{'Content-Type':type}:{});const template=json?'{"ok":true}':'price changed';posted=[];const ok=await new WebhookProvider('https://example.invalid',headers,template).send({});const uiOK=webhookTemplateProblem(template,webhookSendsPlainText(headers))===null;assert.equal(uiOK,ok);assert.equal(posted.length,ok?1:0);if(ok)assert.deepEqual(posted[0][1],json?{ok:true}:template);if(!ok)wrong.push(type)}assert.deepEqual(wrong,EXPECTED);console.log(JSON.stringify({cases:cases.length,wrong}));
```
