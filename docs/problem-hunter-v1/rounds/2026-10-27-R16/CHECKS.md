# R16 isolated scanner checks

Executed on Node v24.22.1: 9/9 assertions passed. Two unchanged internal functions extracted from src/Challenge.ts at dd2c3e3b21006b80f4de65b218967a0490eaa218; TypeScript erased with Node stripTypeScriptTypes. Node emitted its experimental API warning. No other upstream code was executed.

Scope: scheme-boundary detection only. No challenge decoding, candidate patch, transport collection, full suite, network, secrets, wallet, credentials or payments. These successes do NOT establish the repair. Proposed transport regressions are in DRAFTS.md and remain NOT RUN.

Reproduction: save the following as scanner-check.mjs and run node scanner-check.mjs:

```js
import assert from 'node:assert/strict';
import {stripTypeScriptTypes} from 'node:module';
import vm from 'node:vm';
const source="function startsWithSchemeToken(value: string, index: number, token: string): boolean {\n  if (value.slice(index, index + token.length).toLowerCase() !== token.toLowerCase()) return false\n  const next = value[index + token.length]\n  return Boolean(next && /\\s/.test(next))\n}\n\nfunction findSchemeStarts(value: string, token: string): number[] {\n  const starts: number[] = []\n  let inQuotes = false\n  let escaped = false\n\n  for (let i = 0; i < value.length; i++) {\n    const char = value[i]\n\n    if (inQuotes) {\n      if (escaped) escaped = false\n      else if (char === '\\\\') escaped = true\n      else if (char === '\"') inQuotes = false\n      continue\n    }\n\n    if (char === '\"') {\n      inQuotes = true\n      continue\n    }\n\n    if (!startsWithSchemeToken(value, i, token)) continue\n\n    let boundary = i - 1\n    while (boundary >= 0 && /\\s/.test(value[boundary] ?? '')) boundary--\n    if (boundary >= 0 && value[boundary] !== ',') continue\n    starts.push(i)\n  }\n\n  return starts\n}\n\n";
const ctx=vm.createContext({});vm.runInContext(stripTypeScriptTypes(source),ctx);
const cases=[['X402',0],['Basic realm="Payment hidden"',0],['Bearer realm="x, Payment hidden"',0],['Bearer realm="x\\\" , Payment hidden"',0],['Payment id="bad"',1],['pAyMeNt id="bad"',1],['X402, Payment id="bad"',1],['Paymentish id="x"',0],['Payment id="a", Payment id="b"',2]];
for(const [header,count] of cases) assert.equal(ctx.findSchemeStarts(header,'Payment').length,count,header);
console.log(JSON.stringify({node:process.version,cases:cases.length,passed:cases.length,scope:'Unmodified source-extracted scheme scanner only; no challenge decoding, transport, wallet or payment.'}));

```
