# R9 — NAIF Gravity Problem Hunter — 2026-10-21

Review completed: 2026-10-21 05:08:41 UTC. Base repository commit: `327ac56191dd49558a0e55e62cfd8670196b35c6`.

## Result

- **201 distinct issue URLs** screened from **220 capped search results** across 11 queries (20 each). These are search results, not 201 independently verified open bugs.
- Six candidate threads read in full, including all returned comments and timeline events; **two source investigations completed**. One additional related issue body (#960) checked for duplication, not counted as a complete investigation.
- Two additive English drafts in [DRAFTS.md](DRAFTS.md), pending user approval. No third-party comment, PR or message sent.
- **14 isolated groups passed**: eight timestamp-verifier checks; six Postiz catalog/relay checks. No upstream native suite or deployment test.
- 24 existing tracked threads refreshed. One newly verified **own manual comment**, no new developer replies; one newly observed issue closure. No explicit commercial inquiry.

## Selected issues

### 1. Postiz #2300 — MCP connection rejects a tool missing from a published release

Issue: https://github.com/gitroomhq/postiz-app/issues/2300  
Reporter: raymatos. Created 2026-10-21T04:42:29Z. Open; zero comments at final refresh.

**Evidence.** At main `a41e35f6adf5baf0ec8df4f2fbbcd69e7ae4fcd3`, `McpRelayService.connect` emits the reported error after comparing listed names against `LoadToolsService.coreToolNames()`. `MediaStatusTool` is registered with none of the flags that exempt tools from that required list. The latest observed GitHub release, [v2.25.1](https://github.com/gitroomhq/postiz-app/releases/tag/v2.25.1), was published 2026-10-11T15:19:10Z; its pinned tool list at `91c91f633a0175fb3914dba64c932928c514b72a` has no MediaStatusTool.

[PR #2281](https://github.com/gitroomhq/postiz-app/pull/2281) merged 2026-10-20T07:27:21Z as `499681116ef4591d59a000cccd2cc852d4529296`, adding the tool and adjust workflow. [PR #2296](https://github.com/gitroomhq/postiz-app/pull/2296) changes only submission metadata, not relay enforcement. All 88 open PR entries and the 20 most recent PR entries were screened; both relevant merged PR diffs were read. No issue-linked repair was present at final timeline refresh.

**Diagnosis/confidence.** High confidence in the release/source mismatch and admission mechanism. Moderate confidence this is the reporter's actual deployment cause: neither their running image digest nor the cloud deployment SHA is known. The release tag is not proof of what Docker `latest` serves. The relay reads one list page; pagination could matter for other servers, but there is no evidence it caused this report.

**Proposed action.** Verify sanitized version/digest and complete advertised tool names locally. Maintainers can publish/document a compatible release before requiring the new capability, or deliberately classify the feature as optional while handling unsupported adjustment/status workflows. Do not disable all compatibility checks or pretend a missing tool exists. Keep baseline identity-tool checks and explicit unsupported-call errors. Feature-policy/integration decision remains with maintainers.

**Actual tests.** Six groups PASS: pinned catalog assertions; original rejection; optional metadata permitting baseline connection; mandatory identity rejection; complete catalog acceptance; explicit unknown-tool call error. Core filter, connect and callTool methods are source-extracted; transport, URL-safety result, HTTP exception class and DI are stubbed. No live network, OAuth, image build, ChatGPT session or media processing. Benefit: high if release skew is confirmed; no full fix claimed.

**Policy.** CONTRIBUTING rejects primarily AI-generated PRs. Draft is a disclosed diagnostic discussion only, not a PR offer.

### 2. IntelliFlow CRM #940 — timestamp hardening needs full-string validation

Issue: https://github.com/talyssonoliver/IntelliFlow-CRM/issues/940  
Reporter: talyssonoliver. Created 2026-10-21T02:13:17Z. Open; zero comments at final refresh.

**Evidence.** At `729ce393fdd43ae91f6e63efc30acb4c9d5c1f5d`, both `packages/webhooks/src/framework.ts:stripeVerify` and `apps/api/src/webhooks/handler.ts:StripeSignatureVerifier.verify` use parseInt in the tolerance check. A signed nonnumeric timestamp produces NaN and skips the comparison. The reporter already identifies that bug. Our added evidence: their finite-only proposed guard still accepts a signed current numeric prefix followed by junk. Existing tests were read; malformed full-string cases were absent from the inspected verifier test sections.

**Repair.** Reject missing timestamp or any non-ASCII-digit character; convert with Number and reject unsafe integers. Keep existing tolerance behavior. Use the numeric value only for time comparison and the original timestamp/raw payload for HMAC. Apply consistently to both copies or consolidate with native regressions. A negative-character regex also rejects a trailing newline that an end-anchor-only pattern can overlook.

**Actual tests.** Eight groups PASS against both extracted verifiers: baseline NaN acceptance; finite-only counterexample; strict malformed-input rejection; valid signatures/original timestamp preservation; inclusive ±300-second boundaries and ±301 rejection; unsafe/out-of-window integers; wrong key/modified raw body; missing components. Public synthetic key and fixed clock only. No provider API, real key, payment data, HTTP ingress or full native suite. High confidence in local behavior; benefit moderate (incremental hardening). Not an authentication-forgery claim: every accepted malformed fixture had a correct synthetic HMAC. No evidence of secret-free exploitation or real Stripe malformed timestamps.

**PR/duplicate review.** All three open PR entries plus 30 recent PR entries reviewed. No linked repair in refreshed timeline. Related #960 was read and covers other PG-208 hardening, not this timestamp parser.

## Follow-up changes only

- **Woodhouse #29:** verified the user's comment [6283913029](https://github.com/recursive-cloud/woodhouse/issues/29#issuecomment-6283913029), posted 2026-10-20T05:12:50Z. It is the shortened manual version, not byte-identical to the R8 draft. Cursor advanced to that ID. No developer reply. R8 draft marked historical / do not repost; this is not authorization for another comment.
- **Trinity #3749:** [closure event](https://api.github.com/repos/Abilityai/trinity/issues/events/33778857988) at 2026-10-20T19:44:43Z. PR #3750's merge was already reported in R3 and is not new. No new comment or independently verified live acceptance; no causal credit claimed.
- Remaining 22 tracked threads: no new comments after saved cursors. Historical replies retained; no repeat announcements.
- Commercial interest: **none newly observed**. Closure and technical activity are not a purchase or service request.

## Screening / exclusions

See [SCREENING.json](SCREENING.json) for 201 URL/title entries, query provenance and detailed decisions for six candidate threads. Comparison against the prior radar, ledger and 1,437 URLs extracted from existing screening documents found no URL overlap in this discovery set. This is URL-based deduplication, not proof against cross-repository semantic duplicates.

- kagent #3295: open PR #3296 already targets the reported failure and requested turn-continuation boundaries; no additive reply.
- agent-framework #9566: reporter and existing bot response already document data loss, reproduction and proposed mapping; no extra independently verified value.
- OpenCode #57643: existing bot reproduction and top-level-object workaround already cover the observed failure; protocol/degradation decision remains upstream.
- Harbor #24186: report already includes source, reproduction and repair boundaries. No additional verified result; no heavy deployment test.
- Seventeen repetitive “Free private tools/list baseline” promotional entries excluded. Other rows include feature/backlog work, out-of-scope failures and automated CI alerts; not counted as completed investigations.

## Free-tool suitability

Re-read https://naifgravity.com, https://naifgravity.com/tools and the current diagnostic repository README on 2026-10-21. The tools page offers bounded public API reachability and sanitized JSON structure checks; it cannot validate a Stripe signature. The existing MCP probe supports bounded Streamable HTTP discovery and omits tool names from reports, so it cannot prove that mediaStatusTool is present; it does not implement OAuth login or stdio. Neither draft includes an unsuitable promotional link or paid offer.

## Publication and limits

Only documentation/evidence under `docs/problem-hunter-v1/` is proposed for this own-repository update, with a current-head atomic commit. Root AGENTS and all eight workflows were inspected. Three push workflows are path-filtered to server.json, agent metadata or workflow files; this docs-only change does not match them. Other workflows have no push trigger. No workflow was dispatched, edited or requested; no PR created/merged.

No production, payment, V5, server or external system changed. No spending, secret request or heavy work.

Reproducible local evidence: [TESTS.md](TESTS.md), [checks.mjs](checks.mjs), [sources.json](sources.json), [results.json](results.json). Upstream files are not vendored. An initial local source-export newline mismatch was rejected by the hash gate before any checks; exact fetched bytes corrected it, and the final run verifies all seven blob hashes.

For the user: review the two complete English replies before any future third-party publication. No action is required to repeat historical comments. Final delivery links the actual own-repository commit after verification.
