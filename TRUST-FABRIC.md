# NAIF Agent Trust Fabric

NAIF Agent Trust Fabric provides signed, point-in-time technical attestations for AI agents.

It does **not** rank agents, endorse them, predict reliability, or claim to be a security audit.

## Opt-in model

An agent must explicitly opt in on its own domain by publishing:

`/.well-known/naif-trust.json`

The manifest must set `consent: true` and must name the exact Agent Card URL. A2A and MCP endpoints used by the trust check must remain on the same host.

NAIF rejects loopback, private, link-local, reserved, and non-HTTPS targets. Network checks pin a validated public IP for the request and do not follow redirects.

## Trust Passport

Endpoint:

`POST https://naif-store-62-83-19-162.sslip.io/trust/passport`

A Trust Passport is signed with ES256 and currently lasts 24 hours.

It can attest only concrete technical facts observed at issuance, including:

- domain opt-in manifest reachable
- Agent Card reachable and parseable
- Agent Card signature field present
- declared A2A transport reachable
- A2A read endpoint responsive
- declared MCP transport reachable
- MCP initialize exchange responsive

The passport includes `notEndorsement: true` and `notSecurityAudit: true`.

## Delegation Preflight

Endpoint:

`POST https://naif-store-62-83-19-162.sslip.io/trust/preflight`

A preflight accepts a valid Trust Passport, re-checks the opted-in agent, and returns a new signed token valid for five minutes.\n\n### Traffic context\n\nWhen the agent declares A2A or MCP, the preflight also attaches the current privacy-preserving aggregate Traffic Control context for those route classes. Below the public minimum sample threshold the status remains `insufficient_aggregate_data`; absence of a signal is not treated as proof of health.

This is intended for a narrow workflow:

**discover → passport → preflight → delegate**

If the agent later fails during execution, NAIF Rescue Mesh can handle the failure path separately.

## Verification

Endpoint:

`POST https://naif-store-62-83-19-162.sslip.io/trust/verify`

Public verification keys:

`https://naif-store-62-83-19-162.sslip.io/.well-known/jwks.json`

NAIF's own current passport:

`https://naif-store-62-83-19-162.sslip.io/trust/passport.json`

Trust manifest:

`https://naif-store-62-83-19-162.sslip.io/.well-known/naif-trust.json`

## MCP tools

The live remote MCP now exposes:

- `get_agent_trust_passport`
- `delegation_preflight`
- `verify_trust_token`

alongside the existing FixGraph rescue tools.

Official MCP Registry identity:

`io.github.naief9961-tech/naif-fixgraph`

Current registry version: **1.3.0**

## Privacy and scope

The Trust Fabric stores passport IDs, hashes, bounded technical check results, and validity times. It is not intended to ingest secrets, private payloads, private keys, credentials, or personal data.

The result is a technical snapshot, not a guarantee of future behavior.
