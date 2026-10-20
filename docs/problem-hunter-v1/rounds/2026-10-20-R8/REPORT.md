# NAIF Gravity — R8 (2026-10-20)

Reviewed at 2026-10-20T05:04:25.754Z. Base repository commit: `8816595742c00a31de4a243136844c3d381cb157`.

## Verified result

**155 unique issues screened from 160 search results; six complete candidate thread reads; one completed source investigation; two exploratory source reads.** Eight isolated test groups passed. One English draft is ready for review. No third-party comment, PR or message was posted. We deliberately did not fill a five-issue/three-reply quota with duplicate or unverified work.

## Selected issue

| Issue | Engineering result | Confidence / next step |
|---|---|---|
| [Woodhouse #29](https://github.com/recursive-cloud/woodhouse/issues/29) — signed unmatched webhooks return a silent 200 | Verified the pinned Octokit empty-listener early return, before Probot transform/guard. Proposed a per-App subscription index and post-verification metadata diagnostic, preserving HTTP and allowlist semantics. | High for source mechanism; moderate for full integration and unavailable original fixture. [Full English draft](DRAFTS.md), awaiting user approval. |

The original acceptance report/fixture mentioned in #29 is absent from inspected main and returned 404. The reproduction uses a synthetic missing-action event that follows the proven no-listener path; it does not establish the exact contents of the reporter's fixture. This is an observability gap, not a demonstrated authorization bypass.

[Tests and pinned source links](TESTS.md) · [Discovery audit and six candidate decisions](SCREENING.md).

## New follow-up evidence only

Twenty-three existing threads checked, all available comments read and compared with saved cursors.

1. [A2A Python #1341, comment 6274826969](https://github.com/a2aproject/a2a-python/issues/1341#issuecomment-6274826969), posted **2026-10-19 18:54:31 UTC**: rohityan reproduced the issue and points to [PR #1354](https://github.com/a2aproject/a2a-python/pull/1354), still open. Its four-file diff at `27bd15979b99a5198eea1358729d449f4e32c958` includes the REST `Parse` SSE path and streaming regression test. Our previously posted observation is already covered; no duplicate reply. The response addresses the original reporter, not an explicit acknowledgment of NAIF. SDK tests were not rerun.
2. [Cockpit #564](https://github.com/ktysne/agent-cockpit/issues/564) is now closed. [PR #573](https://github.com/ktysne/agent-cockpit/pull/573) merged **2026-10-19 06:06:56 UTC**, merge commit `9b7c9efcf0589d04ec6ba61fe982cdba8e48db12`. Its R7 draft was already held and never posted; now superseded permanently. No causal credit, local native rerun or deployed-release claim.

Other tracked threads had no new comments after saved cursors. The A2A cursor is now **6274826969**. No explicit commercial request or purchase evidence appeared.

## Duplicate prevention and unresolved work

- [crewAI #8289](https://github.com/crewAIInc/crewAI/issues/8289): [PR #8290](https://github.com/crewAIInc/crewAI/pull/8290) already implements ACL username/TLS and regressions; patch inspected, not tested here.
- [Linkid #900](https://github.com/vishnukothakapu/linkid/issues/900): [PR #912](https://github.com/vishnukothakapu/linkid/pull/912) already handles timeout/abort names and a hanging receiver. Source and tests read; no duplicate draft.
- [Ayme #860](https://github.com/ayme-labs/ayme/issues/860) and [codex-acp #647](https://github.com/agentclientprotocol/codex-acp/issues/647): detailed existing diagnosis/repair directions leave maintainer design decisions; no distinct validated contribution.
- [Paperless #14502](https://github.com/paperless-ngx/paperless-ngx/issues/14502): several relevant source files inspected, but no proven root cause or reproduction. No public fix draft; contribution-policy constraints and uncertainty are recorded in TESTS.md.

## NAIF tool fit

Reviewed https://naifgravity.com and https://naifgravity.com/tools on 2026-10-20, plus the current diagnostic repository README. The free tools provide bounded public-API reachability and sanitized payload structure checks; they do not inspect Woodhouse's subscription registry, validate GitHub signatures or diagnose its dispatch path. The MCP probe targets bounded Streamable HTTP discovery and does not implement stdio/OAuth. **No NAIF link or paid offer is added to the draft.**

## Tests and publication boundary

- **8 PASS / 0 FAIL** on Node v24.19.0: three actual pinned receiver-source groups (types stripped; error utilities stubbed), five candidate/helper/model groups.
- No full upstream tests, HMAC/Express/Probot integration, production system or real account tested.
- New helper is documentation/reproduction material only; no patch applied to another repository.
- Root AGENTS.md and full current tree reviewed; no nested AGENTS.md. Its unrelated bounty/payment instructions are outside this task.
- All eight current workflow definitions read. Their push filters do not match this documentation-only change. No workflow changed/dispatched, PR created, merge performed or production/payment/V5/server file edited.
- README latest links, ledger history/cursors, this report, draft, screening audit and reproducible local test material are the only intended changes under `docs/problem-hunter-v1/`.
- Git update uses a fresh parent SHA and conditional, non-forced ref update. The final delivery message links the verified commit.

## User action

Review **R8-01 only** in [DRAFTS.md](DRAFTS.md). It remains unpublished pending explicit approval. Prior drafts already posted or superseded must not be reused. No credentials, payment or infrastructure action is required.
