# R8 — Discovery audit

Checked 2026-10-20T05:04:25.754Z. Eight date-filtered searches, capped at 20 results each: **160 returned rows / 155 unique issue URLs**. These are preliminary search-result screens, not 155 verified diagnoses. Six candidates received full body/comments/timeline reads. One completed source investigation; two exploratory source reads. No claim of exhaustive GitHub coverage. Search result dates were missing in normalized results; actual creation times were read from raw issue responses for all six candidates.

The discovery dates prioritize 2026-10-19/20, with 2026-10-18 included for A2A/x402. Promotional x402 integrations, feature backlogs, bot-generated operational alerts, human-approval gates and cases without additional validated contribution were not selected. 0 search URLs match the existing tracked/excluded ledger; prior cases were not reopened without material new evidence.

## Queries

1. `is:issue is:open created:>=2026-10-19 MCP in:title`
2. `is:issue is:open created:>=2026-10-18 A2A in:title`
3. `is:issue is:open created:>=2026-10-18 x402 in:title`
4. `is:issue is:open created:>=2026-10-19 webhook in:title`
5. `is:issue is:open created:>=2026-10-19 schema in:title`
6. `is:issue is:open created:>=2026-10-19 JSON-RPC`
7. `is:issue is:open created:>=2026-10-19 authentication API`
8. `is:issue is:open created:>=2026-10-19 "GitHub Actions" failure`

## Full candidate reads

| Issue | Created UTC | Comments read | Decision |
|---|---|---:|---|
| [crewAIInc/crewAI #8289](https://github.com/crewAIInc/crewAI/issues/8289) | 2026-10-19T17:46:16Z | 0 | Open PR #8290 already supplies Redis ACL/TLS fix and regressions; related #5700/#8206 noted. No duplicate solution. |
| [ayme-labs/ayme #860](https://github.com/ayme-labs/ayme/issues/860) | 2026-10-20T04:54:23Z | 1 | Existing detailed triage already identifies validator/package boundary, repair and regressions. Maintainer design decision; no distinct validated contribution. |
| [vishnukothakapu/linkid #900](https://github.com/vishnukothakapu/linkid/issues/900) | 2026-10-20T03:36:45Z | 1 | PR #912 head 53a48f6d826f7696d872c699277ba43a00e1ecf5 already implements deadline and both abort error names, with a hanging-receiver test. Source read; no rerun or duplicate reply. |
| [recursive-cloud/woodhouse #29](https://github.com/recursive-cloud/woodhouse/issues/29) | 2026-10-20T04:33:49Z | 0 | Selected: completed source investigation; one review draft, not posted. |
| [paperless-ngx/paperless-ngx #14502](https://github.com/paperless-ngx/paperless-ngx/issues/14502) | 2026-10-20T04:41:22Z | 0 | Exploratory source read did not prove queryset-evaluation trigger. Original large-instance OOM not reproduced. Contribution policy requires AI disclosure/observed-only AI reports and rejects mostly AI-derived PRs. No speculative public draft. |
| [agentclientprotocol/codex-acp #647](https://github.com/agentclientprotocol/codex-acp/issues/647) | 2026-10-20T04:51:42Z | 0 | Reporter already supplies pinned code locations, proposed repair and capability-contract alternatives. No additional verified contribution; maintainer decision pending. |

## All preliminary results

Items not selected here were not fully investigated; this is not a declaration that their bugs are invalid or solved.

| # | Issue | Query | Disposition |
|---:|---|---:|---|
| 1 | [[MCP] Read-only remote exposure and local control policy](https://github.com/phynics/axoloty-debug/issues/4) | 1 | Preliminary only; not selected |
| 2 | [Cannot send a glasses photo to WhatsApp via MCP — no path for photo bytes to reach a tool call](https://github.com/macedonga/visor/issues/27) | 1 | Preliminary only; not selected |
| 3 | [[Gap]: Document manual authorization management for Enterprise MCP resources](https://github.com/stacklok/docs-website/issues/1258) | 1 | Preliminary only; not selected |
| 4 | [P2-跟进：A6.5-pr10a MCP 客户端遗留（outputSchema 校验、握手中 close、https 传输、夹具缺口）](https://github.com/daqi-dev/pilotdeck-rs/issues/361) | 1 | Preliminary only; not selected |
| 5 | [[customer] [Feature] PaddleSnitch MCP server (remote, OAuth) so AI assistants can use the s](https://github.com/baldur/paddlesnitch/issues/512) | 1 | Preliminary only; not selected |
| 6 | [port: fix: treat email usernames as case-insensitive without losing saved credentials (from RohanMuppa/brightspace-mcp-server#269)](https://github.com/RohanMuppa/Brightspace-API/issues/61) | 1 | Preliminary only; not selected |
| 7 | [Doc-example tokens in skills native-mcp.md are eaten by our own redactor — replace ghp_/sk- fakes with measured un-eatable placeholders](https://github.com/NousResearch/hermes-agent/issues/141875) | 1 | Preliminary only; not selected |
| 8 | [Add MCP servers from an MCP registry](https://github.com/cjohnstoniv/wardyn/issues/3387) | 1 | Preliminary only; not selected |
| 9 | [MCP servers in their own sandbox, relayed to the agent's](https://github.com/cjohnstoniv/wardyn/issues/3386) | 1 | Preliminary only; not selected |
| 10 | [[HT-QA-06A] Reintentar el 503 inicial del proveedor y hacer configurable el timeout de herramienta MCP](https://github.com/creep1ng/sre-agent/issues/719) | 1 | Preliminary only; not selected |
| 11 | [ayme mcp's own tools don't check their input against their schemas](https://github.com/ayme-labs/ayme/issues/860) | 1 | See candidate decision above |
| 12 | [[Maker MCP] get_ad_config repeatedly times out after 300 seconds (0.0.36 / Codex / Windows)](https://github.com/taptap/instant-games-open-mcp/issues/734) | 1 | Preliminary only; not selected |
| 13 | [GitHub remote MCP passed](https://github.com/githubnext/gh-aw-test/issues/24028) | 1 | Preliminary only; not selected |
| 14 | [MCP set-up for more clients in `docs/mcp.md`](https://github.com/thinkerwave-ai/thinkerwave/issues/4) | 1 | Preliminary only; not selected |
| 15 | [范围确认：现有 ZIP 导入的可选百智 MCP 停用示例包与指南](https://github.com/yynxxxxx/Codex-X/issues/75) | 1 | Preliminary only; not selected |
| 16 | [A late permission notification and MCP elicitation are shown wrong](https://github.com/torikatsupg/claude-tmux-sidebar/issues/44) | 1 | Preliminary only; not selected |
| 17 | [feat(slack-mcp): derive toolPolicy from the manifest row selection](https://github.com/higherorderfunctor/nix-agentic-tools/issues/2732) | 1 | Preliminary only; not selected |
| 18 | [Deployed Worker at /mcp does not match the 0.2.0 source: version, listChanged, close_account and error text are all still the old behavior](https://github.com/IndianOpinion/mcp/issues/12) | 1 | Preliminary only; not selected |
| 19 | [Large MCP JSON payload passed](https://github.com/githubnext/gh-aw-test/issues/24014) | 1 | Preliminary only; not selected |
| 20 | [[Server Submission]: shuita AI Price (ai-price-mcp) — AI subscription price tracker](https://github.com/cline/mcp-marketplace/issues/3114) | 1 | Preliminary only; not selected |
| 21 | [Add an A2A (Agent2Agent) server over the JSON-RPC binding to ballerina/a2a (JsonRpcListener)](https://github.com/ballerina-platform/ballerina-library/issues/9334) | 2 | Preliminary only; not selected |
| 22 | [Add an A2A (Agent2Agent) server over the HTTP+JSON binding to ballerina/a2a (RestListener)](https://github.com/ballerina-platform/ballerina-library/issues/9333) | 2 | Preliminary only; not selected |
| 23 | [[Bug]: Desktop Messaging shows "Needs setup" forever for token-free platforms (WhatsApp, webhook, A2A, ...): scoped _platform_enablement requires a required env var](https://github.com/NousResearch/hermes-agent/issues/141854) | 2 | Preliminary only; not selected |
| 24 | [[P1][a2a] Test the A2A ingress in the bridge module](https://github.com/FabioLeitao/zero-bridge/issues/50) | 2 | Preliminary only; not selected |
| 25 | [Implement A2A Agent Card discovery and cross-domain exchange](https://github.com/DBChoi85/AI-Agent-Collaboration/issues/3) | 2 | Preliminary only; not selected |
| 26 | [A2A bridge: keep the same-caller check across standalone replicas for calls without a caller](https://github.com/ptone/scion/issues/5393) | 2 | Preliminary only; not selected |
| 27 | [[A2A] Agent Card Resolver 缺少缓存机制：重复发现请求导致不必要的网络开销](https://github.com/openJiuwen-ai/agent-protocol/issues/148) | 2 | Preliminary only; not selected |
| 28 | [[BUG] A2A task cache drops the Redis ACL username and rediss TLS from REDIS_URL](https://github.com/crewAIInc/crewAI/issues/8289) | 2 | See candidate decision above |
| 29 | [v2 idea: identity-bound retrieval for the A2A request path (bind request to recipient twin / TODA SDA file)](https://github.com/StarwaterHeaven/secure-secrets-exchange/issues/2) | 2 | Preliminary only; not selected |
| 30 | [A2A message/stream: accept requests that send Accept: text/event-stream](https://github.com/tpsdev-ai/flair/issues/2717) | 2 | Preliminary only; not selected |
| 31 | [combo argument is silently ignored in MCP route_request and A2A message/send, but reported in routing telemetry](https://github.com/diegosouzapw/OmniRoute/issues/17188) | 2 | Preliminary only; not selected |
| 32 | [Next release gate: scoped agent access and A2A interoperability](https://github.com/Lthighway/academia-singularidade-site/issues/2) | 2 | Preliminary only; not selected |
| 33 | [A2A card advertises JSON-RPC transport and streaming that n-get does not implement](https://github.com/bingeboy/n-get/issues/199) | 2 | Preliminary only; not selected |
| 34 | [[L5 基礎 5] A2A 只標準化溝通，哪些事仍留給 harness？MCP 和 A2A 的工作單位差在哪裡？](https://github.com/chihmingyang/cs2680/issues/54) | 2 | Preliminary only; not selected |
| 35 | [Protocol watch: MCP, UCP, A2A (2026-10-19)](https://github.com/openbooking-sh/openbooking/issues/74) | 2 | Preliminary only; not selected |
| 36 | [a2a-apicurio-registry: support publishing and discovering tenant-hosted A2A agents](https://github.com/quarkiverse/quarkus-langchain4j/issues/3005) | 2 | Preliminary only; not selected |
| 37 | [[BUG] Remote A2A tool: agent card fetched without the caller's token (401), and the caller's tenant is forwarded ("tenant does not match the Agent URL")](https://github.com/kagent-dev/kagent/issues/3275) | 2 | Preliminary only; not selected |
| 38 | [Task: 文書 — MCP サーバと A2A の相手の足し方を agent_config.d/ の形に揃える](https://github.com/iunct-lab/Decentralized-Agent-Kit/issues/860) | 2 | Preliminary only; not selected |
| 39 | [Task: agent/dak_agent/config.py — agent_config.d/ の 1 項目 1 ファイルの MCP サーバと A2A の相手を読む](https://github.com/iunct-lab/Decentralized-Agent-Kit/issues/858) | 2 | Preliminary only; not selected |
| 40 | [Task: compose/test/ — 承認・検査・OTel・A2A のテスト用の構成を docker-compose.test.yml から移す](https://github.com/iunct-lab/Decentralized-Agent-Kit/issues/855) | 2 | Preliminary only; not selected |
| 41 | [Add Grey Ridge Signals (x402 v2, USDC on Base): token safety + on-chain checks](https://github.com/withgrokbot/verified-catalog/issues/4) | 3 | Preliminary only; not selected |
| 42 | [Optional: pre-trade sellability gate for Base tokens (free preview, x402 paid)](https://github.com/BlockRunAI/Franklin-Trading/issues/25) | 3 | Preliminary only; not selected |
| 43 | [x402 pre-trade safety gate for flyai-x402 skill: Base go/hold/block (free preview)](https://github.com/alextitonis/fly.ai/issues/13) | 3 | Preliminary only; not selected |
| 44 | [HAL-028: Three example agents: direct pay, x402 fetch, MCP](https://github.com/haloralabs/halora/issues/29) | 3 | Preliminary only; not selected |
| 45 | [Please independently verify a live Base x402 seller (24 routes, free previews)](https://github.com/kzmttkc/vet402/issues/67) | 3 | Preliminary only; not selected |
| 46 | [Optional pre-swap token safety gate for the agent flow (x402, Base)](https://github.com/JustaLab-co/x402-near-intents-demo/issues/1) | 3 | Preliminary only; not selected |
| 47 | [Provider onboarding request: On-chain Forensics (x402-native due-diligence API, live on Base)](https://github.com/NoFxAiOS/claw402-open/issues/24) | 3 | Preliminary only; not selected |
| 48 | [Token-safety gate for ranked Base pools (free preview, x402 paid route)](https://github.com/LPSignals/lpsignal-mcp/issues/1) | 3 | Preliminary only; not selected |
| 49 | [Optional token-contract layer for pre-sign verdicts (x402 route, free preview)](https://github.com/septagos/subcento/issues/1) | 3 | Preliminary only; not selected |
| 50 | [Optional: contract-level honeypot/sellability gate in buyGate (free preview, x402 paid)](https://github.com/Kitomv/KuroTrade/issues/9) | 3 | Preliminary only; not selected |
| 51 | [Optional paid fallback for token-safety checks (Base, x402 pay-per-call)](https://github.com/Solizardking/clawd-automation/issues/4) | 3 | Preliminary only; not selected |
| 52 | [Optional paid fallback for token-safety checks (Base, x402 pay-per-call)](https://github.com/richardtise/sniper-bot/issues/1) | 3 | Preliminary only; not selected |
| 53 | [Optional paid fallback for token-safety checks (Base, x402 pay-per-call)](https://github.com/ninhnn2/coin-rarda/issues/1) | 3 | Preliminary only; not selected |
| 54 | [Optional paid fallback for token-safety checks (Base, x402 pay-per-call)](https://github.com/araxis33/meme-scout/issues/4) | 3 | Preliminary only; not selected |
| 55 | [Optional paid fallback for token-safety checks (Base, x402 pay-per-call)](https://github.com/Shamrock2245/shamrock-trading-bot/issues/20) | 3 | Preliminary only; not selected |
| 56 | [Optional paid fallback for token-safety checks (Base, x402 pay-per-call)](https://github.com/alioanka/claudedex/issues/372) | 3 | Preliminary only; not selected |
| 57 | [Optional paid fallback for token-safety checks (Base, x402 pay-per-call)](https://github.com/maxpandelakis-boop/Meme-Bot/issues/1) | 3 | Preliminary only; not selected |
| 58 | [Optional paid fallback for token-safety checks (Base, x402 pay-per-call)](https://github.com/nestumfigos/dex-trading-bot/issues/2) | 3 | Preliminary only; not selected |
| 59 | [Optional paid fallback for token-safety checks (Base, x402 pay-per-call)](https://github.com/JonesKapedo/monroe-sniper/issues/16) | 3 | Preliminary only; not selected |
| 60 | [Optional paid fallback for token-safety checks (Base, x402 pay-per-call)](https://github.com/theselfruleorg/polyrob/issues/27) | 3 | Preliminary only; not selected |
| 61 | [Shiprocket: tracking webhook and status updates](https://github.com/priyamchauhanwork/ecomsellercentral/issues/62) | 4 | Preliminary only; not selected |
| 62 | [Webhook SSRF hardening: DNS-rebinding defence, pinned resolution, redirect and egress controls](https://github.com/Ledger-Lenz/Ledgerlens-core/issues/1158) | 4 | Preliminary only; not selected |
| 63 | [Webhook event catalog with CloudEvents envelopes, versioned schemas and server-side filters](https://github.com/Ledger-Lenz/Ledgerlens-core/issues/1148) | 4 | Preliminary only; not selected |
| 64 | [webhooks: signed but unroutable events vanish with a silent 200](https://github.com/recursive-cloud/woodhouse/issues/29) | 4 | See candidate decision above |
| 65 | [OpenAPI 3.2: author, import and generate webhook contracts](https://github.com/CaliLuke/loom/issues/959) | 4 | Preliminary only; not selected |
| 66 | [Gateway: an admission-observation hook so producers (webhook) can publish ordered delivery lifecycle events on the unified runtime](https://github.com/NousResearch/hermes-agent/issues/141851) | 4 | Preliminary only; not selected |
| 67 | [Webhook job delivery has no timeout and can stall the worker](https://github.com/vishnukothakapu/linkid/issues/900) | 4 | See candidate decision above |
| 68 | [WhatsApp: expor endpoint HTTP de webhook (verificação + recebimento de mensagens)](https://github.com/maurofneto/GiomCaptionVideos/issues/140) | 4 | Preliminary only; not selected |
| 69 | [Shared miner-signature finding: the webhook only describes the first box (box B's throttle, release and the resolve are never delivered)](https://github.com/FootprintAI/Containarium/issues/2820) | 4 | Preliminary only; not selected |
| 70 | [Webhook por instância (somar ao global ou substituir)](https://github.com/delltrak/wamcp/issues/142) | 4 | Preliminary only; not selected |
| 71 | [Webhook: eventos de canal (newsletter), entrada em grupo e etiquetas](https://github.com/delltrak/wamcp/issues/141) | 4 | Preliminary only; not selected |
| 72 | [Webhook: filtro de JIDs ignorados com curingas](https://github.com/delltrak/wamcp/issues/140) | 4 | Preliminary only; not selected |
| 73 | [Como Mauro, quero trocar o bot de ECS Service sempre ligado para Lambda + webhook, para não pagar por tempo ocioso](https://github.com/maurofneto/GiomCaptionVideos/issues/49) | 4 | Preliminary only; not selected |
| 74 | [T14-Validar la API key en los webhooks del Flujo C y rechazar las llamadas sin ella.](https://github.com/CarlosChDev/Grupo1_EcoPredict-NLQ/issues/239) | 4 | Preliminary only; not selected |
| 75 | [[S2] Repo indexer: GitHub webhook and periodic sync](https://github.com/rdlucas2/rlp/issues/93) | 4 | Preliminary only; not selected |
| 76 | [A refused webhook (401) logs only its code: no peer or header presence to trace where it came from](https://github.com/humandelegatedtrustprotocol/hdtp-gateway-agent/issues/56) | 4 | Preliminary only; not selected |
| 77 | [Webhook cloud parity test regex-parses batondeck's TypeScript; read a data export instead](https://github.com/humandelegatedtrustprotocol/hdtp-gateway/issues/255) | 4 | Preliminary only; not selected |
| 78 | [Users with project-scoped trigger permissions can't create or edit runbook webhook triggers in the UI](https://github.com/OctopusDeploy/Issues/issues/10327) | 4 | Preliminary only; not selected |
| 79 | [Webhook de recebimento com verificação de assinatura](https://github.com/insignia-corp/omnia/issues/61) | 4 | Preliminary only; not selected |
| 80 | [[W1-07][F2][Contract] Chuẩn hóa MQTT topics, schema và lifecycle phiên bản lịch](https://github.com/khanhpn308/LoRa-P2P-Hybrid-TDMA-MVP/issues/14) | 5 | Preliminary only; not selected |
| 81 | [New Invoice posts camelCase into a schema that strips it — the create always 400s (the unfixed half of #2876)](https://github.com/vinayakss007/nucrm-bigplan-by-vm-enterprise-v2/issues/2888) | 5 | Preliminary only; not selected |
| 82 | [[EPIC-08][DATA-01] Design users, workspaces, calculation snapshots and dependencies schema](https://github.com/Irsan-R/hitungin/issues/55) | 5 | Preliminary only; not selected |
| 83 | [leptris adapter: Schema#content_valid? raises NoMethodError (c_ptr) on Identity::ELEMENT wrappers](https://github.com/lutaml/moxml/issues/410) | 5 | Preliminary only; not selected |
| 84 | [Database: MySQL schema and SQLx queries](https://github.com/Rumeasiyan/heimdall/issues/3) | 5 | Preliminary only; not selected |
| 85 | [Agent: fix the tool-schema traps (title/name, the data wrapper)](https://github.com/ryanskarnulis/project-command-center/issues/411) | 5 | Preliminary only; not selected |
| 86 | [Agent: per-model profiles, and pin tool schemas and request bytes in CI](https://github.com/ryanskarnulis/project-command-center/issues/402) | 5 | Preliminary only; not selected |
| 87 | [Canonical structured log schema with sampling and correlation fields](https://github.com/Ledger-Lenz/Ledgerlens-core/issues/1192) | 5 | Preliminary only; not selected |
| 88 | [La persistance iOS ne laisse ni copie de secours ni texte SQL en clair dans les journaux, et son schéma est épinglé](https://github.com/isopen-io/meeshy/issues/11098) | 5 | Preliminary only; not selected |
| 89 | [F2.2 Poka-yoke ba lớp cho tiếp nhận văn bản đến: một JSON Schema dùng chung](https://github.com/HIT-Champion/HVL/issues/34) | 5 | Preliminary only; not selected |
| 90 | [F1.10 Tài liệu API tự xuất: schema GraphQL + OpenAPI](https://github.com/HIT-Champion/HVL/issues/24) | 5 | Preliminary only; not selected |
| 91 | [建议：为模组 INI 提供 LSP 或导出机器可读 schema](https://github.com/yomi2539/RWX/issues/11) | 5 | Preliminary only; not selected |
| 92 | [[BUG] GET /api/schema/ takes tens of minutes and grows a web worker past 8 GB on a large instance](https://github.com/paperless-ngx/paperless-ngx/issues/14502) | 5 | See candidate decision above |
| 93 | [Specification & Schema Ratification with Fail-Soft Addon Invariants](https://github.com/Adithya-Jayan/playnite-mobile-companion/issues/4) | 5 | Preliminary only; not selected |
| 94 | [Reconcile the in-code schema migrations in storage.py with Alembic into one authoritative path](https://github.com/Ledger-Lenz/Ledgerlens-core/issues/1127) | 5 | Preliminary only; not selected |
| 95 | [Feature schema registry with training/serving skew detection](https://github.com/Ledger-Lenz/Ledgerlens-core/issues/1118) | 5 | Preliminary only; not selected |
| 96 | [Define a chain-agnostic ChainEvent schema and a plugin SPI for new chain adapters](https://github.com/Ledger-Lenz/Ledgerlens-core/issues/1091) | 5 | Preliminary only; not selected |
| 97 | [PieroloOS release gate: consolidate security remediation and schema validation](https://github.com/Ebisindo/pieroloos-platform/issues/71) | 5 | Preliminary only; not selected |
| 98 | [Adoption evaluation: modelcontextprotocol/python-sdk](https://github.com/mcpmark-eval-liuhezi/mcp-sdk-triage/issues/1) | 6 | Preliminary only; not selected |
| 99 | [Terminal turn errors reach non-AIR clients as agent text with `stopReason: "end_turn"`](https://github.com/agentclientprotocol/codex-acp/issues/647) | 6 | See candidate decision above |
| 100 | [首次 RPC 验证应拒绝无效响应，不能误报 onboarding 成功](https://github.com/blockvectra/agent-quickstart/issues/3) | 6 | Preliminary only; not selected |
| 101 | [工作台 UI 交互规范：统一视觉层级、直接操作与连续反馈](https://github.com/liukun158959-beep/tebb/issues/124) | 6 | Preliminary only; not selected |
| 102 | [日程时间编排：周时间轴、拖拽改期与调整时长](https://github.com/liukun158959-beep/tebb/issues/123) | 6 | Preliminary only; not selected |
| 103 | [Design: csquad 3.0 - Go single binary, Codex engine, dependencies, checks and auto-merge (supersedes #40)](https://github.com/ShunL12324/c-squad/issues/41) | 6 | Preliminary only; not selected |
| 104 | [Agent 重跑遇到损坏钱包时应保留原身份，禁止静默覆盖](https://github.com/blockvectra/agent-quickstart/issues/1) | 6 | Preliminary only; not selected |
| 105 | [Signal channel over signal-cli JSON-RPC and SSE](https://github.com/amolenk/agrippa/issues/10) | 6 | Preliminary only; not selected |
| 106 | [Session adoption design note: docs/session-adoption.md](https://github.com/barelyworkingcode/relay/issues/526) | 6 | Preliminary only; not selected |
| 107 | [feat: post an image or a document as the Page](https://github.com/sirantd/paperclip-linkedin-org/issues/14) | 6 | Preliminary only; not selected |
| 108 | [Dependency security debt: 71 reachable vulnerabilities, 41 of them in the Go standard library](https://github.com/33cn/chain33/issues/1409) | 6 | Preliminary only; not selected |
| 109 | [[G02] Verifiera inbäddad granskning, CSP, remount och replay i faktisk klient](https://github.com/alex-engvall/fortnox-mcp/issues/32) | 6 | Preliminary only; not selected |
| 110 | [[G01] Verifiera klientprotokoll, OAuth och återladdning i ChatGPT](https://github.com/alex-engvall/fortnox-mcp/issues/31) | 6 | Preliminary only; not selected |
| 111 | [Spec: Agrippa V1 — self-hosted personal assistant over Signal](https://github.com/amolenk/agrippa/issues/1) | 6 | Preliminary only; not selected |
| 112 | [Standalone interactive CLI sessions are invisible to desktop app clients after the shared-host removal (senpi#2328)](https://github.com/code-yeongyu/senpi/issues/3779) | 6 | Preliminary only; not selected |
| 113 | [🦞 OpenClaw Ecosystem Digest 2026-10-20](https://github.com/datnguyenquy94/news-radar/issues/831) | 6 | Preliminary only; not selected |
| 114 | [Stable release audit: verified defects, architecture priorities and OpenAPI 3.2 coverage](https://github.com/CaliLuke/loom/issues/1023) | 6 | Preliminary only; not selected |
| 115 | [高 CPU：v0.1.6 全局响应钩子逐分片重复解析完整长请求（12 秒约 5.24 GB 内部传参）](https://github.com/jiandanc/CLIProxyAPI-freetier2api-plugin/issues/9) | 6 | Preliminary only; not selected |
| 116 | [MGB: Website Navigation Bar + Technicality Feature](https://github.com/apcspt1/portfolio/issues/10) | 7 | Preliminary only; not selected |
| 117 | [[FLOWER-MATRIX-PROVIDER-PROBE]](https://github.com/joseungil-kr/fwith-site-factory/issues/440) | 7 | Preliminary only; not selected |
| 118 | [[EPIC-08][AUTH-01] Evaluate authentication provider, backend/API and security threat model](https://github.com/Irsan-R/hitungin/issues/54) | 7 | Preliminary only; not selected |
| 119 | [CVE-response: CVE-2026-75128 (CRITICAL CVSS 9.8)](https://github.com/sattyamjjain/agent-audit-kit/issues/1055) | 7 | Preliminary only; not selected |
| 120 | [[aw] Test Copilot Assign To Agent Reasoning Effort failed to assign agent](https://github.com/githubnext/gh-aw-test/issues/24034) | 7 | Preliminary only; not selected |
| 121 | [Backend REST API: endpoints, authentication and logging](https://github.com/Rumeasiyan/heimdall/issues/2) | 7 | Preliminary only; not selected |
| 122 | [bitFlyer: take the quantities from the API and the prices from the public price page](https://github.com/y-marui/tauri-robo-advisor/issues/103) | 7 | Preliminary only; not selected |
| 123 | [Spec: Walking skeleton milestone 1c – web UI](https://github.com/mtiews/tendworks/issues/38) | 7 | Preliminary only; not selected |
| 124 | [Ligar o app a um projeto Firebase real (Spark)](https://github.com/dv-dev1/achei-no-campus/issues/5) | 7 | Preliminary only; not selected |
| 125 | [Hackathon [Feature]:  Add Railway data-Source Connector](https://github.com/topoteretes/cognee/issues/6083) | 7 | Preliminary only; not selected |
| 126 | [Apply standing Director-agent permission on the existing testing-retry route](https://github.com/cbusillo/launchplane/issues/4186) | 7 | Preliminary only; not selected |
| 127 | [PRD: Agent token usage report](https://github.com/ying0515/cms-1019/issues/6) | 7 | Preliminary only; not selected |
| 128 | [[Bug] Headless CLI auth blocked: api.z.ai/api/auth/z/login returns identical error for valid, invalid, and empty tokens (desktop 3.15.3, Linux)](https://github.com/zai-org/feedback/issues/1126) | 7 | Preliminary only; not selected |
| 129 | [[23120262][BUG-C09] User thường xóa được coupon của Admin](https://github.com/tkob-team/eshop-sut/issues/46) | 7 | Preliminary only; not selected |
| 130 | [[23120262][BUG-C08] User thường đọc được danh sách coupon quản trị](https://github.com/tkob-team/eshop-sut/issues/45) | 7 | Preliminary only; not selected |
| 131 | [[23120262][BUG-C07] User thường tạo được coupon của Admin](https://github.com/tkob-team/eshop-sut/issues/44) | 7 | Preliminary only; not selected |
| 132 | [[23120262][BUG-C06] Usage limit âm được lưu, zero bị đổi ngầm thành 1](https://github.com/tkob-team/eshop-sut/issues/43) | 7 | Preliminary only; not selected |
| 133 | [[23120262][BUG-C05] min_order_amount âm vẫn được lưu](https://github.com/tkob-team/eshop-sut/issues/42) | 7 | Preliminary only; not selected |
| 134 | [[23120262][BUG-C04] discount_value bằng 0 hoặc âm vẫn tạo coupon](https://github.com/tkob-team/eshop-sut/issues/41) | 7 | Preliminary only; not selected |
| 135 | [[23120262][BUG-C03] Type ngoài enum percent/fixed vẫn được lưu](https://github.com/tkob-team/eshop-sut/issues/40) | 7 | Preliminary only; not selected |
| 136 | [Alert: generated dataset refresh failed](https://github.com/asopitech-labs/global-executables/issues/94) | 8 | Preliminary only; not selected |
| 137 | [[self-heal] pmsec ci failed](https://github.com/HikaruEgashira/pmsec/issues/143) | 8 | Preliminary only; not selected |
| 138 | [docs: ship pixel-town READMEs with scheduled repository status cards](https://github.com/BotHarness/DeepSeekBot/issues/2373) | 8 | Preliminary only; not selected |
| 139 | [[WIP] Daily Documentation Diagram: work in progress](https://github.com/github/gh-aw/issues/70435) | 8 | Preliminary only; not selected |
| 140 | [[github-docs-seo] Daily baseline report: improve Agentic Workflow discoverability](https://github.com/github/gh-aw/issues/70434) | 8 | Preliminary only; not selected |
| 141 | [Feed workflow failed](https://github.com/nvm-windows/ossf-malicious-packages/issues/3) | 8 | Preliminary only; not selected |
| 142 | [[Teams] Falha na notificação de commits](https://github.com/ericson-j-santos/reqsys-v2-enterprise-real/issues/2927) | 8 | Preliminary only; not selected |
| 143 | [[aw] The Great Escapi: had a request rejected](https://github.com/github/gh-aw/issues/70433) | 8 | Preliminary only; not selected |
| 144 | [Reproc: corrida fallida o colgada](https://github.com/MendozaVolcanic/VRP-chile/issues/870) | 8 | Preliminary only; not selected |
| 145 | [Deploy stalled at approval gate — a release is waiting on a human click](https://github.com/unnfazzed/Lynia/issues/1273) | 8 | Preliminary only; not selected |
| 146 | [Main CI failed: Managed Agent gate on d236885bab16](https://github.com/QwenLM/qwen-code/issues/14835) | 8 | Preliminary only; not selected |
| 147 | [[CI] SultanC Integration — Landed Commit Qualification / Qualification Required](https://github.com/sultan-language/sultanc/issues/27) | 8 | Preliminary only; not selected |
| 148 | [[CI] SultanC Integration — Landed Commit Qualification / Native Host / arm64-darwin](https://github.com/sultan-language/sultanc/issues/26) | 8 | Preliminary only; not selected |
| 149 | [[CI] SultanC Integration — Landed Commit Qualification / Native Host / x86_64-linux](https://github.com/sultan-language/sultanc/issues/25) | 8 | Preliminary only; not selected |
| 150 | [[CI] SultanC Security — CodeQL / Stage0 C-C++ / Trusted](https://github.com/sultan-language/sultanc/issues/24) | 8 | Preliminary only; not selected |
| 151 | [[Firewall Test] Escape test failed](https://github.com/github/gh-aw/issues/70432) | 8 | Preliminary only; not selected |
| 152 | [[windows-integration] Expand Windows CLI shell coverage for path and PATHEXT edge cases](https://github.com/github/gh-aw/issues/70431) | 8 | Preliminary only; not selected |
| 153 | [[hikaevi] Issue #35: [pr] Make #23 mergeable: Bump postcss and next](https://github.com/HikaruEgashira/tutorial-nextjs-prisma-postgres/issues/52) | 8 | Preliminary only; not selected |
| 154 | [[AUTO-FIX] Arvin Build (0658fa2445b8120a184b044895abaa35828c513d) failed at 0658fa2445b8](https://github.com/mobinpda-lab/Arvin-clean/issues/2853) | 8 | Preliminary only; not selected |
| 155 | [[content-watch] 🧩 Advanced NL2SQL and advanced DAX generation in Fabric data agents (+8 more today)](https://github.com/smoens/knowledge-cabinet/issues/79) | 8 | Preliminary only; not selected |
