# R6 — Discovery and selection audit

Date: 2026-10-18. Eight capped queries, at most 30 results each, sorted by creation descending. 240 returned entries, 237 distinct issue URLs. These are discovery/screening counts, not exhaustive GitHub totals or completed diagnoses.

## Queries

- `is:issue is:open created:>=2026-10-17 MCP in:title`
- `is:issue is:open created:>=2026-10-16 A2A in:title`
- `is:issue is:open created:>=2026-10-16 x402 in:title`
- `is:issue is:open created:>=2026-10-17 webhook in:title`
- `is:issue is:open created:>=2026-10-17 schema in:title`
- `is:issue is:open created:>=2026-10-17 JSON-RPC`
- `is:issue is:open created:>=2026-10-17 authentication API`
- `is:issue is:open created:>=2026-10-17 "GitHub Actions" failure`

The search tool omits some creation/state metadata. Selected issue timestamps/state/reporters were verified through issue REST responses, not inferred from search ranking.

## Full reads

- https://github.com/opena2a-org/agent-identity-management/issues/772
- https://github.com/chrisbennight/waygate/issues/218
- https://github.com/monid-ai/monid/issues/149
- https://github.com/yeongseon/azure-functions-scaffold-python/issues/423
- https://github.com/monstercameron/NextGenScriptingLanguage/issues/175
- https://github.com/reeenatamc/wp-content-agent/issues/6
- https://github.com/Danathar/tududi/issues/263
- https://github.com/google/adk-python/issues/7589

Issue descriptions, available comments and timelines were read for these eight. Selected threads were reread. Open PR collections and relevant all-state searches were checked for selected candidates; WordPress PR #3 and its discussion were reviewed after its head changed. Monid PR #151's patch already contains the proposed fix. Waygate received exploratory source inspection but no completed diagnosis, tests or draft.

See [discovery.json](discovery.json) for all distinct URLs/titles and selection stages. Unselected title/body matches include broad/noisy search hits, feature proposals, reporter-supplied fixes and subjects without sufficient incremental evidence; their full code was not investigated. No filler ranking.

## Follow-up audit

- https://github.com/cyanheads/musicbrainz-mcp-server/issues/21: closed; 2 comments read; zero after prior cursor.
- https://github.com/wbskt/Wbskt/issues/293: closed; 2 comments read; zero after prior cursor.
- https://github.com/abi83/prepify/issues/279: open; 3 comments read; zero after prior cursor.
- https://github.com/logly/mureo/issues/807: closed; 1 comments read; zero after prior cursor.
- https://github.com/scaffold-studio-hq/scaffold-studio-mcp/issues/68: closed; 5 comments read; zero after prior cursor.
- https://github.com/api-evangelist/roadmap/issues/938: open; 2 comments read; zero after prior cursor.
- https://github.com/parisbs/codex-subagent-mcp/issues/143: closed; 3 comments read; zero after prior cursor.
- https://github.com/HuginnIndustries/CodeCartographer/issues/463: open; 1 comments read; zero after prior cursor.
- https://github.com/web3insight-ai/web3insight/issues/32: closed; 5 comments read; zero after prior cursor.
- https://github.com/LumenRoute/lumenbazaar-frontend/issues/8: closed; 4 comments read; zero after prior cursor.
- https://github.com/microsoft/vscode/issues/341683: open; 1 comments read; zero after prior cursor.
- https://github.com/a2aproject/a2a-python/issues/1341: open; 1 comments read; zero after prior cursor.
- https://github.com/Abilityai/trinity/issues/3749: open; 3 comments read; zero after prior cursor.
- https://github.com/agnt-gg/agnt/issues/169: open; 1 comments read; zero after prior cursor.
- https://github.com/owasp-noir/noir/issues/3078: open; 2 comments read; zero after prior cursor.
- https://github.com/Gentleman-Programming/engram/issues/1899: closed; 4 comments read; zero after prior cursor.
- https://github.com/MementoRC/mcp-git/issues/298: closed; 1 comments read; zero after prior cursor.
- https://github.com/huiliyi37/Tianshu-harness/issues/507: closed; 1 comments read; zero after prior cursor.

No prior comment is presented as new. All existing ledger histories remain. The separate new-candidate bot claim on Tududi #263 is recorded but is not a reply to NAIF.
