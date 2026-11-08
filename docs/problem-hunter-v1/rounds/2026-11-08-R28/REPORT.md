# R28 — 2026-11-08: bounded discovery and duplicate suppression

Checked at 2026-11-08T05:01:34Z; repository base 1385593908330d6333b1263f294cb522de35205a. Prior radar, README, ledger and R27 report retrieved before discovery. No previous outcome is presented as new.

## Counts
70 capped search results; 65 distinct URLs initially screened; 5 candidate bodies/comments/timelines read; 2 exploratory source inspections; 0 new completed engineering investigations; 5 isolated comprehension test groups passed; 0 upstream/public-API suites; 0 English drafts; 0 external comments/PRs/messages.

44 saved discussion threads checked, including all comment pages. Four tracked PR review and inline-comment streams checked. No new comment after saved cursors, no state changes, no new review, and no explicit commercial request observed. Existing comment IDs retained; last_checked timestamps advanced.

Discovery: seven newest-first searches, ten results each, using is:issue is:open <keyword> bug created:>=2026-11-05 with MCP, A2A, x402, webhook, schema, API and "GitHub Actions". This is not an exhaustive search.

## Five candidate decisions (not five ready fixes)
### 1. [assistant-ui/assistant-ui/issues/10396](https://github.com/assistant-ui/assistant-ui/issues/10396)
Reporter: Elon-Jiang; created 2026-11-08T04:27:58Z.

Existing open PR #10397 canonicalizes protocol header names and includes HTTP regression coverage. Source confirms the original case-sensitive spread. No additive reply; PR tests not rerun.

### 2. [aibtcdev/aibtc-mcp-server/issues/760](https://github.com/aibtcdev/aibtc-mcp-server/issues/760)
Reporter: secret-mars; created 2026-11-07T08:58:33Z.

Existing open PR #762 implements exact canonical asset matching; contributor has claimed the fix. No signing/payment test performed; do not duplicate the diagnosis.

### 3. [honua-io/geospatial-mcp/issues/186](https://github.com/honua-io/geospatial-mcp/issues/186)
Reporter: mikemcdougall; created 2026-11-08T04:51:56Z.

Maintainer has already claimed the coordinated serviceLayerIndex contract repair and specified schema/fixture scope. No independent source investigation completed.

### 4. [Arize-ai/phoenix/issues/17742](https://github.com/Arize-ai/phoenix/issues/17742)
Reporter: Jacqueline122; created 2026-11-08T04:59:17Z.

Source-extracted auto-detection comprehension reproduces AttributeError for int/tuple/None labels; five isolated groups verify the already-reported isinstance guard. Reporter already has the same fix and wider tests, so no duplicate reply. No pandas/public API or full-suite execution.

### 5. [vllm-project/vllm/issues/66351](https://github.com/vllm-project/vllm/issues/66351)
Reporter: SohamDutta02; created 2026-11-08T04:53:21Z.

Reporter already identifies the streaming status/error gap and proposes terminal failure handling coordinated with PRs #62789, #49721 and #65213. Those PRs were read; no independent runtime/source investigation completed for this issue.


## Source evidence and verification limits
- [assistant-ui/assistant-ui: packages/react-a2a/src/A2AClient.ts](https://github.com/assistant-ui/assistant-ui/blob/eb65bd4558b769550093003c95e5867ad0ec8eba/packages/react-a2a/src/A2AClient.ts); commit eb65bd4558b769550093003c95e5867ad0ec8eba; blob 72eb8fa0826cf7b26343f6bcb974445610dc694f.
- [Arize-ai/phoenix: packages/phoenix-evals/src/phoenix/evals/utils.py](https://github.com/Arize-ai/phoenix/blob/464a60fd3c24aaed780cea3f2e0e437d3c8ba037/packages/phoenix-evals/src/phoenix/evals/utils.py); commit 464a60fd3c24aaed780cea3f2e0e437d3c8ba037; blob 9dd797daf113206c1f73837ee55aa57c9920c868.

Assistant-ui: original getHeaders spreads case-sensitive custom keys beside canonical keys. High confidence in static duplicate-key mechanism; native HTTP execution was not repeated. Existing PR #10397, head 7a7fde6c1e5c44a58b4d4f7f4e5d97e286878f4b, already canonicalizes the four protocol header names and adds HTTP tests. Its comments and three patches were retrieved. Repeating its fix/test matrix has low additional value.

Phoenix: auto-detection calls col.endswith on all labels. High confidence for the isolated expression failure. Guarding with isinstance(col, str) preserves score order in our controls, but this was already proposed with broader regression coverage by the reporter. The open-PR inventory read was capped at 100 and is not exhaustive; no claim that no PR exists is made.

## Linked fixes read
- [assistant-ui/assistant-ui/pulls/10397](https://github.com/assistant-ui/assistant-ui/pull/10397): open, head 7a7fde6c1e5c44a58b4d4f7f4e5d97e286878f4b; body, discussion and changed-file patches retrieved.
- [aibtcdev/aibtc-mcp-server/pulls/762](https://github.com/aibtcdev/aibtc-mcp-server/pull/762): open, head 5d9ec790201224ccf982366613d34faba30c926c; body, discussion and changed-file patches retrieved.
- [vllm-project/vllm/pulls/62789](https://github.com/vllm-project/vllm/pull/62789): open, head a6d7a36b6653a5ff2191ca6b9aceed934bb5d964; body, discussion and changed-file patches retrieved.
- [vllm-project/vllm/pulls/49721](https://github.com/vllm-project/vllm/pull/49721): open, head ce13ddc80bc7372980f959e90de3d2c6a8473958; body, discussion and changed-file patches retrieved.
- [vllm-project/vllm/pulls/65213](https://github.com/vllm-project/vllm/pull/65213): open, head d842d0482c2fc75a223e1351a24cacb59e16767d; body, discussion and changed-file patches retrieved.

Existing x402 and vLLM proposals are credited to their authors. No actual payment, wallet, credential, GPU/model call or deployment was used. No upstream test result is claimed as our own.

## Drafts and next step
No new English comment warrants approval this round. No external publication was attempted. Do not repost old drafts. No NAIF tool is recommended for these cases, so no fresh tool-page validation or fit is claimed. No paid service or commercial lead is inferred.

The limits are already-proposed fixes, active author work, incomplete runtime investigation and capped discovery. No user action is needed. Revisit only if a material new development makes an additive contribution possible.

## Write controls
Complete tree is not truncated; only root AGENTS.md applies. Its unrelated bounty/wallet instructions do not change this task's permissions. All eight workflow triggers inspected at the base SHA: docs-only updates do not match push path filters. No workflow changed/dispatched. Only README, ledger and this round's REPORT/TESTS documentation are written, atomically with a fresh expected-head check. Prior ledger history and comment cursors preserved.

## Initial screening inventory
These are search candidates, not independently confirmed diagnoses; prior entries, digests, ads, plans and unrelated bugs are not promoted to full investigation.
1. [fix(schemas): distinguish service layer indexes from storage ids](https://github.com/honua-io/geospatial-mcp/issues/186)
2. [ Bug : 插件市场解锁失效2](https://github.com/BigPizzaV3/CodexPlusPlus/issues/2985)
3. [ Bug : 自定义连接健康检查误报及 connectionKey / connectorId 定位不一致](https://github.com/duhu2000/dsh-mcp-connector/issues/218)
4. [bug: Codex MCP registration fails - CONFIG_WRITE_REFUSED](https://github.com/Hao0321/Editkin/issues/113)
5. [Exercise: Integrate MCP with Copilot](https://github.com/richardw2021/skills-integrate-mcp-with-copilot/issues/1)
6. [Preserve startup deadline evidence through partial SDK entry cleanup](https://github.com/KestrelSovereignAI/kestrel-feature-mcp/issues/52)
7. [ Bug : agy acp: sessions under a custom agent no longer offer or run /compact (regression since 1.5.2)](https://github.com/google-antigravity/antigravity-cli/issues/1472)
8. [AgentKit feedback: ak update failed: engineer](https://github.com/bestagentkits/agentkit-support/issues/561)
9. [Spec: 0.6.0, measure and trim](https://github.com/Aceotopes/brigade/issues/11)
10. [MCP equipment: disclose equipped-weapon Battle support before encounter commitment](https://github.com/dearlordylord/5e-quint/issues/619)
11. [ Bug : A2A protocol headers duplicate their values when custom names use another casing](https://github.com/assistant-ui/assistant-ui/issues/10396)
12. [📡 AI Ecosystem Digest 2026-11-08](https://github.com/yaojiejia/agents-radar/issues/440)
13. [Triage unverified bug candidates from the 2026-11-07 swarm audit experiment](https://github.com/Castrozan/.dotfiles/issues/258)
14. [⚙️ AI Infrastructure Digest 2026-11-08](https://github.com/HuggerHustle/ai-radar/issues/183)
15. [ CI Monitor  Daily Report - 2026-11-08](https://github.com/bingxche/sglang-ci-bot/issues/278)
16. [Tracker: Move the laptop data plane to Praxis when the upstream gaps close](https://github.com/rossoctl/cortex/issues/1714)
17. [ BUG  Workspace-bound task brief skips pending A2A reply delivery](https://github.com/kckylechen1/Tachi/issues/2231)
18. [ Test  Bespoke gateway spawners predate the harness rules: bare Child without GatewayChildGuard (#4991), SIGKILL teardown that loses coverage profiles, kernel-ephemeral handoff ports, and secrets_functional's startup smoke](https://github.com/ferrum-edge/ferrum-edge/issues/7077)
19. [Daily research 2026-11-08](https://github.com/esengine/DeepSeek-Reasonix/issues/15010)
20. [tool_trajectory_avg_score fails for confirmation-gated tools because the framework adk_request_confirmation call is counted as an agent tool call](https://github.com/google/adk-python/issues/8025)
21. [x402: any '*.sbtc-token' asset is treated as sBTC and paid in the canonical contract](https://github.com/aibtcdev/aibtc-mcp-server/issues/760)
22. [Cross-link idea: sanctions screen / non-JP KYB as the step after jp_supplier_resolve (both x402 on Base)](https://github.com/japanverify/jpverify-mcp/issues/1)
23. [Grant readiness gate: complete technical, legal, and external validation prerequisites](https://github.com/itswork-app/aivoguard/issues/2)
24. [End-to-end suite over every flow, with artifacts](https://github.com/ss251/countersign/issues/39)
25. [ FEATURE  Community tool: AgentReader — pay-per-call UK/US/EU company + KYB data for research crews (x402, Base USDC)](https://github.com/crewAIInc/crewAI/issues/9147)
26. [Feature/example: agenti calling AiphaBrainLab CEX Execution Gate ($0.10 x402) as a trading pre-submit check](https://github.com/nirholas/agenti/issues/216)
27. [Spec: Allowance — agent budgets paid through contract-signed x402 payments](https://github.com/Rahat-ch/allowance/issues/1)
28. [spec v2: require the resource server to match accepted against its own accepts   before /verify](https://github.com/x402-foundation/x402/issues/4161)
29. [cli: infer web search/fetch --provider rejects valid provider ids with different casing](https://github.com/openclaw/openclaw/issues/193535)
30. [MCP HTTP transport: no supported way to add an application PSR-15 middleware (MiddlewareFactory is final, the controller builds a fixed stack)](https://github.com/symfony/ai/issues/2883)
31. [Spec: move Clerk from Next.js on Vercel to Remix 3 and self-hosted Eve behind a Cloudflare Tunnel](https://github.com/rymanacevedo/business-wiki-agent/issues/134)
32. [Devaro review fight: live findings, challenges and verdicts](https://github.com/amsinghnavdeep/god/issues/9)
33. [Unused helpers include a reconcile keep-list the code no longer uses](https://github.com/krzysztofbury/virgil/issues/214)
34. [tech-debt: saved-search alerts — turning job-alert email off still mails the pending digest](https://github.com/strelov1/freehire/issues/4284)
35. [Weekly sweep 2026-11-08 — Email templates & senders](https://github.com/wavespestcontrolfl/waves-customer-portal/issues/7765)
36. [🦞 OpenClaw 生态日报 2026-11-08](https://github.com/leisure3318/agents-radar/issues/3158)
37. [ Bug : S3 objects from previous storage use not detected as orphans](https://github.com/nextcloud/server/issues/66476)
38. [Acquire immutable provenance for the historical preview Postgres image](https://github.com/chase-sets/chase-sets/issues/11157)
39. [Audit: Security Hardening, Generic EPay (Xiaodou/Caihong) & Multi-USDT Gateway, Checkout Input Bug, Bot Mitigation, and Chat UX](https://github.com/arifulcrypto/24goods-web/issues/25)
40. [🦞 OpenClaw Ecosystem Digest 2026-11-08](https://github.com/kouweizhu/agents-radar/issues/869)
41. [bug: re-indexing an edited knowledge branch retains stale passages and duplicate source URIs](https://github.com/dovvnloading/Graphlink/issues/496)
42. [ PBI  feat: github-milestone assign mode enforces the milestone rule](https://github.com/GravionLabs/skills/issues/439)
43. [bug: 🐛 Token refresh rejected (HTTP 400, gateway 10201) 3–4 days after QR login, well before the ~7-day boundary](https://github.com/kongesque/line-cli/issues/29)
44. [bug(admin): scope cache keepalive summary aggregate to horizon and renewal evidence](https://github.com/isac322/cc-lb/issues/1124)
45. [bug(storage): filter and prune unmatched cache_keepalive_evidence follow-up rows](https://github.com/isac322/cc-lb/issues/1123)
46. [sqlite3_deserialize of non-database bytes fails at once; stock accepts it and reports NOTADB on first use](https://github.com/dolthub/doltlite/issues/4706)
47. [Backup restore must validate everything it accepts and refresh dependent views](https://github.com/inhesrom/openbiblesoftware/issues/258)
48. [ Bug  dsh 0.2.2-rc.1：插件激活后 web boot 失败（client 入口缺 dsh-client-runtime/client 模块表条目）](https://github.com/FSMargoo/dsh-at-file/issues/48)
49. [ BUG : to_annotation_dataframe fails on unrelated non-string column names](https://github.com/Arize-ai/phoenix/issues/17742)
50. [Build stopped at 98% @@error build.py stopped: clang-23: error: clang frontend command failed due to signal (use -v to see invocation)](https://github.com/NotRexed/Hookshot/issues/476)
51. [bug: deleteChatNode accepts non-chat node IDs and bypasses node-specific cleanup](https://github.com/dovvnloading/Graphlink/issues/497)
52. [ Bug : OpenCode background shells aren't pending work: the thread looks finished, Stop and restart recovery miss them](https://github.com/pingdotgg/t3code/issues/32829)
53. [ Bug  DeepSeek 超长历史图片导致后续请求持续 400，Coopanion 未做请求侧兼容](https://github.com/Pal-AI-Lab/Coopanion/issues/653)
54. [Bug: the Insights 12-month load-time e2e test fails on CI runners](https://github.com/streetlampsalad/calories-counter/issues/134)
55. [ Bug : Background /v1/responses requests that fail during generation stay "queued" forever (streaming case not covered by open PRs)](https://github.com/vllm-project/vllm/issues/66351)
56. [fix(store): LLM レビューの一時失敗が reasoning 軸の下落として回帰検出される](https://github.com/flipslidersand-labs/safecode-arena/issues/228)
57. [ PBI  feat: issue conventions check the milestone rule on milestoned/demilestoned](https://github.com/GravionLabs/ci/issues/199)
58. [bug: Error message without telling me how to resolve it](https://github.com/projectbluefin/chairlift/issues/738)
59. [Runner label starved: glaeda-ios-sim+glaeda-std-xcode-26.6](https://github.com/manaflow-ai/cmux/issues/38232)
60. [bug(benchmark): mock service startup uses a fork callback in the threaded runner](https://github.com/agentic-os-org/ANOLISA/issues/9698)
61. [ Bug  Crash app in landscape](https://github.com/deniscerri/ytdlnis/issues/1485)
62. [fix(deps): web の npm 依存の脆弱性 14 件を直し週次の npm audit を green にする](https://github.com/taito-station/paddock/issues/826)
63. [Track PR #155: Bump github/codeql-action/analyze from 4.39.1 to 4.39.3](https://github.com/martinslavov/rcas/issues/158)
64. [Track PR #154: Bump github/codeql-action/init from 4.39.1 to 4.39.3](https://github.com/martinslavov/rcas/issues/157)
65. [fix(deps): cargo の依存の脆弱性 20 件を直し週次の cargo audit を green にする](https://github.com/taito-station/paddock/issues/825)
