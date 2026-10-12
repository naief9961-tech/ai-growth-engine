# NAIF Gravity — MCP & Integration Diagnostics

[![GitHub stars](https://img.shields.io/github/stars/naief9961-tech/ai-growth-engine?style=flat)](https://github.com/naief9961-tech/ai-growth-engine/stargazers)
[![Diagnostic requests](https://img.shields.io/github/issues/naief9961-tech/ai-growth-engine)](https://github.com/naief9961-tech/ai-growth-engine/issues)
[![Listed on mcpHQ](https://img.shields.io/badge/Listed%20on-mcpHQ-8A2BE2)](https://github.com/mcpHQ/awesome-mcp-servers)

NAIF Gravity provides bounded diagnostics and repair workflows for MCP, AI-agent integrations, APIs, authentication, and webhooks, with reproducible developer-facing diagnostics and machine-readable agent discovery.

**Start with the [Diagnostic Hub](NAIF-GRAVITY.md)** or visit [NAIF Gravity](https://naifgravity.com).

This repository contains public diagnostic guidance, a small Python MCP health-check script, issue templates, and discovery metadata. It is not a complete source distribution of the hosted service.

## Install NAIF JSON Rescue for your agent

[NAIF JSON Rescue](skills/naif-json-rescue/SKILL.md) checks a sanitized JSON sample locally before any external call. The free Node.js checker does not upload data, modify files or spend funds. Optional hosted diagnostics provide the existing bounded JSON artifact through x402 on Base, only within the buyer's disclosure permission and payment budget. A valid syntax-only sample needs no paid call.

With the [Skills CLI](https://github.com/vercel-labs/skills), review and install just this skill:

```bash
npx skills add naief9961-tech/ai-growth-engine --skill naif-json-rescue
```

Choose your supported agent in the installer. Installing does not authorize payments or fund a wallet. For a free offline demonstration after cloning this repository:

```bash
node skills/naif-json-rescue/scripts/check-json.mjs skills/naif-json-rescue/assets/valid.json
node --test tests/naif-json-rescue.test.mjs
```

Requires Node.js 18+. The local checker validates syntax only; duplicate keys and JSON Schema conformance are outside its scope. The hosted check accepts at most 4096 UTF-8 bytes and supports only bounded trailing-comma repair. See the skill for live discovery, regional policy, spending limits and accurate delivery interpretation.

## Live discovery for AI agents

NAIF Gravity is openly discoverable through its machine-readable, read-only entry points:

- [A2A Agent Card](https://naifgravity.com/.well-known/agent-card.json) — identity, skills, protocol interfaces.
- [Remote MCP endpoint](https://naifgravity.com/mcp) — Streamable HTTP; MCP clients should negotiate using the MCP protocol (a normal browser GET may return 405).
- [AI service catalog](https://naifgravity.com/.well-known/ai-catalog.json) and [agent catalog API](https://naifgravity.com/api/agent/catalog) — use live descriptions, eligibility and purchase instructions.
- [LLM capability guide](https://naifgravity.com/llms.txt) and [A2A discovery guide](AGENT-DISCOVERY.md).
- [A2A Registry listing](https://www.a2a-registry.org/agent/com.naifgravity.naif_technical_rescue_agent) and [Official MCP Registry listing](https://registry.modelcontextprotocol.io/?q=io.github.naief9961-tech%2Fnaif-fixgraph).

This repository's [MCP metadata](server.json) is broadcast to the official MCP Registry via a pinned, verified GitHub Actions publisher when it changes. Listing, crawling, or a registry publish does not prove a visit, a qualified lead, or a sale.

## Launch offer — one-time technical services (October 12–26, 2026)

**Live automatic discount, no coupon or manual agent approval.** The launch prices below apply to newly created eligible quotes through **2026-10-26 05:40 UTC (08:40 Saudi time)** **or the first 10 verified purchases of campaign products**, whichever happens first. Existing quotes and past payments retain their original terms. These are prices for **bounded technical-service jobs**, not per-call x402 tools.

| Bounded technical service | Regular USD | Launch USD |
| --- | ---: | ---: |
| NAIF API Fixer | $89 | **$79** |
| Web3 QA Sprint | $99 | **$89** |
| NAIF Data Factory | $129 | **$115** |
| Repair CI Gate Pilot | $129 | **$115** |
| RPC Reliability Audit | $129 | **$115** |
| Web3 Backend Rescue | $149 | **$129** |
| x402 Endpoint Sprint | $149 | **$129** |
| Smart-Contract Integration Review | $179 | **$159** |
| Agentic Wallet & Payments | $199 | **$179** |
| Automation Factory | $199 | **$179** |
| AI Agent Engineering Sprint | $249 | **$219** |
| Wallet Authentication Integration | $249 | **$219** |
| Trading Agent Infrastructure Sprint | $299 | **$269** |
| Web3 Automation Pilot | $399 | **$349** |

For **real-time eligibility and exact currently purchasable prices**, agents should call [the live agent catalog](https://naifgravity.com/api/agent/catalog), then **POST /api/agent/quote → POST /api/quote/accept → select an eligible payment rail**. Use the amount returned in the accepted quote and checkout; never calculate a discount client-side. USDC on Base and USDT on TRON may be available to eligible international requests; Apple Pay requires a human handoff. Wallet availability follows country and purchase policy. Quote acceptance alone never transfers funds or triggers implementation. Most engineering products require a verified paid Work handoff and are **not instant downloadable results**.

### Instant x402 API tools (separate from launch offer)

These **four published full-scope paid API endpoints** remain at their existing exact per-call prices until the payment challenge and live catalog are changed together:

| API tool | Price per call | Endpoint (POST) |
| --- | ---: | --- |
| JSON Validity Check | $1.00 USDC | [x402 JSON validity](https://naifgravity.com/api/x402/json-validity-check) |
| API Response Shape Check | $2.00 USDC | [x402 response shape](https://naifgravity.com/api/x402/api-response-shape-check) |
| JSON Normalize Mini | $3.00 USDC | [x402 JSON normalize](https://naifgravity.com/api/x402/json-normalizer) |
| CSV Schema Audit Mini | $5.00 USDC | [x402 CSV schema](https://naifgravity.com/api/x402/csv-schema-audit) |

Discover supported routes using the [x402 manifest](https://naifgravity.com/.well-known/x402), [x402 catalog](https://naifgravity.com/api/x402/catalog), and [OpenAPI](https://naifgravity.com/openapi.json). All four are published as self-registered services in [402 Index](https://402index.io) and are discoverable via [Agent402](https://agent402.tools/sell), which currently recognizes four tools on Base. **Lite trial rates have not been published: do not request, quote, or announce them as live.** A successful 402 challenge or an external directory listing is not proof of a settled sale or inclusion in Coinbase Bazaar.

## Individual purchases (no new recurring billing)

The [services catalog](https://naifgravity.com/services) lists the current individual, one-time technical services. New monthly subscriptions are paused. Pricing, purchase eligibility and region-specific payment options must be obtained from the live store; do not rely on older subscription offers, cached prices or an assumed wallet/payment path. Existing customer subscriptions and past payments are unaffected by this discovery documentation.


## Buy the JSON check with USDC on Base

- **Human buyers:** open the [JSON Validity Check product](https://naifgravity.com/service/json-validity-check). Use the payment options offered by the live checkout.
- **AI agents:** the [x402scan listing](https://www.x402scan.com/server/a95c7242-15af-44a7-a85d-2b2ffa251755) includes a **Try with AgentCash** option. The [OpenAPI document](https://naifgravity.com/openapi.json) describes the paid API.
- **Price:** 1 USDC on **Base mainnet** (`eip155:8453`) per bounded JSON check. Wallet network fees may apply. This price is for the JSON check, not every catalog service.

An x402 v2 client sends `POST https://naifgravity.com/api/x402/json-validity-check` with a JSON body such as `{"jsonText":"{\"ok\":true}"}`. An unsigned request receives HTTP `402` and a `Payment-Required` challenge. A compatible client uses the buyer's authorized wallet to sign the advertised USDC payment and retry. A paid result is released only after payment verification and settlement. A browser visit or a GitHub star does not buy the service.

The check accepts one sanitized sample of at most 4096 UTF-8 bytes. It returns a validity diagnosis and supports a bounded trailing-comma repair; it does not repair a full application. Never send secrets, private keys or customer data.

VPN/proxy use is no longer a standalone purchase blocker. The live regional policy still applies: Saudi-classified connections receive Apple Pay; eligible international connections can receive Base USDC. Consult the [live payment policy](https://naifgravity.com/api/commerce/policy) rather than assuming a wallet option is available everywhere. Agent wallets using Base may also need ETH for network fees.

## Service discovery

These hosted pages map common developer problems to a focused diagnostic or repair path:

| Problem or intent | Start here |
| --- | --- |
| API integration failures, request/response mismatch, or small integration fixes | [API integration diagnostic](https://naifgravity.com/service/api-integration-mini?utm_source=github&utm_medium=readme&utm_campaign=seo_discovery) |
| JSON validity, malformed payloads, or schema-adjacent checks | [JSON validity check](https://naifgravity.com/service/json-validity-check?utm_source=github&utm_medium=readme&utm_campaign=seo_discovery) |
| Automation workflow failures and broken task handoffs | [Automation factory](https://naifgravity.com/service/automation-factory?utm_source=github&utm_medium=readme&utm_campaign=seo_discovery) |
| Data transformation, structured output, or pipeline repair | [Data factory](https://naifgravity.com/service/data-factory?utm_source=github&utm_medium=readme&utm_campaign=seo_discovery) |
| Docker service health, container startup, or deployment checks | [Docker health fix](https://naifgravity.com/service/docker-health-fix?utm_source=github&utm_medium=readme&utm_campaign=seo_discovery) |
| Small bounded repair verification | [Repair check](https://naifgravity.com/service/repair-check-beta?utm_source=github&utm_medium=readme&utm_campaign=seo_discovery) |

The canonical home page is [naifgravity.com](https://naifgravity.com). These direct service links make the relationship between each developer problem and its destination explicit for both people and search engines.

## Try the MCP health check

Requires Python 3 and uses only the standard library. Run against a server you own or are authorized to test:

```bash
git clone https://github.com/naief9961-tech/ai-growth-engine.git
cd ai-growth-engine
python3 tools/mcp_health_check.py https://your-mcp.example/mcp
```

Replace the example URL with your endpoint. The script negotiates `initialize`, sends `notifications/initialized`, and reads `tools/list` when advertised. It supports JSON and SSE responses, optional bearer authentication through an environment variable, and bounded pagination; it never calls a tool. Protocol errors produce a nonzero exit status without printing server response bodies or secrets.

See the [quick start and limitations](docs/DIAGNOSTIC-QUICKSTART.md) before interpreting the result. This is a discovery probe for supported handshake-era revisions, not a full MCP conformance suite.

Try the [offline webhook signature example](examples/webhook_signature_fixture.py) to see why parsing and reserializing JSON can break raw-body verification. It uses synthetic data and makes no network requests.

## Find the right diagnostic path

| Failure | Useful evidence | Start here |
| --- | --- | --- |
| MCP connection, session, or schema | Transport, client/server versions, sanitized JSON-RPC error | [MCP diagnostic template](.github/ISSUE_TEMPLATE/mcp-diagnostic.md) |
| API authorization or OAuth | HTTP status, auth scheme, expected behavior, sanitized error code | [API/Auth diagnostic template](.github/ISSUE_TEMPLATE/api-auth-diagnostic.md) |
| Webhook delivery or processing | Provider, delivery and handler status, signature result, redacted payload shape | [Webhook diagnostic template](.github/ISSUE_TEMPLATE/webhook-diagnostic.md) |

Read the [troubleshooting index](docs/TROUBLESHOOTING.md) for common `401`, `403`, `invalid_grant`, raw-body signature, retry, and idempotency failures. Open an issue using the matching template once you have a minimal reproduction.

**GitHub issues are public.** Remove tokens, cookies, signing secrets, private keys, payment credentials, and customer data before sharing evidence.

## For AI-agent builders

[Agent discovery documentation](AGENT-DISCOVERY.md) describes the hosted MCP transport, A2A Agent Card, and canonical domain. [server.json](server.json) contains the provider's MCP registry metadata.

Documentation and discovery metadata describe the provider's interfaces; they do not guarantee current availability or certify protocol conformance. Diagnostic discovery does not automatically execute a production repair.

## Contribute

Useful contributions include reproducible sanitized examples, clearer troubleshooting steps, and corrections to diagnostic documentation. Explain the problem, expected behavior, and how to reproduce or verify your change. Never include private production logs.

This repository also contains material from the earlier AI Growth Engine project. See [the historical README](docs/LEGACY-GROWTH-ENGINE.md) and [the existing contribution guide](CONTRIBUTING.md) for that context. Historical bounty amounts, payout automation, and endpoint status are not current commitments.

If these diagnostics help you debug an integration, consider starring the repository so other builders can find it.

## Service boundary

The hosted service is available at https://naifgravity.com. Public GitHub diagnostic guidance and optional commercial repair workflows are separate; an issue or contribution does not purchase a service or guarantee a repair.
