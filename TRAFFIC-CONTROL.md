# NAIF Agent Traffic Control

NAIF Agent Traffic Control is a privacy-preserving aggregate traffic-intelligence layer for AI agents.

It is designed to answer a narrow question before or during agent work:

> Are recent aggregate observations showing degradation for this class of API, RPC, MCP, A2A, or webhook route?

It does **not** rank providers, identify individual agents, or guarantee uptime.

## Live endpoints

- Manifest: https://naif-store-62-83-19-162.sslip.io/traffic/manifest.json
- Beacon intake: `POST /traffic/beacon`
- Preflight: `POST /traffic/preflight`
- Aggregate feed: https://naif-store-62-83-19-162.sslip.io/traffic/feed
- Aggregate map: https://naif-store-62-83-19-162.sslip.io/traffic/map.json

## Privacy model

The intake accepts only bounded route-class fields:

- route type: API, RPC, MCP, A2A, or webhook
- target class
- success or failure
- bounded failure class
- optional chain name
- optional two-letter region code
- coarse latency bucket
- bounded source label

Raw URLs, hosts, endpoints, payloads, request or response bodies, headers, tokens, secrets, cookies, IP addresses, emails, agent IDs, and user IDs are rejected by schema.

The service retains observations for 24 hours.

## Public aggregation gate

Public output requires at least **5 observations** in the same aggregate cluster.

Test observations are excluded from public output.

The feed explicitly reports that independent reporter count is unknown. Therefore the public values are **observed aggregates**, not a claim that five independent agents reported the issue.

Absence of a public signal does not mean a route is healthy.

## Status labels

The service can emit:

- `nominal_observed`
- `limited_observations`
- `degraded_observed`
- `severe_degradation_observed`
- `insufficient_aggregate_data`

These are descriptive summaries of recent aggregate observations. They are not provider scores.

## MCP tools

The public remote MCP exposes:

- `report_traffic_observation`
- `traffic_preflight`
- `get_agent_traffic_feed`

These are available alongside FixGraph rescue and Agent Trust Fabric tools.

Official MCP Registry identity:

`io.github.naief9961-tech/naif-fixgraph`

Current registry version: **1.2.0**

## Agent discovery

The signed A2A Agent Card advertises the skill:

`agent_traffic_intelligence`

The Rescue Mesh discovery beacon also points agents to the traffic manifest, feed, and map.

Current AGNTCY/OASF CID:

`baeareiguemjhhy7r7fo7da3r4fr4mr2fc3x3wdqt5w5yev2rb7y52phkhq`

## Intended lifecycle

**discover → traffic preflight → trust passport → delegation preflight → execute → rescue on failure → signed receipt**

This makes traffic intelligence one input into an agent's own decision process rather than a command from NAIF.
