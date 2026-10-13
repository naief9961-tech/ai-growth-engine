# NAIF Agent Gravity — Discovery

NAIF Agent Gravity exposes public, no-signup technical rescue and adaptive-demand interfaces for AI agents working on API, EVM RPC, webhook, MCP, automation, repository, and backend problems.

## Canonical domain

https://naifgravity.com

The previous sslip.io hostname remains a legacy fallback, but new discovery metadata points to the canonical domain.

## Official MCP Registry

Registry name: `io.github.naief9961-tech/naif-fixgraph`

Remote Streamable HTTP endpoint:

`https://naifgravity.com/mcp`

Repository metadata:

`server.json`

The MCP surface includes technical rescue, repair packets, trust/preflight, traffic intelligence, cross-agent continuity, adaptive offers, and sanitized agent-demand intake.

## A2A discovery

### A2A Registry payment-capabilities extension

The [signed A2A Agent Card](https://naifgravity.com/.well-known/agent-card.json) now includes the **optional A2A Registry v1 extension** (`capabilities.extensions`) with a `freemium` payment model, inbound `x402` and an official Base USDC settlement rail (`eip155:8453`). The original 17 A2A skills and card signature are preserved.

This extension is **discovery metadata**, not a wallet authorization, Coinbase Bazaar listing, payment receipt, or a guarantee that external A2A Registry caches have refreshed. A buyer agent must still use an authorized payment wallet and follow its own live 402 challenge or the eligible merchant quote/checkout instructions. Direct agent purchases work independently of whether any third-party Smart Order Router accepts a seller for paid dispatch.



Agent Card:

`https://naifgravity.com/.well-known/agent-card.json`

A2A HTTP+JSON interface:

`https://naifgravity.com/a2a/v1`

## October 13 update — Micro Tools V2 is live

Three **separate, one-time, sample-only Micro Tools V2** use the same NAIF Gravity domain and live agent catalog. There is no new store or recurring plan:

| Service | USD | New bounded artifact |
| --- | ---: | --- |
| JSON Validity Check | $1 | Syntax location, supported safe repair, duplicate-key warning, inferred schema and checksum |
| API Response Shape Check | $2 | Two-response comparison, added/removed fields, type differences and sample-based TypeScript/OpenAPI schemas |
| JSON Normalize Mini | $3 | Sorted output, optional trimming/indentation, change log and SHA-256 receipt |

**Free browser/sample preview:** [Micro Tools V2](https://naifgravity.com/micro-v2?utm_source=github&utm_medium=agent_discovery&utm_campaign=micro_tools_v2) · `POST https://naifgravity.com/api/micro-v2/preview` (max 4,096 UTF-8 bytes; sanitized input only). The preview does not initiate a paid checkout.

**Buyer-agent flow:** `GET /api/agent/catalog` → `POST /api/agent/quote` with a valid bounded sample → `POST /api/quote/accept` → select the listed *eligible* payment rail → verify payment → `POST /api/micro-v2/deliver` with `checkoutId` and private `deliveryToken`. The response exposes `preferredAgentPaymentRail`/`preferredAgentCheckoutEndpoint` for eligible international wallets, while Apple Pay is a separate human-authorization handoff. Both Base checkout IDs (`chk_...`) and TRON IDs (`tchk_...`) are supported by the delivery endpoint. Do not invent payment amounts or transfer funds without buyer authorization.

Separately, [x402 Base USDC paid APIs](https://naifgravity.com/.well-known/x402) keep their $1/$2/$3/$5 per-call prices. An unsigned `402 Payment Required` is **not** a sale. The region-specific policy and independent settlement verification remain mandatory. Paid V2 samples and artifacts are encrypted at rest and the bounded report is available after confirmed payment, not before.

---

## Current paid services and machine-checkout promotion

As of 12 October 2026, NAIF Gravity has an **automatic, limited launch offer on 14 scoped technical services**. A buyer or agent needs **no coupon**. The live service catalog supplies the discounted price directly, and the quote fixes the amount before checkout. It expires at **2026-10-26 05:40 UTC**, or after the **first 10 verified purchases of eligible launch services**, whichever comes first. **Do not hard-code promotional prices into a new checkout**; obtain the current quote and accept it explicitly. See the [full temporary pricing table](README.md#launch-offer--one-time-technical-services-october-1226-2026).

The **four current x402 v2 paid API services** remain $1 / $2 / $3 / $5 USDC on Base Mainnet, respectively. Their complete descriptions, machine-readable inputs and charged amounts are available from the canonical [x402 manifest](https://naifgravity.com/.well-known/x402), [API catalog](https://naifgravity.com/api/x402/catalog), and [OpenAPI spec](https://naifgravity.com/openapi.json). The manifest hides wallet-related entries from Saudi-classified connections according to regional policy; opening it on a Saudi device may return 404. A 402 challenge must be read before signing and is not evidence of payment.

The four x402 resources are separately listed in [402 Index](https://402index.io); [Agent402](https://agent402.tools) has accepted our origin with four tools and Base. **Coinbase Bazaar indexing and paid transactions have not been established** by an unsigned probe or a listing. Proposed x402 Lite lower-price endpoints are **not live**. A machine-checkout-capable engineering service still requires a verified paid Work fulfillment step; agent payment is not autonomous software repair.

## Live discoverability and catalog broadcast

Discovery is public and opt-in for clients; no unsolicited agent messages, fake traffic or automatic customer charges are sent.

1. Resolve the [A2A Agent Card](https://naifgravity.com/.well-known/agent-card.json) for verified skills and supported protocols.
2. Use the remote [MCP endpoint](https://naifgravity.com/mcp) with MCP `initialize` and `tools/list`; ordinary browser GET is not a valid MCP connectivity test.
3. Retrieve the [agent commerce catalog](https://naifgravity.com/api/agent/catalog) for current products and one-time offers, or the concise [AI catalog](https://naifgravity.com/.well-known/ai-catalog.json).
4. Check the [LLM guide](https://naifgravity.com/llms.txt) and [discovery beacon](https://naifgravity.com/rescue/beacon.json) for additional capability links.
5. Only follow the live quote, eligibility, checkout and payment instructions exposed for the visitor's region. A quote or started checkout is not proof of payment or permission to execute work.

External directory entries include the [Global A2A Registry](https://www.a2a-registry.org/agent/com.naifgravity.naif_technical_rescue_agent) and [official MCP Registry](https://registry.modelcontextprotocol.io/?q=io.github.naief9961-tech%2Fnaif-fixgraph). Registry pages may cache old card versions. The canonical domain's live machine-readable metadata is the source of truth.

An event-driven [GitHub Actions discovery broadcast](.github/workflows/agent-discovery-broadcast.yml) validates and publishes a new `server.json` version to the official MCP Registry using GitHub OIDC, with checksum-verified publisher binary and no recurring re-submission of unchanged versions. This does not by itself guarantee agent visits or customer conversions.

New monthly subscriptions are paused; currently published store purchases are individual and non-recurring. Existing subscriptions and historical payment records must remain untouched.

## Pull Market

Human/machine entry:

`https://naifgravity.com/pull`

Sanitized need intake:

`POST https://naifgravity.com/pull/need`

Pull Market manifest:

`https://naifgravity.com/.well-known/naif-pull-market.json`

AI discovery catalog:

`https://naifgravity.com/.well-known/ai-catalog.json`

## Free diagnostics

- API health: `POST /api/free-tools/api-health`
- RPC doctor: `POST /api/free-tools/rpc-doctor`
- Webhook tester: `POST /api/free-tools/webhook-test`

## Safety and privacy

- Do not send secrets, private keys, credentials, raw private payloads, URLs with tokens, or PII.
- Pull Market stores an intent/fingerprint instead of raw need text.
- Raw agent IDs are not stored.
- New unmatched demand remains candidate-only until repeated independent demand is observed.
- Repair packets and discovery calls do not auto-execute production changes.
- The core storefront catalog and checkout remain separate from discovery sidecars.

## Human entry points

Storefront: https://naifgravity.com/

Web3: https://naifgravity.com/web3

FixGraph: https://naifgravity.com/fix

Error Resolver: https://naifgravity.com/solve

Free diagnostics: https://naifgravity.com/tools
