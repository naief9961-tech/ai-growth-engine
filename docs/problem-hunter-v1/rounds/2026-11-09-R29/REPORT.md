> **Update 2026-11-10: SUPERSEDED — DO NOT POST R29-01.** Upstream PR100 merged and issue80 closed. This is historical evidence only; see [R30](../2026-11-10-R30/REPORT.md). No R29 comment was posted.

# R29 — 2026-11-09: post-write confirmation deadline

Reviewed at 2026-11-09T05:03:33Z (08:03 Saudi Arabia). Base main: `6548bd33a7ccaba1018d25e62e3f8cd3df125440`.

## Counts and selection

- 69 returned search results, 67 unique issue URLs initially screened across seven topic queries (MCP, A2A, x402, webhook, schema, API, GitHub Actions), open issues created since 2026-11-06, newest-first, up to ten per query. This is capped discovery, not all of GitHub.
- Five candidate issue descriptions with all returned comments and timeline events read; one related issue (#79) read separately.
- One completed bounded source investigation (#80); one additional exploratory source read (Tender). Two existing PR implementations/test patches reviewed for exclusion.
- Five isolated regression assertion groups passed. No upstream complete suite, live endpoint, payment, CLI or deployed-system test.
- One English review draft; zero third-party comments, PRs, messages or repairs.
- 44 prior follow-up threads and four PR review/inline-comment streams checked. Zero new human replies; one automated Codecov update. No new explicit commercial inquiry.

## Selected case (one; no quota filling)

[open-bot #80 — save persists but no acknowledgement](https://github.com/shpaw415/open-bot/issues/80), opened 2026-11-09T04:46:47Z, reporter shpaw415. Open, zero comments/timeline events at final recheck.

Post-success confirmSave starts GET before checking the overall save deadline, while each call has a separate 20s timeout. This gap is demonstrated locally; causal attribution to reported deployment remains unproven.

The source declares a 25s save budget, but confirmSave checks it after an awaited get, while call supplies a fresh 20s abort timeout. The CLI buffers output until the request finishes and its 90s curl limit is longer than the report's outer 12/30s limits. In addition, optional group assignment precedes the final saved message; deployment revision and per-stage timings are needed before assigning the field symptom exclusively to confirmation.

Proposed change: Return confirmed:false after acknowledged POST when confirmation budget is exhausted; check before/after polling; pass remaining budget into the read's abort signal. Preserve success-with-indexing-note. Do not automatically retry an uncertain write; full write-stage budgets need separate design.

Confidence: High for pinned-source confirmation gap and isolated regression; medium as explanation for this deployment; deployed SHA/stage timings unknown.

Regression evidence: Five isolated Node v24.22.1 assertion groups passed using actual pinned source (import suffix adjusted), candidate source, injected fetch, synthetic payload and controlled clock. One candidate stalled read respects real abort signal. No CLI/router/OpenViking/integration/upstream suite or payment test. See [exact harness and candidate diff](TESTS.md). A successful isolated check does not prove that the full reported system is fixed. Validation, snapshot, delete, POST, rollback, desktop startup and group assignment are not given a complete shared deadline by this candidate.

Related [#79](https://github.com/shpaw415/open-bot/issues/79) reports a missing write after timeout; #80 reports verified persistence. They are related but not treated as the same proven cause. Both have zero comments/events. All PRs listing returned only [historical #2](https://github.com/shpaw415/open-bot/pull/2), merged 2026-10-15 and unrelated to this confirmation gap.

### Source evidence

Pinned revision: `dddefb9bcd7c57d2b9605a8f41c7ea03ad6e0bec`.
- [apps/control/src/viking-skills.ts](https://github.com/shpaw415/open-bot/blob/dddefb9bcd7c57d2b9605a8f41c7ea03ad6e0bec/apps/control/src/viking-skills.ts) — blob `d438b5f0c70dd608449cc1f1578f376a1d9f8e32`.
- [apps/control/src/skills-routes.ts](https://github.com/shpaw415/open-bot/blob/dddefb9bcd7c57d2b9605a8f41c7ea03ad6e0bec/apps/control/src/skills-routes.ts) — blob `99eb3f93faf72d2812be412f814015b465c06576`.
- [scripts/ob-skill.sh](https://github.com/shpaw415/open-bot/blob/dddefb9bcd7c57d2b9605a8f41c7ea03ad6e0bec/scripts/ob-skill.sh) — blob `619947e2f8d1c6233b591647f70da47dfe06368d`.
- [apps/control/src/viking-skills.test.ts](https://github.com/shpaw415/open-bot/blob/dddefb9bcd7c57d2b9605a8f41c7ea03ad6e0bec/apps/control/src/viking-skills.test.ts) — blob `5a0a30b89a1bb428875de4ad9498c89e23da6801`.
- [scripts/ob-skill.test.ts](https://github.com/shpaw415/open-bot/blob/dddefb9bcd7c57d2b9605a8f41c7ea03ad6e0bec/scripts/ob-skill.test.ts) — blob `387162893f670c2808cf6c396e037529313b8603`.
- [apps/control/src/http-error.ts](https://github.com/shpaw415/open-bot/blob/dddefb9bcd7c57d2b9605a8f41c7ea03ad6e0bec/apps/control/src/http-error.ts) — blob `cf7fb905dc0065c98989bcc56f9b22d588de9740`.

## Four reviewed candidates withheld

- [residuum issues 852](https://github.com/Grizzly-Endeavors/residuum/issues/852) — Existing open PR #854 already adds the timeout, concurrent refresh and nonblocking registration; relevant source patch and regression test read. No additive reply.
- [woocommerce-gateway-stripe issues 6180](https://github.com/woocommerce/woocommerce-gateway-stripe/issues/6180) — Existing open PR #6179 already guards null charge, queues bounded retry and adds a regression test; relevant implementation and test patch read. No payment tests or new reply.
- [tender issues 8](https://github.com/heyarca/tender/issues/8) — Reporter already gives the missing post-handler 402 branch, proposed response normalization and regression criteria. Current handlers.ts at a4980b8cf0c3294610b8777d34cfe74679f405c2 corroborates >=500 guard, but SDK settlement path not independently tested. No additive reply; status normalization alone must not be described as preventing double payment.
- [mikro-orm issues 8652](https://github.com/mikro-orm/mikro-orm/issues/8652) — Reporter provides PostgreSQL forms, diagnosis, regression and explicitly plans a fix. Latest 30 updated PRs inspected; no matching new PR observed, not an exhaustive historical absence claim. No independent DB test or additive proposal.

Relevant existing fixes: [Residuum #854](https://github.com/Grizzly-Endeavors/residuum/pull/854) and [Stripe #6179](https://github.com/woocommerce/woocommerce-gateway-stripe/pull/6179). Their tests were read, not executed here.

## Follow-up: new information only

One new [Codecov report on BanyanDB #1460](https://github.com/apache/skywalking-banyandb/pull/1460#issuecomment-6729639145). It is automated coverage metadata, not a developer response or commercial interest. Cursor advanced from 6643237537 to 6729639145; prior human acknowledgements are retained in history and not reannounced. No other new issue comments or PR review comments were found. All 44 existing states remained unchanged.

## Free-tool fit

Read the current diagnostics repository README at `d58c1c2322ade7fdb03d7bfdb97200751dd43431`, [website](https://naifgravity.com/) and [/tools](https://naifgravity.com/tools). The tools page retrieval was cached five days earlier; no live probe was run. The bounded public HTTP/JSON tools do not diagnose this internal save lifecycle. The MCP discovery probe does not test tools/call, stdio or OAuth, and does not fix A2A, payment settlement or webhook signature behavior. No NAIF link or sales offer is included in the technical draft.

## Repository and safety verification

Mandatory prior radar, README, ledger and latest R28 report read from the current main. Root AGENTS.md read; recursive tree has no nested AGENTS.md affecting this documentation path. Out-of-scope bounty/payment operations in root guidance were not performed. All eight workflow definitions read: push triggers are scoped to server.json, discovery metadata or named workflow files, not this docs directory. PR/review/comment/schedule/dispatch workflows are not invoked by this direct docs-only update.

Prepared one atomic expected-head update, preserving all prior issue/follow-up/history entries. Files limited to this directory: README, ledger, and R29 REPORT/DRAFTS/TESTS/SCREENING. Commit result is provided with the delivered report after read-back. No workflow dispatch, production/store/payment/V5/server changes, spending or heavy work.

## Review decision

[R29-01 full English response](DRAFTS.md) is PENDING_USER_APPROVAL and not posted. User action: review and approve this specific response if desired. Re-read the live issue and linked PRs immediately before any future post. No second or third draft was manufactured.
