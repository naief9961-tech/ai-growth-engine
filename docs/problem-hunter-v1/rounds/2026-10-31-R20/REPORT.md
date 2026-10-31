# R20 • 31 October 2026

2026-10-31T05:03:29Z. 7 capped title searches (MCP/A2A/x402/webhook/schema/API/GitHub Actions, open issues created since Oct 28, bug, newest first). 41 results, 41 distinct URLs; 6 candidate threads fetched including comments/timeline; one completed source investigation.

## Selected: [Discord feed retry #118](https://github.com/codercops/discord-bot/issues/118)
Reporter: anurag2787; opened 2026-10-31T04:08:53Z. Generic retry marker loses delete-event provenance; resync removes marker before failed lookup. Store typed deletion intent and render fields across 429 retries; consume without refetch, never create missing feed for deletion. Avoid wrongly marking inaccessible issues deleted; preserve retry intent on repeated 429.

- [src/webhook.ts](https://github.com/codercops/discord-bot/blob/2f94380aeb61f06559ed2f438a4b413de6d21744/src/webhook.ts), blob e32f6041e881e2021fb31a05477f18c07f3361bc
- [src/github.ts](https://github.com/codercops/discord-bot/blob/2f94380aeb61f06559ed2f438a4b413de6d21744/src/github.ts), blob f3a8916867935e3b5cab3e30bc2a7f08e60597a6
- [test/webhook.test.ts](https://github.com/codercops/discord-bot/blob/2f94380aeb61f06559ed2f438a4b413de6d21744/test/webhook.test.ts), blob 1db29d5aeab46ba9f92f66e453a1ae6335046f2b

Read historical #48/#64. Only open PR #116 concerns account linking; no linked fix in #118 timeline. Another contributor asked to work on the issue. No assignment requested or implementation offered. Source inspected at 2f94380aeb61f06559ed2f438a4b413de6d21744. High confidence in baseline branch; proposed repair and concurrency behavior not integration-tested. Preserve delete-before-processing semantics and test overlapping marks before shipping. See [isolated evidence](TESTS.md).

## R20-01 — English draft pending owner approval
Destination: https://github.com/codercops/discord-bot/issues/118

One detail for whoever picks this up: the retry marker currently stores only "1", so by the time getIssue returns 404 the worker has lost the fact that GitHub actually delivered an issues.deleted event. A failed lookup alone doesn't distinguish deletion from loss of repository access.

I'd persist the deletion intent and the minimal feed-rendering fields from the verified webhook when the original Discord edit gets a 429. On retry, consume that deletion record without fetching the issue again. If a feed record exists, edit its existing message through writeFeed with the unavailable state. If no record exists, consume the marker without posting. Keep the deletion payload on a second 429; writing "1" there would lose it again. Ordinary refresh marks should keep their existing behavior.

I ran the current resync function in isolation with a synthetic 404: it consumed the marker and left the stored feed open. I didn't run the Worker or either service. A useful regression sequence is: deleted webhook → Discord 429 twice → successful edit of the original message. Assert that no replacement message is posted. Also cover an ordinary refresh with a GitHub 404 (no inferred deletion), and a Discord 404 on the unavailable edit (preserve the existing message-gone behavior from PR #64).

## Follow-up
33 previous issue threads plus R19 PR destination checked. Verified [R19 account comment](https://github.com/wevm/mppx/pull/1133#issuecomment-6515624633); do not repost. No subsequent developer reply. [Noir #3078](https://github.com/owasp-noir/noir/issues/3078) closed after [#3395](https://github.com/owasp-noir/noir/pull/3395) merged October 30 at 13:53:08 UTC. [Commit](https://github.com/owasp-noir/noir/commit/cd4893e22fbb36c122f9b41928873897a143a48a) omits explicit readOnly:true from request parameters for OAS2/3 JSON/YAML. No test rerun, production confirmation or attribution. Zero explicit commercial inquiries or external publication by this round.

## Other candidate decisions
- https://github.com/temporalio/ai-integrations/issues/325: Existing PR #326 addresses this bug.
- https://github.com/codercops/discord-bot/issues/114: Active fix #116; implementation guidance already posted.
- https://github.com/UsefulSoftwareCo/executor/issues/2472: Reporter provides reproduction and workaround; SDK source not established today.
- https://github.com/QuanLyVanBanTLBM/QuanLyVanBan_TLBM/issues/405: Static report, already proposes shared validation and regressions; no independent endpoint reproduction.
- https://github.com/forge-ci/setup-soldr/issues/621: Maintainer settings and version resolution already diagnosed in thread.

## Screening URLs
- https://github.com/ToanMobile/agent-workbench/issues/734
- https://github.com/GenAI-Security-Project/agent-control-standard/issues/383
- https://github.com/foxletters-hq/BaiShou-Next/issues/71
- https://github.com/AAswordman/Operit/issues/1436
- https://github.com/microsoft/powerbi-modeling-mcp/issues/144
- https://github.com/zeroclaw-labs/zeroclaw/issues/12146
- https://github.com/zeroclaw-labs/zeroclaw/issues/12143
- https://github.com/temporalio/ai-integrations/issues/325
- https://github.com/oscarbol09/a2a-hub/issues/17
- https://github.com/sgl-project/sglang/issues/47490
- https://github.com/IBM/mcp-context-forge/issues/7382
- https://github.com/openJiuwen-ai/agent-runtime/issues/356
- https://github.com/crewAIInc/crewAI/issues/8735
- https://github.com/A-Comm-Tech/a-comm-evidence-protocol/issues/108
- https://github.com/JMAN730/opendroid/issues/97
- https://github.com/codercops/discord-bot/issues/118
- https://github.com/cebertowicz/corsia/issues/1891
- https://github.com/codercops/discord-bot/issues/114
- https://github.com/pingdotgg/t3code/issues/27701
- https://github.com/trustflow-protocol/trustflow-backend/issues/985
- https://github.com/trustflow-protocol/trustflow-backend/issues/984
- https://github.com/trustflow-protocol/trustflow-backend/issues/983
- https://github.com/UsefulSoftwareCo/executor/issues/2472
- https://github.com/openclaw/openclaw/issues/188935
- https://github.com/NousResearch/hermes-agent/issues/147036
- https://github.com/oscarbol09/a2a-hub/issues/24
- https://github.com/morluto/rea/issues/8244
- https://github.com/CopilotKit/CopilotKit/issues/8125
- https://github.com/drizzle-team/drizzle-orm/issues/6619
- https://github.com/SpecterOps/BloodHound/issues/3622
- https://github.com/anthropics/claude-code/issues/106348
- https://github.com/mrveiss/AutoBot-AI/issues/20173
- https://github.com/open-gsd/gsd-core/issues/5825
- https://github.com/docker-hardened-images/catalog/issues/692
- https://github.com/codercops/discord-bot/issues/117
- https://github.com/catchhole-soma/catchhole-backend-java/issues/348
- https://github.com/OpenDCAI/gugu/issues/1163
- https://github.com/QuanLyVanBanTLBM/QuanLyVanBan_TLBM/issues/405
- https://github.com/ElMouafikFatima-Ezzahra/tp-github-actions-events/issues/2
- https://github.com/forge-ci/setup-soldr/issues/621
- https://github.com/navaismo/Marlin_bugfix_2.1_E3V3SE/issues/95

Documentation only. Root AGENTS and eight workflows checked; no docs push trigger. No NAIF tool recommended.
