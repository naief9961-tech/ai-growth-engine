# R29 — English reply for review

Status: **PENDING_USER_APPROVAL — NOT POSTED**.

## R29-01

Destination: https://github.com/shpaw415/open-bot/issues/80

---

I found a remaining deadline gap in the post-write confirmation path at [`dddefb9`](https://github.com/shpaw415/open-bot/blob/dddefb9bcd7c57d2b9605a8f41c7ea03ad6e0bec/apps/control/src/viking-skills.ts).

`save()` calculates a 25-second deadline, but `confirmSave()` starts its first `get()` before checking that deadline, and checks subsequent attempts only after the read finishes. Each `call()` independently uses `AbortSignal.timeout(20_000)`. Thus, even when the POST has succeeded and the save budget is already exhausted, confirmation can still start another read with a fresh 20-second timeout. The CLI's current 90-second curl timeout also exceeds the 12/30-second outer limits in this report.

A narrow candidate fix is to bound **post-success confirmation**:
1. Return `confirmed: false` immediately if no time remains before the first read.
2. Check the remaining budget before and after a poll delay; skip the poll if the delay consumes it.
3. Thread the remaining budget through `get()` into `call()`, using `AbortSignal.timeout(Math.min(20_000, remainingMs))` only when `remainingMs > 0`.
4. Keep the existing success-with-indexing-note response once POST has acknowledged the write. Do not turn a confirmation timeout into another save attempt.

For regression coverage, I ran five isolated groups against this source and a candidate change, with synthetic responses/injected fetch and a controlled clock: immediate confirmation; an expired budget after successful POST; 10 ms remaining versus the current fresh 20,000 ms timeout; insufficient budget for a second poll; and a signal-aware stalled confirmation read. These checks passed. They do **not** run the CLI, control-plane route, real OpenViking, or deployed application.

This does not yet establish the cause of the observed instance: its deployed revision and stage timings are unknown. Also, validation/snapshot/delete/POST and any desktop-startup or optional group-assignment work have separate timing concerns; this change alone does not impose an end-to-end 25-second bound. Useful confirmation would be the deployed revision plus sanitized per-stage timings, particularly “POST acknowledged” to “confirmation finished”, without tokens or skill contents. Issue #79's missing-write observation should remain distinct from this post-write case.

---

One draft only. No third-party post this round. Recheck live thread before posting.
