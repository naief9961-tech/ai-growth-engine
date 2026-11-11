# R31 isolated verification

Executed on11November2026, Node v24.22.1, exit0. **Six assertion groups passed.** One baseline defect reproduction, five candidate/control groups. No package install, network/API call, account, health data, token, wallet or payment used by the test. No upstream build/typecheck/full suite or native/client integration ran.

## Pinned inputs

- [src/services/summary.ts](https://github.com/davidmosiah/withings-mcp/blob/7b0b1ff9359478d89d7e9484e482df6d49638c86/src/services/summary.ts), Git blob `d967e86800f59367231f53f88a6f88d885f05f4b`.
- [src/services/measures.ts](https://github.com/davidmosiah/withings-mcp/blob/7b0b1ff9359478d89d7e9484e482df6d49638c86/src/services/measures.ts), Git blob `9cbf4e092acebc001924dd798b0cb8dea2e96a82`.
- [src/services/redaction.ts](https://github.com/davidmosiah/withings-mcp/blob/7b0b1ff9359478d89d7e9484e482df6d49638c86/src/services/redaction.ts), Git blob `d16e82985a7e471d18cf185358b4c0d462a2b6f3`.

Prepare those three files in an isolated directory. Keep filenames summary.ts, measures.ts, redaction.ts. Verify their Git blob hashes before adapting imports. For Node's direct TypeScript loader, change only the two runtime import suffixes in summary.ts from ./measures.js and ./redaction.js to .ts. The type-only WithingsClient import is erased by Node; no client module is loaded. Both helper modules remain upstream code, not stubs.

Copy summary.ts to candidate.ts and replace exactly one array:

```diff
- [stats.has_activity_error, stats.has_sleep_error, stats.has_measures_error]
+ [stats.has_activity_error, stats.has_sleep_error, stats.has_measures_error, stats.has_heart_error]
```

The existing filter/length/ternary remains unchanged. Restoring the import suffixes in the baseline copy produced the three Git blob hashes above. A newline added while saving files was removed before the final successful run.

## Executed harness (test.mjs)

```js
import assert from "node:assert/strict";
import { buildDailySummary as baseline } from "./summary.ts";
import { buildDailySummary as candidate } from "./candidate.ts";
const endpoints = ["/v2/measure", "/v2/sleep", "/measure", "/v2/heart"];
const names = ["activity", "sleep", "measures", "heart"];
const fixtures = [
  { body: { activities: [{steps: 1000}] } },
  { body: { series: [{data: {sleep_score: 80, total_sleep_time: 25200, hr_average: 60}}] } },
  { body: { measuregrps: [{measures: [{type: 1, value: 7000, unit: -2}]}] } },
  { body: { heart: [{hr_average: 61}] } }
];
const results = [];
async function run(build, failed) {
  const calls = [];
  let stderr = "";
  const original = process.stderr.write;
  process.stderr.write = (chunk) => { stderr += String(chunk); return true; };
  try {
    const summary = await build({ async get(endpoint) {
      calls.push(endpoint);
      const index = endpoints.indexOf(endpoint);
      assert.notEqual(index, -1);
      if (endpoint === failed) throw new Error("synthetic domain unavailable");
      return fixtures[index];
    } }, {days: 1, timezone: "UTC"});
    assert.deepEqual(calls.slice().sort(), endpoints.slice().sort());
    return {summary, stderr};
  } finally { process.stderr.write = original; }
}
const original = await run(baseline, "/v2/heart");
assert.equal(original.summary.data_quality.missing_or_failed.heart, true);
assert.equal(original.summary.data_quality.confidence, "high");
assert.match(original.stderr, /synthetic domain unavailable/);
results.push({case:"baseline heart-only error", confidence:"high", heart_error:true, reproduced:true});
for (const failed of [null, ...endpoints]) {
  const before = await run(baseline, failed);
  const after = await run(candidate, failed);
  const expected = failed ? "partial" : "high";
  assert.equal(after.summary.data_quality.confidence, expected);
  for (let i=0; i<endpoints.length; i++)
    assert.equal(after.summary.data_quality.missing_or_failed[names[i]], endpoints[i] === failed);
  // Aside from confidence and the creation timestamp, preserve the whole public result.
  for(const s of [before.summary, after.summary]) {
    delete s.generated_at;
    delete s.data_quality.confidence;
  }
  assert.deepEqual(after.summary, before.summary);
  results.push({case:failed || "all domains succeed", expected_confidence:expected, result_preserved:true});
}
console.log(JSON.stringify({runtime:process.version,groups_passed:results.length,results},null,2));
```

Run `node test.mjs` from that directory. Actual final result: baseline heart-only failure has heart=true and confidence=high; candidate all-success=high; candidate activity/sleep/measures/heart failure=partial. All four failure flags, endpoint call sets and all other output data (excluding timestamp/confidence) were checked against baseline.

## Limits

The injected client models four synthetic responses and a thrown error. It does not validate HTTP/OAuth handling, actual Withings payloads, npm distribution, MCP serialization, Windows browser launching, timezone boundaries, days semantics or empty-success coverage. This is evidence for the specific aggregation expression, not a complete repair of issue31. Empty successful collections can still yield high; separate policy needed.

Upstream regression to add after maintainer review: extend scripts/summary-fixture-test.mjs with heart-only failure and assertions on both confidence and missing_or_failed. Run the repository's normal checks before shipping; they were not run here.
