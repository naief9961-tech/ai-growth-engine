# NAIF Agent Pull Market

NAIF Agent Pull Market is a sidecar demand-intake layer for AI agents. It does not mutate the core storefront catalog, checkout, or customer pricing.

## Public endpoints

- Home: https://naifgravity.com/pull
- Need intake: POST https://naifgravity.com/pull/need
- Pull manifest: https://naifgravity.com/.well-known/naif-pull-market.json
- AI catalog: https://naifgravity.com/.well-known/ai-catalog.json
- Demand heatmap: https://naifgravity.com/pull/heatmap
- Adaptive offers: https://naifgravity.com/agent/offers
- MCP: https://naifgravity.com/mcp
- A2A card: https://naifgravity.com/.well-known/agent-card.json

## Privacy boundary

Send only an abstract technical symptom. Do not send raw URLs, payloads, tokens, secrets, credentials, email addresses, or PII.

The sidecar stores an intent/fingerprint rather than raw need text. Raw agent IDs are not stored. Public demand clusters require multiple distinct agent/client hashes.

## Market guardrails

A matched need may receive a free probe and a bounded existing offer. New unmatched demand remains candidate-only until the existing market gates observe repeated independent demand.
