# R24 — BanyanDB MCP startup | 2026-11-04

42 distinct open issue results screened (seven capped title searches, created since 2026-11-01). Six full issue discussions inspected; one completed source investigation. Checked 40 prior threads against saved comment IDs and checked reviews/inline comments on the three tracked PRs. No newly observed developer reply, change in tracked issue/PR state, or explicit commercial request. IntelliFlow #940 was readable again. Previous cursors retained; two new tracking records initialized. Nothing sent externally.

## Candidate retained

[apache/skywalking#14194](https://github.com/apache/skywalking/issues/14194), reported by UchihaIthachi on 2026-11-04T03:39:04Z. The open implementation is in [apache/skywalking-banyandb#1460](https://github.com/apache/skywalking-banyandb/pull/1460); reply there only, if approved. Both threads and the PR reviews/inline discussion were checked. The only PR conversation comment was unrelated to the ordering finding.

[Default-branch config](https://github.com/apache/skywalking-banyandb/blob/adc78b887ec00c07c2da402d36436a02f2da8e90/mcp/src/config.ts) · [entry point](https://github.com/apache/skywalking-banyandb/blob/adc78b887ec00c07c2da402d36436a02f2da8e90/mcp/src/index.ts) · [PR config](https://github.com/apache/skywalking-banyandb/blob/bcb9a55d448fbf59c131d35254c38f7db941ff00/mcp/src/config.ts) (blob `b70ff3c02f3248fe8283c57e01daf41cb3d843a3`) · [HTTP use](https://github.com/apache/skywalking-banyandb/blob/bcb9a55d448fbf59c131d35254c38f7db941ff00/mcp/src/server/http.ts) · [PR tests](https://github.com/apache/skywalking-banyandb/blob/bcb9a55d448fbf59c131d35254c38f7db941ff00/mcp/src/config.test.ts).

At PR head `bcb9a55d448fbf59c131d35254c38f7db941ff00`, the explicit loader runs after three exported constants are evaluated. Later constants do see the file. The HTTP auth guard checks the captured token for truthiness before comparing a request token. This makes the ordering significant; no deployed exposure or live behavior was tested. Confidence high for the config-module finding. Moving both loader lines first fixes the isolated case without changing the default precedence. No NAIF tool is needed for this local startup test.

## Verification

Node v24.22.1; three clean child processes, no listener, external endpoint, credentials, or package installation. Used the exact PR config as an .mts module. Substituted only the dotenv package with a local CommonJS module whose config function calls Node's synchronous process.loadEnvFile('.env'). The candidate moves only the dotenv import and invocation above the first export. The working directory contained a synthetic .env with address example.invalid:1234, loopback host 127.0.0.2, a synthetic token marker, port 4555 and transport http. Compared the token as a boolean.

| Config / child environment | Address | Host | Token matches fixture | Port | Transport |
|---|---|---|---|---:|---|
| PR / no inherited variables except PATH | localhost:17900 | 127.0.0.1 | false | 4555 | http |
| Reordered / same environment | example.invalid:1234 | 127.0.0.2 | true | 4555 | http |
| Reordered / MCP_HOST=127.0.0.3 | example.invalid:1234 | 127.0.0.3 | true | 4555 | http |

All three rows asserted. Not tested: real dotenv package, upstream test suite, HTTP authentication, network binding, production or release.

## R24-01 — English reply for review only

Destination: [open fix PR #1460](https://github.com/apache/skywalking-banyandb/pull/1460). Pending user approval. Recheck head and discussion before posting once.

Three settings are still read before `dotenv.config({ quiet: true })` runs at [bcb9a55](https://github.com/apache/skywalking-banyandb/blob/bcb9a55d448fbf59c131d35254c38f7db941ff00/mcp/src/config.ts): `BANYANDB_ADDRESS`, `MCP_HOST`, and `MCP_AUTH_TOKEN`. Importing dotenv loads the package; it does not move the explicit config call ahead of those assignments. With only a working-directory `.env`, the port and transport can therefore change while the address and host stay at their defaults and the configured token stays empty.

I checked the evaluation order in fresh Node processes with a synthetic env file and a substitute dotenv loader. Moving the import and config call above the first environment read made all five exports match the fixture, and an existing process-level host still won. I did not start an HTTP listener or test live authentication.

Could the PR move those two lines to the top and add a child-process regression using the real dotenv dependency? Start with the five variables unset, import the config once, and assert all five exports (compare the token without logging it). Repeat with `MCP_HOST` set in the child environment to cover precedence. That catches the startup path even if the tests that set `process.env` directly continue to pass.

## Other complete candidate reads

- [mastra-ai/mastra/issues/29360](https://github.com/mastra-ai/mastra/issues/29360): Reporter already identifies both key-collision paths and suggests mitigations; no additional verified fix.
- [a2aproject/a2a-rs/issues/484](https://github.com/a2aproject/a2a-rs/issues/484): Existing REST compatibility work: a2a-rs PRs #485 and #489. No additional regression demonstrated.
- [a2aproject/a2a-js/issues/807](https://github.com/a2aproject/a2a-js/issues/807): a2a-js PR #808 already targets the webhook response lifetime. No distinct fix verified.
- [mark3labs/mcp-go/issues/1165](https://github.com/mark3labs/mcp-go/issues/1165): Reporter supplies the alias/validation mismatch, patch direction and mitigations. No additional result.
- [0xPlaygrounds/rig/issues/3012](https://github.com/0xPlaygrounds/rig/issues/3012): Reporter already supplies the nullable collection failure, root cause and regression matrix.

## Screening inventory

- https://github.com/nicsuzor/mem/issues/832
- https://github.com/zts212653/clowder-ai/issues/1833
- https://github.com/mastra-ai/mastra/issues/29360
- https://github.com/apache/skywalking/issues/14194
- https://github.com/daniel-ospina/tortoise/issues/10846
- https://github.com/dorname/coldrawdb/issues/76
- https://github.com/yetone/magpie/issues/5136
- https://github.com/murray17/rovai-ai/issues/1007
- https://github.com/a2aproject/a2a-rs/issues/484
- https://github.com/a2aproject/a2a-rs/issues/479
- https://github.com/BerriAI/litellm/issues/49869
- https://github.com/BerriAI/litellm/issues/49867
- https://github.com/crewAIInc/crewAI/issues/8968
- https://github.com/a2aproject/a2a-go/issues/516
- https://github.com/BerriAI/litellm/issues/49622
- https://github.com/crewAIInc/crewAI/issues/8930
- https://github.com/a2aproject/a2a-js/issues/807
- https://github.com/cryostatio/cryostat-operator/issues/1516
- https://github.com/PuzzleTechHub/bot-be-named/issues/442
- https://github.com/EasySoft-Tech-SL/dolibarr-easyocr-module/issues/5
- https://github.com/sampath-0003/git-test/issues/2
- https://github.com/rancher/rancher/issues/58520
- https://github.com/Adyen/adyen-magento2/issues/3408
- https://github.com/Adyen/adyen-magento2/issues/3407
- https://github.com/mark3labs/mcp-go/issues/1165
- https://github.com/0xPlaygrounds/rig/issues/3012
- https://github.com/first-tree-ai/opentag/issues/1217
- https://github.com/spatney/rayfin-fabricator/issues/77
- https://github.com/tinacms/tinacms/issues/7996
- https://github.com/ford442/pachinball/issues/505
- https://github.com/griddynamics/rosetta/issues/391
- https://github.com/mcclowes/clip/issues/119
- https://github.com/anthropics/claude-code/issues/107137
- https://github.com/koji/answer-before-you-go/issues/7
- https://github.com/ChronoAIProject/NyxID/issues/2175
- https://github.com/first-tree-ai/opentag/issues/1220
- https://github.com/Tunefish92/Aurora-Theme/issues/32
- https://github.com/xiufengsun/TokenTracker/issues/1018
- https://github.com/multica-ai/multica/issues/9911
- https://github.com/alokeb/url-shortener/issues/2
- https://github.com/unibrain1/devkit/issues/91
- https://github.com/floiaassistant-design/Le-laboratoire-ia/issues/11
