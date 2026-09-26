# NAIF FixGraph — Agent Discovery

NAIF FixGraph exposes public, no-signup technical rescue interfaces for AI agents working on API, EVM RPC, and webhook failures.

## Official MCP Registry

Registry name: `io.github.naief9961-tech/naif-fixgraph`

Remote Streamable HTTP endpoint:

`https://naif-store-62-83-19-162.sslip.io/mcp`

The MCP server exposes:

- `resolve_technical_error` — sanitize and match an error to safe repair packets.
- `get_repair_packet` — retrieve a bounded repair packet for a known FixGraph slug.
- `list_fix_topics` — list the current public FixGraph problem topics.

## A2A discovery

Agent Card:

`https://naif-store-62-83-19-162.sslip.io/.well-known/agent-card.json`

A2A HTTP+JSON interface:

`https://naif-store-62-83-19-162.sslip.io/a2a/v1`

The agent is stateless for direct technical-rescue requests. Streaming and push notifications are intentionally disabled.

## Safety and privacy

- Do not send secrets, private keys, credentials, raw private payloads, or PII.
- Incoming technical error text is sanitized by FixGraph before matching.
- Raw error text is not stored by the Agent Gateway.
- Repair packets do not auto-execute changes.
- Paid work always requires human approval.

## Human entry points

FixGraph: https://naif-store-62-83-19-162.sslip.io/fix

Error Resolver: https://naif-store-62-83-19-162.sslip.io/solve

Free diagnostics: https://naif-store-62-83-19-162.sslip.io/tools
