# R43 screening and follow-up coverage

Checked 2026-11-27T05:10:25Z. Search window: created >= 2026-11-24; seven queries, at most ten newest results each. Capped discovery sample, not exhaustive search.

70 retrieved result rows; **63 unique issue URLs**. Three full candidate threads (body, all comments and timeline; each endpoint <100 entries). One completed source-and-test investigation; two exploratory source/PR checks. Other rows are title-level triage only.

## Queries

- `is:issue is:open created:>=2026-11-24 MCP bug -repo:DreamCo-Technologies/Dreamcobots`
- `is:issue is:open created:>=2026-11-24 A2A bug -repo:DreamCo-Technologies/Dreamcobots`
- `is:issue is:open created:>=2026-11-24 x402 bug -repo:DreamCo-Technologies/Dreamcobots`
- `is:issue is:open created:>=2026-11-24 API authentication bug -repo:DreamCo-Technologies/Dreamcobots`
- `is:issue is:open created:>=2026-11-24 webhook bug -repo:DreamCo-Technologies/Dreamcobots`
- `is:issue is:open created:>=2026-11-24 JSON schema bug -repo:DreamCo-Technologies/Dreamcobots`
- `is:issue is:open created:>=2026-11-24 "GitHub Actions" bug -repo:DreamCo-Technologies/Dreamcobots`

## Distinct results

| Issue | Title | Disposition/depth |
|---|---|---|
| [MisakaNet/issues/5861](https://github.com/Ikalus1988/MisakaNet/issues/5861) | [Intake] Problem 仓库 .gitignore 为「厂商数据不入库」政策加了全局 glob（如 `*-3d.def`）后，tests/fixtures/ 下的**合 | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [boss-agent-cli/issues/3013](https://github.com/can4hou6joeng4/boss-agent-cli/issues/3013) | [Bug] MCP boss_wizard 对 status/stop 强制执行 --timeout，CLI 却忽略；宿主还静默封顶 900s | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [nexo-cli/issues/65](https://github.com/winning-sales-nexus/nexo-cli/issues/65) | [BUG] nexo connect push não mostra o campo do manifesto recusado (meta.issues) | Title screening; PR69 independently covers meta.issues diagnostics. No separate full investigation. |
| [nexo-cli/issues/63](https://github.com/winning-sales-nexus/nexo-cli/issues/63) | [BUG] nexo connect quarantine reprocess responde 400: a prévia vai sem corpo | Full thread + merged PR69 diff; body:{} already implemented. No duplicate. |
| [clowder-ai/issues/2111](https://github.com/zts212653/clowder-ai/issues/2111) | Bug: ACP 凭据停止清理、恢复隔离与失败原子性后续（#2105） | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [openbot/issues/17650](https://github.com/nightly-labs/openbot/issues/17650) | [Bug]: Adding Paper with the plus button reports a missing local executable | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [agents-radar/issues/1158](https://github.com/kouweizhu/agents-radar/issues/1158) | ⚙️ AI Infrastructure Digest 2026-11-27 | Title-level exclusion: digest/aggregation, not an original reproducible bug. |
| [agents-radar/issues/1157](https://github.com/kouweizhu/agents-radar/issues/1157) | 🦞 OpenClaw Ecosystem Digest 2026-11-27 | Title-level exclusion: digest/aggregation, not an original reproducible bug. |
| [agents-radar/issues/1156](https://github.com/kouweizhu/agents-radar/issues/1156) | 📊 AI CLI Tools Digest 2026-11-27 | Title-level exclusion: digest/aggregation, not an original reproducible bug. |
| [agents-radar/issues/1155](https://github.com/kouweizhu/agents-radar/issues/1155) | ⚙️ AI 基础设施日报 2026-11-27 | Title-level exclusion: digest/aggregation, not an original reproducible bug. |
| [OmniRoute/issues/21401](https://github.com/cheaper-inference/OmniRoute/issues/21401) | feat(arch): incremental Rust migration for OmniRoute's hot data plane (compression, open-sse & routing) to solve 8–12 GB V8 memory & latency ceilings | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [big_model_radar/issues/766](https://github.com/litang9/big_model_radar/issues/766) | 📊 AI CLI 工具社区动态日报 2026-11-27 | Title-level exclusion: digest/aggregation, not an original reproducible bug. |
| [huaweicloud-devkit/issues/1182](https://github.com/huaweicloud/huaweicloud-devkit/issues/1182) | [Docs] 修正 ECS 删除指引：按挂载策略确认 EIP 和云硬盘去留 | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [agentiplex/issues/21](https://github.com/tbrandenburg/agentiplex/issues/21) | [P3][wait-until] Groom: wait_deliveries and watch/wake events (observer pattern) for coordinators | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [agent-gossip/issues/95](https://github.com/agent-habilis/agent-gossip/issues/95) | Tasks stall silently: 5 stalls cost about 4 hours in a 6-agent team | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [hermes-agent/issues/160508](https://github.com/NousResearch/hermes-agent/issues/160508) | [Bug]: A2A shows "Needs setup" forever — plugin is_connected() ignores PlatformConfig.enabled and needs A2A_PORT | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [AI-PDLC/issues/177](https://github.com/eitri-edd/AI-PDLC/issues/177) | [Tech Radar] High-priority emerging agent products: governance, managed agents, workflows and MCP security | Title-level exclusion: digest/aggregation, not an original reproducible bug. |
| [bifrost/issues/10558](https://github.com/maximhq/bifrost/issues/10558) | [Bug]: Data race in Bootstrap: the push relay reads TracingMiddleware before Bootstrap sets it | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [salesagent/issues/2734](https://github.com/prebid/salesagent/issues/2734) | RFC: admin panel architecture — one authorization seat, one tenant address, one write path per entity | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [ag-ui/issues/3485](https://github.com/ag-ui-protocol/ag-ui/issues/3485) | [Bug]: @ag-ui/mastra: durable agent run hangs at a tool suspension (stream() needs closeOnSuspend: true) | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [aih-scan/issues/203](https://github.com/samartomar/aih-scan/issues/203) | Complete inspection for the 98 pending Catalog versions | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [obolus/issues/148](https://github.com/geekinasuit/obolus/issues/148) | Payment-keyed idempotency cache for retried and concurrent settles | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [ontario-address-changes/issues/94](https://github.com/skfd/ontario-address-changes/issues/94) | windsor 2026-11-26 — mass-modified: Legal1, Zoning, full, street, street_suffix (+4 more) | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [x402/issues/4453](https://github.com/x402-foundation/x402/issues/4453) | [Bug]: Stellar exact client cannot sign for a contract account with its own signature value | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [brain/issues/600](https://github.com/teenydroid/brain/issues/600) | [fence-proposal] carve the attest grading endpoint out of the wallet freeze | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [scaffold-eth-2/issues/1351](https://github.com/scaffold-eth/scaffold-eth-2/issues/1351) | create-eth v3.0: single-repo switch, ETHSkills, and our agent-friendly direction | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [x402/issues/4437](https://github.com/x402-foundation/x402/issues/4437) | [Bug]: SVM exact: Phantom adds a Lighthouse assertion on the facilitator's fee payer, so Phantom payments fail verify (fee_payer_transferring_funds) | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [reddi-agent-protocol/issues/1172](https://github.com/nissan/reddi-agent-protocol/issues/1172) | [Epic] V1 feature freeze: close these gaps, then code freeze at the release commit | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [Haven-AI/issues/5087](https://github.com/d-hinders/Haven-AI/issues/5087) | Epic: selling from your own MCP server — buyer fixes and guide now, a ready-made seller package later (parked) | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [agents-radar/issues/1153](https://github.com/kouweizhu/agents-radar/issues/1153) | 📊 AI CLI 工具社区动态日报 2026-11-27 | Title-level exclusion: digest/aggregation, not an original reproducible bug. |
| [agents-radar/issues/546](https://github.com/yaojiejia/agents-radar/issues/546) | 📡 AI Ecosystem Digest 2026-11-27 | Title-level exclusion: digest/aggregation, not an original reproducible bug. |
| [agents-radar/issues/4504](https://github.com/duanyytop/agents-radar/issues/4504) | 🦞 OpenClaw Ecosystem Digest 2026-11-27 | Title-level exclusion: digest/aggregation, not an original reproducible bug. |
| [agents-radar/issues/4503](https://github.com/duanyytop/agents-radar/issues/4503) | 📊 AI CLI Tools Digest 2026-11-27 | Title-level exclusion: digest/aggregation, not an original reproducible bug. |
| [agents-radar/issues/4501](https://github.com/duanyytop/agents-radar/issues/4501) | 🦞 OpenClaw 生态日报 2026-11-27 | Title-level exclusion: digest/aggregation, not an original reproducible bug. |
| [news/issues/77555](https://github.com/SecOpsNews/news/issues/77555) | [RegisterSec] Free e-government platform that serves two billion people in ten countries has critical SQL injection bug | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [GoLiveBypass/issues/478](https://github.com/bezumiya/GoLiveBypass/issues/478) | conta n entra no app | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [open5gs/issues/5136](https://github.com/open5gs/open5gs/issues/5136) | [Bug]: PCF double-free in `clear_ipv4addr()`/`clear_ipv6prefix()` when an SM Policy update supplies an invalid address after a valid one (v2.8.0 and main) | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [ha-mcp/issues/3221](https://github.com/homeassistant-ai/ha-mcp/issues/3221) | [BUG] Embedded server calls Supervisor REST /addons with Core's SUPERVISOR_TOKEN, raising the "Deprecated use of the Supervisor API token" repair (breaks 2027.6.0) | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [openclaw/issues/206320](https://github.com/openclaw/openclaw/issues/206320) | [Bug]: Since 2026.11.10, Codex threads on OpenClaw's base prompt ignore a workspace rule to finish every item, and long cron jobs stop early | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [agents-radar/issues/1154](https://github.com/kouweizhu/agents-radar/issues/1154) | 🦞 OpenClaw 生态日报 2026-11-27 | Title-level exclusion: digest/aggregation, not an original reproducible bug. |
| [gh-aw/issues/81544](https://github.com/github/gh-aw/issues/81544) | [github-docs-seo] Daily Docs SEO baseline: Agentic Workflows discoverability gaps | Title-level exclusion: digest/aggregation, not an original reproducible bug. |
| [WorkSphere/issues/10735](https://github.com/SatyamPandey-07/WorkSphere/issues/10735) | bug(webhooks): prevent concurrent Svix retries from bypassing inbox deduplication | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [laravel-autobuilder/issues/72](https://github.com/Grazulex/laravel-autobuilder/issues/72) | Bug: triggers are not registered in console processes (queue workers, commands, scheduler) | Full thread + two source files; author already identifies guard/fix. No additive tested repair; no draft. |
| [magicui/issues/1104](https://github.com/magicuidesign/magicui/issues/1104) | [bug]: POST /api/blog-webhook accepts `Bearer undefined` when BLOG_WEBHOOK_ACCESS_TOKEN is unset | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [down-the-stack/issues/9](https://github.com/tyevco/down-the-stack/issues/9) | Idea: Backlog tickets and Regressions: named floors, borrowed zone palettes, old bosses reopened | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [agents-radar/issues/3459](https://github.com/leisure3318/agents-radar/issues/3459) | 🦞 OpenClaw 生态日报 2026-11-27 | Title-level exclusion: digest/aggregation, not an original reproducible bug. |
| [big_model_radar/issues/163](https://github.com/huajiao1998/big_model_radar/issues/163) | 🦞 OpenClaw 生态日报 2026-11-27 | Title-level exclusion: digest/aggregation, not an original reproducible bug. |
| [tasirin-vaultwarden-host/issues/2997](https://github.com/tasirin1/tasirin-vaultwarden-host/issues/2997) | [audit] Laporan audit putaran 10 — 17 temuan baru (#2980-#2996), 3 Sedang + 14 Rendah | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [jbook/issues/2](https://github.com/MI1309/jbook/issues/2) | tugas | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [healthwatch-ms/issues/215](https://github.com/kabnpy/healthwatch-ms/issues/215) | Spec: Architecture Deepening (Wave 2) — Agency Dashboard, Client Ledger, Policy Detail, and Advisory Rating | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [aihub/issues/312](https://github.com/MyDataIntelligence/aihub/issues/312) | Team settings: team show/validate/preview/edit/init and aihub.bar.team* commands | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [env-saaf/issues/494](https://github.com/abhi478jeetur-rgb/env-saaf/issues/494) | Bug: `check --values` silently ignores keys not in the schema | Full thread + pinned source + paired CLI tests; selected R43-01. |
| [sglang-omni/issues/4719](https://github.com/sgl-project/sglang-omni/issues/4719) | [Bug] [Realtime] response.done usage uses chat-completions fields instead of the Realtime usage schema | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [buddy/issues/137](https://github.com/kimipsen/buddy/issues/137) | [Bug] Backend mutation testing crashes on .NET 11: Stryker can't load System.Runtime 11.0.0.0 | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [maui/issues/40688](https://github.com/dotnet/maui/issues/40688) | FadeToAsync and other *ToAsync methods: a token cancelled off the UI thread aborts the next animation of the same kind on that view | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [vermeer-text/issues/214](https://github.com/POPAISTUDIO/vermeer-text/issues/214) | 🔴 Canary providers KO — 2026-11-27 | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [todo-lab/issues/1](https://github.com/cstpeace0191/todo-lab/issues/1) | [CI] GitHub Actions CI 추가 | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [pipelines/issues/15991](https://github.com/kubeflow/pipelines/issues/15991) | bug(sdk): local runner fails in dsl.ParallelFor when iterating over NamedTuple, OneOf, or nested dict-subvar outputs | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [AgenVe2/issues/1](https://github.com/marjhonie-siasol/AgenVe2/issues/1) | ci: add GitHub Actions CI, Dependabot, and PR/Issue templates | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [plate/issues/1525](https://github.com/akasper/plate/issues/1525) | [Bug]: tag-release-merge finds 0 release artifacts when the Release PR is merged with a merge commit | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [qwen-code/issues/18495](https://github.com/QwenLM/qwen-code/issues/18495) | deflake: packages/web-shell/client/e2e/web-shell.standalone.spec.ts › lists a new standalone session before its first turn finishes from the composer @smoke | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [maui/issues/40686](https://github.com/dotnet/maui/issues/40686) | [iOS, Mac Catalyst] NavigationPage raises NavigatedTo before Loaded on non-animated PushAsync/PopAsync (.NET MAUI 11 regression) | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |
| [ci/issues/164](https://github.com/jbhirsh/ci/issues/164) | Replace the fixed-time waits in the GIF tool and the pictures route with events | Title-level triage only; not advanced. No root cause, fix or resolution asserted. |

## Existing follow-ups

Read all **56** tracked issue/PR issue-comments endpoints and issue states; all comment lists <100 entries. Also read combined review/inline comments for four tracked PR threads. No new comment after saved cursors, no state changes, no new confirmed repairs or explicit commercial requests. Prior replies are not reannounced. Cursors stay unchanged; checked timestamps advance.

- https://github.com/cyanheads/musicbrainz-mcp-server/issues/21 — no new comment after stored cursor 6148454351.
- https://github.com/wbskt/Wbskt/issues/293 — no new comment after stored cursor 6140314655.
- https://github.com/abi83/prepify/issues/279 — no new comment after stored cursor 6093268389.
- https://github.com/logly/mureo/issues/807 — no new comment after stored cursor 6050810750.
- https://github.com/scaffold-studio-hq/scaffold-studio-mcp/issues/68 — no new comment after stored cursor 6051654617.
- https://github.com/api-evangelist/roadmap/issues/938 — no new comment after stored cursor 6834033166.
- https://github.com/parisbs/codex-subagent-mcp/issues/143 — no new comment after stored cursor 6201356227.
- https://github.com/HuginnIndustries/CodeCartographer/issues/463 — no new comment after stored cursor 6050883458.
- https://github.com/web3insight-ai/web3insight/issues/32 — no new comment after stored cursor 5797651890.
- https://github.com/LumenRoute/lumenbazaar-frontend/issues/8 — no new comment after stored cursor 6195420882.
- https://github.com/microsoft/vscode/issues/341683 — no new comment after stored cursor 6184978396.
- https://github.com/a2aproject/a2a-python/issues/1341 — no new comment after stored cursor 6274826969.
- https://github.com/Abilityai/trinity/issues/3749 — no new comment after stored cursor 6186662739.
- https://github.com/agnt-gg/agnt/issues/169 — no new comment after stored cursor 6735706097.
- https://github.com/owasp-noir/noir/issues/3078 — no new comment after stored cursor 6228187553.
- https://github.com/Gentleman-Programming/engram/issues/1899 — no new comment after stored cursor 6221741562.
- https://github.com/MementoRC/mcp-git/issues/298 — no new comment after stored cursor 6209070203.
- https://github.com/huiliyi37/Tianshu-harness/issues/507 — no new comment after stored cursor 6230037956.
- https://github.com/reeenatamc/wp-content-agent/issues/6 — no new comment after stored cursor 6246051674.
- https://github.com/opena2a-org/agent-identity-management/issues/772 — no new comment after stored cursor 6246052455.
- https://github.com/Danathar/tududi/issues/263 — no new comment after stored cursor 6246053246.
- https://github.com/ktysne/agent-cockpit/issues/564 — no new comment after stored cursor none.
- https://github.com/bergbacher/hyde-mcp-gateway/issues/34 — no new comment after stored cursor 6260256914.
- https://github.com/recursive-cloud/woodhouse/issues/29 — no new comment after stored cursor 6283913029.
- https://github.com/gitroomhq/postiz-app/issues/2300 — no new comment after stored cursor 6308625082.
- https://github.com/talyssonoliver/IntelliFlow-CRM/issues/940 — no new comment after stored cursor 6308670609.
- https://github.com/janowoc/northplan/issues/100 — no new comment after stored cursor none.
- https://github.com/casdoor/casdoor/issues/5957 — no new comment after stored cursor 6362808135.
- https://github.com/volcengine/OpenViking/issues/6471 — no new comment after stored cursor 7002017251.
- https://github.com/agentscope-ai/QwenPaw/issues/8424 — no new comment after stored cursor 6552861498.
- https://github.com/f4exb/sdrangel/issues/3039 — no new comment after stored cursor 6427656486.
- https://github.com/wevm/mppx/issues/1113 — no new comment after stored cursor 6434639013.
- https://github.com/paoloamato2/fortinet-mcp-server/issues/5 — no new comment after stored cursor 6461200657.
- https://github.com/wevm/mppx/pull/1133 — no new comment after stored cursor 6515624633.
- https://github.com/codercops/discord-bot/issues/118 — no new comment after stored cursor 6539924670.
- https://github.com/mikeknight85/PriceStalker/issues/268 — no new comment after stored cursor none.
- https://github.com/mikeknight85/PriceStalker/pull/269 — no new comment after stored cursor 6569547936.
- https://github.com/WeatherXM/wg1200-firmware/issues/2 — no new comment after stored cursor 6955833500.
- https://github.com/langfuse/langfuse/issues/19594 — no new comment after stored cursor 6592837310.
- https://github.com/langfuse/langfuse/pull/19595 — no new comment after stored cursor 6660209061.
- https://github.com/apache/skywalking/issues/14194 — no new comment after stored cursor none.
- https://github.com/apache/skywalking-banyandb/pull/1460 — no new comment after stored cursor 6729639145.
- https://github.com/mlorentedev/pdf-modifier/issues/232 — no new comment after stored cursor 6650352332.
- https://github.com/MrLesk/Backlog.md/issues/1179 — no new comment after stored cursor 6694189099.
- https://github.com/shpaw415/open-bot/issues/80 — no new comment after stored cursor 6758118327.
- https://github.com/nightly-labs/openbot/issues/7357 — no new comment after stored cursor 7176163364.
- https://github.com/davidmosiah/withings-mcp/issues/31 — no new comment after stored cursor none.
- https://github.com/weyucou/wyc6k-task-runner/issues/83 — no new comment after stored cursor 6840233542.
- https://github.com/microsoft/apm/issues/3711 — no new comment after stored cursor 6951326074.
- https://github.com/aws-samples/sample-spec-driven-presentation-maker/issues/665 — no new comment after stored cursor 7031098102.
- https://github.com/modelcontextprotocol/servers/issues/5641 — no new comment after stored cursor 7150180799.
- https://github.com/handi7/lontar-cms/issues/452 — no new comment after stored cursor none.
- https://github.com/GoodOlClint/CrossTalk/issues/243 — no new comment after stored cursor none.
- https://github.com/publira/publira/issues/5943 — no new comment after stored cursor none.
- https://github.com/Mag1cFall/Antigravity2API/issues/11 — no new comment after stored cursor 7157796113.
- https://github.com/KhubaibQaiser/fitness-app/issues/131 — no new comment after stored cursor none.

## Candidate PR checks

- env-saaf: latest30 PR summaries; query494 returns0; open-PR query returns one (#488), whose files are CHANGELOG.md/index.js/test.js and concern scanner parameter defaults. Query values read30 results (capped); historical #384/#410 introduction read, #400 closed without merge. No #494 fix found in this bounded search; timeline has labels only and0comments. Main stayed at 0b9a97dcb87badf5d198314df0617e716a34214b on recheck.
- Laravel AutoBuilder: latest30 PR summaries, full timeline has #70 issue reference; no linked repair PR. Provider and manager source at 90d60615a35dccec687d4ccebcf3d20b88abc7c7 confirm the author's console guard diagnosis. No Laravel test/runtime executed.
- Nexo: PR69 is merged; exact diff adds body:{} to quarantineReprocess, with a preview-body assertion. Head 00d870a6c7fa84dd4d10fc20e509b8f1540d2be8. Upstream reported tests not rerun or represented as ours.
