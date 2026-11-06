# R26 — source evidence and deduplicated follow-up | 2026-11-06

## Actual counts
75 unique URLs screened from 85 results across eight capped recent open-issue searches. Seven keyword searches (MCP, A2A, x402, webhook, schema, API, GitHub Actions), top 10 each, plus MCP in:title bug, top 15; created since 2026-11-03. These are capped results, not an exhaustive GitHub count.

Five new candidate issue bodies, all comments and timelines read. Two bounded source investigations completed with isolated tests (Backlog and Hatchet), plus two exploratory source reads (STAC and AWS). **No new end-to-end fix proven. One diagnostic English draft; no external publication.** Four candidates withheld rather than filling five slots.

43 prior/manual discussion threads checked, plus reviews and inline comments on four tracked PRs. One manually posted PDF Modifier comment reconciled; zero new human replies. One new CLA bot comment on Langfuse belongs to that PR submission and is not a response to us. All cursor updates preserve prior history, including empty comment collections.

## Selected contribution: Backlog.md #1179
- [Issue](https://github.com/MrLesk/Backlog.md/issues/1179), reporter kenorb, created 2026-11-06T02:34:52Z; open, no comments or linked timeline PR at final recheck.
- Report: acceptanceCriteriaSet silently truncates 520 characters to 500 in installed 1.55.3 binary.
- Reported tag v1.55.3 resolves to `0cf4fdbc70020327f4366a29d3f405f83d180301`. Current main inspected at `3a296c0f6f949b31e458b849b9617702c56c1023`.
- **Evidence:** the unchanged tagged validator rejects 501/520 ASCII characters and returns no sanitized data; it preserves 441/500 characters. A mixed valid/oversize batch is rejected at item index 1. Five isolated Node v24.22.1 case groups passed.
- Tagged task registration uses createSimpleValidatedTool; wrapper checks isValid before calling handler. Tagged/current validators are consistent for this path.
- **Root cause remains unresolved:** isolated source behavior does not reproduce reported installed-binary behavior. No conclusion that the user is mistaken or that the deployed client is at fault.
- Proposed next check: synthetic fixture only; compare argument length before transport and at registered-tool entry, then verify the executable actually launched. A 500-character arrival identifies pre-handler shortening; 520 arriving with success requires tracing the actual runtime validation path. Test rejected calls do not invoke edit or mutate the fixture, and a 500-character control round-trips.
- Confidence: high for isolated source result; low/unresolved for runtime attribution. Benefit: directs investigation to the differing boundary without inventing a sanitizer patch.
- Untested: release binary, Bun runtime, MCP transport, tool wrapper execution, filesystem persistence and upstream suite. No server patch proposed or installed.
- PR checks: searches for issue number and acceptanceCriteriaSet returned zero; broader truncation/500 PR searches showed unrelated matches. No linked fix or existing matching diagnostic reply found.
- Approval: **AWAITING_USER_APPROVAL**, publication **DRAFT_NOT_POSTED**. Full text in [DRAFTS.md](DRAFTS.md).

### Pinned source
- [src/mcp/validation/validators.ts](https://github.com/MrLesk/Backlog.md/blob/0cf4fdbc70020327f4366a29d3f405f83d180301/src/mcp/validation/validators.ts) — blob `8c8427578231f1cbd3378f2baecddac03ea191ea`.
- [src/mcp/utils/schema-generators.ts](https://github.com/MrLesk/Backlog.md/blob/0cf4fdbc70020327f4366a29d3f405f83d180301/src/mcp/utils/schema-generators.ts) — blob `577952e27d835952b28c96076e60e1218107ff46`.
- [src/mcp/validation/tool-wrapper.ts](https://github.com/MrLesk/Backlog.md/blob/0cf4fdbc70020327f4366a29d3f405f83d180301/src/mcp/validation/tool-wrapper.ts) — blob `235a632047a4f6de7dd3255d7f83e6aaac3c8cda`.
- [src/mcp/tools/tasks/index.ts](https://github.com/MrLesk/Backlog.md/blob/0cf4fdbc70020327f4366a29d3f405f83d180301/src/mcp/tools/tasks/index.ts) — blob `8a185daaf7110e69bd5f353c0a1bc23855432030`.

## Other reviewed candidates — withheld
1. [Hatchet #5448](https://github.com/hatchet-dev/hatchet/issues/5448), uinstinct, 2026-11-06T03:56:17Z: high confidence in fallback URL port loss. Source `00d4dd2afa601324cf7d219ff04d063509e47419`, [use-webhooks.tsx](https://github.com/hatchet-dev/hatchet/blob/00d4dd2afa601324cf7d219ff04d063509e47419/frontend/app/src/pages/main/v1/webhooks/hooks/use-webhooks.tsx), blob `bf5296e557666d517cf9d26c9199e4067b9ae848`. Seven isolated case groups pass after hostname→host; four baseline port-loss cases reproduced. Reporter-specific tenant.serverUrl branch is unconfirmed. **Exact diagnosis and host/origin solution already exist in [PR #3697 review](https://github.com/hatchet-dev/hatchet/pull/3697#discussion_r3137827336)**. No duplicate draft. Read the merged PR description, relevant diff, conversation, reviews and inline comments. Recent webhook PR search found no matching new URL fix. AI_POLICY requires human review/editing and AI disclosure for public material; nothing sent.
2. [AWS AgentCore #2276](https://github.com/awslabs/agentcore-samples/issues/2276), amommendes, 2026-11-05T21:08:33Z: source at `e668c275b0c891c0944999e56cbe8831f389b631` serves agent.json. [Existing PR #2279](https://github.com/awslabs/agentcore-samples/pull/2279) already describes the route and three documentation corrections. Read PR discussion/reviews; files endpoint returned empty, so no claim to have independently verified its patch. No new runtime test or reply.
3. [STAC virtual-assets #5](https://github.com/stac-extensions/virtual-assets/issues/5), J-Christophe, 2026-11-06T04:55:28Z: source/README at `d499e03a4849231761e49d47720e19bddc3f1d8a`, schema blob `484de2e2b421863e6147616b0063ff1baef6f005`, confirm reported overlapping alternatives. Reporter already supplies cause and anyOf proposal; no additive reply. No linked PR; targeted PR search empty. Python jsonschema unavailable locally, no schema test executed.
4. [MCPM #516](https://github.com/pathintegral-institute/mcpm.sh/issues/516), gjwang, 2026-11-06T04:52:02Z: report already includes pinned model/parser evidence and explicit transport option. No independent source execution or new fix claimed; no additive reply.

## New follow-up facts only
- [PDF Modifier manual comment](https://github.com/mlorentedev/pdf-modifier/issues/232#issuecomment-6650352332), naief9961-tech, 2026-11-05T05:16:09Z, verified. It is the prior installed-entry-point regression suggestion. No developer reply. Added to ledger with last_seen_comment_id=6650352332; do not repost. No installed-package test was performed.
- [Langfuse automated CLA notice](https://github.com/langfuse/langfuse/pull/19595#issuecomment-6660209061) is not human engagement or a commercial lead. Cursor advanced only.
- No new direct human response, technical acknowledgement, state change or explicit commercial interest in the other tracked threads. Earlier BanyanDB and PriceStalker outcomes not reannounced.

## Verification, scope and limitations
12 isolated test groups total, using synthetic strings and URL objects only; no network requests from tests, credentials, wallets, real payments, server startup, or production changes. [TESTS.md](TESTS.md) includes executed harnesses and scope. This is not a full-system repair certification.

Read mandatory radar, README, ledger and R25 report; fresh root AGENTS and nontruncated recursive tree contain no nested AGENTS. Read all eight workflow triggers: docs-only push matches none of their push paths. New commit is scoped to docs/problem-hunter-v1/ and uses a current-head lease; no workflows dispatched or modified. No NAIF tool recommended because none is needed for this diagnostic boundary; no marketing or paid offer. Existing diagnostic repository left untouched.

## Screening inventory
- [Handoff for Ark: open backend issues after the 6 Nov triage, ranked (6 P1, 21 P2, 52 P3) ](https://github.com/waldoco/waldo-backend/issues/1934)
- [planning Agent work packs and start order for the open ryan-tools backlog ](https://github.com/Chain-Frost/ryan-tools/issues/240)
- [Use admin/refreshToken for MCP token generation ](https://github.com/hotwax/company/issues/532)
- [Bug: Direct Claude Desktop remote formatter loses Streamable HTTP transport ](https://github.com/pathintegral-institute/mcpm.sh/issues/516)
- [3.5.0 follow-ups: rvf 0.4 migration, upstream ruvllm/router pins, found-not-fixed bugs ](https://github.com/ruvnet/agentdb/issues/46)
- [Bug: Reminder guard appends "I did not schedule a reminder" even after a successful `automations` add (claude-cli / MCP tool path) ](https://github.com/openclaw/openclaw/issues/193958)
- [Bug Agent 记忆超过快照上限后，on-success 写任务一直失败且不重试 ](https://github.com/Ancienttwo/byok-sdk/issues/1474)
- [Bug SSE stream failed: Server-sent event exceeded the 1048576 byte limit ](https://github.com/morluto/rea/issues/9093)
- [bug(mcp): account link flow hides Channel and bot accounts ](https://github.com/OxyHQ/oxy/issues/2184)
- [chore: port the agent harness layout from the current app template ](https://github.com/tomada1114/web-game-template/issues/7)
- [A2A v1.0: implement the real protocol under the A2A* names ](https://github.com/agbossjs/agboss/issues/805)
- [gateway: stopping hermes-gateway.service leaves desktop serve backends alive as PPid-1 orphans holding the profile store (they live outside the unit cgroup) ](https://github.com/NousResearch/hermes-agent/issues/149838)
- [⚙️ AI Infrastructure Digest 2026-11-06 ](https://github.com/kouweizhu/agents-radar/issues/840)
- [⚙️ AI 基础设施日报 2026-11-06 ](https://github.com/kouweizhu/agents-radar/issues/837)
- [⚙️ AI Infrastructure Digest 2026-11-06 ](https://github.com/yueguan/agents-radar/issues/152)
- [CI Monitor Daily Report - 2026-11-06 ](https://github.com/bingxche/sglang-ci-bot/issues/275)
- [Security: Re-setting a guest allowance after clearing it delivered nothing in a test; cause unknown (FR-T17) ](https://github.com/DarkPyonix/darkpyonix-ember/issues/416)
- [MCP first end-to-end run: feedback from driving kube-agents from Claude Code ](https://github.com/gke-labs/kube-agents/issues/4966)
- [Bug Wrong agent card url in 01-features/02-host-your-agent/01-runtime/01-hosting-agents/02-a2a-protocol ](https://github.com/awslabs/agentcore-samples/issues/2276)
- [Test plan: catch harness, approval-routing and docs drift bugs before they reach the examples ](https://github.com/a2aproject/a2a-serve/issues/148)
- [FEATURE Community tool: AgentReader — pay-per-call UK/US/EU company + KYB data for research crews (x402, Base USDC) ](https://github.com/crewAIInc/crewAI/issues/9147)
- [Feature/example: agenti calling AiphaBrainLab CEX Execution Gate ($0.10 x402) as a trading pre-submit check ](https://github.com/nirholas/agenti/issues/216)
- [Spec: Allowance — agent budgets paid through contract-signed x402 payments ](https://github.com/Rahat-ch/allowance/issues/1)
- [spec v2: require the resource server to match accepted against its own accepts before /verify ](https://github.com/x402-foundation/x402/issues/4161)
- [cli: infer web search/fetch --provider rejects valid provider ids with different casing ](https://github.com/openclaw/openclaw/issues/193535)
- [MCP HTTP transport: no supported way to add an application PSR-15 middleware (MiddlewareFactory is final, the controller builds a fixed stack) ](https://github.com/symfony/ai/issues/2883)
- [Store buckets: a rollup's space at a store, kept while its funding wallet covers it ](https://github.com/hpp-io/hpplite/issues/207)
- [Sync: New scrape parameter — key_default_max_age, target_selector, attribution (from #39142) ](https://github.com/RapierCraft/n8n-nodes-alterlab/issues/594)
- [X402 free-first VM: package, validate and stage Drogon API + secure admin (preserve mail services) ](https://github.com/methakon/Madalasa-Alarka/issues/39)
- [🎯 Bounty Alert: 11 New Opportunityies found ](https://github.com/dev-kp-eloper/BountyScout/issues/1725)
- [agent:go: route on three narrow Jev questions instead of one five-level difficulty Score ](https://github.com/MidfieldMafia/cfb-pickem/issues/548)
- [Fix call disconnects: agent drops and webhook ends call for everyone ](https://github.com/avinashankur/meetmind/issues/28)
- [Stripe webhook redelivery credits a deposit twice (WebhookEvent.process_once is not idempotent) ](https://github.com/thiagohrcosta/Kinko-FinancialApp-Monorepo/issues/11)
- [BUG MIssing port in the webhook url ](https://github.com/hatchet-dev/hatchet/issues/5448)
- [mission design: Phase 3 — briefs instead of comments ](https://github.com/tapaskar/archwhere/issues/16)
- [🦞 OpenClaw Ecosystem Digest 2026-11-06 ](https://github.com/kouweizhu/agents-radar/issues/839)
- [🦞 OpenClaw 生态日报 2026-11-06 ](https://github.com/kouweizhu/agents-radar/issues/836)
- [Bug:关于评论问题的若干意见 ](https://github.com/openRin/Rin/issues/586)
- [BugStripe支付EventTypeCheckoutSessionAsyncPaymentFailed处理不完整 ](https://github.com/QuantumNous/new-api/issues/8226)
- [Vibe verification ](https://github.com/yestechgroup/rexlang/issues/137)
- [Sandown Practice 1/2 investigation: kerb strikes and other timing data missing from the application display ](https://github.com/J-Haynes/supercars-timing/issues/43)
- [Bug: `oneOf` makes the virtual-assets v1.0.0 schema dependent on a non-standard `iri-reference` implementation ](https://github.com/stac-extensions/virtual-assets/issues/5)
- [REA-RUST-036: independent replay verifier and conformance oracle for typed claim results ](https://github.com/Luminous-Dynamics/symthaea/issues/10673)
- [Phase FIX / P0 Researcher Feedback & Bugfixes — standing priority lane ](https://github.com/krunchyMonkey/tracing-guatemala-desktop/issues/204)
- [Verify every README.md claim on a real model (GPT-2) and make the README honest ](https://github.com/kapildhinwa2010-dev/fluidtech/issues/19)
- [PBI feat(delivery): milestones hold PBIs and Bugs, Features only when complete, Epics never ](https://github.com/GravionLabs/skills/issues/327)
- [Bug: Android, Galaxy Z Fold7 cover screen: tapping an agent row gives haptic feedback but the chat does not open ](https://github.com/nightly-labs/openbot/issues/5279)
- [Build mode shows a developer camera readout ("cam / tgt / dir" plus a Copy button) to every builder ](https://github.com/RunbotRobot/higglehaven/issues/3219)
- [Feature: Let the Full Control Orchestrator Read the First Message and Propose Its Scope, With the Decision Model Checking Only the Owner's Stated Constraints ](https://github.com/picoduck/wollipog/issues/4282)
- [Bug: Qwen Issue Audit rejects model-proposed canonical labels before Issue repair ](https://github.com/BestNathan/nession/issues/2818)
- [Fireworks key from the environment gets saved to the keychain on Reconnect ](https://github.com/amd/gaia/issues/6803)
- [Opt-in: see and steer remote CAO agents from a local herdr session ](https://github.com/awslabs/cli-agent-orchestrator/issues/1238)
- [Gateway: return 404 for unknown paths instead of 400 invalid_request_body / EPP plain-text 400 ](https://github.com/kaito-project/production-stack/issues/272)
- [bug: Control Center's settings file has a mistake ](https://github.com/projectbluefin/chairlift/issues/731)
- [e2e-scan Test: Improve e2e coverage for portal sync publication lifecycle (expand scenario) ](https://github.com/Kong/kongctl/issues/2727)
- [Seat screen lane: idle-wake premise fails when the last warm click repaints after the observer's first frame ](https://github.com/Derek-X-Wang/wefty/issues/1520)
- [TODAY: FW 13.52 offline exploit discovery sprint, 3 tracks, 4-hour cap ](https://github.com/RuxaXa/ps4rf/issues/17)
- [Todo sort preference silently reverts when its storage write fails ](https://github.com/404-PF/New-Tab/issues/1167)
- [Step "Read this run's pages" of job "Read the docs against the code" in docs-audit.yml fails on main ](https://github.com/phuongnse/axis/issues/3069)
- [CI fast guards is red on main ](https://github.com/manaflow-ai/cmux/issues/36990)
- [QA program: release SOP on mature open-source QA tooling (Founder 2026-11-06) ](https://github.com/jerry200176-png/AllTrue_System/issues/4952)
- [fix(ci): Pin 'All checks passed' required check to the GitHub Actions app in main branch protection ](https://github.com/DankerMu/mindsprout/issues/64)
- [bug(test): `mcp_cli::list_reports_a_connected_server` exits 1 with empty stderr on Windows CI ](https://github.com/misaalanshori/lca/issues/582)
- [Bug: MCP task_list caps an explicit limit at 1000 and returns no total, so a partial store reads as complete ](https://github.com/MrLesk/Backlog.md/issues/1183)
- [Bug: MCP task_list silently omits tasks moved to completed/ or archive/ ](https://github.com/MrLesk/Backlog.md/issues/1182)
- [Bug: MCP task_edit acceptanceCriteriaSet silently truncates an item longer than 500 characters to exactly 500 ](https://github.com/MrLesk/Backlog.md/issues/1179)
- [Bug: MCP task_edit commentsAppend stores only the first ~34 characters of a comment body when commentAuthor is set ](https://github.com/MrLesk/Backlog.md/issues/1177)
- [BugZCode 团队套餐账号刷不出额度:查询只实现了 billing/balance(个人套餐),缺少 mcp/usage 团队路径 ](https://github.com/jlcodes99/cockpit-tools/issues/3026)
- [Bug agent-hook-plugin 的 MCP 代理未注册 rule_search 工具，openviking-rule-search 技能在 ZCode 宿主无法检索规则 ](https://github.com/volcengine/OpenViking/issues/7109)
- [Bug Official MCP Registry API (/v0): DIRECT endpoint remote URL rendered as null://... and official meta.status never populated ](https://github.com/alibaba/nacos/issues/16004)
- [Bug Official MCP Registry API (/v0): MCP server without frontProtocol causes NPE — silently dropped from list, HTTP 500 on versions ](https://github.com/alibaba/nacos/issues/16003)
- [Bug: mcp login stalls after the OAuth callback: an idle browser socket parks the callback listener and the synchronous server.shutdown() with it ](https://github.com/NousResearch/hermes-agent/issues/149771)
- [bug(antigravity): Engram MCP is not active in Antigravity due to ~/.gemini/config/mcp_config.json & plugin path mismatch (also check engram repo) ](https://github.com/Gentleman-Programming/gentle-ai/issues/5988)
- [BUGP1 Resend 403: auditar DNS con MCP de Hostinger y verificar el dominio remitente ](https://github.com/Facudominguez7/Torneo-Mitai/issues/204)
- [BUG Desktop SSH: a host MCP server fails while Desktop is away if claude_desktop_config.json has a server with the same name ](https://github.com/anthropics/claude-code/issues/107761)
