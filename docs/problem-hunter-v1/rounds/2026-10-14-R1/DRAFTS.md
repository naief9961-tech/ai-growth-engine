# Proposed comments — 2026-10-14 R1

Status: PENDING USER APPROVAL. None posted upstream. Re-read each thread immediately before any approved posting.

## R1-01 — Microsoft Agent Framework — Unicode serialization

Target: https://github.com/microsoft/agent-framework/issues/9366

I checked the relevant paths at `cd3f6c8`. The proposed fix needs **four call sites across three files**: one in `_mcp.py`, two in `FunctionTool.parse_result` (including the mixed `Content`/object list branch), and one in `Content.from_function_result`.

Use `json.dumps(value, default=str, ensure_ascii=False)` at those model-visible serialization boundaries. Keep existing `Content` instances, plain strings, and the result-selection modes unchanged. Both the escaped and Unicode forms are valid JSON; this addresses the model-visible representation, not a malformed server response.

I ran eight isolated checks against extracted source functions/expressions, using a minimal `Content` stub. They covered Spanish, Arabic, Japanese and emoji, nested JSON types, a Pydantic model, mixed rich-content/object output, `None`/string passthrough, and `default=str`. The baseline emitted escapes; the candidate preserved literal Unicode and the same parsed JSON values. This was **not** the full framework suite or a live MCP run, and I did not measure tokenizer savings.

For upstream regression coverage, exercise `structured_first`, `structured_only`, `content_first` fallback and `both` with real MCP result models. Assert unchanged text/image ordering, unchanged `_meta` propagation, and that an existing text block is not serialized twice. Include the mixed-list branch explicitly so fixing the ordinary dict path does not leave a second escaped path.

## R1-02 — Owlat — retry identity and receipt retention

Target: https://github.com/wolvesdotink/owlat/issues/1367

I checked `47ccccd`. The existing claim path already distinguishes `duplicate_in_flight` from `duplicate_completed`, and the HTTP handler returns retryable 503 versus duplicate 200 respectively. That machinery can be reused.

The remaining mismatch is in `verifyPluginSvixDelivery`: the digest includes both timestamp and signature, while receipt expiry is only `nowMs + 2 * toleranceSeconds * 1000` (10 minutes at a 300-second tolerance).

After the existing signature/freshness verification, derive a versioned digest from an unambiguous encoding of:

```text
[scheme, pluginId, transportKind, svixId, SHA256(rawBody)]
```

Exclude the attempt timestamp and signature, but preserve their verification. Give receipts a separate retention policy that covers the configured retry schedule. I used 48 hours in the synthetic candidate; this is a proposed policy, not a guarantee for arbitrarily late manual replays. Do not increase the signature freshness window to obtain longer deduplication.

Nine isolated source-extract checks passed: authentic re-signed attempts produced different baseline digests and the same candidate digest; signature-list ordering did not change identity; body/ID/plugin/transport separation remained; tampering and stale signatures were rejected. These did **not** run the Convex database.

Before merging, test real claim concurrency, cleanup/expiry and rollout from old digests. Also inject a crash after a handler commits but before completion is recorded: stable delivery identity alone cannot guarantee exactly-once side effects across that boundary. Preserve handler-level idempotency or an atomic durable effect/receipt boundary.

## R1-03 — agent-manager — namespaced A2A part metadata

Target: https://github.com/giantswarm/agent-manager/issues/157

At `fe929b6`, `partType` only checks `adk_type` and `kagent_type`, so a data part carrying only `kagent.dev/a2a/part-type` returns the empty type before the transcript's tool-call handling can recognize it.

A minimal compatibility patch is to append the namespaced key while preserving current legacy precedence:

```go
for _, key := range []string{
    "adk_type",
    "kagent_type",
    "kagent.dev/a2a/part-type",
} {
    if v, ok := fields[key]; ok {
        return v.GetStringValue()
    }
}
```

Keep the existing `GetData() == nil` guard. Appending the key avoids silently changing behavior for mixed metadata from older installations. If namespaced metadata should instead win when keys disagree, that needs an explicit policy and regression case.

Suggested table coverage: each of the three keys with `function_call` and `function_response`; absent metadata; a text-only part; and conflicting keys to pin precedence. Then add a complete synthetic transcript containing a call and matching result and assert that both the transcript view and `get_session` retain them. Re-run an old-key fixture unchanged.

I inspected the source and prepared the small patch, but **did not compile or run the Go tests** because this environment has no Go runtime. The remaining acceptance check is `go test ./internal/agents` plus the complete transcript fixture on the maintainer's normal toolchain.