# R11 — English reply for review (2026-10-23)

Status: **PENDING_USER_APPROVAL — NOT POSTED**. This is one new reply, not approval to reuse earlier drafts. Re-read the issue, comments and linked PRs before any later approved publication. No third-party publication is permitted during the scheduled run.

## R11-01 — OpenViking #6471

Target: https://github.com/volcengine/OpenViking/issues/6471

Copy only the text between the markers below, after approval and a fresh duplicate check.

<!-- BEGIN REPLY -->
An additional regression boundary is the failure path for **client error responses**, as well as the empty-202 case.

In an AI-assisted isolated check of the complete proxy core at [`0d546854b4be`](https://github.com/volcengine/OpenViking/blob/0d546854b4be4b24a277c1b3ca7cf06c02d61a14/examples/memory-plugin-shared/lib/mcp-proxy-core.mjs), both a result response and an error response produced an unsolicited stdout error when the injected POST returned 403/500 or threw an `AbortError`. The shared cause is `isRequest()`: it treats every object carrying an `id` as a request, so both the empty-body branch and the catch branch reply to responses.

For well-formed messages, the minimal classification change I tested was:

```js
function isRequest(message) {
  return typeof message?.method === "string"
    && Object.prototype.hasOwnProperty.call(message, "id");
}
```

Keep failures delivering a response in the diagnostic path; do not fabricate another response with the same ID. Keep genuine requests with `id: 0` eligible for normal responses and mapped errors.

The isolated before/after matrix passed 21 assertion groups: result/error responses × IDs `0`/`"server-ping"` × 202/403/500/injected abort, plus five request/notification controls. Before the change, all 16 response cases produced a spurious error; afterward they produced no stdout message, and failed deliveries still logged diagnostics. Each input was forwarded once.

The canonical source and its three committed generated copies have identical content after removing the generated banner. Apply the fix in the canonical module and use the existing `examples/memory-plugin-shared/sync.mjs` workflow for generated copies.

These checks used an injected fetch implementation, synthetic data and no credentials. They did **not** test live MCP clients, session reinitialization/replay, real elapsed-time timeouts, packaging, or the upstream suite. The predicate is not a complete JSON-RPC validator. Native integration checks should still cover those boundaries before release.
<!-- END REPLY -->

Evidence and reproducible isolated harness: [TESTS.md](TESTS.md). No NAIF product link is included: the available HTTP discovery probe does not test this stdio proxy path.
