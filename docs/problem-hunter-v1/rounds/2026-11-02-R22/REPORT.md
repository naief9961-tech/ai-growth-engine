**R22-01 posted and verified: [account comment](https://github.com/WeatherXM/wg1200-firmware/issues/2#issuecomment-6569936002). Do not repost.**

# R22 — 2 November 2026

Checked 2026-11-02T04:59:36Z. 43 results / 42 unique issue URLs from seven searches: open issues created since Oct 30; MCP, A2A, x402, webhook, schema, API and GitHub Actions in title with bug, latest eight each. Six candidate threads (descriptions, comments, timelines); two source investigations, one public-comment draft. No external publication.

## [WeatherXM/wg1200-firmware #2](https://github.com/WeatherXM/wg1200-firmware/issues/2)
Reporter andrevza; opened 2026-11-02T03:46:48Z.

Only the wind direction of 10 extraction destinations disagrees with its descriptor. ref_field_val casts the member address to T*, then get_field_val dereferences it; a float read of the U16 member is not numeric conversion and its value cannot be relied upon. Read as uint16_t, convert after success; keep presence/error state distinct from legitimate zero degrees.

Confidence: High for source type mismatch; observations on a physical device are reporter evidence only. Tests: 4 host cases passed with pinned helper bodies and synthetic pack types. No ESP32, real HTTP, full firmware, or bad-pointer baseline executed. No linked PR or comments; repo all-state PR list empty.

- [main/ws/web_server.cpp](https://github.com/WeatherXM/wg1200-firmware/blob/a30374b045c138dac3f6dd4267ef8eb7390a7670/main/ws/web_server.cpp), blob c8500a444bb1e2107e511d566ea74338bedfe302
- [main/ws/include/ws_fields.h](https://github.com/WeatherXM/wg1200-firmware/blob/a30374b045c138dac3f6dd4267ef8eb7390a7670/main/ws/include/ws_fields.h), blob 55e6da370162c0ab2713fc41eaa18e14c7fc922a

## [usekaneo/kaneo #2168](https://github.com/usekaneo/kaneo/issues/2168)
Reporter z3099644; opened 2026-11-02T01:25:49Z.

Outbound lease is keyed by integration and task; inbound locks the integration row and looks up the external issue number. This permits import before outbound createIssue returns its number. Prior #1393 fixed the opposite event ordering. Persist a pending outbound operation before the remote call; correlate the webhook only with a verified integration/project-scoped pending operation. Do not treat a user-editable task footer alone as proof. Reconcile early webhook vs response idempotently, including dispatch failure or crash. Keep normal external issue import.

Confidence: High for the ordering window; attribution to reported duplicates remains unverified. Tests: Static source review only. Proposed: block createIssue response, deliver webhook twice, release response; assert one original task and link, then test ordinary external issue with copied footer and crash/recovery. Timeline, #1393 fix, recent open PR list, issue-number and duplicate searches; no matching new fix found.

- [apps/api/src/plugins/gitea/events/task-created.ts](https://github.com/usekaneo/kaneo/blob/dd92f6bc9b5f86b3b4dfc396026350d220e129a5/apps/api/src/plugins/gitea/events/task-created.ts), blob 40791e62cf4a458bb84379dd6c441ec6f7b50173
- [apps/api/src/plugins/gitea/webhooks/issue-opened.ts](https://github.com/usekaneo/kaneo/blob/dd92f6bc9b5f86b3b4dfc396026350d220e129a5/apps/api/src/plugins/gitea/webhooks/issue-opened.ts), blob dd88123cdb36f6801fa00f4b4a788c84e071af8d
- [apps/api/src/plugins/sync/create-task-issue.ts](https://github.com/usekaneo/kaneo/blob/dd92f6bc9b5f86b3b4dfc396026350d220e129a5/apps/api/src/plugins/sync/create-task-issue.ts), blob 8469126f4d6a3b9f734cf7e6f2ed6060ef73e4d4
- [apps/api/src/plugins/github/services/link-manager.ts](https://github.com/usekaneo/kaneo/blob/dd92f6bc9b5f86b3b4dfc396026350d220e129a5/apps/api/src/plugins/github/services/link-manager.ts), blob 57001304062dacd719d590da720877c707785817
- [AI_POLICY.md](https://github.com/usekaneo/kaneo/blob/dd92f6bc9b5f86b3b4dfc396026350d220e129a5/AI_POLICY.md), blob b37802c5d63ab4ac509a88b6d59db2032435c5f6

Kaneo's AI_POLICY requires human-authored comments. Keep analysis internal; no copy-and-paste draft. No NAIF tool was recommended.

## R22-01 — English draft for approval
Destination: https://github.com/WeatherXM/wg1200-firmware/issues/2. Not sent. Recheck before publication.

I checked all ten get_field_val_from_pack calls in extract_weather_data at a30374b. Wind direction is the only destination whose type differs from its descriptor; the wind speed and gust destinations already match FLOAT.

The important detail is that ref_field_val returns a cast pointer and get_field_val dereferences it. Reading the U16 member through a float pointer is not a numeric conversion, so the regression shouldn't depend on the old code always producing exactly 0.0.

I tried the proposed uint16_t destination in a small host harness with the three original accessor templates and synthetic field packs. 0, 151 and 359 all survived extraction and conversion to float; an absent field returned ERROR_NOT_FOUND without overwriting the destination. For the endpoint test I'd include both 0 degrees (valid north) and a missing direction, as well as 151, so missing data can't accidentally become north. I didn't build the firmware or test the device or HTTP endpoint.

## Evidence
[Wind extraction host test and static cross-check](TESTS.md).

## Follow-ups
37 threads checked. One new own comment, [PriceStalker R21-01](https://github.com/mikeknight85/PriceStalker/pull/269#issuecomment-6553838250); cursor 6553838250. No subsequent developer response or commercial inquiry. No other new top-level comments or state changes. No attributed sales.

## Other candidate decisions
- https://github.com/bytedance/deer-flow/issues/7797: Existing contributor plan and PRs #7799/#7800.
- https://github.com/crewAIInc/crewAI/issues/8930: Existing fix PR #8931.
- https://github.com/a2aproject/a2a-rs/issues/423: Reporter has precise reproduction and announced PR; not independently extended.
- https://github.com/mastra-ai/mastra/issues/29167: Reported transform and reproducer; maintainer triage pending; no independent finding.

## Screening URLs
- https://github.com/kirodotdev/KiroCrew/issues/27743
- https://github.com/temporalio/ai-integrations/issues/375
- https://github.com/EliteaAI/elitea-testing-public/issues/2859
- https://github.com/paul356/KiCad-AI-Assistant/issues/230
- https://github.com/TerrenoLabs/terreno/issues/1672
- https://github.com/bytedance/deer-flow/issues/7797
- https://github.com/nicsuzor/academicOps/issues/3389
- https://github.com/ErixWong/touwaka-ai-mate/issues/1265
- https://github.com/crewAIInc/crewAI/issues/8930
- https://github.com/a2aproject/a2a-rs/issues/427
- https://github.com/a2aproject/a2a-rs/issues/423
- https://github.com/BerriAI/litellm/issues/49569
- https://github.com/a2aproject/a2a-rs/issues/410
- https://github.com/BerriAI/litellm/issues/49427
- https://github.com/BerriAI/litellm/issues/49424
- https://github.com/a2aproject/a2a-rs/issues/404
- https://github.com/A-Comm-Tech/a-comm-evidence-protocol/issues/108
- https://github.com/Silo-Server/silo-server/issues/3416
- https://github.com/usekaneo/kaneo/issues/2168
- https://github.com/IceSqueez/forge/issues/112
- https://github.com/kyverno/kyverno/issues/18393
- https://github.com/GravionLabs/elysion/issues/901
- https://github.com/GravionLabs/elysion/issues/900
- https://github.com/QRun-IO/qqq/issues/1361
- https://github.com/NousResearch/hermes-agent/issues/147371
- https://github.com/Startempire-Wire/focusa/issues/704
- https://github.com/openclaw/openclaw/issues/190865
- https://github.com/apache/gravitino/issues/14492
- https://github.com/novuhq/novu/issues/13153
- https://github.com/KanishJebaMathewM/Truxify/issues/19706
- https://github.com/mastra-ai/mastra/issues/29167
- https://github.com/apache/gravitino/issues/14457
- https://github.com/apache/gravitino/issues/14437
- https://github.com/wso2/api-platform/issues/4010
- https://github.com/stardelt/stardelt-platform/issues/476
- https://github.com/AbdelrhmanAh7/Mizano/issues/695
- https://github.com/vllm-project/vllm-omni/issues/9731
- https://github.com/ZenMux/zenmux-doc/issues/311
- https://github.com/WeatherXM/wg1200-firmware/issues/2
- https://github.com/GravionLabs/herdr-plugins/issues/165
- https://github.com/ArchAstro/aster/issues/265
- https://github.com/ElMouafikFatima-Ezzahra/tp-github-actions-events/issues/2

Base d44e47a244a233c55489b1f2ca10784f91e716ba; root AGENTS and eight workflow triggers inspected; no matching docs push trigger.