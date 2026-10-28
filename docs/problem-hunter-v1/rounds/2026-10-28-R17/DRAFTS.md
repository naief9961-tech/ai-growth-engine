# R17 — English reply for review (2026-10-28)

Status: **POSTED_MANUALLY_VERIFIED — DO NOT REPOST.**

The user manually published the plain-text variant at 2026-10-28T05:10:13Z: [comment 6461200657](https://github.com/paoloamato2/fortinet-mcp-server/issues/5#issuecomment-6461200657). Verified at 2026-10-28T05:10:45Z; no subsequent developer reply.

This is an archived draft. Its publication is verified; it does not authorize another comment or future external communication.

## R17-01 — Fortinet MCP generic JSON arguments

Destination: https://github.com/paoloamato2/fortinet-mcp-server/issues/5

Historical English draft (the posted variant uses plain-text source references):

---

The proposed union/helper approach fits the current signatures. One additional regression boundary is the **decoded shape**, not just whether `json.loads` succeeds.

At [`5c82a1e`](https://github.com/paoloamato2/fortinet-mcp-server/blob/5c82a1e6e2b7a336cd9b22881d50a658d8bdcb06/tools/generic.py), all six listed parameters are string-only (nullable for the optional ones). In [`_vdom_params`](https://github.com/paoloamato2/fortinet-mcp-server/blob/5c82a1e6e2b7a336cd9b22881d50a658d8bdcb06/fortios_client.py), a truthy `extra` is consumed through `.items()`. Valid JSON such as `[1]`, `1`, `true`, or a double-encoded object therefore still needs to be rejected after parsing. Falsy scalars should not silently become omitted parameters either.

A small object-only normalization boundary could be:

```python
def json_object(value: dict[str, Any] | str, field: str) -> dict[str, Any]:
    parsed = json.loads(value) if isinstance(value, str) else value
    if not isinstance(parsed, dict):
        raise ValueError(f"{field} must be a JSON object")
    return parsed
```

Use `dict[str, Any] | str` for required `data`, and add `| None` for optional parameters. Catch `ValueError` around normalization and return the tool's existing error object before invoking the client. Keep optional defaults outside the helper: `None` (and the currently accepted empty string, if retaining compatibility) should preserve the existing query `None` / POST `{}` defaults. Decode once; do not recursively decode strings.

There is also overlap with [PR #2](https://github.com/paoloamato2/fortinet-mcp-server/pull/2): at head `fdcf62f`, its `monitor_get` change already checks that decoded `extra_params` is a dict. Coordinate that guard with the shared helper so the other five handlers receive the same validation without undoing its paging logic.

For regression coverage, test all six handlers with a native object and equivalent JSON string, then malformed JSON, lists, scalars, and a double-encoded object. Assert invalid inputs never invoke the mocked client; check omitted optional arguments and the advertised `tools/list` schema as well as `tools/call` validation.

I ran 29 isolated check groups using Python 3.12.14 / Pydantic 2.14.1: source-derived parameter annotations, the unmodified `_vdom_params` method, and the helper above. They passed. These checks do **not** exercise FastMCP dispatch, patched handlers, Claude Code conversion, HTTP, a FortiGate, or the upstream suite; those integration checks remain necessary.
