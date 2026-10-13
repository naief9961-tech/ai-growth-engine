# NAIF Gravity — GitHub Diagnostic Hub

NAIF Gravity helps developers and AI agents diagnose bounded integration failures without handing over private keys or rebuilding an entire stack.

## New in October 2026: useful results before you pay

**A malformed JSON payload should not require an expensive repair project.** NAIF Gravity now offers **Micro Tools V2** with a *free, bounded preview* and three fixed-price, one-time diagnostics:

- **$1 — JSON Validity Check:** syntax location, duplicate-key warnings, safe trailing-comma repair, inferred sample schema, CI snippet and checksum.
- **$2 — API Response Shape Check:** compare two response samples, see added/removed fields and type changes, and get sample-based TypeScript/OpenAPI schemas.
- **$3 — JSON Normalize Mini:** deterministic formatted JSON, optional trimming/indentation, change log and SHA-256 receipt.

**[Run the free preview →](https://naifgravity.com/micro-v2?utm_source=github&utm_medium=diagnostic_hub&utm_campaign=micro_tools_v2)** · [Live agent catalog](https://naifgravity.com/api/agent/catalog) · [x402 API catalog](https://naifgravity.com/api/x402/catalog)

**Built for humans and buyer agents:** preview first, obtain an exact quote, explicitly accept it, choose an eligible payment method and receive the encrypted bounded report after verified settlement. No automatic transfers, no new subscription and no production system access for sample-only Micro Tools V2. Saudi-classified buyers use Apple Pay with human authorization; eligible international buyers can use Base USDC or TRON USDT according to the live policy. Instant per-call x402 Base USDC resources are a *separate paid API route*.

Micro V2 reads only supplied sanitized input (4,096 bytes maximum). Do not paste credentials, private keys or customer records; uploaded samples do not mean live API endpoint testing.

---

## Start here

1. **MCP problem** — run `python3 tools/mcp_health_check.py https://your-mcp.example/mcp` against an endpoint you own or are authorized to test.
2. **API / Auth problem** — collect the HTTP status, sanitized error code, auth method and expected behavior.
3. **Webhook problem** — collect the provider, delivery status, signature-verification result and a redacted payload shape.
4. If the failure is reproducible, open the matching GitHub diagnostic request template.

## Direct diagnostic paths

Use the narrowest matching destination instead of sending every visitor to the home page:

- [API integration diagnostic](https://naifgravity.com/service/api-integration-mini?utm_source=github&utm_medium=diagnostic_hub&utm_campaign=seo_discovery) — API integration errors, request/response mismatch, small integration failures.
- [JSON validity check](https://naifgravity.com/service/json-validity-check?utm_source=github&utm_medium=diagnostic_hub&utm_campaign=seo_discovery) — malformed JSON, payload validity, and structured-data checks.
- [Automation factory](https://naifgravity.com/service/automation-factory?utm_source=github&utm_medium=diagnostic_hub&utm_campaign=seo_discovery) — automation workflow failures and broken handoffs.
- [Data factory](https://naifgravity.com/service/data-factory?utm_source=github&utm_medium=diagnostic_hub&utm_campaign=seo_discovery) — structured data transformation and pipeline repair.
- [Docker health fix](https://naifgravity.com/service/docker-health-fix?utm_source=github&utm_medium=diagnostic_hub&utm_campaign=seo_discovery) — container health, startup, and deployment diagnostics.
- [Repair check](https://naifgravity.com/service/repair-check-beta?utm_source=github&utm_medium=diagnostic_hub&utm_campaign=seo_discovery) — bounded repair verification.

Canonical home: https://naifgravity.com

## Launch discount and direct agent purchases (12–26 October 2026)

The currently published, one-time developer-service offers include a **temporary 14-product launch discount**, applied automatically to new eligible quotes without a coupon. The price is locked in a Quote and remains unchanged while its checkout is completed. The campaign ends **2026-10-26 at 05:40 UTC or after 10 verified purchases of eligible launch products**, whichever comes first. See [the complete launch offer and price table](README.md#launch-offer--one-time-technical-services-october-1226-2026) and retrieve the authoritative price at the time of purchase from [the live agent catalog](https://naifgravity.com/api/agent/catalog).

For an agent authorized to purchase: fetch the catalog, POST to /api/agent/quote with the real requested scope, POST to /api/quote/accept, then choose an eligible live payment method. Base USDC and TRON USDT are payment options for eligible international buyers; Apple Pay requires human buyer authorization. **No artificial purchase or payment is authorized by these discovery instructions.** All Work-required services begin only after a verified paid job and remain subject to human/scoped delivery checks.

For **instant per-call x402** there are four published full-scope POST endpoints. [x402 manifest](https://naifgravity.com/.well-known/x402) and [OpenAPI](https://naifgravity.com/openapi.json) advertise exact Base USDC requirements and methods. Their existing fixed prices are $1, $2, $3, and $5 per call; **do not offer proposed Lite prices as live endpoints**. On Saudi-classified requests the regional wallet policy still applies.

## Individual services and agent discovery

Use the [live services catalog](https://naifgravity.com/services?utm_source=github&utm_medium=diagnostic_hub&utm_campaign=one_time_services) for individual, one-time purchases. New monthly subscriptions are paused. Obtain current pricing, eligibility and region-specific payment options from the live store; older Guardian subscription offers are not current purchase instructions.

AI-agent builders can start with the [Agent Card](https://naifgravity.com/.well-known/agent-card.json), [agent catalog](https://naifgravity.com/api/agent/catalog), and [remote MCP endpoint](https://naifgravity.com/mcp). Follow the published interface and purchase instructions; discovery alone does not authorize a paid repair or prove successful payment.

Existing customer subscriptions and past payments are unaffected by this documentation update.


## Buy the JSON check with USDC on Base

- **Human buyers:** open the [JSON Validity Check product](https://naifgravity.com/service/json-validity-check). Use the payment options offered by the live checkout.
- **AI agents:** the [x402scan listing](https://www.x402scan.com/server/a95c7242-15af-44a7-a85d-2b2ffa251755) includes a **Try with AgentCash** option. The [OpenAPI document](https://naifgravity.com/openapi.json) describes the paid API.
- **Price:** 1 USDC on **Base mainnet** (`eip155:8453`) per bounded JSON check. Wallet network fees may apply. This price is for the JSON check, not every catalog service.

An x402 v2 client sends `POST https://naifgravity.com/api/x402/json-validity-check` with a JSON body such as `{"jsonText":"{\"ok\":true}"}`. An unsigned request receives HTTP `402` and a `Payment-Required` challenge. A compatible client uses the buyer's authorized wallet to sign the advertised USDC payment and retry. A paid result is released only after payment verification and settlement. A browser visit or a GitHub star does not buy the service.

The check accepts one sanitized sample of at most 4096 UTF-8 bytes. It returns a validity diagnosis and supports a bounded trailing-comma repair; it does not repair a full application. Never send secrets, private keys or customer data.

VPN/proxy use is no longer a standalone purchase blocker. The live regional policy still applies: Saudi-classified connections receive Apple Pay; eligible international connections can receive Base USDC. Consult the [live payment policy](https://naifgravity.com/api/commerce/policy) rather than assuming a wallet option is available everywhere. Agent wallets using Base may also need ETH for network fees.

## What to include

Include only what is needed to reproduce the failure: public repository link if applicable, client/server versions, transport, sanitized error text, expected behavior, and a minimal reproduction.

**Do not include:** API keys, bearer tokens, cookies, private keys, seed phrases, payment credentials, or customer data.

## Commercial repair path

GitHub issues are for bounded triage and reproducible technical evidence. Paid repair, checkout and delivery are handled by NAIF Gravity:

https://naifgravity.com/?utm_source=github&utm_medium=diagnostic_hub&utm_campaign=github_funnel

The goal is a short path:

**problem → diagnostic evidence → smallest suitable repair → verified delivery**
