# R42 — 26 November 2026: four API timestamp paths, one review draft

Checked 2026-11-26T05:04:24Z (Asia/Riyadh date 2026-11-26). No third-party message or PR sent.

## Counts and decision

- 130 capped search results across13 queries; **110 distinct issue titles screened**, with date filter created >=2026-11-23.
- **4 complete candidate-thread reads** (body, all comments and timeline); one additional body-only triage read (kube-agents7276).
- **1 completed bounded source investigation** (fitness-app131); 3 preliminary source/PR overlap reviews (Inspect, Dify, Tokenhop).
- 55 existing tracked threads refreshed, plus4 combined PR review/comment collections and1 newly linked report. All comment collections below100; no further comment page needed.
- **8 executed isolated assertion groups passed**, including4 paired baseline/candidate route groups. No full upstream suite, typecheck, live HTTP/database/native tests.
- **1 English draft** for owner review. No second/third draft or five-issue quota filled with duplicates.
- 1 new collaborator comment linking another report; no repair confirmation and **0 explicit commercial inquiries**.

## Selected issue

[KhubaibQaiser/fitness-app #131](https://github.com/KhubaibQaiser/fitness-app/issues/131), reporter KhubaibQaiser, opened2026-11-26T04:55:22Z.

Four existing API handler paths return database timestamp strings unchanged: GET/POST notes createdAt, GET client check-in history completedAt, and GET check-in detail completedAt. The domain queries/projection preserve those columns; Drizzle timestamp helpers use mode:string. The response schemas are generic anyObject/objectList, so a scan limited to OpenAPI format:date-time misses the fields.

Candidate: explicit serializers with existing toStrictIso. Keep null completedAt, date-only scheduledFor and free text untouched. Apply to list and single/create responses. The aggregated client-detail recentCheckIns and other timestamps remain a separate audit scope; this is not a complete API fix.

**Confidence:** high for these source paths, their synthetic response behavior and the candidate mapping; real database and Hermes incident reproduction unverified. **Benefit:** concrete four-route regression starting point, not another generic instruction to normalize dates.

[Full English reply, pending approval](DRAFTS.md) · [Exact tests, output and limitations](TESTS.md).

Source snapshot: **162bffbd2367f39be6c8dd57d8a213d3b225bed6**, unchanged on final recheck.

- [apps/api/src/routes/clients.ts](https://github.com/KhubaibQaiser/fitness-app/blob/162bffbd2367f39be6c8dd57d8a213d3b225bed6/apps/api/src/routes/clients.ts), blob e1ca94d86c68e10bc9b4dcab4f55264165f61d3b.
- [apps/api/src/routes/check-ins.ts](https://github.com/KhubaibQaiser/fitness-app/blob/162bffbd2367f39be6c8dd57d8a213d3b225bed6/apps/api/src/routes/check-ins.ts), blob 3e1f81888813599236308a52bd341dfca335a9a7.
- [packages/db/src/time.ts](https://github.com/KhubaibQaiser/fitness-app/blob/162bffbd2367f39be6c8dd57d8a213d3b225bed6/packages/db/src/time.ts), blob 530ee9b2aab5889c86bd93770bc64c25f2984dd7.
- [packages/modules/src/coaching/notes.ts](https://github.com/KhubaibQaiser/fitness-app/blob/162bffbd2367f39be6c8dd57d8a213d3b225bed6/packages/modules/src/coaching/notes.ts), blob ab2274aca6f87f4ad15fbba583828edad17f2810.
- [packages/modules/src/coaching/checkins.ts](https://github.com/KhubaibQaiser/fitness-app/blob/162bffbd2367f39be6c8dd57d8a213d3b225bed6/packages/modules/src/coaching/checkins.ts), blob c3976b6334ec5265e3fc00c857839e9808e00ccd.
- [packages/db/src/schema/helpers.ts](https://github.com/KhubaibQaiser/fitness-app/blob/162bffbd2367f39be6c8dd57d8a213d3b225bed6/packages/db/src/schema/helpers.ts), blob c490de21d1948396cacb419765750dcbd3dc4bf5.
- [packages/db/src/schema/tenancy.ts](https://github.com/KhubaibQaiser/fitness-app/blob/162bffbd2367f39be6c8dd57d8a213d3b225bed6/packages/db/src/schema/tenancy.ts), blob 0a21507ada18a72e258a0647fff4deed8d940fa5.
- [packages/db/src/schema/health.ts](https://github.com/KhubaibQaiser/fitness-app/blob/162bffbd2367f39be6c8dd57d8a213d3b225bed6/packages/db/src/schema/health.ts), blob d95223adaadcd1413ad895ffb6af0fdfb499a076.
- [apps/api/src/schemas.ts](https://github.com/KhubaibQaiser/fitness-app/blob/162bffbd2367f39be6c8dd57d8a213d3b225bed6/apps/api/src/schemas.ts), blob 51366a7b825ce962c4476d3346f83723244a61c2.
- [packages/contracts/openapi/openapi.v1.json](https://github.com/KhubaibQaiser/fitness-app/blob/162bffbd2367f39be6c8dd57d8a213d3b225bed6/packages/contracts/openapi/openapi.v1.json), blob 7ea447ee250c3905ea33e8cf9ab3357550273ba0.
- [packages/contracts/src/types.ts](https://github.com/KhubaibQaiser/fitness-app/blob/162bffbd2367f39be6c8dd57d8a213d3b225bed6/packages/contracts/src/types.ts), blob 9652cf9655b71e1af0398d86285da3a19e82d588.
- [pnpm-lock.yaml](https://github.com/KhubaibQaiser/fitness-app/blob/162bffbd2367f39be6c8dd57d8a213d3b225bed6/pnpm-lock.yaml), blob cd8cc80c90d361a81275c7ad6604c4cc90c1ad96.

Root and applicable AGENTS read. Only root and apps/web AGENTS exist; no code modified in that repository. All128 all-state PR summaries retrieved over2 pages and screened for overlap. Merged [PR120](https://github.com/KhubaibQaiser/fitness-app/pull/120) fixes notifications only; its body, full diff and comments read. Open [PR125](https://github.com/KhubaibQaiser/fitness-app/pull/125) and [PR127](https://github.com/KhubaibQaiser/fitness-app/pull/127) file inventories checked;127's clients.ts diff adds Roster to clients.ts without repairing these notes responses. No linkedPR and zero issue comments on final reread. Native maintainer merge gates remain outstanding.

## Other reviewed candidates — no draft

| Issue | Review outcome |
| --- | --- |
| [Inspect AI #6796](https://github.com/UKGovernmentBEIS/inspect_ai/issues/6796) | New auth-refresh/backoff report already contains diagnosis, synthetic reproducer and proposed fixes. Current retry source at a1175d932c8ddd95f5c59ba52f69edd6c079c354 confirms before_sleep invokes before_retry; no additional contribution established. Reporter tests not rerun. |
| [Dify Tongyi #4345](https://github.com/langgenius/dify-official-plugins/issues/4345) | Missing customizable schema and TTS/ASR invocation caveats already covered by reporter and comment7182902095. Inspected TTS/ASR at731c850c88eccb2eaf0d1297d3fea0f5d3622768. No duplicate reply, provider test or credential use. |
| [Tokenhop #1235](https://github.com/tokenhop/tokenhop/issues/1235) | [PR1236](https://github.com/tokenhop/tokenhop/pull/1236) mocks resolveLiveModels in the unit suite. Head bc224f72d8acb24648d6761b6b49baea8369f281; exact diff reviewed. PR subsequently merged; issue closed2026-11-26T05:03:11Z. Author-reported tests not rerun. Excluded from open opportunities. |

[kube-agents #7276](https://github.com/gke-labs/kube-agents/issues/7276) received only a body-level triage read. Existing generic panic-containment proposal is not a completed new investigation.

## New follow-up only

[Openbot collaborator comment7176163364](https://github.com/nightly-labs/openbot/issues/7357#issuecomment-7176163364), Sniezka1927,2026-11-25T22:16:49Z, links [new report16624](https://github.com/nightly-labs/openbot/issues/16624). That report describes the working-directory MCP omission for Hermes on Linux. Read its complete body/comments/timeline: zero comments, still open. This is an additional report, not confirmation of our workaround or a fix, and not commercial interest.

Cursor for7357 advanced from7002266130 to7176163364 with history retained. No other new comments after saved cursors; no newly changed tracked issue state. No subsequent reply on the already verified Antigravity11 manual post; do not repost it.

## Tests and limits

Actual SHA-checked route source registered with stubbed Hono/schema/domain/auth/db objects; the real time.ts helper ran with Luxon3.7.2. npm archive SHA512 matched the upstream lockfile. Single library runtime extracted locally; no install scripts or system/global install. Four original handlers emitted the raw synthetic SQL string; four candidate handlers emitted the strict UTC ISO value. Additional null, offset, malformed-input and OpenAPI-shape groups passed. Auth call arguments were preserved, but authorization enforcement was not tested.

Initial harness run failed because deepStrictEqual compared different VM object prototypes; changed that assertion to compare serialized call records. Final eight groups passed. This harness failure is not a product bug. No application dependency install, migrations, real endpoints, customer data, secrets, wallets or payments.

## Tool fit, publication and safety

NAIF homepage and current diagnostic repository README refreshed. No referral added: MCP discovery does not fix timestamp serialization or stdio working-directory omissions and does not implement OAuth. The free technical solution stands on its own; no paid pitch.

Mandatory radar, README, ledger and R41 report read at own head d3d8a53253d4775b1fba4ff9ca90be7540f1f23a. Own untruncated tree and root AGENTS checked. All8 workflow definitions inspected; docs paths match no push trigger. No workflow dispatch or change, production/payment/V5/server/store change, heavy work or auto-merge. Only docs/problem-hunter-v1 updated with a current-head lease.

Owner action: review R42-01; approval is required before any future third-party publication. No publication attempted in this round.
