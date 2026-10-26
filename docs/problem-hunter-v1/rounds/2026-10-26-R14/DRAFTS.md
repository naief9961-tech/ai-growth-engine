# R14-01 — QwenPaw #8424

Status: **AWAITING USER APPROVAL — NOT POSTED**.
Destination: https://github.com/agentscope-ai/QwenPaw/issues/8424
Re-read the issue, linked PRs and contribution policy before any separately approved publication.

---

AI-assisted source review at [b501aca9](https://github.com/agentscope-ai/QwenPaw/blob/b501aca97f8e13c730669fa1c6365f4f053895b6/src/qwenpaw/drivers/handlers/mcp_streamable_http.py). I independently checked the complete extracted `_negotiate` method with synthetic RPC outcomes, rather than running a real MCP server.

The narrow change is to remove the HTTP-404 exception inside the `_JSONRPC_METHOD_NOT_FOUND` branch, leaving its existing `_LegacyProtocolError` as the outcome. I compared the original method and that candidate in 10 paired cases (20 executions):

- 404 / -32601 changes from RuntimeError to the legacy-fallback signal.
- 200 and 400 / -32601 retain their existing fallback signal.
- 404 / -32020 and -32021 remain hard failures.
- -32022 advertising only handshake-era versions still falls back; advertising the modern version does not.
- Successful modern discovery, legacy-only discovery, and malformed discovery retain their previous outcomes.

This supports a targeted change without broadly rewriting HTTP errors or relaxing driver policy. The existing `HttpAutoClient._connect_locked` catches that signal, closes the modern client and passes the remaining timeout to one legacy attempt; I inspected that path but did not execute it.

Before merging, add an integration regression through HttpAutoClient: the reported 404/-32601 followed by successful initialize, plus failed legacy authentication and timeout/cleanup cases. Assert that fallback happens at most once and that modern protocol errors do not trigger it.

Limits: the local harness extracts source via AST, injects `_rpc`, and uses a minimal HTTPStatusError type placeholder. It does not exercise HTTP/SSE parsing, OAuth, real server connectivity, lifecycle cleanup or the upstream suite. The tests establish the classification boundary, not end-to-end compatibility.
