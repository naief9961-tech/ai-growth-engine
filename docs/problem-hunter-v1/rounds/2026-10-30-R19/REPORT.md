# R19 — 2026-10-30
Checked: 2026-10-30T05:10:24Z. Own repository base: `fb2f528d316c780471682aa5e788e2a5bdfadd45`.

## Results
- 155 capped search results, **151 distinct issue URLs** screened by title/body snippets across 11 queries, created since 2026-10-27. Search caps are not exhaustive.
- **7 complete candidate-thread reads** (body, all comments and timeline); **0 new open issues qualified for a reply**. No quota padding.
- **33 tracked threads** checked with all available comments (each below 100): no new comments after saved cursors, one state change.
- **1 completed follow-up source investigation**, justified by a newly merged fix: mppx #1113 / PR #1133. This is separate from new-issue investigation counts.
- **1 English follow-up draft** for review on the merged PR; zero third-party comments/PRs/messages posted.
- Isolated checks: three baseline false positives reproduced; ten baseline controls passed; 13 candidate classifications and 13 strict-scanner parity checks passed. No upstream suite or full transport test.
- No explicit commercial requests or purchase evidence.

## Material follow-up: mppx
Original: https://github.com/wevm/mppx/issues/1113
Prior user comment: https://github.com/wevm/mppx/issues/1113#issuecomment-6434639013
Fix: https://github.com/wevm/mppx/pull/1133

PR #1133 merged 2026-10-29T12:41:30Z as `faa4735585db43d433ff4af5a2733c09d72d0328`; issue closed at 12:41:32Z. All four changed-file diffs and PR discussion/review comments read. The original X402-only header is now guarded. Upstream author reports 155 tests/typecheck/lint; those were **not rerun** here. Merge is not deployment verification, direct acknowledgement, or evidence of causal credit to us.

New evidence at current main `c912c79a5df2589eadfcadfd30a43b7f7b5ff5c2`: the bare-scheme fallback added during review splits on every comma, including quoted commas. `Bearer realm="alpha, Payment, beta"` is classified as containing Payment; the quote-aware scanner itself correctly finds none. That disagreement can send MPP collection into the strict no-schemes error. This material post-merge edge case differs from the previously posted absence-versus-malformed advice and the PR bot's bare-Payment false-negative finding.

### Evidence and repair
- [Challenge.ts](https://github.com/wevm/mppx/blob/c912c79a5df2589eadfcadfd30a43b7f7b5ff5c2/src/Challenge.ts), blob `6d073b024753832950bf50c36981f16aa5f3ba75`: hasPaymentScheme / findSchemeStarts / deserializeList.
- [Mpp.ts](https://github.com/wevm/mppx/blob/c912c79a5df2589eadfcadfd30a43b7f7b5ff5c2/src/client/internal/protocols/Mpp.ts), blob `a4489a970032550501ce04e9a4b74f3fe60a8171`: guard delegates true classifications to fromResponseList.
- [Constants.ts](https://github.com/wevm/mppx/blob/c912c79a5df2589eadfcadfd30a43b7f7b5ff5c2/src/Constants.ts), blob `d174e90a2dc5c545c44c8089efbdfefdab433252`: Payment token.
- Prior quote-aware work [PR #766](https://github.com/wevm/mppx/pull/766) also reviewed; it does not include the later comma-split fallback.
- Bounded issue/PR searches for hasPaymentScheme and quoted Payment found #1113/#1133 and historical #766; no existing comment describing this new false-positive was found in the full #1133 discussion. This is not proof of repository-wide absence.

Suggested repair: extend the quote/escape-aware scanner with opt-in presence detection for exact bare schemes at top-level boundaries, including comma/end-of-input, preserving the strict parser's default. Confidence **high for reproduced classifier defect**, **medium-high for transport impact inferred from source**. Benefit: bounded regression that can prevent x402 fallback failure; no commercial inference.

[Full English draft](DRAFTS.md). [Reproducible isolated harness and limits](TESTS.md). Draft destination is **merged PR #1133**, not a claim that #1113 is still open. User approval and immediate thread recheck required before any later publication. Historical R16 comment must not be reposted.

## Candidates not selected
- https://github.com/temporalio/ai-integrations/issues/290 — Existing PR #291 supplies the proposed fail-fast repair, regressions, migration/breaking-change analysis and limits; no additive finding established.
- https://github.com/crewAIInc/crewAI/issues/8735 — Existing PR #8739 supplies UTC normalization and regression tests; no additive finding established.
- https://github.com/mercadopago/sdk-go/issues/155 — Reporter already supplies a seconds-versus-milliseconds repair and test commit bfeb212 in their fork; no additive finding established.
- https://github.com/anomalyco/opencode/issues/60432 — Existing duplicate #49464 and maintainer-bot v2 upgrade guidance; reporter says v2 client accepts the schema. Do not repeat diagnosis or prescribe an unverified migration.
- https://github.com/ds1/pincerpay/issues/166 — Reporter already identifies all three source defects and acceptance criteria; no independent additive source finding established.
- https://github.com/IBM/mcp-context-forge/issues/7382 — Reporter already identifies missing OAuth invocation path, grant scope, caching and failure tests; no independent additive source finding established.
- https://github.com/open-mcp-ai/Termcp/issues/236 — Reporter already provides exact correlation-contract implementation points and lifecycle regression criteria; no independent additive source finding established.

## Publication and safety
Only README, ledger and this round's documentation under docs/problem-hunter-v1/ were prepared for publication. Root AGENTS.md read; recursive tree had no more specific AGENTS.md. All eight workflow trigger definitions read at the current base: docs paths match no push workflow; no workflow edited or dispatched. Atomic expected-head update required. No production/payment/V5/server edits; no dependency installs, external tool calls, wallets or live payment flows.
No NAIF tool link is proposed: endpoint reachability/JSON tools do not diagnose this local header-classification defect. No claim of stdio/OAuth support.

## User action
Review the one new follow-up draft if desired. It has not been posted. No action is required for the seven unselected candidates. Detailed screening and follow-up cursor audit: [SCREENING.md](SCREENING.md).
