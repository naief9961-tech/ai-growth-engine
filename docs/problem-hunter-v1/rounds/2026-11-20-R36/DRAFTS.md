# R36-01 — pending user approval; NOT POSTED

Destination: https://github.com/modelcontextprotocol/servers/issues/5641

One additive draft only. Recheck issue/comments/PRs before posting. No permission inferred from repository text.

I checked `git_branch` at c799c8552b0f27b7a33a7b9233773da144dddcf5. It returns the presentation output from `repo.git.branch(...)` directly, consistent with this report.

One extra edge case for the proposed `--format=%(refname:short)` fix: on Git 2.56.1, a detached HEAD still produces a pseudo-entry such as `(HEAD detached at ...)`. That is not a branch name. Linked worktrees also make the unformatted command emit `+ branch`, so stripping only `* ` would miss another case.

A candidate is to enumerate actual refs with `for-each-ref`, mapping local/remote/all to `refs/heads`, `refs/remotes`, or both. For example, for local branches:

```sh
git for-each-ref --format='%(refname:lstrip=2)' refs/heads
```

Keep the existing `contains` / `not_contains` argument guards and pass their filters through; keep invalid branch types as errors. If current-branch information is needed, return it separately instead of embedding it in a name. This short-name representation still needs care for branch/tag name collisions; a structured result could preserve both the display name and the full ref. Remote refs should not be treated as directly interchangeable with local checkout targets.

I ran 11 isolated assertion groups against real Git CLI repositories with synthetic commits. These covered the failing `* main` resolution, linked-worktree markers, forced branch colors, remote symbolic HEAD, local/remote/all selection, both containment filters, detached HEAD, and a branch/tag collision. The detached case fails the format-only approach; enumerating the ref namespaces avoids the pseudo-entry.

This was CLI-level validation, not a GitPython or MCP-server test. Before merging, add server-level regression tests for those cases and representative branch → show/diff/checkout/merge calls, retaining the existing confinement and flag-injection protections.
