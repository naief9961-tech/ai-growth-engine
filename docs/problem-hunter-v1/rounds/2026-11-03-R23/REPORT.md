# R23 • 3 November 2026

2026-11-03T05:06:11Z. Seven title searches (MCP/A2A/x402/webhook/schema/API/GitHub Actions with bug, since 31 October, latest 8 each); 41 distinct open URLs, six complete candidate threads, one new source investigation. Historical radar, index, ledger and R22 report checked. No duplicate of selected URL in prior rounds. No outside post.

## [Langfuse #19594](https://github.com/langfuse/langfuse/issues/19594)
Reported by boeschj, opened 2026-11-03T01:17:33Z. Existing [code PR](https://github.com/langfuse/langfuse/pull/19595) and [docs PR](https://github.com/langfuse/langfuse-docs/pull/4199) already address the generic error. New contribution concerns reproducing the exact cap from other languages. The PR uses JSON.stringify(schema).length (UTF-16 code units). Unicode scalar count, UTF-8 bytes and original request length are not the enforcement metric. Retain current size policy, clarify compact serialized UTF-16 units; add a non-BMP boundary test to the existing ASCII cases. High for size gate; SDK/Cloud path untested. [Source](https://github.com/langfuse/langfuse/blob/440fb06980c5db03f770f64451a7658b29f5bd20/packages/shared/src/utils/jsonSchemaValidation.ts) blob 924df99826cac3a74561a9aea18d71f8fd617efe. Docs branch b65b16dba17f74bc5d27e50103fcbbfbde6e1fec. The docs are proposed, not released. [Tests and limits](TESTS.md).

## R23-01 — English draft for owner review
Destination: https://github.com/langfuse/langfuse/pull/19595. Awaiting approval; re-read before posting.

One boundary worth adding to the ASCII test: the 10,000 limit counts UTF-16 code units in JSON.stringify(schema). A Python caller counting Unicode code points in the same compact JSON text can get a different answer.

I checked the size gate at 440fb069 with a string schema whose description ends in a single 😀. At 10,000 serialized JS units (9,999 code points) it reached the compile step. Appending one ASCII letter gave 10,001 units but exactly 10,000 code points, and the gate returned the size error before compile. I stubbed the compiler to observe that branch; this wasn't a Cloud or SDK test.

I'd keep the existing limit, add that pair to the regression table, and use “10,000 UTF-16 code units after JSON.stringify” in the companion docs so users can reproduce the boundary.

## Follow-up
[PriceStalker contributor's reply](https://github.com/mikeknight85/PriceStalker/pull/269#issuecomment-6569547936) explicitly confirms the reported header parameter edge, cites [fix](https://github.com/mikeknight85/PriceStalker/commit/85719238db78e1184e92fe28e8f6f28d4241c042) and thanks the account. [PR #269](https://github.com/mikeknight85/PriceStalker/pull/269) merged 2 November at 07:27:27 UTC; #268 closed. Six prior isolated cases passed against merge 33c8e3e2ccb7093efb8a5477d27921652f9e8dfd; no full suite, delivery or deployment verified. Technical uptake, no commercial interest. WeatherXM own post already reported; reconciled cursor without counting as new developer reply. 37/38 tracked discussions readable. IntelliFlow #940 and comments both returned 404 on recheck. Did not infer closure or reset its cursor. No other new top-level replies on accessible threads.

## Other reads
- https://github.com/zai-org/feedback/issues/1374: Later reporter update qualifies restart symptom; client internals and cause not verified.
- https://github.com/a2aproject/a2a-go/issues/516: Reporter supplies transport comparison and precise splitting/trim regression plan.
- https://github.com/a2aproject/a2a-go/issues/512: Reporter supplies round-trip cases, proposed repair and table tests.
- https://github.com/stevezau/media_preview_generator/issues/438: Pinned register/unregister/rotation order and corrective alternatives already supplied.
- https://github.com/AppJars/appjars/issues/21: Published-jar inspection and two affected paths already reported. No independent source reproduction.

## Screening URLs
- https://github.com/sakho13/moto-reco/issues/638
- https://github.com/temporalio/ai-integrations/issues/387
- https://github.com/milind-soni/OpenMausBot/issues/4247
- https://github.com/duhu2000/dsh-mcp-connector/issues/209
- https://github.com/zai-org/feedback/issues/1374
- https://github.com/picoduck/wollipog/issues/4072
- https://github.com/anthropics/claude-code/issues/106854
- https://github.com/xai-org/plugin-marketplace/issues/1863
- https://github.com/a2aproject/a2a-go/issues/516
- https://github.com/a2aproject/a2a-go/issues/512
- https://github.com/BerriAI/litellm/issues/49622
- https://github.com/alibaba/nacos/issues/15975
- https://github.com/crewAIInc/crewAI/issues/8930
- https://github.com/a2aproject/a2a-rs/issues/427
- https://github.com/BerriAI/litellm/issues/49569
- https://github.com/BerriAI/litellm/issues/49427
- https://github.com/stevezau/media_preview_generator/issues/438
- https://github.com/AppJars/appjars/issues/21
- https://github.com/nightly-labs/openbot/issues/4509
- https://github.com/EasySoft-Tech-SL/dolibarr-easyocr-module/issues/4
- https://github.com/zedu-team-neo-mando/office-zedu-be/issues/50
- https://github.com/Silo-Server/silo-server/issues/3416
- https://github.com/usekaneo/kaneo/issues/2168
- https://github.com/kyverno/kyverno/issues/18393
- https://github.com/vastsa/PI-Desktop/issues/2079
- https://github.com/transistorsoft/react-native-background-geolocation/issues/2679
- https://github.com/SpearSystems/LCP/issues/181
- https://github.com/daniel-ospina/tortoise/issues/10685
- https://github.com/SpearSystems/LCP/issues/175
- https://github.com/openJiuwen-ai/agent-runtime-java/issues/261
- https://github.com/langfuse/langfuse/issues/19594
- https://github.com/pandazxx/codex-slack/issues/283
- https://github.com/xpert-ai/xpert/issues/1328
- https://github.com/vastsa/PI-Desktop/issues/2076
- https://github.com/wso2/agent-manager/issues/2273
- https://github.com/dujiao-next/dujiao-next/issues/380
- https://github.com/vllm-project/vllm-ascend/issues/20734
- https://github.com/OpenBMB/StaffDeck/issues/303
- https://github.com/openclaw/openclaw/issues/191644
- https://github.com/IamRamgarhia/All-In-One-Free-SEO-Tool/issues/57
- https://github.com/ArchAstro/aster/issues/265

Root AGENTS and eight workflow triggers inspected at edb92a0c220b2115bb7ef69ec510f126c0212559. No docs-only push matches. No tool recommendation or external action.