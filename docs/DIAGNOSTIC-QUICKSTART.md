# Diagnostic quick start

Use this guide to gather a small, reproducible integration failure before opening a public diagnostic issue.

## MCP: basic HTTP probe

1. Install Python 3 and clone the repository.
2. Choose an MCP-over-HTTP endpoint that you own or are authorized to test.
3. Run:

```bash
python3 tools/mcp_health_check.py https://your-mcp.example/mcp
```

The example hostname is a placeholder. The script posts an `initialize` request using protocol version `2025-06-18`, followed by `tools/list`, passing an MCP session ID if the server returned one. Each request has a 10-second timeout.

On a server returning plain JSON results, output has this general shape; the count varies:

```text
[initialize] HTTP 200
json-rpc: result

[tools/list] HTTP 200
json-rpc: result
tools: <count>

No tools were executed.
```

### Interpret the evidence carefully

- HTTP `401` or `403`: investigate the server's authentication requirements and authorization policy; this script does not accept authorization headers.
- Connection error: check URL, DNS, TLS, reachability, and timeout separately.
- JSON-RPC error: keep the error code and a sanitized message alongside client/server versions.
- Non-JSON or streaming response: this script does not parse SSE event frames. That output alone does not mean the server is broken.
- Successful JSON response: basic reachability and discovery evidence, not proof that tools execute correctly.

### Current limitations

The probe does not send the `notifications/initialized` lifecycle notification or the negotiated `MCP-Protocol-Version` header on subsequent requests. Servers requiring those steps can reject `tools/list` even when healthy. Use a conforming MCP client to verify such cases.

It does not implement stdio transport, OAuth, bearer authentication, complete SSE handling, or full schema/conformance validation. A zero exit code does not establish protocol correctness: JSON-RPC error responses and streaming/unexpected response shapes can be printed without a nonzero exit code.

No `tools/call` request is made. However, the probe does make network requests and prints a short response excerpt for non-JSON output; inspect and redact output before posting it publicly.

## API / Auth: minimum useful report

Include method and sanitized route, HTTP status, authentication scheme, sanitized error code, expected behavior, and a minimal reproduction. Never copy a live Authorization header or a URL containing a token.

Example evidence format, using fictional values:

```text
Method: GET
Route: /v1/example-resource
HTTP status: 403
Authentication scheme: Bearer (token omitted)
Expected: read a resource owned by the test account
Observed: insufficient_scope
Reproduction: use a test account with the documented read scope
```

Use the [API/Auth diagnostic template](../.github/ISSUE_TEMPLATE/api-auth-diagnostic.md).

## Webhooks: delivery versus processing

Record the provider, sanitized event type, delivery status, handler status, signature-verification result, and a redacted payload shape. Check whether your verifier receives the original raw-body bytes, and whether event IDs or idempotency keys prevent duplicate processing.

A provider reporting successful delivery does not establish that your application's handler completed the intended work. Keep those outcomes separate in the reproduction.

Use the [Webhook diagnostic template](../.github/ISSUE_TEMPLATE/webhook-diagnostic.md) and [troubleshooting index](TROUBLESHOOTING.md).

## Share only sanitized evidence

GitHub issues are public. Remove credentials, cookies, signing secrets, private keys, payment details, customer data, and private endpoint information. Use synthetic fixtures whenever possible.

Return to the [Diagnostic Hub](../NAIF-GRAVITY.md).
