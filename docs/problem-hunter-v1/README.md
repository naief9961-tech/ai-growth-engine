# NAIF Gravity — GitHub AI Problem Hunter V1

Evidence-based help with user approval before posting to third-party repositories.

- [Latest report — 2026-10-21 R9](rounds/2026-10-21-R9/REPORT.md)
- [R9: two English drafts awaiting approval](rounds/2026-10-21-R9/DRAFTS.md)
- [R9 isolated checks and limits](rounds/2026-10-21-R9/TESTS.md)
- [Previous report — 2026-10-20 R8](rounds/2026-10-20-R8/REPORT.md)
- [R8 historical draft — manually posted, do not repost](rounds/2026-10-20-R8/DRAFTS.md)
- [R8 isolated checks and limits](rounds/2026-10-20-R8/TESTS.md)
- [Previous report — 2026-10-19 R7](rounds/2026-10-19-R7/REPORT.md)
- [Previous report — 2026-10-18 R6](rounds/2026-10-18-R6/REPORT.md)

- [Previous follow-up — 2026-10-17: Tianshu withdrawal and Noir candidate](rounds/2026-10-17-R5/FOLLOWUP-2026-10-17.md)
- [Noir #3078 patch and 28 unexecuted native regression cases](rounds/2026-10-17-R5/NOIR-3078-CANDIDATE.md)

- [Previous report — 2026-10-17 R5](rounds/2026-10-17-R5/REPORT.md)
- [R5 reply withdrawn after maintainer declined the fix](rounds/2026-10-17-R5/DRAFTS.md)
- [R5 isolated tests](rounds/2026-10-17-R5/TESTS.md)
- [R5 discovery audit](rounds/2026-10-17-R5/SCREENING.md)
- [Previous report — 2026-10-16 R4](rounds/2026-10-16-R4/REPORT.md)
- [R4 historical comment](rounds/2026-10-16-R4/DRAFTS.md)
- [R4 isolated evidence](rounds/2026-10-16-R4/TESTS.md)
- [Previous report — 2026-10-16 R3](rounds/2026-10-16-R3/REPORT.md)
- [Previous report — 2026-10-15 R2](rounds/2026-10-15-R2/REPORT.md)
- [First report — 2026-10-14 R1](rounds/2026-10-14-R1/REPORT.md)
- [R1 proposed comments](rounds/2026-10-14-R1/DRAFTS.md)
- [Tracking ledger](ledger.json)
- [Prior radar / exclusions](../GITHUB-ISSUE-RADAR-2026-10-14.md)

Historical round R4: 398 unique URLs screened (86 previously screened in R3); 11 full candidate reads; three source investigations. One open reply draft, one policy hold, one withdrawn after closure. Twenty-one isolated assertion groups passed (six source-extracted baseline groups; fifteen candidate/model groups); no upstream full suite. No external comment sent. The three R3 manual posts are verified; no subsequent developer reply or commercial request was present at the latest check.

Historical R3 round: 215 unique issue URLs screened; nine full candidate reads; three source investigations; 16 tracked/draft threads checked. Eight isolated cases passed (two source-extracted baseline reproductions; six candidate/design model cases). No upstream suite or external post this round.

**Daily scheduling ACTIVE:** Created after the user removed other tasks. Daily at 08:00 Asia/Riyadh, starting 2026-10-15.

**Round update (2026-10-15):** R2 produced three new reply drafts awaiting approval; no external post was attempted in the scheduled run. Ten tracked threads had no comment after their saved cursor.

**Publication update (2026-10-14):** The user approved all three replies. All three GitHub comment attempts returned 403 `Resource not accessible by integration`; no upstream comment was posted and no permission workaround was attempted. Drafts remain available below. Future replies still require individual approval.

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

## R3 update — 2026-10-16

- Reconciled three user-posted comments from 15 October (VS Code, A2A Python, Trinity) with exact URLs in the ledger. No duplicate comments sent.
- New direct technical acknowledgement from parisbs; successor #180 retains configuration/isolation criteria. Trinity PR #3750 merged into dev; live acceptance remains pending. No commercial request.
- All three R3 comments were subsequently posted manually by the user and verified; see the ledger and R4 report for exact URLs. This does not authorize other comments. AGNT does not accept outside auth PRs; the comment provides reproduction evidence only.
- R2 correction: VS Code's slash retry does not establish the cause of general restart disablement; registry detail serialization is another unresolved observation. REST SSE in A2A Python uses Parse, not ParseDict; the manually posted comment correctly states this.
- [Local evidence and limits](rounds/2026-10-16-R3/TESTS.md).

## R4 manual publication — 2026-10-16

The user manually published the sole R4 reply at 08:52:54 Asia/Riyadh: [MCP Git #298](https://github.com/MementoRC/mcp-git/issues/298#issuecomment-6209070203). Verified in GitHub; no subsequent developer reply or commercial request was present at verification. The ledger cursor is 6209070203. R4's draft is now a historical copy and must not be posted again.

## R5 update — 2026-10-17

316 unique URLs screened from 320 capped results; seven complete candidate reads; one new source investigation (Tianshu #507). Eight isolated assertion groups passed; no full suite, typecheck, desktop or provider validation. At the initial check one additive reply was pending user approval; it was subsequently withdrawn after the maintainer declined the fix and closed #507. No external comment sent.

Seventeen tracked threads checked. Four new comments: Noir's maintainer agreed with the technical diagnosis and invited a PR; an Engram contributor described reproduction and tests. Separately verified merged PRs: [Engram #1915](https://github.com/Gentleman-Programming/engram/pull/1915) and [MCP Git #304](https://github.com/MementoRC/mcp-git/pull/304). Their tests were not rerun, no deployed release verified, and no causal credit claimed. No explicit commercial request. Comment cursors and outcome history updated in the ledger.

## R5 follow-up — 2026-10-17

Tianshu #507 was closed as not_planned at 05:14:16Z. The owner confirmed the reported mechanism but declined a fix; this is not a repair. R5-01 is withdrawn and must not be posted. The ledger cursor is 6230037956.

Noir's existing PR invitation was followed with a local eight-file inline candidate and 28 authored Crystal regressions. Patch applicability, source hashes, fixture parsing/parity and eight-file manifest agreement were checked. Crystal/shards/just/Docker are unavailable; no native tests, build or full suite ran. Candidate is held for native validation, with no upstream publication or commercial request.

## R6 update — 2026-10-18

237 unique URLs screened from 240 capped results; eight complete candidate reads; three completed source investigations and one exploratory source read. Three review drafts, no external publication. Eleven isolated checks passed (four source-extracted baseline/guard checks and seven candidate/model checks); no upstream suite. Eighteen prior tracked threads checked with no new comments after saved cursors and no explicit commercial interest. WP PR #3 merged during review but #6 remains unresolved; Tududi #263 has another agent's active claim, so recheck its work before posting.


## R7 update — 2026-10-19

[Latest report](rounds/2026-10-19-R7/REPORT.md) · [Two review drafts](rounds/2026-10-19-R7/DRAFTS.md) · [Evidence and tests](rounds/2026-10-19-R7/TESTS.md).

199 unique URLs screened, seven candidate threads read, two completed source investigations, eight isolated groups passed. Twenty-one previous threads checked: one new maintainer comment and three newly verified merged PRs; four issues closed. Merge and maintainer reports are distinguished from independent acceptance tests. Remaining Retry-After/concurrent-retry limits are recorded; no causal credit or commercial request claimed. Comment cursors advanced only for new evidence. No external publication in R7.

R6's three drafts were subsequently approved and published; see [R6 publication evidence](rounds/2026-10-18-R6/PUBLICATION.md). Do not post them again. R7 drafts need their own explicit approval.


## R8 update — 2026-10-20

155 unique URLs screened, six candidate threads read, one completed investigation and two exploratory source reads. One Woodhouse #29 review draft; eight isolated checks passed; no upstream integration suite or external publication. Twenty-three tracked threads checked: one new technical update on A2A #1341 (PR #1354 includes REST SSE) and Cockpit #564 closed after PR #573 merged. No duplicate comment and no commercial request. Cursor/history preserved. [R8 report](rounds/2026-10-20-R8/REPORT.md).

R7-01 is superseded by merged PR #573; R7-02 was manually published and verified. **Do not repost either R7 draft.** R8-01 was subsequently posted manually and verified in R9; do not repost.

## R9 update — 2026-10-21

201 distinct URLs screened from 220 capped results; six complete candidate-thread reads, one related-body check and two completed source investigations. Two new English drafts (Postiz #2300 and IntelliFlow CRM #940) await approval. Fourteen isolated groups passed; no upstream suite or live deployment test. No third-party publication in this round.

Twenty-four prior tracked threads checked: the user's [Woodhouse comment](https://github.com/recursive-cloud/woodhouse/issues/29#issuecomment-6283913029) was verified and its cursor advanced. **R8-01 is historical; do not repost.** Trinity #3749 newly closed; its R3 merge is not new and live acceptance remains unverified. No new developer reply or explicit commercial inquiry. [R9 report](rounds/2026-10-21-R9/REPORT.md).
