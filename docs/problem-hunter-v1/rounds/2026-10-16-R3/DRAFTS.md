# R3 — English replies for review (2026-10-16)

Status: **R3-01, R3-02 and R3-03 POSTED_MANUALLY_VERIFIED**. The scheduled run sent no comments. The user subsequently published all three manually on 2026-10-16: [AGNT at 05:23:05Z](https://github.com/agnt-gg/agnt/issues/169#issuecomment-6208715705), [Noir at 05:26:11Z](https://github.com/owasp-noir/noir/issues/3078#issuecomment-6208753257), and [currently visible Engram comment at 05:32:58Z](https://github.com/Gentleman-Programming/engram/issues/1899#issuecomment-6208832958). An earlier Engram comment ID 6208777198 was observed at 05:28:14Z and was absent from the later comment listing; no cause is inferred. No subsequent developer reply was present at the latest check. These manual posts do not authorize other comments. The texts below are historical copies, not requests to post them again.

## R3-01 — AGNT OAuth concurrency
Target: https://github.com/agnt-gg/agnt/issues/169

I reproduced the two reported concurrency boundaries using the class from `MCPOAuthService.js` at `52f1a8644bf8f672df660534dc3584fbeb3138fc`, with storage replaced by a cloned in-memory map and token exchange replaced by manually released promises:

- Ten concurrent `getAccessToken("a")` calls on an expiring synthetic session made ten token-exchange calls.
- Starting refreshes for A and B, completing B first and then A, restored B's old access token from A's pre-request snapshot.

An important detail for the proposed store mutex: serializing only `_writeAll(oldSnapshot)` still permits the second failure. The critical section needs to read the latest store, merge the updated server entry, and persist that result together. The network exchange can remain outside the global write lock; per-server single-flight handles overlapping refresh requests.

For regression coverage, use explicit promise barriers to force B-before-A completion, then assert that both new sessions remain stored. Separately assert that all ten same-server callers receive the new token after exactly one exchange. A small candidate concurrency model passed those two checks, but it is not an upstream patch or proof of durable credential storage.

I have not tested the real token file, atomic rename/permissions, provider rotation/revocation, cross-process access, or HTTP session recovery. I also read the contribution policy excluding external auth PRs; this is reproduction evidence for the existing issue, not a proposed auth PR.

## R3-02 — Noir readOnly request properties
Target: https://github.com/owasp-noir/noir/issues/3078

There are four matching emission points at `8d8600bf8aab07c40ee8a75f2b9b4a93d82f626b`: `collect_schema_props_json/yaml` in `oas3.cr` and `collect_body_props_json/yaml` in `oas2.cr`. Each uses `props.each do |name, _|`, discarding the property schema before calling `add_param`.

One scope detail: these collectors also emit form parameters, so a fix limited to `param_type == "json"` would leave the same issue in supported form request bodies.

I would retain the property value and skip an explicitly boolean `readOnly: true` at request-property emission, in both formats and versions. Keep `readOnly: false`, absent annotations and `writeOnly: true` properties. Use guarded hash/boolean access so a scalar or null property does not make later properties disappear.

Suggested regressions:
- Equivalent JSON and YAML fixtures, for OAS2 and OAS3.
- JSON and supported form media types.
- A required read-only ID alongside writable fields: only the ID is omitted.
- Referenced properties and composed schemas. A direct flag check alone will not inspect an annotation behind a property-level `$ref`; that path needs the existing resolver's document and cycle safeguards.
- Do not mutate the shared schema used by responses.

This is source inspection plus a small synthetic predicate test. I have not compiled Crystal, run Noir, or verified reference/composition behavior in its test suite.

## R3-03 — Engram blank MCP configuration
Target: https://github.com/Gentleman-Programming/engram/issues/1899

At current inspected main `9c4382f60e2fb300c6cb877bb6ff295ecfbdf2ee`, `StaleMCPCommands()` in `internal/setup/registry.go` calls `json.Unmarshal(data, &config)` immediately after a successful read and returns on a parse error. This confirms why an empty earlier adapter prevents inspection of later ones.

A narrowly scoped fix is a blank-file guard in this read-only inspection loop, after checking the read error and before unmarshalling:

```go
// Add "bytes" to imports.
if len(bytes.Trim(data, " \t\r\n")) == 0 {
    continue
}
```

This treats empty files and JSON whitespace as no registrations while retaining errors for nonempty malformed JSON. I would avoid changing the shared `readJSONConfig` writer/setup behavior just to repair doctor.

The key regression should place an empty config before a later adapter containing an otherwise setup-owned Engram registration with a nonexistent absolute command. Assert that the later stale-command finding is still returned. Run the same case with whitespace, absent and `{}` configs; keep malformed nonempty JSON as an error. Also assert that doctor leaves every config byte unchanged and creates no missing files.

I checked this boundary in a synthetic scan model only. Go is unavailable in my environment, so I have not run `engram doctor` or its tests. Any implementation would still need the repository's issue approval and assignment workflow.
