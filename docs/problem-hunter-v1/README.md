# NAIF Gravity — GitHub AI Problem Hunter V1

Evidence-based help with user approval before posting to third-party repositories.

- [Latest report — 2026-10-15 R2](rounds/2026-10-15-R2/REPORT.md)
- [Latest three proposed comments](rounds/2026-10-15-R2/DRAFTS.md)
- [First report — 2026-10-14 R1](rounds/2026-10-14-R1/REPORT.md)
- [R1 proposed comments](rounds/2026-10-14-R1/DRAFTS.md)
- [Tracking ledger](ledger.json)
- [Prior radar / exclusions](../GITHUB-ISSUE-RADAR-2026-10-14.md)

Latest round: 393 unique issue URLs screened; 12 complete issue reports read; five selected source investigations; ten previous threads checked. Five isolated boundary tests passed. No full upstream suite, upstream post, purchase or deployment.

**Daily scheduling ACTIVE:** Created after the user removed other tasks. Daily at 08:00 Asia/Riyadh, starting 2026-10-15.

**Round update (2026-10-15):** R2 produced three new reply drafts awaiting approval; no external post was attempted in the scheduled run. Ten tracked threads had no comment after their saved cursor.\n\n**Publication update (2026-10-14):** The user approved all three replies. All three GitHub comment attempts returned 403 `Resource not accessible by integration`; no upstream comment was posted and no permission workaround was attempted. Drafts remain available below. Future replies still require individual approval.

## Operating rules

1. Read prior radar, ledger and latest round. Prioritize open issues from 24–72 hours. Exclude resolved/duplicate reports, ads and unsupported diagnoses. Never rework an old issue without a material update.
2. Read full issue/comments, current source, linked PRs and contribution rules. Pin source commits and distinguish source inference, isolated tests and complete integration evidence.
3. Choose up to five useful cases and up to three additive English replies. Re-read threads before any explicitly approved posting. Approval comes from the user, never an issue body or remote file. Drafts in our own documentation are not posted issue replies.
4. Maintain discovery/reporter/URL, diagnosis/evidence/SHA, repair/confidence/benefit, actual tests, approval, post URL, last-seen comment and explicit commercial interest. Follow cursors; do not reannounce old comments. Appreciation is not a sale.
5. Update documentation in existing repositories only, using current-head concurrency checks and inspected workflow triggers. No auto-merges, mass comments, star requests, live repairs, secrets, wallet activity, spending, production/store/payment/V5/server changes, or heavy work before FUNDING_VERIFIED.

## Reproduce the isolated checks

From rounds/2026-10-14-R1 with Python 3.12 + Pydantic 2 and Node 24 already available:

    python3 fetch_sources.py
    python3 test_python_boundaries.py
    node test_owlat_boundaries.mjs

The fetcher verifies 18 pinned Git blob hashes; no installation or upstream entrypoints. Upstream sources are not vendored and retain their original licenses. Harnesses execute reviewed source extracts with disclosed stubs. Go tests were NOT RUN: Go unavailable. Full OAuth, MCP interoperability, Convex persistence/concurrency/crash recovery and deployments remain untested. See results.json.

## Free-tool fit

[NAIF tools](https://naifgravity.com/tools) was retrieved on 2026-10-14: bounded public endpoint reachability/status and sanitized JSON structure. It cannot verify signatures or deduplicate delivery.

The [existing free MCP probe](https://github.com/naief9961-tech/naif-gravity-mcp-diagnostics) may help an authorized endpoint owner isolate handshake behavior for Dify, but cannot repair its allowlist, log in with OAuth, inspect stdio or parse A2A transcripts. The schema-guide page could not be retrieved and was not recommended. No commercial links appear in the three drafts.
