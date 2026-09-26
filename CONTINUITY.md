# NAIF Agent Continuity Exchange (ACE)

NAIF ACE is a signed, privacy-preserving handoff layer for moving an in-progress task between AI agents without forcing the receiving agent to restart from zero.

## Live endpoints

- Manifest: https://naif-store-62-83-19-162.sslip.io/continuity/manifest.json
- Schema: https://naif-store-62-83-19-162.sslip.io/continuity/schema.json
- Create capsule: `POST /continuity/capsule`
- Resume task: `POST /continuity/resume`
- Checkpoint: `POST /continuity/checkpoint`
- Handoff: `POST /continuity/handoff`
- Verify: `POST /continuity/verify`

## Capsule state

A capsule carries only bounded structured state:

- goal
- completed work
- verified facts
- remaining work
- constraints
- required capabilities
- next action

Text is sanitized before signing. Raw URLs, email addresses, IP addresses, bearer tokens, JWTs, private-key material, wallet-like identifiers, home-directory paths, and long token-like values are redacted.

## Stateless task transport

The signed capsule carries the sanitized task state.

The ACE server ledger does **not** store that task text or the capsule token. It stores only:

- capsule JTI
- parent JTI
- operation type
- chain depth
- state hash
- token hash
- optional recipient Agent Card hash
- issue and expiry times

Capsules expire after 24 hours and the chain depth is capped at 20 transitions.

## Checkpoint

A checkpoint adds only the progress delta:

- completed additions
- verified-fact additions
- remaining additions
- remaining-item indexes marked done
- constraint additions
- required-capability additions
- next action

A new signed capsule is issued with a parent pointer to the previous capsule.

## Handoff

A capsule can be handed off without binding it to a specific recipient.

When a recipient Agent Card URL is supplied, NAIF uses Agent Trust Fabric to require the recipient domain's explicit opt-in, issue a Trust Passport, perform a short-lived Delegation Preflight, and embed only bounded technical trust facts and current aggregate traffic context into the new handoff capsule.

This is a technical snapshot, not an endorsement or security audit.

## Resume

A receiving agent verifies and unpacks the capsule, obtains the sanitized state and next action, and can continue with another checkpoint or handoff.

## MCP tools

The live remote MCP exposes:

- `create_handoff_capsule`
- `resume_agent_task`
- `checkpoint_agent_task`
- `handoff_agent_task`
- `verify_handoff_capsule`

Official MCP Registry identity:

`io.github.naief9961-tech/naif-fixgraph`

Current registry version: **1.3.0**

## A2A

The signed A2A Agent Card advertises:

`cross_agent_continuity`

A2A clients can send a data part with `continuityAction` set to `create`, `resume`, `checkpoint`, `handoff`, or `verify`.

## Intended lifecycle

**discover → traffic preflight → trust passport → delegation preflight → execute → checkpoint → handoff → resume → rescue if needed → signed receipt**

ACE is additive. It does not modify storefront checkout, pricing, payments, V7 code, FixGraph data, or the existing Rescue / Trust / Traffic contracts.
