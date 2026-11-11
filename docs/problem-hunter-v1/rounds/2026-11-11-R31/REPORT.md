# R31 — 11 November 2026: one additive Withings regression draft

Checked 2026-11-11T05:07:28.948Z. Base ai-growth-engine SHA: `c10b5a9961f54cbac87de0d69914ad583f3c936d`.

## Work completed

- 70 results from seven capped searches; **63 unique URLs screened by title and available description**. Five complete candidate descriptions, comment collections and timelines read.
- **One completed additive source investigation**, three exploratory source checks, one existing-fix PR diff review. Six isolated assertion groups passed. No upstream build/full suite, MCP integration, Windows/OAuth, health-account or payment tests.
- 45 prior tracked discussions checked, plus review/inline streams for all four tracked PRs. **No new developer replies or state changes after saved checks.**
- One additional existing NAIF comment reconciled on OpenBot7357. No subsequent reply. One English draft pending user approval; zero third-party comments, PRs or messages sent.

Search window: created since 2026-11-08, open issues; topics MCP, A2A, x402, webhook, schema, API and "GitHub Actions", sorted newest, limit10 each. This is capped sampling, not exhaustive coverage. Promotional offers, copied course reports, feature epics and unrelated cases were excluded. [Screening list](SCREENING.md).

## Selected case — Withings #31

[Original issue](https://github.com/davidmosiah/withings-mcp/issues/31), author **chaputjp**, created **2026-11-11T04:45:59Z**. Open; zero comments and no linked timeline PR at final check. Not previously recorded.

The author reports Windows OAuth URL truncation, UTC/local-day errors and misleading confidence for empty data. Our additive finding is narrower: **a failed heart-domain request is recorded but omitted from daily confidence aggregation**.

At commit `7b0b1ff9359478d89d7e9484e482df6d49638c86`, `dailyStats` produces `has_heart_error`; `missing_or_failed.heart` exposes it. The confidence array contains only the other three flags. A synthetic heart-only failure yielded `heart: true` plus `confidence: "high"`.

**Repair tested:** add `stats.has_heart_error` to that existing array. Keep successful-domain data and public error flags intact. Empty-success coverage, timezone/day-window semantics and Windows launching require separate changes; this candidate does not claim to solve them.

**Confidence:** high in this pinned-source defect and isolated correction; no live-deployment claim. **Expected benefit:** makes the API summary's confidence consistent with its own domain-failure flags; provides a missing regression alongside the reporter's existing findings.

### Evidence

- [src/services/summary.ts](https://github.com/davidmosiah/withings-mcp/blob/7b0b1ff9359478d89d7e9484e482df6d49638c86/src/services/summary.ts) — commit `7b0b1ff9359478d89d7e9484e482df6d49638c86`, blob `d967e86800f59367231f53f88a6f88d885f05f4b`.
- [src/services/measures.ts](https://github.com/davidmosiah/withings-mcp/blob/7b0b1ff9359478d89d7e9484e482df6d49638c86/src/services/measures.ts) — commit `7b0b1ff9359478d89d7e9484e482df6d49638c86`, blob `9cbf4e092acebc001924dd798b0cb8dea2e96a82`.
- [src/services/redaction.ts](https://github.com/davidmosiah/withings-mcp/blob/7b0b1ff9359478d89d7e9484e482df6d49638c86/src/services/redaction.ts) — commit `7b0b1ff9359478d89d7e9484e482df6d49638c86`, blob `d16e82985a7e471d18cf185358b4c0d462a2b6f3`.
- [scripts/summary-fixture-test.mjs](https://github.com/davidmosiah/withings-mcp/blob/7b0b1ff9359478d89d7e9484e482df6d49638c86/scripts/summary-fixture-test.mjs) — commit `7b0b1ff9359478d89d7e9484e482df6d49638c86`, blob `dd71de8a026091b315cffc4cc5c90730fc24eeee`.
- [package.json](https://github.com/davidmosiah/withings-mcp/blob/7b0b1ff9359478d89d7e9484e482df6d49638c86/package.json) — commit `7b0b1ff9359478d89d7e9484e482df6d49638c86`, blob `578e51c70731abad3184763453e2b68a41443412`.

Read root AGENTS.md and CONTRIBUTING.md. Entire returned PR listing (27 entries) inspected; all three open PR file lists (#15/#21/#29) inspected and none changes summary.ts or its summary fixture. Keyword PR search also reviewed. No matching confidence fix was found. Existing summary fixture checks successful results and sleep-error logging, not heart-only confidence.

[Full English review text](DRAFTS.md) · [Actual test method, reproduction harness and limits](TESTS.md).

## Four candidates withheld

- [[Bug]: MCP server validation errors surface to the agent as a fake connection failure](https://github.com/nightly-labs/openbot/issues/7395) — openbotgit[bot], 2026-11-11T04:42:12Z. Validation-to-connection-error symptom is credible, but exact mapping boundary not established. Read pinned local-mcp-bridge.ts, mcp-tools.ts, mcp-effects.ts and acp-client.ts. The bridge preserves isError from result.success; the reported wording may come from the external ACP provider. No protocol capture or matching provider source establishes ownership. No tested fix or draft. Confidence: Low on root cause; high on need for boundary evidence.

- [[Bug]: core schemas reject the 402 a sign-in-only (auth-only) SIWX route sends: PaymentRequired.accepts requires at least one entry](https://github.com/x402-foundation/x402/issues/4206) — A1igator, 2026-11-10T07:13:41Z. Reporter already supplies schema rejection, reproduction and HTTP/MCP distinction. Read current x402MCPClient.ts; schema-policy choice remains a maintainer decision. No additional tested schema/transport solution or draft. Confidence: Report-supported, not independently reproduced.

- [to_script emits bare `inf`/`nan`, so a schema inferred from a column with infinities writes a file that fails to import](https://github.com/unionai-oss/pandera/issues/2659) — Krushil-Dhankecha, 2026-11-11T04:55:58Z. Reporter already supplies failing examples and repr diagnosis. Current common_io.py corroborates repr rendering; no additive tested repair. Related PR2656 appears in listing and addresses pandas scalar imports, not proof that this issue is fixed. Confidence: High for source corroboration; no runtime validation.

- [[Bug] MCP read.uri retains array items after string override, causing Gemini-compatible API 400](https://github.com/volcengine/OpenViking/issues/7424) — codinglemom, 2026-11-11T04:47:22Z. Existing PR7425 at b8a044fa5a0674d282663d01e60f2b85bed0db71 removes stale items after string override and strengthens existing schema tests. Full two-file diff read. Its runtime/provider results are author's claims, not rerun here. No duplicate reply. Confidence: High for existing implementation and regression assertions; runtime untested.

Exploratory source pins:
- OpenBot: `26fc43174f1caf2a98a11909c7fbb7a011e12241`; src/backend/local-mcp-bridge.ts, agent/mcp-tools.ts, mcp-effects.ts, acp-client.ts. Bridge source is not the external Devin provider's error mapper. Latest30PRs inspected; absence is not an exhaustive no-fix claim.
- x402: `d3eb19d018801c190be58acf4017e76f8bcf6d45`; typescript/packages/mcp/src/client/x402MCPClient.ts. No wallet, signature or payment used; latest30PRs inspected.
- Pandera: `0292915e3321e83ee19380d7329788b7ead05291`; pandera/io/common_io.py, blob `70d0ef7f740b7bde70aef0e02105535c57324cc7`. Latest30PRs inspected.
- OpenViking: PR7425 head `b8a044fa5a0674d282663d01e60f2b85bed0db71`; changed source and regression assertions read, not run.

## Follow-up and deduplication

Verified [your OpenBot comment6786447306](https://github.com/nightly-labs/openbot/issues/7357#issuecomment-6786447306), posted **2026-11-11T03:49:00Z**. This is an existing manual contribution, not a post by this round. It distinguishes omitted ACP stdio configurations with workingDirectory from a separate ripgrep timeout. Added a follow-up entry and cursor; **do not repost**. Current issue is open; no later comment. We did not revalidate the comment's proposed Windows workaround and make no repair claim.

All45 prior cursors and history preserved; new checks recorded. Four PR review streams have no new events after prior check times. No new developer reply, request for paid help, sale or verified commercial lead.

## Free tools and scope

Re-read [NAIF tools](https://naifgravity.com/tools) on11November and the diagnostics README at `292b82c5cbf4ac2d87962ca2b4824fd8bece5dba`. Public reachability and sanitized JSON checks do not diagnose the Withings confidence calculation. MCP Doctor's discovery probe does not invoke tools/call, test stdio/OAuth or repair A2A. **No referral or paid offer is included in the draft.**

## Documentation integrity and limitations

Mandatory radar, README, ledger and R30 report read at the base SHA. Recursive tree confirms only root AGENTS applies. All8workflow definitions read: only three have push triggers, scoped to server.json/discovery/workflow metadata; these docs do not match. Other workflows are scheduled/manual/PR/comment driven. No workflow invoked or modified. Unrelated bounty/payment instructions were not executed.

Atomic expected-head update limited to README, ledger and R31 Markdown reports. No third-party writes, production/payment/V5/server changes, package installs, new projects or spending. Initial repository-metadata requests with a trailing slash failed; corrected canonical read URLs succeeded. Source-file writing initially added one trailing newline; it was removed, all three source blob hashes matched after restoring the two local import suffixes, and tests reran successfully.

## Owner action

Review R31-01 in DRAFTS.md. It is **not posted**; explicit approval is required before any external publication, followed by another issue/PR check. There are no other new texts to copy this round. The four withheld cases are not recommended for comments.
