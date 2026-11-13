# R33 — Screening and evidence

Checked 2026-11-13T04:59:46Z. Queries: `is:issue is:open created:>=2026-11-10 <topic>`, topics MCP, A2A, x402, webhook, schema, API, "GitHub Actions"; created descending, top10 each. 70 results /69 unique. Prior radar, README, ledger and R32 report read first. Candidate threads include full comments and timeline, all within one 100-item page. Latest20 all-state PR summaries per candidate repository were inspected; this is bounded and does not prove absence of every historical fix.

## Five full candidate reads; no new completed repair investigation

### Kuadrant/mcp-gateway — https://github.com/Kuadrant/mcp-gateway/issues/1671

Reporter: ManojLamani; created: 2026-11-13T03:32:38Z; discovered: 2026-11-13; state: open. Main SHA: `7459aa32345f658559f8de460c9070e78220849f`.

Reporter already provides parser-disagreement diagnosis, mitigation options and regression matrix. Source review corroborates case-insensitive Go decoding and original-byte unprefixed forwarding; no new additive finding. Related PR1647 typed-Params work must be coordinated. No Go regression or end-to-end security test run.

- [internal/mcp-router/ext_proc_adapter.go](https://github.com/Kuadrant/mcp-gateway/blob/7459aa32345f658559f8de460c9070e78220849f/internal/mcp-router/ext_proc_adapter.go)
- [internal/routing/router_202607.go](https://github.com/Kuadrant/mcp-gateway/blob/7459aa32345f658559f8de460c9070e78220849f/internal/routing/router_202607.go)

Tests: NOT RUN. Publication: no draft; confidence limited to the specific source observations above, not a tested repair.

### NousResearch/hermes-agent — https://github.com/NousResearch/hermes-agent/issues/154825

Reporter: a8lefx-dev; created: 2026-11-13T04:37:49Z; discovered: 2026-11-13; state: open. Main SHA: `71b676524e1e26f69a4ddcc9945a89e59a38d650`.

Report already identifies unaudited rejects, pre-send outbound rows and missing delivery outcome. Pinned tools/adapter code corroborates ordering; no independently validated event-schema redesign or new regression contribution. Counts alone do not prove wire delivery.

- [plugins/platforms/a2a/tools.py](https://github.com/NousResearch/hermes-agent/blob/71b676524e1e26f69a4ddcc9945a89e59a38d650/plugins/platforms/a2a/tools.py)
- [plugins/platforms/a2a/adapter.py](https://github.com/NousResearch/hermes-agent/blob/71b676524e1e26f69a4ddcc9945a89e59a38d650/plugins/platforms/a2a/adapter.py)

Tests: NOT RUN. Publication: no draft; confidence limited to the specific source observations above, not a tested repair.

### jamesward/heroku-ops — https://github.com/jamesward/heroku-ops/issues/17

Reporter: jamesward; created: 2026-11-13T04:53:43Z; discovered: 2026-11-13; state: open. Main SHA: `e087c000448c0eef7876f3bc1a9b0b1ede12bc55`.

Deployment/restart false-alarm hypothesis is plausible but source path and sanitized webhook payload were not independently reviewed. Need exact classifier and genuine-crash controls before suppressing alerts. Reporter already proposes correlation/delayed health checks. No runtime validation.

Source not inspected; commit identity only.

Tests: NOT RUN. Publication: no draft; confidence limited to the specific source observations above, not a tested repair.

### luthersystems/tf-modules — https://github.com/luthersystems/tf-modules/issues/99

Reporter: sam-at-luther; created: 2026-11-13T04:56:52Z; discovered: 2026-11-13; state: open. Main SHA: `cf0d04073a919a84d7d739f95616a6fcd4f36e48`.

Deployment resource lacks redeployment triggers in pinned source, matching reporter's diagnosis and trigger-hash proposal. No additive solution; no Terraform plan, provider integration or AWS test.

- [aws-sftp/api_gateway.tf](https://github.com/luthersystems/tf-modules/blob/cf0d04073a919a84d7d739f95616a6fcd4f36e48/aws-sftp/api_gateway.tf)

Tests: NOT RUN. Publication: no draft; confidence limited to the specific source observations above, not a tested repair.

### ensera-ai/taisce — https://github.com/ensera-ai/taisce/issues/262

Reporter: althunibat; created: 2026-11-13T04:56:48Z; discovered: 2026-11-13; state: open. Main SHA: `a98c1fb5179a110143de18cf4fade4f89e568c03`.

Reporter supplies composite scope/endpoint FK proposal and regression criteria. Current insertion reportedly derives scope and endpoint together, so do not claim a demonstrated current cross-project leak. Source/migration/database verification incomplete; no new reply.

Source not inspected; commit identity only.

Tests: NOT RUN. Publication: no draft; confidence limited to the specific source observations above, not a tested repair.

## Existing fix reviewed

[wyc6k PR108](https://github.com/weyucou/wyc6k-task-runner/pull/108), head `10b9b786712b77c8610c55d1dbe755dc3aebc7b3`, open/not merged. Full changed-file patches reviewed, including test_llm_clients.py, test_loop.py and test_tools.py. Retire R32-01; no new suggestion. Author-reported 258 passed not rerun.

## Initial screening inventory

The remaining URLs are search-result-level screening only, not complete investigations. They were not promoted into repair claims; results include feature plans, directory submissions, generated digests, operational gates and unsupported runtime reports. No statement that every unselected issue is resolved or technically invalid.

| URL | Title | Depth |
|---|---|---|
| https://github.com/scoizzle/Poly/issues/856 | Theme G, part 2: table-driven DSL (rows G-26 to G-36) — implementation plan | Initial search-result screening only |
| https://github.com/peterhudson/timegrapher/issues/1507 | Isochronism pane: results in a facts box on the plot, explanation in "i" | Initial search-result screening only |
| https://github.com/rheos/rheostream/issues/567 | Finance: read operations and MCP tools, opt-in only | Initial search-result screening only |
| https://github.com/saworbit/argus/issues/763 | [Tooling] Record the align-cli 0.77.0 trial: what held, what broke, what it found here | Initial search-result screening only |
| https://github.com/cline/mcp-marketplace/issues/3757 | Submission: widespread — verified-work bounty markets | Initial search-result screening only |
| https://github.com/darrencjh8/friday/issues/220 | Auto-evolving personality: friday-memory as source of truth (audit, persona core, calendar, preferences) | Initial search-result screening only |
| https://github.com/626Labs-LLC/626Labs-LLC.github.io/issues/314 | Privacy page: bring the Sanduhr Windows section up to 4.8.0 (Codex limits, renamed codenames) | Initial search-result screening only |
| https://github.com/TensorBlock/awesome-mcp-servers/issues/5899 | Add MCP server: Impulse | Initial search-result screening only |
| https://github.com/maxim-saplin/mcp_safe_local_python_executor/issues/7 | CWE-94: "secure sandbox" run_python tool yields host RCE (root) via CVE-2025-5120 smolagents escape — dynamically confirmed | Initial search-result screening only |
| https://github.com/DMontgomery40/scan-to-make/issues/789 | Design engine round 5: loads and checks round 4 left out | Initial search-result screening only |
| https://github.com/neomjs/neo-agent-brain/issues/1674 | The plane has no sampler for its containers over a window | Initial search-result screening only |
| https://github.com/NousResearch/hermes-agent/issues/154825 | a2a audit log: rejects unaudited and outbound rows lack delivery outcome — cross-agent reconciliation impossible by construction | Full thread; see above |
| https://github.com/kevinswiber/whosonfirst.ai/issues/84 | Add an In the field directory with sourced implementation and deployment evidence | Initial search-result screening only |
| https://github.com/kouweizhu/agents-radar/issues/946 | ⚙️ AI Infrastructure Digest 2026-11-13 | Initial search-result screening only |
| https://github.com/kouweizhu/agents-radar/issues/945 | 🦞 OpenClaw Ecosystem Digest 2026-11-13 | Initial search-result screening only |
| https://github.com/kouweizhu/agents-radar/issues/943 | ⚙️ AI 基础设施日报 2026-11-13 | Initial search-result screening only |
| https://github.com/kouweizhu/agents-radar/issues/942 | 🦞 OpenClaw 生态日报 2026-11-13 | Initial search-result screening only |
| https://github.com/Azure/azure-dev/issues/10947 | Test native A2A agents | Initial search-result screening only |
| https://github.com/Kuadrant/mcp-gateway/issues/1671 | Request guardrails can be bypassed on 2026-07-28 unprefixed routes using case-variant JSON-RPC fields | Full thread; see above |
| https://github.com/sonic-net/sonic-mgmt/issues/29217 | [snappi][pfcwd] Intermittent 1-3 packet background loss in 400G all-to-all test | Initial search-result screening only |
| https://github.com/x402-foundation/x402/issues/4254 | [Spec/extensions]: zero-amount payments unusable — standardize the charge-and-rebate trial pattern | Initial search-result screening only |
| https://github.com/x402-foundation/x402/issues/4253 | [Spec]: facilitator unavailability semantics undefined; sequential settle retries can double-pay | Initial search-result screening only |
| https://github.com/x402-foundation/x402/issues/4251 | [Spec]: 402 responses carry no version or dialect signal — v1/v2 interop fails silently | Initial search-result screening only |
| https://github.com/devbasex/ai-plugins/issues/3178 | Suggestion: let people and agents pay your agent per call (bot) | Initial search-result screening only |
| https://github.com/mzterwalexzyy/clean402/issues/1 | One line in src/app.js makes vet402's free read pass | Initial search-result screening only |
| https://github.com/bilgin-kocak/preflight/issues/1 | vet402's free 402 read of /v1/counterparty | Initial search-result screening only |
| https://github.com/Some1Uknow/paycrawl/issues/2 | vet402 paid for article-1 on Celo | Initial search-result screening only |
| https://github.com/Alex20Sas12/x402-open-rails-agent/issues/2 | vet402 bought /celo/block on Nov 12 | Initial search-result screening only |
| https://github.com/bloom-directory/bloom/issues/494 | Distribute the Bloom skill | Initial search-result screening only |
| https://github.com/PaulieB14/x402-omnigraph/issues/2 | Flag self-payments / seller self-tests so they don't count as organic volume | Initial search-result screening only |
| https://github.com/AusPosRest/restiq-backend/issues/284 | Stripe card payments from the guest's phone (QR) into the restaurant's account, plus card refunds | Initial search-result screening only |
| https://github.com/eriklobster/OMLAYER/issues/7 | P0: Cloudflare omlayer.workers.dev migration — cross-project production release gate | Initial search-result screening only |
| https://github.com/jamesward/heroku-ops/issues/17 | Factory improvement: a deploy's dyno restart counts as `crash` and fires the routine | Full thread; see above |
| https://github.com/apache/fineract-business-intelligence/issues/129 | Send alerts when sources go stale or dead letters spike | Initial search-result screening only |
| https://github.com/vercel/chat/issues/1157 | Slack adapter: upgrade to @slack/web-api 8 and @slack/socket-mode 3 without breaking egress proxy support | Initial search-result screening only |
| https://github.com/fluentcms/FluentCMS/issues/3104 | Describe the bodies of the plugin routes in the OpenAPI document | Initial search-result screening only |
| https://github.com/yohsuke1977/leaguru/issues/8 | 停止のお知らせ「再申込でデータ引き継ぎ」が実際とずれている | Initial search-result screening only |
| https://github.com/yohsuke1977/leaguru/issues/7 | 30日後の自動削除の失敗を見逃さず、結果を運営に知らせる | Initial search-result screening only |
| https://github.com/else-bot/else/issues/322 | Park a turn on a computer job until it ends instead of polling from the model | Initial search-result screening only |
| https://github.com/Spheroman/newgit/issues/451 | newgit.dev's webhook refused three pulls from GitHub; `main` there is stuck behind the mirror | Initial search-result screening only |
| https://github.com/aws-samples/sample-aws-genai-db-modernizer/issues/2202 | [Feature] Design DocumentDB in parallel parts like DynamoDB | Initial search-result screening only |
| https://github.com/ensera-ai/taisce/issues/263 | an unaudited unpark that names no project is exported and has no caller | Initial search-result screening only |
| https://github.com/majidhussainqadri1-dot/12-pdf-library-and-digital-reading-foundation/issues/53 | File12→File26 rights withdrawal: outbox sent is not verified consumer acknowledgement (stop-ship staging gate) | Initial search-result screening only |
| https://github.com/ensera-ai/taisce/issues/262 | a delivery's link to its endpoint does not carry the project, so the schema accepts one that crosses projects | Full thread; see above |
| https://github.com/aws-samples/sample-aws-genai-db-modernizer/issues/2201 | [Feature] Redesign rounds redesign only what changed | Initial search-result screening only |
| https://github.com/aws-samples/sample-aws-genai-db-modernizer/issues/2200 | [Feature] Start each schema review as soon as its design finishes | Initial search-result screening only |
| https://github.com/majidhussainqadri1-dot/10-video-wall-and-educational-broadcasting-foundation/issues/26 | V12.1 STO-09: durable File10→File26 tombstone delivery/ack and CDN purge acceptance required | Initial search-result screening only |
| https://github.com/Moke110/arc/issues/185 | Stage 2 01_bases rebuild: raw counts, corpus, disease DEGs, the two gene axes and views | Initial search-result screening only |
| https://github.com/MikeyMadeIt/qcu-student-planner/issues/165 | Security: Improve Error Handling and Prevent Sensitive Information Disclosure | Initial search-result screening only |
| https://github.com/Weaverse/forward/issues/135 | Add a cookbook for previewing account pages locally with a mock | Initial search-result screening only |
| https://github.com/autobutler-org/quark/issues/4121 | [Feature] Let Docs, Sheets, Slides, and Books use their files without a Files grant | Initial search-result screening only |
| https://github.com/luthersystems/tf-modules/issues/99 | aws-sftp: redeploy the API Gateway when its methods change | Full thread; see above |
| https://github.com/Moke110/arc/issues/186 | Bases rebuild 01 - raw-count release and raw corpus on the frozen axis | Initial search-result screening only |
| https://github.com/edwinsiguas/store/issues/1 | OWASP ZAP - Alertas de Seguridad en Backend API | Initial search-result screening only |
| https://github.com/henkisdabro/sandcastle-kit/issues/953 | A project checked out under /tmp/claude-<uid>/ crashes every Claude pass: set CLAUDE_CODE_TMPDIR in the sandbox | Initial search-result screening only |
| https://github.com/YAT-Publish/status/issues/1647 | 🛑 Hashi Random Images API(Temporary) is down | Initial search-result screening only |
| https://github.com/autobutler-org/quark/issues/4115 | [Feature] Refuse requests for an app the account cannot open | Initial search-result screening only |
| https://github.com/autobutler-org/quark/issues/4116 | [Feature] Store which apps an account can open | Initial search-result screening only |
| https://github.com/AnshChhikara001/hybridrag/issues/10 | Remove Streamlit and use the real test count | Initial search-result screening only |
| https://github.com/luthersystems/tf-modules/issues/98 | aws-platform-ui-storage: support more than one deployment per account (GitHub OIDC provider) | Initial search-result screening only |
| https://github.com/tariiq222/liwan/issues/703 | CI is red on main | Initial search-result screening only |
| https://github.com/fumito-ito/RSS-XML-Firebase-Releases/issues/3 | Dependency Dashboard | Initial search-result screening only |
| https://github.com/BryxCinco/matchie/issues/7 | Supabase keepalive failed (2026-11-13) | Initial search-result screening only |
| https://github.com/marcduiker/azure-functions-university/issues/999 | Link Checker Report | Initial search-result screening only |
| https://github.com/BarbossHack/reproducible/issues/233 | Signal-Android: check v8.35.2 | Initial search-result screening only |
| https://github.com/BarbossHack/reproducible/issues/232 | SimpleX-Android: check v7.1.3 | Initial search-result screening only |
| https://github.com/Abraham721/dodam-price-monitor/issues/17 | 도담티켓 가격연동 장애 | Initial search-result screening only |
| https://github.com/Badmaniren/my-userbot/issues/2755 | Jules Task: исправить сбой модуля repo_health_trend_calculator | Initial search-result screening only |
| https://github.com/dydrkflqmdl/sistech-homepoint/issues/3 | [배포 실패] 배포 워크플로가 실패했습니다 | Initial search-result screening only |
