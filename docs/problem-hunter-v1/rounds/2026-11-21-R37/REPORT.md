# R37 — 2026-11-21
Checked 2026-11-21T05:06:28.476Z. No third-party publication or deletion.

## Counts
70 capped hits;65 unique URLs screened. Seven newest-first queries,10 each: is:issue is:open created:>=2026-11-18 plus MCP,A2A,x402,webhook,schema,API,"GitHub Actions". Not exhaustive72-hour coverage.
Five full issue/comment/timeline reads; one completed bounded source investigation.51 tracked issue/PR threads checked with paginated issue comments; four PR review timelines checked. Zero new developer replies to NAIF; one other-contributor comment on an unposted draft; one duplicate manual post verified.
Eight isolated assertions passed; no upstream suite. One new review draft. No commercial request established.

## Selected: Lontar CMS #452
https://github.com/handi7/lontar-cms/issues/452
Reporter: handi7. Discovery2026-11-21. Open, zero comments at review.
The actual locale projector treats an object-valued localized scalar as a locale dictionary. Re-projecting selected richText therefore returns null. Dispatcher re-projects the supplied doc; mutation forwards result.doc. Publish and unpublish use different updateLocale choices, so globally removing projection is unsafe.
Added evidence beyond the report: an absent requested/default key does not prove a value is already projected. A canonical {fr:richText} would be passed through by that heuristic. Explicit representation-boundary model avoids double projection. Keep read-access sanitization unchanged.
Confidence: high for isolated projector behavior; medium for design proposal. Benefit: concrete counterexample to a tempting fix and publish/unpublish regression distinction.
No linked fix in the complete timeline; zero open PRs; latest30 all-state summaries checked. Existing localization implementation PRs444/437 are not a new repair.

### Pinned sources
- [packages/core/src/operations/locale.ts](https://github.com/handi7/lontar-cms/blob/d16fd22d49bb74579a73a09b8c06649c17184b9d/packages/core/src/operations/locale.ts); commit d16fd22d49bb74579a73a09b8c06649c17184b9d; blob c1c51d3a85be8680049dfa55820f5668235ccdf8
- [packages/core/src/webhooks/dispatcher.ts](https://github.com/handi7/lontar-cms/blob/d16fd22d49bb74579a73a09b8c06649c17184b9d/packages/core/src/webhooks/dispatcher.ts); commit d16fd22d49bb74579a73a09b8c06649c17184b9d; blob 6451b46f0f59d89bd8bd16318716eab4259fe303
- [packages/core/src/operations/publish.ts](https://github.com/handi7/lontar-cms/blob/d16fd22d49bb74579a73a09b8c06649c17184b9d/packages/core/src/operations/publish.ts); commit d16fd22d49bb74579a73a09b8c06649c17184b9d; blob 28407193228a1e5948adddfec2b62dde2fe5101c
- [packages/core/src/operations/mutation.ts](https://github.com/handi7/lontar-cms/blob/d16fd22d49bb74579a73a09b8c06649c17184b9d/packages/core/src/operations/mutation.ts); commit d16fd22d49bb74579a73a09b8c06649c17184b9d; blob 7bfa978aaae7e26e533bf3c55715ebb109ad5117
- [packages/db-postgres/src/localization.ts](https://github.com/handi7/lontar-cms/blob/d16fd22d49bb74579a73a09b8c06649c17184b9d/packages/db-postgres/src/localization.ts); commit d16fd22d49bb74579a73a09b8c06649c17184b9d; blob 565b2b2927359643f8c984318ea8607133262d60

## Other candidates — not selected as solutions
- [paperclipai/paperclip/issues/22475](https://github.com/paperclipai/paperclip/issues/22475): Deferred: protocol-era mismatch reported, but no source/protocol validation completed; do not bypass metadata/authentication checks.
- [ymtdzzz/otel-tui/issues/507](https://github.com/ymtdzzz/otel-tui/issues/507): Release assets independently confirmed empty. Reporter already supplies workaround; failed build's root cause not established, no new tested repair.
- [gke-labs/kube-agents/issues/6782](https://github.com/gke-labs/kube-agents/issues/6782): Active PR6783 already addresses corrected test synchronization cause. Do not repeat the initial diagnosis, which the author corrected. PR tests author-reported, not rerun.
- [vAPI-Network/vapi-network/issues/83](https://github.com/vAPI-Network/vapi-network/issues/83): Deferred: valid local signature recovery does not prove server nonce/domain/authorization acceptance; server cause unproven. No wallet/signature/payment action performed.
PR6783 head bd24dcbdd3e4cf27a75d79e7bfb11445172288a0 is open/unmerged. Read metadata/body; tests were not rerun and diff not independently validated. otel-tui v0.7.6 assets=[] verified via release API; published2026-11-21T03:11:12Z. No workflow rerun.
Paperclip/GKE open-PR inventories capped100; no exhaustive PR search claimed.

## Follow-ups
- PowerPoint: original https://github.com/aws-samples/sample-spec-driven-presentation-maker/issues/665#issuecomment-7000865667 remains; second identical own comment https://github.com/aws-samples/sample-spec-driven-presentation-maker/issues/665#issuecomment-7031098102 verified. Record duplicate, do not repost. No deletion performed; no developer reply. This confirms the screenshot concern.
- Git5641: https://github.com/modelcontextprotocol/servers/issues/5641#issuecomment-7044776922 covers worktree/color markers. This is not a reply to NAIF because R36 was never posted. Retain R36 evidence but refresh/reduce overlapping draft before any publication; detached-HEAD evidence remains separate. No R36 post authorized by the user's PowerPoint confirmation.
- OpenViking8001 remains open/unmerged, same head b96a6e8729aef43ae9b74217f2ab6b6cd9b8df09. No new success claim.
All observed issue-comment cursors advanced; review namespaces retained separately. No explicit commercial interest.

## Tests and limitations
[Exact harness](TESTS.md). Native Node24.22.3 type stripping runs the reviewed locale.ts with imports removed; unused validation paths are not invoked. Baseline and small boundary model only; no database/webhook network/ACL/full-operation test, no installed-package repair. One guessed source path returned404, resolved through imports/tree to operations/locale.ts.
No free-tool referral: MCP HTTP probe does not repair CMS projection, and /tools cannot validate webhook signatures or this defect. No paid offer.

Root AGENTS and complete untruncated tree checked; no scoped AGENTS. All8 own workflows read, doc paths do not match push triggers. Only docs/problem-hunter-v1 changed with fresh-head atomic update. No workflows dispatched, production/payment/V5/server work or spending.

## Full English review draft R37-01 — NOT POSTED
Destination https://github.com/handi7/lontar-cms/issues/452
Pending user approval in an interactive turn, followed by a fresh issue/comment/PR check.

I reproduced the projection boundary at d16fd22d49bb74579a73a09b8c06649c17184b9d using the actual locale.ts module with its imports removed. For a localized richText field, projecting {body: {id: richTextDoc, en: ...}} once preserves the rich-text document; projecting that result again returns body: null.

There is a useful constraint on the proposed fix: checking only whether the object has the requested/default locale keys is not sufficient to identify an already-projected value. A canonical {fr: richTextDoc} with requested locale id and fallback en has neither key, but must not be passed through as if it were a rich-text document. That heuristic exposes the locale dictionary in the payload instead of producing the expected missing-value result.

I would make the representation explicit at the mutation/dispatcher and transition boundaries, and project only canonical input. Do not simply remove every projection: publish.ts deliberately uses updateLocale='all' for publish, while unpublish uses the requested locale; the publish path still needs its projection. Keep sanitizeDocRead and its existing ordering/overrideAccess behavior intact.

The regression matrix should cover create/update/unpublish with already-projected richText, publish from canonical data, a canonical value missing both requested and fallback locales, valid fallback, locale='all', and both collection/global paths. Assert the actual webhook payload and public operation result, with a denied field to ensure access filtering remains effective.

Eight isolated assertions passed: they reproduce the double projection, exercise a small explicit-representation boundary model, and demonstrate the missing-key heuristic counterexample. This is not an integrated repair: I have not run either database adapter, webhook delivery, access-control integration or the upstream suite.
