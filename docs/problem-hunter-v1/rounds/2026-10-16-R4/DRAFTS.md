# R4 — reply for review (2026-10-16)

Status: **PENDING_USER_APPROVAL**. No external comment or PR was sent. Only one new reply is ready for review. Re-read the thread immediately before publication.

## R4-01 — MCP Git parameter-shape validation

Target: https://github.com/MementoRC/mcp-git/issues/298

AI-assisted source investigation and isolated testing; this is not a deployed-server test.

One additional regression boundary at `648cb467d80311ef83f7246dfa9a07bd930db072`: the outcome depends on both the method and whether invalid `params` is truthy.

Using source-extracted handlers with request/response stand-ins:
- `initialize` and `tools/list` accepted all eight tested non-object values.
- `tools/call` with `null`, `[]`, `false`, `0`, or `""` returned -32602 with the missing-name message, because `call_params = params or {}` replaces those values.
- Nonempty string/list and a nonzero number instead reached -32603.

A check only inside the tool runner, or a test of only `"params": "x"`, would miss these differences. For methods requiring object parameters, validate their shape before dispatch, distinguish an omitted `params` from explicit `null`, and preserve the request ID. Validate the top-level JSON shape before calling `.get()`; keep the batch-policy decision separate from this parameter fix.

Suggested regression: the three methods × those eight invalid values, with an assertion that no method handler/session side effect runs; also retain omitted-params and `{}` controls for `tools/list`. Notification handling needs its own no-response checks.

A local candidate passed the 24 request cases and the two tools/list controls. These checks used extracted classes, not FastAPI/ASGI or the live HTTP endpoint; no Git operations, full upstream suite, notification behavior, or negotiated batch interoperability were tested.

## Not for publication

- pi-claude-subscription #22: withdrawn after the owner closed it during this investigation. No duplicate comment.
- MCP Python #3710: engineering findings are in REPORT.md, but no copy-ready comment is recommended until the repository's personal-understanding/firsthand-reproduction and AI disclosure conditions are actually met. No user approval is inferred and no firsthand production claim is made.

