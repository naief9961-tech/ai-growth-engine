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

Agent Card:

`https://naifgravity.com/.well-known/agent-card.json`

A2A HTTP+JSON interface:

`https://naifgravity.com/a2a/v1`

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
