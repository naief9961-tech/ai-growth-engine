# R27 — 2026-11-07: verified technical follow-up; no duplicate replies

Checked at 2026-11-07T05:05:19Z. Base main commit: `833c168dfde37919255694b91405a16e56268c7e`.
This is a bounded discovery and follow-up round, not five completed engineering investigations.

## Result

The [Backlog.md reporter's new reply](https://github.com/MrLesk/Backlog.md/issues/1179#issuecomment-6694189099), posted by kenorb on 2026-11-06 at 20:00:17 UTC, explicitly confirms our validator analysis. The reporter tested the v1.55.3 release binary through stdio MCP with a disposable fixture store and closed the issue as not reproducible on the server. Our [approved R26 comment](https://github.com/MrLesk/Backlog.md/issues/1179#issuecomment-6677434895) had identified the difference between isolated validation and the installed runtime.

This is useful technical feedback, not a code fix, purchase inquiry, or independent end-to-end test performed in R27. The original client/harness cause remains unproven by us.

## Counts and coverage

| Measure | Count |
| --- | ---: |
| Search queries | 7 |
| Capped results retrieved | 70 |
| Unique URLs initially screened | 65 |
| New candidate bodies, all comments and timelines read | 5 |
| Exploratory source inspections | 3 |
| New completed engineering investigations | 0 |
| Previously tracked discussion threads read | 44 |
| Tracked PR review/inline-comment streams checked | 4 |
| New human replies on tracked threads | 1 |
| New bot comments on tracked threads | 0 |
| New isolated tests or upstream suites executed | 0 |
| New English review drafts | 0 |
| Third-party comments, messages or PRs sent in this round | 0 |
| Explicit commercial requests observed | 0 |

Searches used `is:issue is:open <keyword> bug created:>=2026-11-04`, newest first, capped at ten per keyword: MCP, A2A, x402, webhook, schema, API, and "GitHub Actions". These are bounded search results, not exhaustive coverage of GitHub or the 72-hour window. Search overlap accounts for five duplicate results.

All 44 follow-up comment lists were below the 100-item page limit. Four tracked PRs also had review submissions and inline comments inspected: [mppx #1133](https://github.com/wevm/mppx/pull/1133), [PriceStalker #269](https://github.com/mikeknight85/PriceStalker/pull/269), [Langfuse #19595](https://github.com/langfuse/langfuse/pull/19595), and [BanyanDB #1460](https://github.com/apache/skywalking-banyandb/pull/1460). No other new follow-up comments were found after saved cursors. Previously reported merges and acknowledgements are not counted again.

## Five candidate threads — withheld, not five recommended replies

| Thread | Reporter / created UTC | Decision |
| --- | --- | --- |
| [rriggs/hermes-agent-a2a-async-plugin #20](https://github.com/rriggs/hermes-agent-a2a-async-plugin/issues/20) | rriggs; 2026-11-07T04:47:15Z | Hold: reported reply_parts behavior is in the #14 worktree, not the fetched main commit. Reporter already supplies reload/forward fix and test plan. Exact worktree SHA and runtime reproduction needed; no additive draft. |
| [mnzsss/ivar #261](https://github.com/mnzsss/ivar/issues/261) | mnzsss; 2026-11-07T04:49:09Z | Suppress duplicate advice: main source confirms OAuth requirement classification depends on oauth.is_some(), and reporter already explains missing metadata and proposed state-model fixes. Bot links implementation tracking. No isolated or runtime test run. |
| [aws-samples/sample-aws-genai-db-modernizer #2012](https://github.com/aws-samples/sample-aws-genai-db-modernizer/issues/2012) | tebanieo; 2026-11-06T23:45:42Z | Suppress duplicate fix: open PR #2024 already sets the shared docstring before tool decoration and adds description/parameter and prompt regression tests. Inspected all four patches, comments and reviews; tests were not rerun. |
| [vercel/eve #6128](https://github.com/vercel/eve/issues/6128) | coygeek; 2026-11-07T03:46:00Z | Hold/no additional reply: reporter already provides credential-selection diagnosis, offline reproduction and installationId workaround. Independent source/credential-path investigation was not completed; no runtime test run. |
| [rogerbarreto/agent-framework-public #13](https://github.com/rogerbarreto/agent-framework-public/issues/13) | rogerbarreto; 2026-11-07T05:01:30Z | Hold: reporter supplies schema example and workaround, but exact dependency source/provider behavior and upstream ownership were not independently validated. No completed source investigation or test. |

### Hermes #20

The issue concerns persisted DataPart/FilePart output missing from terminal SSE. The reporter already proposes reloading the terminal task record, passing persisted parts into the emitter, and testing already-completed and live-completing subscriptions plus text-only and non-completed controls.

The reported behavior refers to the [#14 implementation worktree](https://github.com/rriggs/hermes-agent-a2a-async-plugin/issues/14). The fetched main source has no `reply_parts` support. Thus main is not sufficient to prove the reported implementation's defect. Confidence is high in this version mismatch; the runtime diagnosis is unverified. Need the exact worktree commit before testing or proposing a change. Additional benefit from repeating the reported fix is low.

### ivar #261

Static inspection confirms `oauth_requirement()` returns NotApplicable for local servers, Required when `oauth.is_some()`, and NotRequired otherwise. The issue already explains why a provider/CIMD authentication path without an OAuth block can be classified incorrectly and proposes explicit auth state/metadata with authenticated and unauthenticated controls. Its one comment is a bot link to implementation tracking, not technical validation or interest in our services.

Confidence is high in the local classification branch, but no complete credential setup or runtime reproduction was executed. No additional fix beyond the reporter's proposals was established.

### AWS schema tools #2012

Main assigns shared function docstrings after tool decoration. Existing [PR #2024](https://github.com/aws-samples/sample-aws-genai-db-modernizer/pull/2024), head `839fef1e169723794133b2e83a1527c1832dd9fd`, already wraps each function with a factory that assigns its docstring before calling `tool(fn)`. All four file patches, issue comments, review submissions and inline comments were inspected; review and comment lists were empty at inspection.

The PR includes assertions for the six tool descriptions and both parameter descriptions, plus prompt-step consistency tests. We did not rerun them or the PR author's reported suite. Static confidence that the existing patch addresses the reported ordering is high; runtime acceptance is unverified. A new reply repeating this patch would add little value.

### Eve #6128 and structured output #13

Eve's reporter already supplies a credential-selection explanation, offline reproduction and explicit-installation-ID workaround. We did not independently complete its source/auth-path investigation. The structured-output report includes a nested-reference schema and workaround, but the dependency implementation and provider behavior were not independently verified. Both are held; neither is presented as an established diagnosis from us.

## Pinned source evidence

| Repository / file | Commit | Blob |
| --- | --- | --- |
| [rriggs/hermes-agent-a2a-async-plugin: a2a_async_plugin/adapter.py](https://github.com/rriggs/hermes-agent-a2a-async-plugin/blob/42c623774c950fa7454e2a4d482758161e92f78d/a2a_async_plugin/adapter.py) | `42c623774c950fa7454e2a4d482758161e92f78d` | `956b5c5626d02d4d99f07c818b2cfbc3b9ce21c9` |
| [mnzsss/ivar: src/domain/mcp.rs](https://github.com/mnzsss/ivar/blob/a9930222ffe8cea3fc0e7b4988a7f08a6ab16945/src/domain/mcp.rs) | `a9930222ffe8cea3fc0e7b4988a7f08a6ab16945` | `cdd0c9ff9640434e962f530d272db5d2e643934b` |
| [aws-samples/sample-aws-genai-db-modernizer: src/atx_orchestrator/tools.py](https://github.com/aws-samples/sample-aws-genai-db-modernizer/blob/f6af8489671103ff23ab2ea4b04e81efe16dc6b1/src/atx_orchestrator/tools.py) | `f6af8489671103ff23ab2ea4b04e81efe16dc6b1` | `b52e9da4ffab579044e96fdb802fee7bc8f1e709` |

No new regression harness was executed. Existing issue and PR regression proposals were reviewed only. No model/provider call, OAuth session, real credential, payment, deployment, or upstream full suite was used.

## New tracked reply: Backlog.md #1179

The author reports the following release-binary results; these are **author-reported**, not our execution:

- 441 and 500 ASCII characters accepted and persisted intact.
- 501 and 520 rejected; mixed valid/over-limit arrays rejected at the invalid index.
- The fixture store remained unchanged after rejected edits.
- 520 characters consisting of 500 characters plus 20 trailing spaces became 500 after whitespace trimming.
- The add/create MCP paths also rejected the over-limit value; CLI editing stored 520 intact.
- The original October 6 observation came through an agent harness and predates v1.55.3. The author will investigate the client/harness.

The issue is now closed as not reproducible. No follow-up reply is necessary merely to acknowledge this acknowledgement. Cursor advanced from `6677434895` to `6694189099`; the prior own-comment ID remains `6677434895`. Prior issue analysis and historical approvals are retained.

## Draft/publication status

**No new English reply is ready for approval.** Do not copy or repost the R26 reply: it was already approved, posted, and read back on November 6. No third-party publication was attempted in R27. Appreciation and technical validation are recorded separately from commercial interest; no explicit commercial interest was found.

No NAIF tool link is recommended for these candidates. No tool suitability or fresh site validation is claimed. Public endpoint probes would not establish the worktree, OAuth classification, decorator, credential-selection or provider-schema causes.

## Repository write controls

The prior radar, README, ledger and latest R26 report were read before discovery. The complete repository tree was checked for applicable AGENTS.md files. Root AGENTS.md describes an unrelated bounty/wallet flow; it does not authorize external claims, payments or changes outside this user's scope.

All eight workflow triggers were inspected at the base commit. Push workflows filter on server.json, .well-known/agent.json or specific workflow files; the remaining triggers are PR/review/comment, schedule or manual dispatch. This round changes only documentation under docs/problem-hunter-v1/. No workflow is changed or dispatched. Main will be advanced with an expected-head check and a non-forced update. The report and cursor changes share one commit.

## Limits and next step

No access blocker prevented the documentation update. Investigation limits were missing worktree provenance, already proposed fixes, and unverified runtime/provider paths. Zero new completed investigations and zero new tests are deliberate disclosures, not evidence of a successful repair. No action is required from the user for this round. A future material update may justify revisiting a held candidate; unchanged reports must not be repeated.

## Discovery inventory

The inventory records initial screening, not full investigation or current-state verification of every result. The five candidates above received detailed reads. Other results include planning/docs, advertisements/digests, broader audits, provider-specific reports and cases without an established additive contribution in this round.

1. [.NET:  Bug : Surface Foundry OAuth consent response items as typed agent content](https://github.com/rogerbarreto/agent-framework-public/issues/32)
2. [.NET:  Bug : Foundry Toolbox granular require_approval object is treated as unsupported, so every tool requires approval](https://github.com/rogerbarreto/agent-framework-public/issues/9)
3. [bug: N41.1 full-migration test forbids N41.2 registry activation](https://github.com/Mymayankyadav/lemma/issues/1024)
4. [security: low-risk hardening checklist](https://github.com/iamsaquib8/stockwise/issues/298)
5. [documentation: Knowledge note for the agents module (MCP access, suggestions, run history)](https://github.com/boulaajaj/sprecher-east-neighborhood-website/issues/782)
6. [documentation: Knowledge note for the accounts module (sign-up, sign-in, passwords, roles)](https://github.com/boulaajaj/sprecher-east-neighborhood-website/issues/781)
7. [ Bug : OpenCode 2.x ctx_* tools never check OpenCode permissions](https://github.com/mksglu/context-mode/issues/1331)
8. [groupify-pr Evidence steps: screenshot save path fails, and phone-width shots can lose the repro](https://github.com/gebrielmolla19/Groupify/issues/47)
9. [security(3.1.0): release gate for MCP/Host correctness and least privilege](https://github.com/tse-wei-chen/hs-sql-agent/issues/575)
10. [mcp status reports not-required for an OAuth server whose auth left no oauth block](https://github.com/mnzsss/ivar/issues/261)
11. [ Bug : SubscribeToTask omits persisted DataPart and FilePart output from terminal SSE events](https://github.com/rriggs/hermes-agent-a2a-async-plugin/issues/20)
12. [【bug】uninstall --target opencode 残留 MCP 配置条目（只移除 skills，不移除 opencode.json 的 MCP 块）](https://github.com/huaweicloud-mate/hdcommunity-mng-toolkit/issues/13)
13. [⚙️ AI Infrastructure Digest 2026-11-07](https://github.com/HuggerHustle/ai-radar/issues/176)
14. [ Bug  AWS Transform schema-design tools reach the model with no description](https://github.com/aws-samples/sample-aws-genai-db-modernizer/issues/2012)
15. [⚙️ AI Infrastructure Digest 2026-11-07](https://github.com/zhangzuxuan2023-hub/agents-radar/issues/64)
16. [⚙️ AI 基础设施日报 2026-11-07](https://github.com/zhangzuxuan2023-hub/agents-radar/issues/61)
17. [ RFC  Physical shard order for N-D parameter storage in AutoParallel](https://github.com/meta-pytorch/autoparallel/issues/570)
18. [Tell the room when a cancel can't reach a waiting profile parent, and keep climbing](https://github.com/gke-labs/kube-agents/issues/5111)
19. [ Bug : gRPC error details have a size limit the specification does not mention, and no defined encoding for types outside google.rpc; the SDKs differ](https://github.com/a2aproject/A2A/issues/2433)
20. [ Bug : mooncake-ep JIT: nvcc spawn intermittently fails with exit_code=127 and no output during CUDA graph capture](https://github.com/kvcache-ai/Mooncake/issues/5316)
21. [Grant readiness gate: complete technical, legal, and external validation prerequisites](https://github.com/itswork-app/aivoguard/issues/2)
22. [Passport 5/5: SDK merchant verify helper + demo merchant as first (advisory) consumer](https://github.com/d-hinders/Haven-AI/issues/4723)
23. [Passport 3/5: the agent reads its own passport reference (agent read, SDK, hosted haven_get_agent, settle relay)](https://github.com/d-hinders/Haven-AI/issues/4721)
24. [Passport 2/5: state availability, correct the overclaims, name the half-configured state on the ops page](https://github.com/d-hinders/Haven-AI/issues/4720)
25. [End-to-end suite over every flow, with artifacts](https://github.com/ss251/countersign/issues/39)
26. [ FEATURE  Community tool: AgentReader — pay-per-call UK/US/EU company + KYB data for research crews (x402, Base USDC)](https://github.com/crewAIInc/crewAI/issues/9147)
27. [Feature/example: agenti calling AiphaBrainLab CEX Execution Gate ($0.10 x402) as a trading pre-submit check](https://github.com/nirholas/agenti/issues/216)
28. [Spec: Allowance — agent budgets paid through contract-signed x402 payments](https://github.com/Rahat-ch/allowance/issues/1)
29. [spec v2: require the resource server to match accepted against its own accepts   before /verify](https://github.com/x402-foundation/x402/issues/4161)
30. [cli: infer web search/fetch --provider rejects valid provider ids with different casing](https://github.com/openclaw/openclaw/issues/193535)
31. [Tap to Pay donations still send a public ID or slug as Stripe event_id metadata](https://github.com/hackclub/hcb/issues/15608)
32. [design: unified GH rate-limit strategy for automated processes](https://github.com/jcronq/alice/issues/786)
33. [T7.2 — Responder task, autonomy policy and headless run](https://github.com/cancinoray/stockroom/issues/62)
34. [T7.1 — Alert poller and evidence collector](https://github.com/cancinoray/stockroom/issues/61)
35. [Acquire complete safe c1 evidence through the landed terminal reader](https://github.com/chase-sets/chase-sets/issues/11125)
36. [fix(github): proactive sends to private repositories skip configured credentials](https://github.com/vercel/eve/issues/6128)
37. [Robustness/UX suggestions from real use: status reasons, dependency health, startup retry, search throttling, blocked imports](https://github.com/TheIndieArmy/placeholdarr/issues/142)
38. [App Insights review: production failure fixes (Nov 2026)](https://github.com/HoffmanEngineering/3d-print-log-api/issues/309)
39. [PRD: Email subscriptions synced with Salesforce, and project emails sent from subscriptions](https://github.com/nico-kneler-as/as-comms-platform/issues/751)
40. [🦞 OpenClaw 生态日报 2026-11-07](https://github.com/leisure3318/agents-radar/issues/3143)
41. [Phase 10 research: feature inventory and recommended order](https://github.com/ahaqqu/RumaQ/issues/516)
42. [.NET:  Bug : Type-generated structured-output schema can contain nested $ref rejected by OpenAI Responses](https://github.com/rogerbarreto/agent-framework-public/issues/13)
43. [Make a custom-task plugin's parameters its contract, with plugin versions](https://github.com/nightBaker/fleans/issues/1051)
44. [ Refactor  監査結果  全現行実装の修正候補と検証範囲（2026-11-07）](https://github.com/kukuri-app/kukuri/issues/2052)
45. [Bug: Lean's challenge step lets the adversary child submit test files](https://github.com/trail-openers/pi-rukas/issues/2074)
46. [documentation: Knowledge note for rich text and the editorial blocks (src/platform/richtext)](https://github.com/boulaajaj/sprecher-east-neighborhood-website/issues/790)
47. [documentation: Knowledge note for the news module (posts, categories, search, top issues)](https://github.com/boulaajaj/sprecher-east-neighborhood-website/issues/785)
48. [documentation: Knowledge note for the directory module (FAQ, resources, team members)](https://github.com/boulaajaj/sprecher-east-neighborhood-website/issues/784)
49. [.NET:  Bug : AsAIFunction() fails under Foundry hosting: forwarded ChatHistoryProvider override conflicts with Responses-backed child agent's ConversationId](https://github.com/rogerbarreto/agent-framework-public/issues/29)
50. [.NET:  Bug : AIAgent.RunStreamingAsync does not surface the final image from HostedImageGenerationTool](https://github.com/rogerbarreto/agent-framework-public/issues/28)
51. [Python: .NET:  Bug : Zero-metric evaluation items are counted as failures](https://github.com/rogerbarreto/agent-framework-public/issues/25)
52. [Python: .NET:  Bug : `ContainsExpected` reports missing expected output as a model failure](https://github.com/rogerbarreto/agent-framework-public/issues/24)
53. [Python: .NET:  Bug : Workflow result counts do not roll up `SubResults`](https://github.com/rogerbarreto/agent-framework-public/issues/23)
54. [@ektor_andrade](https://github.com/cli/cli/issues/14980)
55. [Coordinate upstream libdwarf producer fixes: AArch64 relocation width and string-table isolation](https://github.com/zwilcox/GhidraDwarfForge/issues/187)
56. [ bug/reliability  P2 — Giveaway zapisuje konkurs i ogłasza sukces mimo nieudanej publikacji Discord](https://github.com/abanach-com/rust-discord-bot/issues/271)
57. [ github-docs-seo  Baseline AW recommendation SEO report and minimal docs update plan](https://github.com/github/gh-aw/issues/75607)
58. [ auto-ui  profile: slow no feedback on profile: Write my CV gives no visible response](https://github.com/jobadabra/jobadabra/issues/3460)
59. [ auto-ui  settings: consistency on settings: AI shown as connected with an API key, but the key is Not se](https://github.com/jobadabra/jobadabra/issues/3459)
60. [ Worker  Fase 2 — Sacar el runtime del preview, defecto de entorno fail-closed y verificación automática](https://github.com/rbalam/EDARSA_HUB/issues/142)
61. [Colombia Huila image does not load](https://github.com/MarcusGCY/KoffeeBean/issues/94)
62. [ claudinite-work  claudinite/growth-extract](https://github.com/missingbulb/NoRFinder/issues/820)
63. [🐛 - Bugbot misses restored fixed replacement source guard](https://github.com/vypdev/copilot/issues/919)
64. [Fix security-alert composite vars-context regression across all four repositories](https://github.com/VanillaIceCube/FullStackTemplate/issues/300)
65. [Pre-push hook skips tests/test_docgen.py](https://github.com/mithro/gf180-tcad/issues/165)
