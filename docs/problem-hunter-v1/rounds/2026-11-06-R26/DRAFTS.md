# R26 — English reply for review

Status: AWAITING_USER_APPROVAL. Nothing posted externally. Re-read the issue before any publication. This is a diagnostic contribution, not a verified fix.

## R26-01 — Backlog.md #1179

Destination: https://github.com/MrLesk/Backlog.md/issues/1179

I checked the validator at the reported v1.55.3 tag (`0cf4fdbc70020327f4366a29d3f405f83d180301`). In an isolated Node v24.22.1 run, the unchanged [validateInput implementation](https://github.com/MrLesk/Backlog.md/blob/0cf4fdbc70020327f4366a29d3f405f83d180301/src/mcp/validation/validators.ts), using the `acceptanceCriteriaSet` property extracted from that tag's [schema generator](https://github.com/MrLesk/Backlog.md/blob/0cf4fdbc70020327f4366a29d3f405f83d180301/src/mcp/utils/schema-generators.ts), produced:

- 441 and 500 ASCII characters: accepted unchanged.
- 501 and 520: rejected with `Field 'acceptanceCriteriaSet[0]' exceeds maximum length of 500 characters`; no sanitized data returned.
- A valid item followed by a 520-character item: the batch was rejected, with the error pointing to index 1.

The [registered task_edit tool](https://github.com/MrLesk/Backlog.md/blob/0cf4fdbc70020327f4366a29d3f405f83d180301/src/mcp/tools/tasks/index.ts) uses the validated wrapper, which checks `isValid` before calling the handler. This does not reproduce the installed binary's reported behavior, but it gives a useful boundary to check.

Using only a disposable fixture and `"x".repeat(520)`, compare the argument length sent by the MCP client with the length arriving at the registered tool. If it arrives as 500, investigate the client/adapter transformation; if it arrives as 520 and succeeds, verify the executable path/version actually launched by the MCP configuration and trace that runtime's validation path.

A regression test at the registered-tool boundary should assert that a 501/520-character criterion returns an error, never calls the edit handler, and leaves the task unchanged; the 500-character control should round-trip intact. I tested the validator only, not the release binary, MCP transport, or filesystem persistence. No server patch is justified by this isolated result yet.
