# NAIF Gravity Troubleshooting Index

These short guides are designed around errors developers actually search for. Use them as a first-pass diagnostic; never expose credentials in an issue.

## MCP

### 1. MCP initialize fails
Check transport URL, protocol/version negotiation, content type, and whether the server returns a valid JSON-RPC response.

### 2. MCP `tools/list` returns an error
Verify the session is initialized first, the transport supports the method, and the server returns a valid `tools` array.

### 3. MCP tool schema is rejected
Inspect JSON Schema types, required fields, unsupported keywords and mismatches between declared input schema and runtime parsing.

### 4. MCP client connects but cannot call tools
Compare tool names exactly, confirm initialization/session state, then inspect authorization and transport-level failures separately.

## API & Auth

### 5. HTTP 401 / unauthorized
Separate missing credentials from invalid credentials. Verify header name, auth scheme, token audience/issuer and clock skew.

### 6. OAuth `invalid_grant`
Check redirect URI equality, code reuse/expiry, PKCE verifier pairing and client configuration before rotating credentials.

### 7. HTTP 403 after successful authentication
Authentication may be valid while authorization is not. Check scopes, roles, resource ownership and policy rules.

## Webhooks

### 8. Webhook signature verification failed
Verify the raw request body is used, the correct signing secret is selected, timestamp tolerance is valid and body parsing has not changed bytes before verification.

### 9. Webhook delivered but application did nothing
Log the provider event ID, handler status, routing decision and idempotency outcome. Separate delivery from business-logic processing.

### 10. Duplicate webhook processing
Use the provider event ID or a stable idempotency key, persist the processed state and make retries safe.

## Need a bounded repair?

Open the matching GitHub issue template with sanitized evidence, or continue at:

https://naifgravity.com/?utm_source=github&utm_medium=troubleshooting&utm_campaign=github_funnel
