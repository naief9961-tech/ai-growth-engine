# R21 — 1 November 2026

Checked 2026-11-01T05:05:00Z. 54 unique open issues screened, 6 threads read (body, all comments and timeline), 1 completed source investigation. Seven newest-first searches capped at ten each: MCP, A2A, x402, webhook, schema, API and GitHub Actions in title with bug, created since 29 October. Compared to prior radar/ledger; this is a sample, not exhaustive.

## Selected: [PriceStalker #268](https://github.com/mikeknight85/PriceStalker/issues/268)
Reported by arbrick, 2026-10-31T14:43:16Z. Original escaping bug already has [PR #269](https://github.com/mikeknight85/PriceStalker/pull/269); do not repeat its fix. Our finding is specific to the unmerged branch, not a claim about a release. Both layers in open PR #269 search the entire Content-Type for json, including parameters. Prevents settings from blocking valid plain text and provider from dropping delivery before POST. Compare normalized media type essence, preserve missing-header default and +json support. High for isolated literal-template branch; no deployed reproduction.

- [backend/src/services/notifications/providers/webhook.ts](https://github.com/mikeknight85/PriceStalker/blob/01fefec9556c0ad6e8a0b6c76eb06770b3317106/backend/src/services/notifications/providers/webhook.ts) blob ed08f84badb20b818dfc3e2a044c3922c5cdbd68
- [frontend/src/features/settings/webhookJson.ts](https://github.com/mikeknight85/PriceStalker/blob/01fefec9556c0ad6e8a0b6c76eb06770b3317106/frontend/src/features/settings/webhookJson.ts) blob f14edf46240dfd81eb6b3a9e2ed0fbe64c2c370b
- [frontend/src/features/settings/webhookJson.test.ts](https://github.com/mikeknight85/PriceStalker/blob/01fefec9556c0ad6e8a0b6c76eb06770b3317106/frontend/src/features/settings/webhookJson.test.ts) blob cb6904890e816cc33580805d102390bcc65b4b45

[Isolated test procedure](TESTS.md). No real delivery or dependencies installed; no NAIF product needed. No external message sent.

## R21-01 — English text for owner review
Destination: https://github.com/mikeknight85/PriceStalker/pull/269. Pending approval; recheck before posting.

One regression case for #269: with Content-Type: text/plain; profile="json" and the literal template price changed, the settings validator reports invalid JSON and the provider returns false before posting. The substring /json/i matches the parameter even though the media type is text/plain.

I checked the UI helpers and provider from 01fefec9 in isolation with a stubbed HTTP sender and literal templates. Two plain-text parameter cases were misclassified; the four controls behaved as expected. Classifying the lowercased, trimmed type/subtype before the first semicolon (application/json or a +json subtype, keeping the missing-header default) passed all six cases locally.

I'd use the same case table in both packages: expect one plain-text post for the example above, and keep JSON parsing for application/json; charset=utf-8 and application/problem+json. This checks media-type selection only; I did not run the full suite or send a real webhook.

## Follow-up
35 tracked discussions checked. Two new comments after NAIF's earlier QwenPaw comment: https://github.com/agentscope-ai/QwenPaw/issues/8424#issuecomment-6550564154 and https://github.com/agentscope-ai/QwenPaw/issues/8424#issuecomment-6552861498. Independent user reports legacy initialize works on ezBookkeeping 2.1.1, discovery returns 404/-32601; contributor invited that user to test open [PR #8445](https://github.com/agentscope-ai/QwenPaw/pull/8445), inspected head faea091fa4cf60617ea8f0648da2865ad2bfed53. Branch success not verified. No business inquiry.

One new [comment on Discord #118](https://github.com/codercops/discord-bot/issues/118#issuecomment-6539924670) assigned another contributor. No NAIF comment preceded it. [PR #119](https://github.com/codercops/discord-bot/pull/119) merged Oct 31 as 73ad2e04dc15982c120361b979694da0f3e3cf2f; upstream handles missing issue with existing feed, no deployment or test rerun claimed. R20 draft withdrawn. Later [#131](https://github.com/codercops/discord-bot/pull/131) separately handles retryable API failures. No causal credit.

## Screening decisions
- https://github.com/CherryHQ/cherry-studio/issues/23290: A released fix was already identified in discussion.
- https://github.com/a2aproject/a2a-rs/issues/404: Detailed transport repro and affected paths supplied; no independently verified additive finding.
- https://github.com/a2aproject/a2a-rs/issues/399: Published protobuf conversion diagnosis and reproducer; no new tested distinction.
- https://github.com/twilio/twilio-java/issues/989: Includes signed vector, existing cross-language comparison and proposed treatment; not independently extended.
- https://github.com/vllm-project/vllm/issues/64940: Linked fix #64941; no separate contribution established.

## Screened URLs
- https://github.com/kirodotdev/Kiro/issues/12204
- https://github.com/repowise-dev/repowise/issues/5161
- https://github.com/repowise-dev/repowise/issues/5154
- https://github.com/yetone/magpie/issues/4671
- https://github.com/CherryHQ/cherry-studio/issues/23290
- https://github.com/solidlime/MCP-Hub/issues/2
- https://github.com/bannff/python-software-factory/issues/55
- https://github.com/cogwheel0/conduit/issues/920
- https://github.com/rul-lang/rul/issues/7
- https://github.com/istefox/obsidian-mcp-connector/issues/664
- https://github.com/a2aproject/a2a-rs/issues/410
- https://github.com/BerriAI/litellm/issues/49427
- https://github.com/BerriAI/litellm/issues/49424
- https://github.com/a2aproject/a2a-rs/issues/404
- https://github.com/a2aproject/a2a-rs/issues/399
- https://github.com/oscarbol09/a2a-hub/issues/17
- https://github.com/sgl-project/sglang/issues/47490
- https://github.com/IBM/mcp-context-forge/issues/7382
- https://github.com/openJiuwen-ai/agent-runtime/issues/356
- https://github.com/Qunsultant/cfagent/issues/2548
- https://github.com/A-Comm-Tech/a-comm-evidence-protocol/issues/108
- https://github.com/NousResearch/hermes-agent/issues/147371
- https://github.com/n0nuser/decathlon-cli/issues/4
- https://github.com/mikeknight85/PriceStalker/issues/268
- https://github.com/artemu78/page_parcel/issues/5
- https://github.com/twilio/twilio-java/issues/989
- https://github.com/loickballoy/NOGOMAN/issues/133
- https://github.com/JMAN730/opendroid/issues/97
- https://github.com/cebertowicz/corsia/issues/1891
- https://github.com/pingdotgg/t3code/issues/27701
- https://github.com/trustflow-protocol/trustflow-backend/issues/985
- https://github.com/XiaomiMiMo/MiMo-Code/issues/2758
- https://github.com/block/schemabot/issues/1864
- https://github.com/Gentleman-Programming/gentle-shell/issues/2723
- https://github.com/Gareji-AI/rbxoc/issues/84
- https://github.com/Gentleman-Programming/gentle-ai/issues/5906
- https://github.com/libredb/libredb-studio/issues/2128
- https://github.com/Universal-Commerce-Protocol/ucp/issues/1025
- https://github.com/aws-cloudformation/cloudformation-coverage-roadmap/issues/2597
- https://github.com/morluto/rea/issues/8366
- https://github.com/astubenbord/paperless-mobile/issues/704
- https://github.com/yongliancai/withu/issues/9
- https://github.com/jianxcao/pan-302-plugin/issues/1
- https://github.com/repowise-dev/repowise/issues/5156
- https://github.com/openclaw/openclaw/issues/190078
- https://github.com/pixelelated/distribution/issues/1393
- https://github.com/cyanheads/bls-labor-mcp-server/issues/108
- https://github.com/cyanheads/bls-labor-mcp-server/issues/107
- https://github.com/cyanheads/bls-labor-mcp-server/issues/106
- https://github.com/CherryHQ/cherry-studio/issues/23299
- https://github.com/vllm-project/vllm/issues/64940
- https://github.com/ArchAstro/aster/issues/265
- https://github.com/ElMouafikFatima-Ezzahra/tp-github-actions-events/issues/2
- https://github.com/forge-ci/setup-soldr/issues/621

Root AGENTS and 8 workflow triggers inspected on 175e916045d59763ce7d6b028140b85c6bc60e50; no docs paths match a push trigger. Docs-only expected-head update.