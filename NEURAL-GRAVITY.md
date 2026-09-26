# NAIF Neural Gravity Mesh

NAIF Neural Gravity Mesh is a shadow-only collective intelligence sidecar for NAIF Agent Gravity.

It observes privacy-safe aggregate signals from Pull Market, Agent Market Maker, storefront conversion events, trust, traffic, and continuity. It does not write to the core storefront, checkout, catalog, or pricing.

## Public read-only endpoints

- Manifest: https://naifgravity.com/.well-known/naif-neural-gravity.json
- State: https://naifgravity.com/neural/state
- Interference field: https://naifgravity.com/neural/interference
- Anonymized graph: https://naifgravity.com/neural/graph
- Shadow recommendations: https://naifgravity.com/neural/recommendations
- Health: https://naifgravity.com/neural-health

## Architecture

The sidecar computes:

- bounded intent feature vectors,
- deterministic cold-start neural expert heads,
- anonymized agent → intent → product graph relationships,
- pairwise demand interference states,
- drift detection,
- shadow-only recommendation candidates.

The neural layer starts in `FROZEN_COLD_START`. It does not promote itself to an action layer. Training is gated behind enough settled conversion labels and positive payment labels.

## Safety boundary

- Core catalog write: disabled
- Checkout write: disabled
- Pricing write: disabled
- External execution: disabled
- POST mutations: rejected
- Source databases are opened read-only
- Test sources are excluded from demand learning
- Raw Pull Market need text is never ingested because Pull Market stores only sanitized intent/fingerprint records

The output is advisory telemetry only.
