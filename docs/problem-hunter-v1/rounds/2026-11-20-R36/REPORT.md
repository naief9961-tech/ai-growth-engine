# R36 — 2026-11-20

Checked 2026-11-20T05:09:56.687Z. One bounded source/CLI investigation completed; one English draft pending user approval. **No third-party comment, PR or message sent.**

## Counts and coverage
- 70 capped search results, 67 distinct issue URLs screened; seven queries with ten newest results each, `is:issue is:open created:>=2026-11-17` plus MCP / A2A / x402 / webhook / schema / API / "GitHub Actions". This is not exhaustive 72-hour coverage.
- Five complete candidate issue/comment/timeline reads. One completed bounded source investigation; four deferred/excluded candidates, not four additional diagnoses.
- 50 tracked threads checked with all issue-comment pages; four tracked PR discussion/review timelines checked. Two new third-party comments and one manually posted NAIF comment reconciled.
- 11 synthetic Git CLI assertion groups passed; zero GitPython/MCP/protocol/full-suite runs. One draft, zero commercial inquiries established.

## Selected investigation
[modelcontextprotocol/servers #5641](https://github.com/modelcontextprotocol/servers/issues/5641), reporter snowyLumiere, created 2026-11-20T05:03:54Z, open with zero comments at review.
Source: [server.py](https://github.com/modelcontextprotocol/servers/blob/c799c8552b0f27b7a33a7b9233773da144dddcf5/src/git/src/mcp_server_git/server.py), commit c799c8552b0f27b7a33a7b9233773da144dddcf5, Git blob a6116db44b6bf0312e1610477f683bb71dee1f01.
`git_branch` forwards `repo.git.branch(b_type, *contains_sha, *not_contains_sha)` unchanged. The reporter already identified the active-branch marker. Our additional evidence: linked-worktree marker, color, and a detached-HEAD pseudo-entry survive naive approaches; `git for-each-ref` over selected ref namespaces avoids presentation entries in the isolated test.

Candidate: enumerate refs/heads, refs/remotes or both; preserve option-injection guards and contains/not_contains filters, retain invalid-type errors. Separate current-branch metadata. Short display names can collide with tags; remote refs are not universal checkout targets. Full protocol integration remains required.

Confidence: high for observed source/CLI mechanism; medium for integration proposal. Expected value: a specific detached-HEAD regression beyond the existing report, with reproducible test coverage. No guarantee of maintainer adoption.

PR check: complete issue timeline, open PR collection, and newest100 all-state PR summaries; no linked repair observed. The connector's is:pr search returned issue records and was not treated as a valid PR search. Historical PR coverage is bounded, and must be refreshed before posting.

## Other candidates examined, not selected
- [BerriAI/litellm/issues/53031](https://github.com/BerriAI/litellm/issues/53031): Deferred: issue and comments read, but provider-specific schema transformation was not inspected or reproduced. Removing constraints without checking their semantics is not a validated fix.
- [winsznx/routedock/issues/732](https://github.com/winsznx/routedock/issues/732): No additional draft: reporter already identifies mount-relative req.path and supplies the full-path fix/regression requirements; three implementation applications present. No distinct tested addition.
- [winsznx/routedock/issues/731](https://github.com/winsznx/routedock/issues/731): No additional draft: reporter already specifies request-scoped waitUntil and callback ordering; implementation application present. No distinct tested addition.
- [GoodOlClint/CrossTalk/issues/145](https://github.com/GoodOlClint/CrossTalk/issues/145): Excluded: planned startup-registration architecture and dependencies already specified; no bounded defect repair established.

No repair, confidence or runtime validation is claimed for these four. [Screening inventory](SCREENING.md).

## New follow-up evidence
- [PowerPoint #665 manual comment](https://github.com/aws-samples/sample-spec-driven-presentation-maker/issues/665#issuecomment-7000865667): author naief9961-tech, posted 2026-11-19T05:42:24Z. Verified; do not repost. Previous403 attempt remains in history. No later developer response observed.
- [OpenViking new comment](https://github.com/volcengine/OpenViking/issues/6471#issuecomment-7002017251): contributor opened [PR8001](https://github.com/volcengine/OpenViking/pull/8001), open/unmerged at b96a6e8729aef43ae9b74217f2ab6b6cd9b8df09. The reported request/response classification fix and tests are attributed to the contributor; no local rerun, deployment proof or sale claimed.
- [Openbot new comment](https://github.com/nightly-labs/openbot/issues/7357#issuecomment-7002266130): another report, #12550, linked. This is not a resolution or commercial request.

All last_seen_comment_id cursors advanced to observed issue-comment IDs; review IDs remain separate. Existing history preserved.

## Tool fit, limitations and publication
The current naif-gravity-mcp-diagnostics README was read. Its HTTP discovery probe is not a stdio Git tool-output repair; no NAIF link or paid offer is inserted into the draft. No tool-page referral is made.

GitPython is unavailable; no dependency installation was attempted. Tests use only synthetic commits in temporary local repositories and real Git2.56.1. They do not establish MCP-server correctness, macOS behavior, downstream tool compatibility or release readiness.

Root AGENTS.md and all8 workflows were inspected. No scoped AGENTS file appears in the complete tree. These documentation paths do not match any push workflow path filter; no workflow dispatch, workflow edits, production/payment/server/V5 changes or spending performed. Only docs/problem-hunter-v1 paths are prepared for an atomic current-head-checked commit.

## Full review draft — R36-01
Destination: https://github.com/modelcontextprotocol/servers/issues/5641

Status: **PENDING_USER_REVIEW — NOT POSTED**. Fresh issue/comment/PR check required before publication. User approval must refer to this draft.

I checked `git_branch` at c799c8552b0f27b7a33a7b9233773da144dddcf5. It returns the presentation output from `repo.git.branch(...)` directly, consistent with this report.

One extra edge case for the proposed `--format=%(refname:short)` fix: on Git 2.56.1, a detached HEAD still produces a pseudo-entry such as `(HEAD detached at ...)`. That is not a branch name. Linked worktrees also make the unformatted command emit `+ branch`, so stripping only `* ` would miss another case.

A candidate is to enumerate actual refs with `for-each-ref`, mapping local/remote/all to `refs/heads`, `refs/remotes`, or both. For example, for local branches:

```sh
git for-each-ref --format='%(refname:lstrip=2)' refs/heads
```

Keep the existing `contains` / `not_contains` argument guards and pass their filters through; keep invalid branch types as errors. If current-branch information is needed, return it separately instead of embedding it in a name. This short-name representation still needs care for branch/tag name collisions; a structured result could preserve both the display name and the full ref. Remote refs should not be treated as directly interchangeable with local checkout targets.

I ran 11 isolated assertion groups against real Git CLI repositories with synthetic commits. These covered the failing `* main` resolution, linked-worktree markers, forced branch colors, remote symbolic HEAD, local/remote/all selection, both containment filters, detached HEAD, and a branch/tag collision. The detached case fails the format-only approach; enumerating the ref namespaces avoids the pseudo-entry.

This was CLI-level validation, not a GitPython or MCP-server test. Before merging, add server-level regression tests for those cases and representative branch → show/diff/checkout/merge calls, retaining the existing confinement and flag-injection protections.

[Reproducible local evidence and exact harness](TESTS.md).
