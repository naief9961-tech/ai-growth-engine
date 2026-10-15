# Proposed comments — 2026-10-15 R2

Status: **PENDING USER APPROVAL**. These are review drafts only. Nothing was posted to third-party repositories during the scheduled run. Re-read each thread and linked PR state before any later authorized posting.

## R2-01 — microsoft/vscode#341683 — GitHub Pages registry redirects

I traced this against current `main` at `9ebdca5c15f666ab336ca0b0421f5ee25bf1cbe0`. The failure matches the implementation in `src/vs/platform/mcp/common/mcpGalleryService.ts`: `getMcpServerUrlInGallery()` first constrains the detail URL to the registry origin/path, then `getMcpServer()` sends the GET with `followRedirects: 0`. A GitHub Pages directory URL without the terminal slash therefore cannot reach its canonical JSON response; in the renderer the manual cross-origin redirect can surface as status 0, which explains why this is later treated as an undetermined lookup failure.

I would keep the existing redirect boundary and add one narrowly bounded canonical retry instead of enabling redirects globally:

1. Request the validated detail URL exactly as today.
2. If it returns a redirect status, or renderer status 0, and the pathname does not end in `/`, construct the same URL with one trailing slash.
3. Pass that candidate through `getMcpServerUrlInGallery()` again and retry once with `followRedirects: 0`.
4. Do not retry an already slash-terminated URL, and retain the current 404/other-status semantics.

That preserves the same-origin and registry-prefix checks while covering GitHub Pages canonicalization without allowing an arbitrary Location target.

Regression coverage I would add around `McpGalleryService.getMcpServer`:

- slashless detail URL -> redirect/status 0 -> slash URL -> valid server;
- an already canonical slash URL makes one request;
- cross-origin and outside-registry-prefix candidates remain rejected;
- 404 still returns `undefined`;
- 401/403/429/5xx still throw;
- at most one canonical retry, so redirect loops cannot spin.

I only verified the URL/security boundary with an isolated synthetic check; I did not run the VS Code suite or reproduce the renderer's opaque response in a browser.

## R2-02 — a2aproject/a2a-python#1341 — unknown response fields

The report is consistent with current `main` at `a4c4fc91a22778f3d805e5e592bf690915a33033`. In `src/a2a/client/transports/jsonrpc.py`, the response parsers for send/get/list/cancel/push-config/extended-card and streamed `StreamResponse` all call `json_format.ParseDict(...)` without `ignore_unknown_fields=True`. `src/a2a/client/transports/rest.py` has the same strict response parsing. That differs from the card resolver and v0.3 compatibility path, so the compatibility failure is client-transport-wide rather than limited to `send_message`.

A small helper would make the policy hard to miss at future call sites:

```python
def _parse_response(data: dict[str, Any], message: Message) -> Message:
    return json_format.ParseDict(
        data,
        message,
        ignore_unknown_fields=True,
    )
```

Use the helper for every JSON-RPC and REST response parse, including streamed responses (or pass the same option to `Parse` there). I would keep request parsing strict; the forward-compatibility rule is for received protocol messages.

A useful regression matrix is:

- unary JSON-RPC and REST `SendMessageResponse` with an extra top-level field;
- a nested extra field in `Task` or `Message`;
- JSON-RPC and REST task/list/push-config/extended-card paths;
- SSE `StreamResponse` with an extra field;
- malformed known fields still fail;
- an explicit unknown-enum case documenting protobuf's current behavior, so leniency does not accidentally get described as preserving an enum value it cannot represent.

My isolated model test confirmed the strict-versus-ignore behavior boundary. The direct SDK reproduction was not run because `google.protobuf` is not installed in this runner, and I did not run the upstream suite.

## R2-03 — Abilityai/trinity#3749 — long A2A message/send

The current code at `43576279b43d27cca67559a66f47f33e6ddedb56` confirms the missing hand-off. `_run_a2a_task()` awaits `dispatch_and_await_terminal()`; the `message/send` branch awaits that whole call before it has an execution id to return. At the same time, `tasks/get` already maps `running -> working` and `queued -> submitted`. The pollable state exists, but the synchronous path never exposes its handle before the caller's 30-second deadline.

I would split the operation at the durable-dispatch boundary:

1. Dispatch and obtain the execution id before waiting for terminal state.
2. Record AAuth caller ownership and paid-caller/payer binding immediately after durable creation, before any early response.
3. Wait for terminal state under a server budget below the client deadline using a shielded task; a client disconnect or timeout must not cancel the execution.
4. On budget expiry, read the row and return `submitted` or `working` with that execution id.
5. Store idempotency as `messageId -> executionId`, not as a frozen working response. Replays should rebuild the current Task from the row.
6. Emit the terminal audit exactly once from the completion path. The early response should not call the current terminal `idempotency_service.complete(..., task)` or write a completion-looking audit row.

For regression tests, use barriers/fake time rather than real sleeps: fast terminal path byte-for-byte unchanged; slow path returns a handle before the client deadline; bearer/AAuth/paid `tasks/get` ownership; replay while running and after completion; disconnect does not cancel work; one terminal audit only.

I ran a small isolated asyncio check showing that a shielded task can return a working boundary on budget expiry and still complete later. I did not run Trinity, its database, billing, or audit integration tests.
