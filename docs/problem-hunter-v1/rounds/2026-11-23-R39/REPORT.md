# R39 — 2026-11-23: preserve unknown webhook enums

Checked 2026-11-23T05:15:07Z (Asia/Riyadh date 2026-11-23). **One English draft; NOT POSTED.**

## Result

- 14 capped discovery searches:163 entries,148 unique title/body-excerpt screens. This is not148 completed investigations.
- 5 complete candidate descriptions, all their issue comments and available timeline events read.
- 1 completed bounded source investigation (Publira5943),2 exploratory source reads (Publira5848 and axp-stu42),2 deferred/excluded before source diagnosis.
- 23 additional targeted duplicate/overlap search hits, counted separately.
- 53 ledger follow-up threads read;4 tracked PR review/comment threads also read. **0 newly observed developer replies,0 new comments on unposted drafts,0 newly verified commercial requests.**
- 16 isolated assertion groups passed. No upstream full suite or integrated application test.
- No external comment, PR, message, service operation, payment or production change.

## Five candidates and disposition

| Issue | Reporter | Created (UTC) | Comments read | Outcome |
|---|---|---|---:|---|
| [publira/publira/5848](https://github.com/publira/publira/issues/5848) | ykzts | 2026-11-23T04:05:39Z | 0 | DEFERRED: source collapses Stripe ConstructEvent errors to invalid signature, already reported. No independent SDK/version reproduction or additive reply. |
| [publira/publira/5943](https://github.com/publira/publira/issues/5943) | ykzts | 2026-11-23T04:07:48Z | 0 | SELECTED: one completed bounded source investigation; numeric enum round-trip draft. |
| [Avid-Xenoblade-Player/axp-stu/42](https://github.com/Avid-Xenoblade-Player/axp-stu/issues/42) | github-actions[bot] | 2026-11-23T05:06:04Z | 0 | EXCLUDED: duplicate bot reports (#23–42); exploratory source shows raw Liquid HTML scanned before Jekyll build. No native reproduction. |
| [ywleeo/browser-mcp/5](https://github.com/ywleeo/browser-mcp/issues/5) | Saretheya | 2026-11-22T11:34:52Z | 1 | EXCLUDED: maintainer already supplied a dedicated implementation/test branch; new advice would overlap. No test claims independently verified. |
| [elie222/rakazo/6492](https://github.com/elie222/rakazo/issues/6492) | pupanpw | 2026-11-23T05:05:58Z | 0 | DEFERRED: OAuth 403 explanation remains reporter hypothesis; request trace and source diagnosis absent; open PR inventory capped at 100. |

Only Publira5943 qualifies for a new draft; the other four are not presented as solved problems.

## Selected: Publira5943

[Issue](https://github.com/publira/publira/issues/5943) remains open with zero comments at final refresh. Source commit: `234423bc0548032be5beb7cdb2583bd0a5b72a88`. Timeline has milestone/label/type events, no linked PR. Complete current open-PR inventory contains only unrelated PostgreSQL update5782. The latest30 all-state PR summaries and targeted issue-number searches supplied no overlapping enum repair; this is a bounded overlap check, not a proof about all history.

The reporter already identified unknown-enum data loss. The additive finding is the boundary chain: a read-mapper repair alone still fails because the form field whitelist drops a separate preservation channel, the schema admits only known names and requires one known event, and the update RPC maps every input through the string-to-enum table. The API-key unit test explicitly expects unknown scopes to disappear.

Proposed repair: preserve raw unknown numbers separately from editable known choices; display a localized non-editable marker; wire the preservation field through form mapping, schema and action; validate/de-duplicate the combined numeric update payload. Do not broaden API-key or webhook creation, remove server authorization/validation, or make TEST/UNSPECIFIED subscribable. Hidden inputs are untrusted, and client-unknown numbers need not be server-valid. Keep the issue's update contract rather than silently introducing patch semantics.

Confidence: high in observed source/data-boundary diagnosis; medium in candidate integration until native tests pass. Expected technical benefit: prevents an incomplete mapper-only repair and identifies an existing test that locks in the bug. No commercial intent inferred.

## Source evidence

All selected links are pinned to the same commit. Blob hashes are separate from the commit SHA.

| Source | Blob SHA |
|---|---|
| [apps/web-admin/lib/webhooks.ts](https://github.com/publira/publira/blob/234423bc0548032be5beb7cdb2583bd0a5b72a88/apps/web-admin/lib/webhooks.ts) | `1d9da544fc3a7982c53620bccacb03957647e104` |
| [apps/web-admin/lib/api-keys.ts](https://github.com/publira/publira/blob/234423bc0548032be5beb7cdb2583bd0a5b72a88/apps/web-admin/lib/api-keys.ts) | `7cc3f59f9eaed1c166d3df6eeec42edb3eb15725` |
| [apps/web-admin/lib/webhooks.test.ts](https://github.com/publira/publira/blob/234423bc0548032be5beb7cdb2583bd0a5b72a88/apps/web-admin/lib/webhooks.test.ts) | `2481edfe10385965cb3c6eaec3d55f552d2c9f67` |
| [apps/web-admin/lib/api-keys.test.ts](https://github.com/publira/publira/blob/234423bc0548032be5beb7cdb2583bd0a5b72a88/apps/web-admin/lib/api-keys.test.ts) | `15e04deaebec1b503f84b91afe6df8eee62896ef` |
| [apps/web-admin/app/[tenant_id]/[locale]/(protected)/integrations/api-keys-and-webhooks/_lib/form-schemas.ts](https://github.com/publira/publira/blob/234423bc0548032be5beb7cdb2583bd0a5b72a88/apps/web-admin/app/%5Btenant_id%5D/%5Blocale%5D/%28protected%29/integrations/api-keys-and-webhooks/_lib/form-schemas.ts) | `a9d19b5217e8aef5c96dd3956036adbf9433c5f4` |
| [apps/web-admin/app/[tenant_id]/[locale]/(protected)/integrations/api-keys-and-webhooks/_lib/actions.ts](https://github.com/publira/publira/blob/234423bc0548032be5beb7cdb2583bd0a5b72a88/apps/web-admin/app/%5Btenant_id%5D/%5Blocale%5D/%28protected%29/integrations/api-keys-and-webhooks/_lib/actions.ts) | `8d4e4246de55166f87a43e6d774cf701500e92f9` |
| [apps/web-admin/app/[tenant_id]/[locale]/(protected)/integrations/api-keys-and-webhooks/_lib/actions.test.ts](https://github.com/publira/publira/blob/234423bc0548032be5beb7cdb2583bd0a5b72a88/apps/web-admin/app/%5Btenant_id%5D/%5Blocale%5D/%28protected%29/integrations/api-keys-and-webhooks/_lib/actions.test.ts) | `097ebd823b40eab28a7f64253bd67d4f31021974` |
| [apps/web-admin/app/[tenant_id]/[locale]/(protected)/integrations/api-keys-and-webhooks/_components/webhook-endpoint-fields.tsx](https://github.com/publira/publira/blob/234423bc0548032be5beb7cdb2583bd0a5b72a88/apps/web-admin/app/%5Btenant_id%5D/%5Blocale%5D/%28protected%29/integrations/api-keys-and-webhooks/_components/webhook-endpoint-fields.tsx) | `861ac62d4254466336ff50efd864f6d4d69466f4` |
| [apps/web-admin/app/[tenant_id]/[locale]/(protected)/integrations/api-keys-and-webhooks/_components/webhook-endpoint-card.tsx](https://github.com/publira/publira/blob/234423bc0548032be5beb7cdb2583bd0a5b72a88/apps/web-admin/app/%5Btenant_id%5D/%5Blocale%5D/%28protected%29/integrations/api-keys-and-webhooks/_components/webhook-endpoint-card.tsx) | `e1327f21ad911cb8d82913360efe300454caab8c` |
| [packages/utils/src/form-data.ts](https://github.com/publira/publira/blob/234423bc0548032be5beb7cdb2583bd0a5b72a88/packages/utils/src/form-data.ts) | `8bc58bbe615fb084b9a8a559927db68095a129d7` |
| [proto/publira/admin/v1/webhook.proto](https://github.com/publira/publira/blob/234423bc0548032be5beb7cdb2583bd0a5b72a88/proto/publira/admin/v1/webhook.proto) | `e6df46bea3f51394b7c5317870183c7844ec2e13` |
| [proto/publira/admin/v1/api_key.proto](https://github.com/publira/publira/blob/234423bc0548032be5beb7cdb2583bd0a5b72a88/proto/publira/admin/v1/api_key.proto) | `45a3b62ba078a7ec08d4695e1d590eca6694ad9a` |
| [server/api/adminapi/webhook_handlers.go](https://github.com/publira/publira/blob/234423bc0548032be5beb7cdb2583bd0a5b72a88/server/api/adminapi/webhook_handlers.go) | `45e1f355a061c1156a14e025add24a4da39adb92` |

## Validation

See [TESTS.md](TESTS.md) for exact harness, source manifest and observed output.

Six baseline/boundary groups reproduce mixed and unknown-only event loss, unknown key-scope loss, retained TEST exclusion, unknown numeric failure in the existing RPC lookup, and the actual FormData helper dropping a new channel. Ten groups exercise a candidate pure-data preservation contract: mixed/unknown-only/deselected known events, deduplication, int32 boundaries, malformed input, reserved/known codes in the opaque channel, invalid known names, empty subscriptions, TEST/UNSPECIFIED exclusion.

Not tested: integrated React rendering, real Zod validation, ConnectRPC serialization/server acceptance, database persistence, actual older/newer deployments, or `pnpm preflight`. Zod/upstream dependencies were unavailable locally; no dependency install or service setup was performed. A fix to the current console cannot retrofit an already deployed old console.

Native regression plan: render mixed and unknown-only endpoints; submit URL-only and enabled-only edits through actual field mapping/action/schema; assert exact numeric RPC payload; deselect every known event while retaining unknown events; assert malformed inputs fail and server-invalid values remain rejected; render unknown API-key scope labels; replace the drop-unknown test; keep TEST excluded; validate release pairs and run preflight.

## English reply for review (R39-01)

Destination: https://github.com/publira/publira/issues/5943

Status: **PENDING_USER_REVIEW / NOT_POSTED**. Refresh issue/comments/linked work before any later approved posting.

I traced the edit path at `234423b`. The lossy projection you identified has two additional boundaries worth covering in the fix:

- [webhookEndpointFormFields](https://github.com/publira/publira/blob/234423bc0548032be5beb7cdb2583bd0a5b72a88/apps/web-admin/app/%5Btenant_id%5D/%5Blocale%5D/%28protected%29/integrations/api-keys-and-webhooks/_lib/form-schemas.ts) only admits the existing fields. Adding hidden inputs for preserved numbers without adding their field mapping means [toFormDataInput](https://github.com/publira/publira/blob/234423bc0548032be5beb7cdb2583bd0a5b72a88/packages/utils/src/form-data.ts) silently discards them. The current schema also accepts only known string events and requires at least one of them.
- [updateWebhookEndpoint](https://github.com/publira/publira/blob/234423bc0548032be5beb7cdb2583bd0a5b72a88/apps/web-admin/lib/webhooks.ts) converts every value through `rpcEventTypes[value]`. Passing an unknown numeric value through that lookup produces `undefined`; fixing only the read mapper is insufficient.

One implementation route is to keep selected known events and preserved unknown numeric events separate through the view model, form fields, schema and action, then merge/deduplicate their numeric codes at the RPC boundary. Show unknown events as non-editable labels and carry their numbers in hidden fields. Those fields are still untrusted input: validate integer syntax/range, keep UNSPECIFIED and TEST out of subscriptions, and retain the server's authorization and event validation. Unknown to this console does not mean valid to the server. Check non-emptiness after combining the two lists so an unknown-only subscription remains editable. Keep creation restricted to the known choices.

For API keys, preserve and label unknown scopes on reads; this should not expand which scopes the create form can grant. Also replace the existing [api-keys.test.ts](https://github.com/publira/publira/blob/234423bc0548032be5beb7cdb2583bd0a5b72a88/apps/web-admin/lib/api-keys.test.ts) expectation named “leaves off a scope this console has no word for,” which currently locks in the loss.

I ran 16 isolated assertion groups: six baseline/boundary checks using extracted source and ten checks of a candidate pure data contract. They reproduce the dropped event/scope, the omitted FormData channel and the lookup problem, and check numeric preservation, deselection, deduplication and malformed input rejection. This is not an integrated application fix: I did not run React rendering, the real Zod schema, ConnectRPC, or `pnpm preflight`.

For regression coverage, render mixed and unknown-only endpoints, submit an unrelated URL/enabled change through the real action/schema, and assert the exact numeric RPC payload. Include deselecting all known events, the unknown-scope label, and TEST exclusion. A release-pair test is also needed: fixing the current console does not retrofit an already released older console.

## Follow-ups and deduplication

All53 existing follow-up records were refreshed without changing saved comment cursors, because no later comments were found. Histories and publication statuses are preserved. The four PR review reads were mppx1133, PriceStalker269, Langfuse19595 and BanyanDB1460. No historical thank-you, technical success or old review is being announced again. The new Publira draft is an unposted follow-up with null own/seen comment IDs.

Link-checker duplicate search returned20 matching automated reports (#23–42); no new draft. Browser-MCP5 already has the maintainer's implementation branch `fdf15c08d1e43a9522eae6de8776455db51f718d`; claimed tests were not independently run. PR6 covers other lifecycle work. Rakazo's100-entry open-PR cap and missing request trace prevent a confident OAuth diagnosis.

## NAIF tool fit

Live official homepage https://naifgravity.com and current diagnostics README (blob `0cc1c1a7b9edd57a54a44eaf676225c57f10e47b`) were reviewed. Browser webhook body-mapping demo does not validate enum preservation through this console. MCP probe supports bounded HTTP checks, not stdio/OAuth or this application repair. No NAIF link or paid pitch was added to the draft.

## Repository update boundary

Mandatory radar, README, ledger, R38 report, root AGENTS and untruncated tree were read at own-repo head `f0071717256f3f7067c26e41f307a7af3bfcc1ab`. No descendant AGENTS applies. All8 workflow definitions were checked: these docs paths do not match push-trigger paths; remaining triggers are PR/review/comment, schedule or manual. No workflow edited or dispatched.

Only README, ledger and four R39 Markdown files are prepared. Publication uses a fresh parent/expected-head lease and preserves previous history. No merge, production/payment/V5/server change, paid service, heavy setup or new project.

Owner action: review the single full English reply before publication to the other repository.
