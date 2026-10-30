# R19 isolated classifier evidence

Runtime: Node v24.22.1. Executed locally with `node r19-test.mjs`, exit 0.
No dependency installation, network, secrets, credentials, wallets or payments.
The baseline is an unchanged source excerpt from the pinned Challenge.ts; Node stripTypeScriptTypes removes types only. Constants.Schemes.payment is supplied as the source-confirmed literal. The candidate is a local helper variation, not an upstream patch.
Result: 13 baseline classifications, 3 expected false positives reproduced, 10 controls passed. 13 candidate classifications passed. 13 comparisons confirmed default strict-scanner results unchanged on the same finite vectors. This is **not** exhaustive parity, a full transport test, SDK integration, upstream suite or deployed repair.
Transport regressions remain proposed in DRAFTS.md. No full-system success claimed.

Copy this harness to a temporary .mjs file and run Node 24:
```js
// Source-extracted classifier checks only; no transport, credentials, network or payments.
// Source: wevm/mppx c912c79a5df2589eadfcadfd30a43b7f7b5ff5c2
// src/Challenge.ts blob 6d073b024753832950bf50c36981f16aa5f3ba75
import assert from 'node:assert/strict';
import { stripTypeScriptTypes } from 'node:module';
import vm from 'node:vm';
const baseline = "function startsWithSchemeToken(value: string, index: number, token: string): boolean {\n  if (value.slice(index, index + token.length).toLowerCase() !== token.toLowerCase()) return false\n  const next = value[index + token.length]\n  return Boolean(next && /\\s/.test(next))\n}\n\n/**\n * Returns whether a `WWW-Authenticate` value contains a Payment challenge.\n *\n * @internal\n */\nexport function hasPaymentScheme(value: string): boolean {\n  // A bare `Payment` scheme with no parameters is still a (malformed) Payment challenge.\n  return (\n    findSchemeStarts(value, Constants.Schemes.payment).length > 0 ||\n    value\n      .split(',')\n      .some((part) => part.trim().toLowerCase() === Constants.Schemes.payment.toLowerCase())\n  )\n}\n\n/** @internal Finds auth scheme boundaries while ignoring quoted-string contents. */\nfunction findSchemeStarts(value: string, token: string): number[] {\n  const starts: number[] = []\n  let inQuotes = false\n  let escaped = false\n\n  for (let i = 0; i < value.length; i++) {\n    const char = value[i]\n\n    if (inQuotes) {\n      if (escaped) escaped = false\n      else if (char === '\\\\') escaped = true\n      else if (char === '\"') inQuotes = false\n      continue\n    }\n\n    if (char === '\"') {\n      inQuotes = true\n      continue\n    }\n\n    if (!startsWithSchemeToken(value, i, token)) continue\n\n    let boundary = i - 1\n    while (boundary >= 0 && /\\s/.test(value[boundary] ?? '')) boundary--\n    if (boundary >= 0 && value[boundary] !== ',') continue\n    starts.push(i)\n  }\n\n  return starts\n}\n\n";
const candidate = "function startsWithSchemeToken(value: string, index: number, token: string): boolean {\n  if (value.slice(index, index + token.length).toLowerCase() !== token.toLowerCase()) return false\n  const next = value[index + token.length]\n  return Boolean(next && /\\s/.test(next))\n}\n\n/**\n * Returns whether a `WWW-Authenticate` value contains a Payment challenge.\n *\n * @internal\n */\nexport function hasPaymentScheme(value: string): boolean {\n  return findSchemeStarts(value, Constants.Schemes.payment, true).length > 0\n}\n\n/** @internal Finds auth scheme boundaries while ignoring quoted-string contents. */\nfunction findSchemeStarts(value: string, token: string, includeBare = false): number[] {\n  const starts: number[] = []\n  let inQuotes = false\n  let escaped = false\n\n  for (let i = 0; i < value.length; i++) {\n    const char = value[i]\n\n    if (inQuotes) {\n      if (escaped) escaped = false\n      else if (char === '\\\\') escaped = true\n      else if (char === '\"') inQuotes = false\n      continue\n    }\n\n    if (char === '\"') {\n      inQuotes = true\n      continue\n    }\n\n    const sameToken = value.slice(i, i + token.length).toLowerCase() === token.toLowerCase()\n    const next = value[i + token.length]\n    const matches = includeBare\n      ? sameToken && (next === undefined || next === ',' || /\\s/.test(next))\n      : startsWithSchemeToken(value, i, token)\n    if (!matches) continue\n\n    let boundary = i - 1\n    while (boundary >= 0 && /\\s/.test(value[boundary] ?? '')) boundary--\n    if (boundary >= 0 && value[boundary] !== ',') continue\n    starts.push(i)\n  }\n\n  return starts\n}\n\n";
function load(source) {
  const js = stripTypeScriptTypes(source.replace('export function', 'function'));
  return vm.runInNewContext('const Constants = {Schemes:{payment:"Payment"}};\n' + js + '\n({hasPaymentScheme, findSchemeStarts})');
}
const cases = [
 ['quoted comma segment', 'Bearer realm="alpha, Payment, beta"', false],
 ['quoted mixed case', 'Basic realm="a, pAyMeNt, b"', false],
 ['quoted escaped quote', 'Bearer realm="a\\", Payment, b"', false],
 ['x402', 'X402', false],
 ['empty', '', false],
 ['bare', 'Payment', true],
 ['bare mixed case', 'pAyMeNt', true],
 ['bare before other scheme', 'Payment, Basic realm="x"', true],
 ['bare after other scheme', 'Basic realm="x", Payment', true],
 ['parameterized', 'Payment id="x"', true],
 ['quoted prefix only', 'Basic realm="Payment"', false],
 ['prefix collision', 'Paymentish id="x"', false],
 ['quoted plus real', 'Basic realm="a, Payment, b", Payment id="x"', true],
];
const old = load(baseline), fixed = load(candidate);
const failures = cases.filter(([,header,expected]) => old.hasPaymentScheme(header) !== expected).map(([name])=>name);
assert.deepEqual(failures, ['quoted comma segment','quoted mixed case','quoted escaped quote']);
for (const [name,header,expected] of cases) assert.equal(fixed.hasPaymentScheme(header), expected, name);
for (const [,header] of cases) assert.equal(JSON.stringify(old.findSchemeStarts(header,'Payment')), JSON.stringify(fixed.findSchemeStarts(header,'Payment')));
console.log(JSON.stringify({node:process.version, baseline_cases:cases.length, reproduced_classifier_failures:failures, baseline_controls_passed:cases.length-failures.length, candidate_cases_passed:cases.length, strict_scanner_parity_cases_passed:cases.length, full_transport_tests:0, upstream_suites:0},null,2));

```
