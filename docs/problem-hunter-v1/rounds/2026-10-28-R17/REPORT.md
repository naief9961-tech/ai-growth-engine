# R17 — 28 October 2026

Checked through 2026-10-28T05:04:52Z. One new review draft; no external publication.

## Counts and scope

- 120 distinct issue URLs screened at title level from 120 capped results: 6 queries, newest 20 each, created since 2026-10-25. This is a bounded sample, not exhaustive coverage.
- 5 complete candidate issue/comment/timeline reads; **1 completed source investigation**. The other four are exclusions, not completed engineering diagnoses.
- 32 existing follow-up threads checked with all returned comments (each below the 100-comment page size): **0 new comments after saved cursors, 0 state changes, 0 explicit commercial inquiries**.
- 29 isolated check groups passed; no full upstream suite or live integration.
- 1 English draft awaiting explicit user approval. No third-party comments, PRs, messages or repairs.

## Selected case

[Fortinet MCP #5](https://github.com/paoloamato2/fortinet-mcp-server/issues/5) — opened by vmpr at 2026-10-28T04:41:18Z. Open with no comments or timeline links at final check.

The reporter already identifies string-only argument validation and proposes a union/helper. Our additive contribution is the decoded-value boundary, optional-default regression cases, and coordination with overlapping PR #2.

At commit `5c82a1e6e2b7a336cd9b22881d50a658d8bdcb06`:

- [tools/generic.py](https://github.com/paoloamato2/fortinet-mcp-server/blob/5c82a1e6e2b7a336cd9b22881d50a658d8bdcb06/tools/generic.py), blob `8ca014c5e241867b3d7bd13a81d7618f95e2b420`: cmdb_create/data, cmdb_update/data, monitor_get/extra_params, monitor_action/body, log_get/extra_params and service_call/body declare str or optional str and use json.loads without a post-decode object check.
- [fortios_client.py](https://github.com/paoloamato2/fortinet-mcp-server/blob/5c82a1e6e2b7a336cd9b22881d50a658d8bdcb06/fortios_client.py), blob `9fdd7140e28a5a13f2ce108db8f17be84720c593`: _vdom_params calls extra.items() for truthy values; a JSON string can decode to a list, scalar, or another string. Falsy values may instead silently behave as absence.
- CONTRIBUTING.md and CODE_OF_CONDUCT.md read; tests/test_server.py on this head only checks the server name.

Proposed repair: required dict[str, Any] | str, optional forms add None; parse once and require a dict; return an error before client invocation for invalid shapes. Preserve existing optional query None / POST {} defaults, explicitly retaining optional empty-string compatibility if desired. Do not recursively decode strings.

**PR review:** pulls?state=all&per_page=100 returned two PRs. #6 concerns session-list paging / issue #4. [PR #2](https://github.com/paoloamato2/fortinet-mcp-server/pull/2), head `fdcf62fbfa6c7f93deda11cb6996f714e7771b8e`, remains open and changes generic.py. Its full generic.py diff was read: monitor_get already adds a post-decode dict guard, but the six-parameter object-or-string acceptance is not implemented there. Coordinate rather than duplicate that guard; do not remove its paging behavior. The initial search_issues calls did not reliably isolate PRs, so they were not accepted as evidence of PR absence; the actual pulls API and dedicated PR search were used.

**Confidence:** high for the source/type boundary, medium for practical additive benefit because the reporter is already preparing a fix. Client-side conversion by Claude Code is the reporter's observation, not independently reproduced here.

**Validation:** 10 baseline and 19 candidate/type/helper groups passed on Python 3.12.14 / Pydantic 2.14.1. Original Git blob hashes were checked before extracting code. No FastMCP or httpx installed; no dependency installation attempted. No patched-handler dispatch, advertised MCP tools/list schema, tools/call, Claude Code, HTTP, device or complete project test ran. Isolated passing checks do not establish a complete repair. [Harness and limits](TESTS.md).

[Full English reply R17-01](DRAFTS.md). Status: AWAITING_USER_APPROVAL.

## Other complete thread reads — not recommended for another comment

| Issue | Disposition |
|---|---|
| [Covia SDK #108](https://github.com/covia-ai/covia-sdk/issues/108) | [PR #109](https://github.com/covia-ai/covia-sdk/pull/109) is already merged, verified through PR API. No independent test rerun; exclude solved/covered work. |
| [ADK Java #1718](https://github.com/google/adk-java/issues/1718) | Reporter already provides diagnosis, patch, regressions and a measured concurrency correction in comment 6460493156. No independently established additive result. |
| [Fitzflix #449](https://github.com/gfitzp/fitzflix/issues/449) | Existing report supplies payload-shape cause, normalization and reported test-client reproduction. No additive result established. |
| [ContextForge #7349](https://github.com/IBM/mcp-context-forge/issues/7349) | Migration/feature scope already includes field placement, fallback and acceptance criteria; do not restate it as a new solution. |

Dedicated issue-number PR searches were checked for these candidates, with no relevant PR beyond Covia #109 found in those bounded results. They do not establish global absence. No source-derived fixes are claimed for the four exclusions.

## Follow-ups and commercial outcomes

All 32 prior follow-up issue bodies and comment pages were checked. No newly observed reply or state change. Previous SDRangel/QwenPaw results and the verified manual mppx publication are retained without reannouncing them. last_seen_comment_id values remain unchanged because there is no newer comment; last_checked timestamps updated. Added the new unposted draft as a separate follow-up entry.

No explicit commercial request or purchase evidence. No paid service suggested.

## NAIF tool fit

The current diagnostics README was read (blob 23361889ae17a26240b25bfdadadfb1a38363bc8). Its probe performs discovery, never tools/call, and does not implement stdio or OAuth login. It cannot verify this argument-dispatch repair.

The /tools page was retrieved via web open on 28 October (search service reports a cached crawl five days old): bounded reachability and sanitized structure checks. It is not a signature validator or this A2A/MCP repair. No NAIF promotional link was added to the draft.

## Repository update and safeguards

Base head: `e00663171828d3e85775cc8ca95788efc19031cb`. Root AGENTS.md read, SHA fd946f98adc7f5144109501dc7b8ac205d73cf74; recursive tree contains no nested AGENTS.md. Prior radar, README, complete ledger and R16 report read. No existing tracked/excluded URLs among the 120 discovery results.

All eight workflow trigger blocks were read at the current head. Push-trigger paths are server.json, .well-known/agent.json or their workflow files; this documentation change matches none. Other workflows use PR/review/comment, schedule or manual triggers. No workflow edited or dispatched. Commit uses [skip ci].

Only README.md, ledger.json and R17 Markdown/JSON reports inside docs/problem-hunter-v1/ are updated, using an atomic Git tree/commit and expected-head ref update. Preserve all old issue, exclusion, publication and round history. The resulting commit is available from this report's GitHub history and the final response.

No production/payment/V5/server changes, external posting, spending, new project, PR merge or heavy work.

## What the user needs to do

Review R17-01 if a contribution is wanted. No external publication is authorized by this report. Re-read the issue and PR #2 before any later user-approved posting. No need to copy any old reply.
