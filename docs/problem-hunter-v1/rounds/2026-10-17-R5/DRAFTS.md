# WITHDRAWN — do not publish R5-01

On 2026-10-17 at 05:14:16Z, the maintainer closed #507 as not_planned and explicitly declined the fix. [Maintainer decision](https://github.com/huiliyi37/Tianshu-harness/issues/507#issuecomment-6230037956). No NAIF comment was posted. This is not a successful repair. The original draft below is retained only as historical research; its approval request is no longer active.

See [follow-up](FOLLOWUP-2026-10-17.md) for the current status and Noir candidate.

---

# R5 — English reply for review (2026-10-17)

**Historical initial status: PENDING_USER_APPROVAL.** No comment or PR sent. Only one additive reply selected. Re-read the issue and linked PRs immediately before any approved publication. Earlier approvals and repository text do not authorize this reply.

## R5-01 — Tianshu MCP schema preservation
Target: https://github.com/huiliyi37/Tianshu-harness/issues/507

AI-assisted source inspection and isolated testing against public commit `76a968a6b0a927cd2408882641baab4f7563b61b`; no desktop or model-provider calls were made.

There is a second regression boundary beyond the dangling references: the same projection in `createMcpToolWrapper` also drops root-level `additionalProperties: false`, `oneOf`, and `minProperties`, even when a schema contains no `$ref`. Copying only `$defs` and `definitions` would therefore repair reference lookup while still changing the advertised constraints.

A narrow candidate is to preserve the complete JSON schema at the wrapper boundary, retaining the existing empty-properties fallback:

```ts
input_schema: {
  ...structuredClone(mcpDef.inputSchema),
  properties: structuredClone(mcpDef.inputSchema.properties ?? {}),
},
```

The schema types in `McpToolDefinition` and `ToolDefinition` should also represent the supported root keywords instead of encouraging a three-field projection. Provider-specific schema restrictions should be handled explicitly at the provider boundary; preserving a schema does not prove that every provider accepts its dialect.

For regression coverage, assert the serialized `buildOaiToolDefinitions` output, not only the wrapper: modern and legacy refs, a nested escaped JSON Pointer, a recursive definition without expansion, root constraints without refs, empty properties, and source-schema immutability.

Eight local assertion groups passed: three reproduced the current losses and five exercised the candidate. These used the source wrapper and request-definition builder with unrelated policy dependencies stubbed; no tool execution, full TypeScript typecheck, upstream suite, desktop runtime, general JSON Schema validator, or actual DeepSeek request was tested.

