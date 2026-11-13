# NAIF Gravity — GitHub Diagnostic Hub

NAIF Gravity helps developers and AI agents diagnose bounded integration failures without handing over private keys or rebuilding an entire stack.

## Choose a free diagnostic before buying a service

**Find the failure boundary first:** run a free [MCP discovery check](https://github.com/naief9961-tech/naif-gravity-mcp-diagnostics), use [NAIF JSON Rescue](skills/naif-json-rescue/SKILL.md) for local JSON syntax checks, or open [Micro Tools V2](https://naifgravity.com/micro-v2) for a bounded sample preview.

**Important:** the Micro V2 previews are free, but a separate **paid Micro V2 report checkout is not active**. When you need a paid result, select and review a *different* live service page with its own scope, current price and checkout:

- [JSON Validity Check](https://naifgravity.com/service/json-validity-check) — bounded JSON diagnosis.
- [API Response Shape Check](https://naifgravity.com/service/api-response-shape-check) — compare supplied response samples, not a live API probe.
- [JSON Normalize Mini](https://naifgravity.com/service/json-normalizer) — normalize a bounded JSON sample.
- [CSV Schema Audit Mini](https://naifgravity.com/service/csv-schema-audit) — bounded CSV consistency checks.

**[Browse the full problem-to-product directory →](PRODUCTS.md)** · [Live catalog and terms](https://naifgravity.com/services) · [Current agent catalog](https://naifgravity.com/api/agent/catalog)

GitHub documentation does not authorize any payment, production system access or automatic repair. Use only sanitized examples; never paste access tokens, private keys or customer records.

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

## Historical launch offer — ended 26 October 2026

The 12–26 October 2026 introductory discount is **expired** and must not be applied to new purchases. Use the [live catalog](https://naifgravity.com/services) and a separately approved quote to obtain the current price and availability. Neither a GitHub issue nor a free preview starts a paid repair.

The separately documented [x402 API catalog](https://naifgravity.com/api/x402/catalog) and [x402 payment manifest](https://naifgravity.com/.well-known/x402) describe distinct per-call APIs and supported payment protocols. Do not assume a particular payment method is available in every region.

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
