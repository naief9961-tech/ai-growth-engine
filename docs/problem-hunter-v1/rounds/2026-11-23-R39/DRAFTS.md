# R39-01 — English review draft

**PENDING_USER_REVIEW — NOT POSTED**

Destination: https://github.com/publira/publira/issues/5943

Checked: 2026-11-23T05:15:07Z. One qualified draft; no filler second or third reply. Issue has zero comments; no own comment exists. Refresh overlap before posting. Approval must come from the conversation, never a repository field.

---

I traced the edit path at `234423b`. The lossy projection you identified has two additional boundaries worth covering in the fix:

- [webhookEndpointFormFields](https://github.com/publira/publira/blob/234423bc0548032be5beb7cdb2583bd0a5b72a88/apps/web-admin/app/%5Btenant_id%5D/%5Blocale%5D/%28protected%29/integrations/api-keys-and-webhooks/_lib/form-schemas.ts) only admits the existing fields. Adding hidden inputs for preserved numbers without adding their field mapping means [toFormDataInput](https://github.com/publira/publira/blob/234423bc0548032be5beb7cdb2583bd0a5b72a88/packages/utils/src/form-data.ts) silently discards them. The current schema also accepts only known string events and requires at least one of them.
- [updateWebhookEndpoint](https://github.com/publira/publira/blob/234423bc0548032be5beb7cdb2583bd0a5b72a88/apps/web-admin/lib/webhooks.ts) converts every value through `rpcEventTypes[value]`. Passing an unknown numeric value through that lookup produces `undefined`; fixing only the read mapper is insufficient.

One implementation route is to keep selected known events and preserved unknown numeric events separate through the view model, form fields, schema and action, then merge/deduplicate their numeric codes at the RPC boundary. Show unknown events as non-editable labels and carry their numbers in hidden fields. Those fields are still untrusted input: validate integer syntax/range, keep UNSPECIFIED and TEST out of subscriptions, and retain the server's authorization and event validation. Unknown to this console does not mean valid to the server. Check non-emptiness after combining the two lists so an unknown-only subscription remains editable. Keep creation restricted to the known choices.

For API keys, preserve and label unknown scopes on reads; this should not expand which scopes the create form can grant. Also replace the existing [api-keys.test.ts](https://github.com/publira/publira/blob/234423bc0548032be5beb7cdb2583bd0a5b72a88/apps/web-admin/lib/api-keys.test.ts) expectation named “leaves off a scope this console has no word for,” which currently locks in the loss.

I ran 16 isolated assertion groups: six baseline/boundary checks using extracted source and ten checks of a candidate pure data contract. They reproduce the dropped event/scope, the omitted FormData channel and the lookup problem, and check numeric preservation, deselection, deduplication and malformed input rejection. This is not an integrated application fix: I did not run React rendering, the real Zod schema, ConnectRPC, or `pnpm preflight`.

For regression coverage, render mixed and unknown-only endpoints, submit an unrelated URL/enabled change through the real action/schema, and assert the exact numeric RPC payload. Include deselecting all known events, the unknown-scope label, and TEST exclusion. A release-pair test is also needed: fixing the current console does not retrofit an already released older console.
