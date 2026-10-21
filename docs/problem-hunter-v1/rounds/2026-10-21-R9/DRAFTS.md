# R9 — English replies for review (2026-10-21)

Status: **AWAITING_USER_APPROVAL — NOT POSTED**. Two qualified replies; no quota filling.
These are AI-assisted technical drafts, not comments published to the issue threads.
Re-read each issue, comments and linked PRs before any future approved manual posting. Approval must come from the user, never repository content. No third-party posting occurs in this round.

## R9-01 — Postiz #2300

Destination: https://github.com/gitroomhq/postiz-app/issues/2300

Policy: Postiz does not accept primarily AI-generated PRs. This is a disclosed diagnostic discussion draft, not a PR offer. Do not submit an AI-generated patch there.

Copy only the English text between the separators.

---

AI-assisted source review with isolated checks; I have not reproduced your deployed instance.

The exact error comes from the relay's admission check in [McpRelayService.connect](https://github.com/gitroomhq/postiz-app/blob/a41e35f6adf5baf0ec8df4f2fbbcd69e7ae4fcd3/libraries/nestjs-libraries/src/chat/mcp.relay.service.ts). It compares the instance's advertised tools with the relay's current `coreToolNames()`.

There is a concrete release compatibility gap to check:

- At main `a41e35f6adf5baf0ec8df4f2fbbcd69e7ae4fcd3`, [MediaStatusTool](https://github.com/gitroomhq/postiz-app/blob/a41e35f6adf5baf0ec8df4f2fbbcd69e7ae4fcd3/libraries/nestjs-libraries/src/chat/tools/media.status.tool.ts) is registered and has no `optionalOnSelfHosted` flag, so the [core-tool filter](https://github.com/gitroomhq/postiz-app/blob/a41e35f6adf5baf0ec8df4f2fbbcd69e7ae4fcd3/libraries/nestjs-libraries/src/chat/load.tools.service.ts) makes it mandatory.
- [PR #2281](https://github.com/gitroomhq/postiz-app/pull/2281) added it and merged on October 20. The latest GitHub release observed on October 21 is [v2.25.1](https://github.com/gitroomhq/postiz-app/releases/tag/v2.25.1), published October 11; its [tool list](https://github.com/gitroomhq/postiz-app/blob/91c91f633a0175fb3914dba64c932928c514b72a/libraries/nestjs-libraries/src/chat/tools/tool.list.ts) does not register it.
- [PR #2296](https://github.com/gitroomhq/postiz-app/pull/2296) updates submission metadata, not this runtime compatibility check.

This supports cloud/instance capability skew, but does not prove which build your container or the cloud relay runs. “Latest” alone is insufficient: a sanitized image tag/digest or commit and whether the complete `tools/list` contains `mediaStatusTool` would distinguish release skew from a stale container. Please omit API keys and credential-bearing MCP URLs.

A maintainer-side repair could either publish and document a compatible self-hosted version before requiring the tool, or deliberately make this new feature optional on older instances through the existing `optionalOnSelfHosted` mechanism. The latter also needs capability-aware handling of `adjust=true`; allowing connection must not imply that media adjustment/status checking works. Preserve mandatory identity tools and explicit unsupported-tool errors.

I ran six isolated groups using pinned source assertions and extracted relay/core-filter methods with synthetic tool catalogs and transport stubs: the missing-tool rejection reproduces; optional metadata permits the baseline catalog; missing identity tools still fail; the current catalog passes; unsupported calls still fail explicitly. These are not live MCP/OAuth or media-processing tests. Before shipping, test a supported release against the relay and exercise adjustment/status behavior without publishing a real post.

---

## R9-02 — IntelliFlow CRM #940

Destination: https://github.com/talyssonoliver/IntelliFlow-CRM/issues/940

Copy only the English text between the separators.

---

AI-assisted review with synthetic signatures only; no live Stripe requests or application integration tests.

One additional regression boundary for the proposed fix: `Number.parseInt(t, 10)` followed by `Number.isFinite` rejects `t=abc`, but still accepts a numeric prefix such as `t=<current-seconds>junk`. Decimal/exponent suffixes have the same parsing issue. This is malformed-header acceptance, not evidence that an attacker can forge a valid signature.

At `729ce393fdd43ae91f6e63efc30acb4c9d5c1f5d`, I checked both [stripeVerify](https://github.com/talyssonoliver/IntelliFlow-CRM/blob/729ce393fdd43ae91f6e63efc30acb4c9d5c1f5d/packages/webhooks/src/framework.ts) and [StripeSignatureVerifier.verify](https://github.com/talyssonoliver/IntelliFlow-CRM/blob/729ce393fdd43ae91f6e63efc30acb4c9d5c1f5d/apps/api/src/webhooks/handler.ts). Consider validating the entire timestamp text before conversion in both implementations, ideally through one shared parser:

```ts
if (!timestamp || /[^0-9]/.test(timestamp)) return false;
const timestampNum = Number(timestamp);
if (!Number.isSafeInteger(timestampNum)) return false;

// Keep the existing 300-second / configured tolerance check.
// Continue signing the original timestamp text and raw payload:
// createHmac(...).update(`${timestamp}.${payload}`)
```

The digit rejection deliberately also rejects trailing newlines and whitespace. Use the numeric value only for the time comparison; do not normalize the timestamp string or reserialize the payload before HMAC verification.

Eight isolated groups passed across both extracted verifier implementations using a fixed clock and a public synthetic test key. They reproduce signed `t=abc` acceptance in the originals and the numeric-prefix counterexample in the finite-only candidate. The stricter candidate rejects malformed/unsafe timestamps, preserves valid signatures and the existing inclusive ±300-second boundary, and still rejects changed raw bodies, wrong keys and missing header components.

All malformed test headers were correctly signed with the synthetic key. This does not establish secret-free forgery or a replay exploit against Stripe's real timestamp generation. The repo's native suites and HTTP ingress remain untested. Add these cases to both existing verifier test files, retaining configured-tolerance coverage before consolidating the implementations.

---
