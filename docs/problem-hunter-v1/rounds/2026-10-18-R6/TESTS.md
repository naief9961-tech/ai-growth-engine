# R6 — Isolated checks and explicit limits

Executed 2026-10-18 using Python 3.12.14 and Node v24.19.0. **11 checks passed**, exit status 0. The first local source-hash check detected an extra newline introduced while materializing files; removed only that extra newline and verified all five original Git blob hashes before execution. No source changes were hidden by relaxing hash verification.

## Reproduction

Download this directory, then:

```sh
python fetch_sources.py
python test_boundaries.py
node test_webhook.cjs
```

The fetcher is provided for a network-enabled environment. In this run sources were retrieved through the GitHub connector, then independently blob-hash verified locally; the urllib fetcher itself was not executed. Upstream source is not vendored or relicensed. manifest.json pins five reviewed files.

See [Python output](python-results.txt) and [Node output](node-results.txt).

| Area | Source baseline / guard | Candidate / model | Scope |
|---|---:|---:|---|
| AIM | 1 | 2 | AST-extracted list_skills; fake _make_request; pinned server route text |
| WordPress | 2 | 4 | AST-extracted _request; fake responses, transport classes, logger and async sleep; independent delay helper |
| Tududi | 1 | 1 | Extracted recordEvent/handleWebhook; in-memory ORM stub; separate claim model |
| Total | 4 | 7 | 11 passed |

The source baselines reproduce the old AIM path, a 0.5-second retry despite Retry-After:60, and failed webhook retry suppression; the fourth verifies existing POST-500 no-retry behavior.

Candidate checks cover AIM populated/empty lists and authorization-error propagation; delay-seconds, dates, malformed/missing/non-ASCII values and over-budget/oversized deferral; one exclusive model claim across eight contenders and terminal suppression.

## Not executed

- No full Python SDK, pytest/httpx integration or Go server/auth/signature tests. httpx is not installed; fake transport behavior is explicitly substituted.
- No integrated Retry-After patch. The policy helper is tested independently, not wired into the production request loop.
- No Sequelize/Jest tests, real database locks, cross-process concurrency, leases/fencing, crash recovery, provider signatures or side-effect idempotency. The JavaScript claim model does not prove database correctness.
- No WordPress, MCP host, OAuth/stdio, deployments or production/payment calls.
- No benchmark, paid service, dependency install or heavy build.
