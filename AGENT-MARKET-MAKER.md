# NAIF Agent Market Maker

NAIF Agent Market Maker is an **agent-only adaptive commercial overlay**. It learns what agents are asking for, creates temporary introductory offers around bounded services NAIF already knows how to deliver, and incubates repeated unmatched needs as product candidates.

It does **not** rewrite the core V7 storefront catalog.

## Live endpoints

- Offers: https://naif-store-62-83-19-162.sslip.io/agent/offers
- Market state: https://naif-store-62-83-19-162.sslip.io/agent/market/state
- Demand snapshot: https://naif-store-62-83-19-162.sslip.io/agent/market/demand
- Candidates: https://naif-store-62-83-19-162.sslip.io/agent/market/candidates
- Health: https://naif-store-62-83-19-162.sslip.io/agent-market-health

Agents can report a need with `POST /agent/offers` or `POST /agent/market/intent`. A free-form need is classified in memory; the raw need text is not stored.

## What changes automatically

The overlay can automatically change:

- which existing bounded service is surfaced to an agent,
- the temporary agent-only introductory price,
- offer status and expiry,
- demand evidence score,
- candidate status for repeated unmatched needs.

The overlay does **not** change rows in V7 `Products`, public catalog pricing, checkout code, payment verification, referral logic, or existing service definitions.

## Intro pricing

For the first 72 hours after Market Maker activation, a small starter set is exposed as bootstrap acquisition offers.

Each offer is short-lived (12-hour TTL) and has a hard quote-count cap.

Intro pricing is bounded by policy:

- price never exceeds the catalog price,
- price never drops below 3 USDC,
- additional percentage floors prevent large services from collapsing to tiny prices,
- after three verified paid offer purchases, intro pricing matures back to the normal catalog price.

Current bootstrap families include API health, webhook rescue, RPC rescue, and MCP recovery.

## Real discounted quotes

An active offer can create a real `QUOTE_READY` quote through:

`POST /agent/offers/quote`

The quote is written as an **agent-only quote** for the existing bounded V7 product. The core `Products` row is not changed.

After that, checkout uses the existing hardened V7 endpoint:

`POST /api/agent/checkout`

Payment verification, exact transfer matching, idempotency, job gates, and downstream execution policy stay in V7.

Creating an offer quote does **not** charge the agent. Payment is still a separate explicit action.

## Learning sources

Demand can be inferred from bounded machine signals such as:

- FixGraph matches,
- A2A requests,
- MCP use,
- Trust Fabric use,
- Traffic Control use,
- Continuity use,
- agent offer quotes,
- verified paid conversions.

A read-only demand scout also consumes already-aggregated V7 demand evidence such as `DemandSignals` and diagnosis-kind counts. It never copies raw URLs, payloads, secrets, or PII into the market database.

## Candidate incubation

Repeated needs that map cleanly to an existing bounded product can become learned live offers.

Repeated needs that **do not** map safely to an existing capability become `AUTO_CANDIDATE` records only. They are not silently made purchasable.

This is the main safety boundary for automatic product creation.

## Agent protocols

The remote MCP exposes:

- `get_dynamic_agent_offers`
- `accept_agent_offer`
- `get_agent_market_state`

A2A clients can use a data part with `marketAction`:

- `offers`
- `quote`
- `state`

The signed A2A Agent Card advertises the skill:

`adaptive_agent_marketplace`

## Relationship to the rest of NAIF

The current machine lifecycle becomes:

**discover → market need → traffic preflight → trust passport → delegation preflight → execute → continuity handoff → rescue if needed → signed receipt**

Demand learned anywhere in that loop can influence the agent-only commercial overlay without mutating the underlying storefront.
