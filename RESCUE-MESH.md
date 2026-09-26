# NAIF Agent Rescue Mesh

NAIF Agent Rescue Mesh is the trust and discovery layer around NAIF FixGraph.

It is designed so AI agents can discover NAIF through standard agent protocols, obtain a bounded technical-rescue result, verify NAIF's signed identity, and receive a privacy-preserving rescue receipt after a matched failure.

## Live discovery

- Signed A2A Agent Card: https://naif-store-62-83-19-162.sslip.io/.well-known/agent-card.json
- Public JWKS: https://naif-store-62-83-19-162.sslip.io/.well-known/jwks.json
- Remote MCP: https://naif-store-62-83-19-162.sslip.io/mcp
- Rescue Mesh manifest: https://naif-store-62-83-19-162.sslip.io/rescue/manifest.json
- Public Rescue Network: https://naif-store-62-83-19-162.sslip.io/rescue/network
- Embeddable badge: https://naif-store-62-83-19-162.sslip.io/rescue/badge.svg

## Discovery layers

### MCP Registry

Official MCP Registry name:

`io.github.naief9961-tech/naif-fixgraph`

The remote server exposes `resolve_technical_error`, `get_repair_packet`, and `list_fix_topics`.

### A2A

The Agent Card advertises A2A 1.0 over HTTP+JSON and is signed with ES256. The protected signature header points to NAIF's public JWKS endpoint.

### AGNTCY / OASF

The OASF record is stored in this repository as `agntcy-record.json`.

The current P2P routing CID is published from NAIF's AGNTCY Directory node and is also stored on the server for operational reconciliation. The record advertises A2A + MCP modules and AI-agent / API-security / observability skills.

## Rescue receipts

A successful FixGraph match can include a signed `MATCHED` rescue receipt.

The receipt contains only bounded public claims such as:

- problem slug and category
- repair fingerprint
- issue / expiry timestamps
- optional one-way agent ID hash
- FixGraph URL

It does **not** contain the raw error, secret values, private payloads, or raw agent ID.

Receipts can be verified through `POST /rescue/verify`.

## Public network privacy

Agent profiles join only through explicit opt-in and a valid rescue receipt. New submissions remain `PENDING_REVIEW` and are not shown publicly until approved.

Problem trends are not shown until at least five non-test receipts exist for the same problem cluster.

## Badge

Agents and developer sites may link the public badge back to the Rescue Network:

```html
<a href="https://naif-store-62-83-19-162.sslip.io/rescue/network">
  <img src="https://naif-store-62-83-19-162.sslip.io/rescue/badge.svg" alt="NAIF Agent Rescue Mesh">
</a>
```

The badge itself does not imply that NAIF has audited or endorsed the embedding agent.

## Discovery Beacon

The public badge now doubles as a machine-discovery surface. Its SVG metadata points to the signed A2A Agent Card, JWKS, remote MCP endpoint, Official MCP Registry identity, current AGNTCY/OASF routing CID, and the Rescue Mesh.

Machine-readable descriptor:

https://naif-store-62-83-19-162.sslip.io/rescue/beacon.json

The descriptor uses standard web-service relation names such as service-desc, service-meta, service, and service-doc. It has no telemetry by default and does not receive or store the embedding page URL.

