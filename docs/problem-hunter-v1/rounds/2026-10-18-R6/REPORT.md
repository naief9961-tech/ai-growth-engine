# NAIF Gravity — R6, 2026-10-18

Reviewed through 2026-10-18T05:04:01Z. Documentation only; no third-party comments, PRs or messages sent.

## Results

- 240 capped search results across eight queries; **237 distinct URLs screened** by title/body.
- Eight complete candidate issue/comment/timeline reads; **three completed source investigations**, one additional exploratory source read (Waygate). This is not 237 full investigations.
- **Three selected issues and three English drafts**, not five filler selections.
- **11 isolated checks passed**: four source-extracted baseline/guard checks, seven candidate/model checks. No complete upstream suite, deployments, credentials or provider operations.
- 18 prior tracked threads read, **zero new comments after stored cursors**, no state changes, no new explicit commercial requests.
- Existing ledger history preserved. The new Tududi scanner claim is not a developer response to us, customer interest, or permission to act.

## Selected issues

### 1. [reeenatamc/wp-content-agent #6](https://github.com/reeenatamc/wp-content-agent/issues/6)

Reporter: reeenatamc. Created: 2026-10-18T04:55:33Z. Open at check.

**Diagnosis:** The request loop calculates exponential delay without reading Retry-After. The updated PR #3 implementation still has this behavior after its merge.

**Proposed repair:** Carry response-derived delay into the next retry; support seconds/HTTP-date, malformed fallback, bounded parsing and stop/defer beyond wait budget. Preserve existing POST retry eligibility.

**Confidence:** High for source mechanism; moderate for unintegrated delay-policy candidate.

**Likely benefit:** High: cap semantics, date/oversized-header cases, and preservation of POST safety add concrete boundaries.

**Actual validation and limits:** 6 Python cases: 2 extracted baseline/guard checks and 4 standalone delay-policy cases. Integrated helper, native pytest and WordPress/MCP untested.

**Source evidence:** See exact commit/blob hashes in ledger entry and [test source manifest](manifest.json).

**Review draft:** R6-01 in [DRAFTS.md](DRAFTS.md). Approval pending; no external publication.

### 2. [opena2a-org/agent-identity-management #772](https://github.com/opena2a-org/agent-identity-management/issues/772)

Reporter: thebenignhacker. Created: 2026-10-18T04:29:51Z. Open at check.

**Diagnosis:** list_skills GETs an unregistered global path; server exposes the current-agent route with ownership checks and the same skills envelope.

**Proposed repair:** Call GET /api/v1/a2a/agents/{self.agent_id}/skills through _make_request, preserving path signing and auth error propagation; add SDK/router contract tests.

**Confidence:** High for pinned route mismatch and minimal SDK candidate; authorization integration untested.

**Likely benefit:** Medium: validates response compatibility and identifies signing/auth regression boundaries beyond the reporter's route fix.

**Actual validation and limits:** 3 Python cases: extracted wrong-route reproduction, candidate populated/empty response behavior, and synthetic authorization-error propagation. Go/signing/full SDK untested.

**Source evidence:** See exact commit/blob hashes in ledger entry and [test source manifest](manifest.json).

**Review draft:** R6-02 in [DRAFTS.md](DRAFTS.md). Approval pending; no external publication.

### 3. [Danathar/tududi #263](https://github.com/Danathar/tududi/issues/263)

Reporter: Danathar. Created: 2026-10-18T04:17:39Z. Open at check.

**Diagnosis:** A unique event insert returns null even for a failed existing event, and handleWebhook immediately classifies it as a completed duplicate.

**Proposed repair:** Only terminal events suppress replay; design database-backed exclusive retry claim plus crash recovery. Update model validation if introducing processing. Make partial side effects idempotent/outbox-backed.

**Confidence:** High for poisoned-redelivery control flow; moderate for proposed repair design, no ORM patch validated.

**Likely benefit:** High: exposes processing-state validation and concurrency/partial-side-effect boundaries beyond simple existing-row retry.

**Actual validation and limits:** 2 Node groups: source-extracted failed redelivery reproduction and 8-contender exclusive-claim design model. No Sequelize/database/provider/signature/concurrency integration.

**Source evidence:** See exact commit/blob hashes in ledger entry and [test source manifest](manifest.json).

**Review draft:** R6-03 in [DRAFTS.md](DRAFTS.md). Approval pending; no external publication.


## Material review details

WordPress PR [#3](https://github.com/reeenatamc/wp-content-agent/pull/3) merged at 04:58:53Z while this round was being prepared. Re-read its discussion and updated request implementation at e1cc22b4fbb34033ee3da91e901f8167bffa9a22, then confirmed the client blob is identical on main 00b41fd5eecfc561af28dfba8068777e24fdc34f. The merge did not implement Retry-After. #6 remains open.

AIM uses an existing owned-agent route and compatible response envelope. Keep the new path inside _make_request so signing sees the same path as transport. Runtime Go middleware and signature verification remain untested.

Tududi model validation does not currently accept a processing state. A retry fix needs to coordinate model/claim semantics and partial external side effects. Another agent [claimed #263](https://github.com/Danathar/tududi/issues/263#issuecomment-6245886142) at 04:59:59Z. Re-read its resulting patch before posting; omit our draft if already covered.

## Exclusions

- [chrisbennight/waygate #218](https://github.com/chrisbennight/waygate/issues/218): Exploratory source review only. Current code declares SDK 7/runner 10 and includes stamp consistency tests; deployed descriptor/client-cache evidence needed to establish reported mismatch. No verified additional repair; no draft.
- [monid-ai/monid #149](https://github.com/monid-ai/monid/issues/149): Existing PR #151 already includes provider documents in minimum-version aggregation and adds regression coverage; reviewed patch. Avoid duplicate advice; tests not rerun.
- [yeongseon/azure-functions-scaffold-python #423](https://github.com/yeongseon/azure-functions-scaffold-python/issues/423): Reporter already provides precise non-ASCII compare_digest reproduction and regression boundaries. No distinct source-validated contribution completed.
- [monstercameron/NextGenScriptingLanguage #175](https://github.com/monstercameron/NextGenScriptingLanguage/issues/175): Framing-error recovery needs stronger source validation; unsafe to equate invalid JSON inside a bounded frame with missing Content-Length. Not investigated to completion.
- [google/adk-python #7589](https://github.com/google/adk-python/issues/7589): Reporter supplies detailed version/state matrix; final-artifact semantics need a maintainer decision. No distinct completed source investigation or proposed repair.

## Follow-up and commercial evidence

All 18 previous tracked threads were fetched through their available comments; no comment exceeded its saved cursor and no tracked issue changed state. Updated last-checked timestamps, retaining last_seen_comment_id values. New cases start with no own comment; Tududi's bot claim ID 6245886142 is recorded to prevent reannouncing it. Appreciation/technical engagement in earlier rounds was not reclassified as a sale. No new sales lead, buying intent, request for paid help, or purchase established.

## Tool fit and scope

Reviewed https://naifgravity.com/tools on 2026-10-18. It offers bounded public reachability/status and sanitized JSON structure checks; those do not repair SDK routes, retry timing, event claims or signatures. No NAIF promotional/free-tool link inserted in these replies. The existing MCP diagnostic project is not used for stdio/OAuth. No new project created.

## Own-repository publication controls

Started from main 71d3862e08055eced349939eaea4e5c19d78fa63. Read root AGENTS.md and recursively checked for nested AGENTS (none). Its bounty/payment examples were not executed: the user's docs-only scope governs this task. Reviewed all eight workflow trigger definitions: only three have push triggers, constrained to discovery manifests or their workflow files; none match docs/problem-hunter-v1/. No workflow dispatch or workflow edits.

The round files and ledger are prepared as one atomic commit with expected-head lease, force=false and [skip ci]. Read-back/commit URL is reported after publication; this report does not imply that a prepared commit has already landed.

## Remaining work

Review the complete three drafts. Any later external publication requires user approval and a fresh issue/PR check. Tududi deserves an extra check because work is already claimed. Native dependency-heavy suites, live integrations, ORM concurrency and crash recovery remain untested. No secrets, API keys, production payment data, spending or server access are needed.
