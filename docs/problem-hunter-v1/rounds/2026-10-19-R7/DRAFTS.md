# R7 — English replies for review (2026-10-19)

Status update 2026-10-19: **R7-01 HELD — DO NOT POST**. New [PR #573](https://github.com/ktysne/agent-cockpit/pull/573) already covers its recommendations. R7-02 was **MANUALLY PUBLISHED BY USER — VERIFIED**, [comment 6260256914](https://github.com/bergbacher/hyde-mcp-gateway/issues/34#issuecomment-6260256914). Do not post again. These are new drafts; prior approvals do not approve them. Re-read each issue and linked PRs before any later publication. Do not repost if equivalent evidence appears.

## R7-01 — agent-cockpit #564 — historical draft, DO NOT POST

Destination: https://github.com/ktysne/agent-cockpit/issues/564

Historical text retained for audit only; superseded by PR #573:

I checked the current main at `fee87c64df55fddee0a666ac7a22bb8371991fde` and exercised the extracted `postToServer` / `fetchWithDeadline` functions with an injected synthetic transport. Both a truncated successful-response JSON body and a connection reset after a simulated write caused two POST attempts and two simulated effects, even with `retryAfterTimeout: false`.

Your proposed policy split stopped the second attempt in that harness, while preserving recovery for a nested `error.cause.code === 'ECONNREFUSED'` and an explicit 401. Leaving the new option unset preserved the existing body-error retry behavior.

A useful integration boundary is the result propagation: returning `unknownOutcome` from the client alone is insufficient. In [the MCP server at this revision](https://github.com/ktysne/agent-cockpit/blob/fee87c64df55fddee0a666ac7a22bb8371991fde/src/mcp/server.js), `postPlan`, `postPullRequest`, and `postCrossReviewSkip` currently forward only `timedOut` before falling back to HTTP errors/null. Carry the unknown-outcome result through all three and have `callTool` display the “check the dashboard before retrying” guidance; record it distinctly from `unreachable` in diagnostics.

For regression coverage, inject a transport that records the write before failing the response, assert one POST and an unknown-outcome result, and retain the refused-connection, 401 and default-policy controls. Add MCP-entry tests for the user-facing message, including an update whose first application already resolved the decision.

This confirms the retry control flow only. The simulated effects are counters, not persisted decisions; I did not run the full suite, a real Cockpit server, Claude/Codex runtime tests, or the proposed MCP result-propagation patch.

---

## R7-02 — hyde-mcp-gateway #34 — published, DO NOT REPOST

Destination: https://github.com/bergbacher/hyde-mcp-gateway/issues/34

Historical draft retained for audit. The user posted the same technical content with file links rendered as inline paths; see PUBLICATION.md.

At `3a518f59106ad6597ff27896880b1819ded64ca2`, the report reads `[...schemas.redactedSchemas.keys()]`, while the store inserts each app as its asynchronous read finishes. I reproduced the reversed order deterministically with the extracted SchemaStore: start both apps, release crm's reads first, then shop's. The live map was `["crm", "shop"]`.

If registry order is the intended report contract, this small projection in [src/boot.ts](https://github.com/bergbacher/hyde-mcp-gateway/blob/3a518f59106ad6597ff27896880b1819ded64ca2/src/boot.ts) avoids changing refresh or map semantics:

```ts
redacted: appNames(registry).filter(
  app => schemas.redactedSchemas.has(app),
),
```

The `has` filter matters: a registered app whose first schema load failed must remain absent. The isolated checks returned `["shop", "crm"]` for reversed completion, retained the last-good entries after a failed refresh, and reported only crm when shop had never loaded. The map itself remained in completion order and all reads still started concurrently.

One adjacent assertion deserves review: [test/schema-store.test.ts](https://github.com/bergbacher/hyde-mcp-gateway/blob/3a518f59106ad6597ff27896880b1819ded64ca2/test/schema-store.test.ts) also expects log-map keys in `["shop", "crm"]` order, whereas its redacted-map assertion sorts the keys. A report-only fix does not establish ordering for the store's live maps. Compare their membership without order unless that is a separate store contract.

For the boot regression, control completion with deferred promises instead of repeated runs or timing sleeps. I tested source-extracted store/control-flow code with synthetic readers and parser stubs; I did not run Vitest, the full boot integration, or typechecking.

---

لا يوجد رد ثالث. النص الأول موقوف بسبب إصلاح قائم، والثاني نشره المستخدم وتحققنا منه؛ لا تعِد نشر أي منهما.
