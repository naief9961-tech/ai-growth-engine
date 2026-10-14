# NAIF Gravity — GitHub Issue Radar: MCP and x402 failure boundaries
**Review date:** 2026-10-14 · **Type:** public, source-grounded diagnostic notes · **Status:** proposed remediation, not shipped patches.

These observations credit the original reporters and focus on reproducible technical next steps. **NAIF Gravity has not fixed the third-party repositories, reproduced their complete environments, made payment requests, or posted comments to the issue threads.** Do not include customer data, secrets, card details, transaction signatures or private endpoints in examples.

## 1. Stdio MCP bridge: timeout, protocol stdout and HTTP framing

**Original report:** [feedback-loop-ai/swarmail #40](https://github.com/feedback-loop-ai/swarmail/issues/40). Read-only source check at [`ac8c3261`](https://github.com/feedback-loop-ai/swarmail/tree/ac8c3261a7d3fa35e1c415b616731cace7917c75): `src/stdio.rs`, `src/main.rs`, `tests/stdio.rs`.

**Failure boundary:** `src/stdio.rs` applies `READ_TIMEOUT = 10 s` to all HTTP exchanges even though `swarmail_wait_for_email` accepts waits up to 60 s. The bridge writes a newline for a successful HTTP 202 with no body; that empty stdout line is invalid in newline-delimited JSON-RPC. It also passes along the HTTP response tail without checking status or framing, and `src/main.rs` initializes tracing without forcing stderr.

**Testable repair plan:**

1. Decode each inbound request as JSON-RPC and track whether it has an `id`. For successful notification requests such as `notifications/initialized`, consume HTTP 202/204 without emitting any stdout bytes. A valid request with an ID must receive exactly one valid JSON-RPC response/error. Do not manufacture errors with `id:null` in response to notifications.
2. Respect the tool's *validated* `timeout_ms` plus bounded network headroom, while rejecting unsupported values explicitly. A valid 15-second wait cannot be forcibly cut at 10 seconds. Avoid unbounded timeouts.
3. Parse the actual HTTP status, headers and response framing, including `Content-Length`/chunked replies; do not use `raw.split("\r\n\r\n").nth(1)` as an HTTP parser. Surface failed/non-JSON replies as JSON-RPC errors with the request ID, never raw HTML/plain text on stdout. Use parse-error code `-32700` for malformed JSON input.
4. Ensure `tracing_subscriber::fmt().with_writer(std::io::stderr)` for the stdio mode. Normalize trailing slashes so a base URL ending in `/` produces `/mcp`, not `//mcp`.
5. Regression: send `initialize`, `notifications/initialized`, `tools/list` and assert **exactly two nonempty, parseable stdout records and no blank records**, with no test-side blank-line filtering. Cover success after 15 seconds, HTTP 4xx/5xx, malformed/empty responses, chunking, trailing slash and stderr logging.

These are design-level remediation steps; no changes were applied upstream.

## 2. Legacy MCP connection healthy, then health check loops reconnects

**Original report:** [CherryHQ/cherry-studio #21674](https://github.com/CherryHQ/cherry-studio/issues/21674). Windows v2.1.6; observed connect → health-check timeout → tool-list error → reconnect.

**Diagnostic distinction:** The reporter separately observed a legacy protocol negotiation, working `ping`/`tools/list`, and `-32601` for `server/discover`. The provided logs **do not capture** the latter method. That makes a protocol-incompatible optional probe a hypothesis, not yet a confirmed root cause.

**Testable repair plan:**

1. Record negotiated protocol version, health method name, request ID, elapsed time, JSON-RPC error code, child PID and child exit status to stderr (redact workspace/server names).
2. In a fake legacy stdio server, implement `ping` and `tools/list` while returning `-32601` for the unsupported optional method. Confirm whether Cherry actually sends that method and whether it tears down an otherwise working transport.
3. If an optional probe is unsupported, do not infer a dead connection from `-32601` alone; verify a supported `ping` before preserving the connection. A genuine EOF/pipe break is different and should trigger bounded-backoff reconnect.
4. Regress legacy and modern negotiated revisions, true child crashes, slow tools/list, stale catalog cache and repeated reconnections; do not globally disable health checks.

**No-credential checklist:** [MCP server not responding](https://naifgravity.com/discover/mcp-server-not-responding).

## 3. x402 `PAYMENT-REQUIRED` exceeds client header budgets

**Original report:** [x402-foundation/x402 #3803](https://github.com/x402-foundation/x402/issues/3803). The original author reports failures with Node/undici (total headers around 16 KiB) and aiohttp (single header line around 8,190 bytes), often due to lengthy Bazaar examples and schemas inside base64-encoded `PaymentRequired`.

**Testable repair plan:**

1. Measure **encoded on-wire header bytes**, not just JSON/source payload size; base64 expansion is material. Include the header name/delimiter and allow headroom for other response headers/proxies. An advisory around 7 KiB for the individual encoded header leaves safer room than aiming at the parser's exact 8,190-byte line limit.
2. Prioritize compact Bazaar *illustrative* input/output examples rather than full representative datasets. Keep required payment-acceptance fields intact; never silently truncate a security-relevant or signed `accepts` structure.
3. Warn sellers before publishing an oversized example and in middleware when a challenge approaches/exceeds the configured budget; attach the route and largest metadata field names, not raw customer payloads.
4. Regression-test an unpaid 402 from Node native `fetch`, `@x402/fetch`, aiohttp and httpx at both boundary lengths with multiple `accepts` options. Header overflow happens **before payment verification**.
5. Client-side `UND_ERR_HEADERS_OVERFLOW` alone does *not* prove that `PAYMENT-REQUIRED` was the offending header; label it a likely oversized-response-header condition unless corroborated by seller-side header metrics.

## 4. Array/object arguments rejected for MCP tools advertised with `$ref`

**Original report:** [morluto/rea #3408](https://github.com/morluto/rea/issues/3408). Reporter sees strings work, but arrays/objects fail MCP argument validation on Windows with Claude Desktop; `$ref`/`$defs` compatibility is a reported root-cause hypothesis, not yet confirmed by a paired protocol trace.

**Testable repair plan:**

1. Capture and redact the *actual* `tools/list` schema received by each client and the JSON types in one `tools/call` request; distinguish a schema-resolution failure from an argument serialization issue.
2. For compatibility, experiment with **bounded inlining** of local `$ref`s into tool input schemas (detect cycles and limit size). Do not change the server's true typed validation or permissively coerce arbitrary objects from strings.
3. Re-list tools after each schema change to defeat stale client caches; test a string-only call, `allowed_origins` as array, and `capture_browser_scenario` with nested object + array; verify all expected JSON types reach the handler.
4. Make the error identify the offending property and expected type, not just generic `Invalid input`. Do not collect production browser tabs, cookies or credentials during testing.

**No-credential checklist:** [MCP tool schema invalid](https://naifgravity.com/discover/mcp-tool-schema-invalid).

## Limits, ethics and handoff

- These notes were drawn from *public GitHub issue descriptions* and read-only source inspection where explicitly stated; they are **not customer case studies** or proof of successful repairs.
- The [free NAIF Gravity diagnostic tools](https://naifgravity.com/tools) cover bounded public API health and sanitized webhook/JSON samples. The [standalone MCP health probe](https://github.com/naief9961-tech/naif-gravity-mcp-diagnostics) covers Streamable HTTP negotiation and listing; **it does not test stdio servers or execute repairs**.
- Any implementation belongs to the affected repository's maintainers after their review. Do not send unsolicited bulk comments, auto-close third-party issues, fabricate issue ownership, or claim that diagnostics imply a purchase.
- For a real integration request, collect only sanitized reproduction steps, exact tool/client versions, acceptance tests, and an explicit customer authorization before any scoped technical work.
