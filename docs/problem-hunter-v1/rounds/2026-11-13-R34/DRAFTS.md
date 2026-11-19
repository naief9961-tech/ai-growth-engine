# R34-01 — Historical reply; DO NOT POST

**SUPERSEDED_BY_UPSTREAM_FIX — DO NOT POST.** Checked 2026-11-13T05:12:10Z. Destination: https://github.com/microsoft/apm/issues/3711

The reporter's path correction and workaround are already posted; this draft adds only the SSE compatibility boundary and isolated checks. Re-read comments and linked PRs immediately before any future publication. No advertising.

> Retirement verified2026-11-19: [upstream PR3789](https://github.com/microsoft/apm/pull/3789) merged at932e45ffbf92bb7ac6ebdcfa73601ae6232e2149 on2026-11-17, covering serverUrl and unsupported SSE. Issue3711 is closed. This draft was never posted; preserved below solely for history. Prior isolated test claims belong to R34, not a new R35 run.

<!-- BEGIN HISTORICAL REPLY — DO NOT POST -->
One additional transport case to cover after your retest: the inherited formatter also accepts legacy SSE, emitting `{"url": "..."}`. Antigravity CLI's current MCP docs say remote servers require Streamable HTTP; legacy SSE is unsupported:
https://antigravity.google/docs/mcp#global-and-workspace-server-configs

At `4782e389daf2`, Antigravity inherits Gemini's formatter unchanged:
https://github.com/microsoft/apm/blob/4782e389daf2b05f9fd762a65dec8c0cdade5177/src/apm_cli/adapters/client/gemini.py

I'd keep the change in the Antigravity adapter: emit `serverUrl` (or `url`) for HTTP/Streamable HTTP, and reject a selected legacy-SSE endpoint with a clear unsupported-transport error. Renaming a key cannot convert an SSE server's protocol. Gemini should retain its existing `httpUrl`/SSE behavior.

I ran nine offline check groups against extracted, hash-verified source and a small Antigravity-only candidate: HTTP, Streamable HTTP, empty/omitted transport defaults, SSE, an invalid transport, minimal stdio, and both config paths. The candidate handled those cases while retaining Gemini's behavior in the formatter controls.

These were isolated Python checks, not an `agy` connection test or the full APM suite; headers/env resolution and package-backed stdio remain untested. I'd add these transport regressions alongside the existing path tests before integration.
<!-- END HISTORICAL REPLY -->

[Evidence and test limits](TESTS.md).
