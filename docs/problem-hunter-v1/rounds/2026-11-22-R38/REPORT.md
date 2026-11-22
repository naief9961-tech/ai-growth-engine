# R38 — 2026-11-22

Evidence checked 2026-11-22T05:08:06Z. Review only; no external comment, PR or message posted.

## Counts and scope
70 results from seven newest-first searches (10 each), 68 unique URLs initially screened by title/description. Queries: is:issue is:open created:>=2026-11-19 plus MCP, A2A, x402, webhook, schema, API, and "GitHub Actions". One additional targeted TestAdmission search returned the already selected issue only. This is capped discovery, not exhaustive coverage of the72-hour window.

Five complete candidate issue/comment/timeline reads (all zero comments; timelines below100 entries). One completed bounded source investigation, two exploratory source reads, two deferred source investigations. Only one additive English review draft; no padding to five solutions or three replies.

52 previous issue/PR threads checked with paginated issue-comment reads and current issue state. Four PR review timelines checked separately. Zero new developer replies to NAIF, one new other-contributor comment on an unposted draft, one closed issue whose draft is retired. Six abstract-model assertions passed; zero native Go or upstream full suites. Zero verified commercial requests.

## Selected — CrossTalk #243
[Original issue](https://github.com/GoodOlClint/CrossTalk/issues/243) — reporter goodolclint-claude[bot]; created 2026-11-22T04:48:26Z; discovered2026-11-22; open at final recheck.

**Diagnosis:** q1 is ReturnImmediately, so its receiver goroutine need not finish before ScriptInject queues a shared FIFO outcome intended for hang. If q1 consumes Unknown+Entered, the signal belongs to q1. hang can then get default Accepted, become terminal and release its waiting slot; w2 succeeds, matching the reported failure text. q2 is rejected before its receiver starts; it does not consume the queue. The receiver does not serialize all injections behind one global lock. Unknown maps to Working; Accepted completes informs but keeps asks Working.

**Candidate:** retain q1's task and waitState(q1, Working) before queuing the next scripted outcome. Keep production limits unchanged. Add a deterministic beforeReceive regression to delay q1, identify the consumer of Entered, assert too_many_waits, and test cancellation/cleanup with bounded waits. A gate alone cannot ensure which request consumes a FIFO outcome.

**Confidence:** high that source permits this schedule; medium that it explains the original Ubuntu run. The native failing run was not reproduced. Benefit: a specific request-ownership race and test-only correction, beyond the report's generic timing hypothesis.

**Evidence:** six assertions in an abstract Python model.15 valid baseline schedules include3 second-wait admissions;2 barrier schedules include0. These are modeled event orders, not observed failure rates, and do not prove SDK/HTTP or production correctness. [Executed model and remaining regression plan](TESTS.md).

**PR/duplicate checks:** complete issue timeline contains no linked repair; zero open PRs in repository; latest30 all-state PR summaries checked; targeted TestAdmission issue search returns only243. PR242 is merged at2026-11-22T04:48:17Z, head104d401aa08773f451f5db0ae9a8e87b5a66d9bc. Its13-file list/patches do not change TestAdmission, fake.go or tasks.go.242 addresses refresh work, not this test setup. PR-author tests were not rerun. CONTRIBUTING.md and AGENTS.md reviewed for public-response conventions; no claim or external contribution made.

### Source pins
- [internal/a2a/server_test.go](https://github.com/GoodOlClint/CrossTalk/blob/612177bc37bf2cfc3a9ee729bd48810076c45232/internal/a2a/server_test.go) — commit 612177bc37bf2cfc3a9ee729bd48810076c45232; blob 83dd711354380ba117912cc5c0844a32a861da1c
- [internal/a2a/tasks.go](https://github.com/GoodOlClint/CrossTalk/blob/612177bc37bf2cfc3a9ee729bd48810076c45232/internal/a2a/tasks.go) — commit 612177bc37bf2cfc3a9ee729bd48810076c45232; blob 23b98f5883a812f7b54c5c79fde4eac7423f5006
- [internal/adapter/fake.go](https://github.com/GoodOlClint/CrossTalk/blob/612177bc37bf2cfc3a9ee729bd48810076c45232/internal/adapter/fake.go) — commit 612177bc37bf2cfc3a9ee729bd48810076c45232; blob 5e0bc240267b3e7cbae6672ac5e3f21c2a4a3f8e
- [internal/a2a/mapping.go](https://github.com/GoodOlClint/CrossTalk/blob/612177bc37bf2cfc3a9ee729bd48810076c45232/internal/a2a/mapping.go) — commit 612177bc37bf2cfc3a9ee729bd48810076c45232; blob 5d4ba306a9a60a75399f64d8fcb0b569e77dbf8e
- [internal/receiver/receiver.go](https://github.com/GoodOlClint/CrossTalk/blob/612177bc37bf2cfc3a9ee729bd48810076c45232/internal/receiver/receiver.go) — commit 612177bc37bf2cfc3a9ee729bd48810076c45232; blob e1dc08340f9d149eb7631a1048fc2f1116b21029
- [internal/a2a/admission_test.go](https://github.com/GoodOlClint/CrossTalk/blob/612177bc37bf2cfc3a9ee729bd48810076c45232/internal/a2a/admission_test.go) — commit 612177bc37bf2cfc3a9ee729bd48810076c45232; blob cdb13fa2d8e4d73254cd2442074647bf80eeb674

## Other candidates — not proposed as completed solutions
- [Community-VyProjects/VyManager #1438](https://github.com/Community-VyProjects/VyManager/issues/1438) — reporter xTITUSMAXIMUSX; created 2026-11-22T05:04:32Z; open with0comments. Exploratory source confirms post-success refresh rejection replaces the result. Reporter already supplies the repair boundary; no distinct tested addition, no draft. Repository head observed 99264a8c0bc4a1a198bb99bf6bc82651599911fb. Open-PR inventory: 13; latest30 all-state summaries and complete issue timeline read.
- [mattyv/facepalm #129](https://github.com/mattyv/facepalm/issues/129) — reporter mattyv; created 2026-11-22T05:03:59Z; open with0comments. Deferred: reporter already identifies restart ID reuse and preview-lifecycle gaps. No complete source/runtime investigation; no draft or claimed repair. Repository head observed ea763070738062d50cac61591333a2f6d4d387b9. Open-PR inventory: 0; latest30 all-state summaries and complete issue timeline read.
- [margince/margince #13124](https://github.com/margince/margince/issues/13124) — reporter tinnhlt-gra; created 2026-11-22T05:03:39Z; open with0comments. Deferred: reporter supplies schema ordering hypothesis and certification results. Provider wire behavior not independently reproduced; no draft. Repository head observed b0bfb1665d5b95191c00d4d8d307edf13f73016f. Open-PR inventory: 41; latest30 all-state summaries and complete issue timeline read.
- [a-Fig/murmur #981](https://github.com/a-Fig/murmur/issues/981) — reporter a-Fig; created 2026-11-22T05:01:56Z; open with0comments. Exploratory source confirms format patterns scan raw text while credential assignments decode quoted values. Reporter already supplies decoded-value repair; no native Go validation or additive draft. Repository head observed b6ff0ec31441909caef2ac4c11079c2a6ba5b278. Open-PR inventory: 5; latest30 all-state summaries and complete issue timeline read.

Exploratory source pins:
- [VyManager vrf.ts](https://github.com/Community-VyProjects/VyManager/blob/99264a8c0bc4a1a198bb99bf6bc82651599911fb/frontend/src/lib/api/vrf.ts), blob e7d83b864ae9d28d3d6e95a0e6744c278906030f. batchConfigure awaits POST, then refreshConfig, then returns original result. No API/browser/native-device execution; no validated patch.
- [Murmur scrub.go](https://github.com/a-Fig/murmur/blob/b6ff0ec31441909caef2ac4c11079c2a6ba5b278/internal/scrub/scrub.go), blob 3af8198ea8d5a48e8829c1bfb3287413715de9c5. No full decoded-string repair or Go tests. Prior PR970 is merged and addresses credential assignments; issue981 explicitly concerns the remaining format-check path. No fresh repair observed in timeline/open-PR inventory.
Facepalm and Margince remain source-validation deferred. Their existing implementation/certification PRs are context, not proof of repair. No fix is recommended for either.

## New follow-up observations
- [Git5641 comment7073013313](https://github.com/modelcontextprotocol/servers/issues/5641#issuecomment-7073013313): Shanmukh-l33t supplied a format-only branch and author-reported tests. R36 was never posted, so this is not a response to NAIF. Cursor advanced from7044776922 to7073013313. Do not repost overlapping R36 wording; no independent validation of the contributor's branch or full-suite claim.
- [Lontar452](https://github.com/handi7/lontar-cms/issues/452) closed as completed at2026-11-21T09:51:52Z. Zero comments; no closing commit or PR reference in the complete timeline. R37-01 is retired and must not be copied. Closure is verified; the implementation and release are not independently verified. No credit or commercial inference.
- The remaining tracked threads produced no new comment after saved cursors. Previous duplicate PowerPoint post was not reannounced, deleted or reposted. Empty/currently missing prior comments do not erase publication history or move cursors backwards.

## Boundaries and blockers
Go command lookup succeeded but go version returned "Go: Unknown option: version"; the expected Go binary locations were absent. No Go toolchain installed for this round. Native tests remain required; no fabricated test success. Python model used only synthetic event labels and no network, credentials, wallet or payment.

NAIF website and current diagnostics README reviewed. No free-tool referral fits the CrossTalk scheduling defect: MCP Doctor's bounded Streamable HTTP discovery probe does not exercise this A2A test, stdio or OAuth. No paid offer. No production, payment, V5, server or heavy work.

Own root AGENTS and complete untruncated tree checked; no scoped AGENTS. All8 workflows read: docs/problem-hunter-v1 paths do not match push triggers. No workflow dispatch or edits. Publication uses parent/head lease and only documentation within this directory; historical entries retained. Commit/readback reported separately after success.

## Full English review draft R38-01 — NOT POSTED
Destination: https://github.com/GoodOlClint/CrossTalk/issues/243

Pending explicit user approval and a fresh issue/comment/PR check before any external publication.

AI-assisted source review at 612177bc37bf2cfc3a9ee729bd48810076c45232: there is a concrete ordering race worth checking before increasing sleeps or changing production admission limits.

In TestAdmission, q1 is sent with ReturnImmediately=true, so its receiver goroutine may still be pending when ScriptInject queues Unknown + Entered for "hang". Fake.ScriptInject is a shared FIFO, not keyed by message. If q1 reaches Fake.Inject first, it consumes that scripted outcome and signals entered. The later "hang" inform then receives the default Accepted outcome, becomes terminal, and releases its waiting slot. w2 can consequently succeed with nil error, matching the reported failure.

This is a source-supported explanation, not a reproduction of the original Ubuntu CI run. The relevant pieces are TestAdmission in server_test.go, start/SendMessage/enterWait/leaveWait in tasks.go, the FIFO in adapter/fake.go, and outcome in mapping.go. Unknown stays Working; Accepted completes an inform but leaves an ask Working.

A small test-only candidate is to retain q1's task and wait for its receiver result before arming the next scripted outcome:

```go
q1, err := send(t, cl, ctx, textMsg("q1", map[string]any{"kind": "ask"}), true)
if err != nil {
    t.Fatal(err)
}
waitState(t, cl, ctx, q1.ID, sdk.TaskStateWorking)
// Keep the q2 rejection assertion, then ScriptInject and the hang/w2 checks.
```

For a deterministic regression, use the existing beforeReceive hook to hold q1 before it reaches the fake, queue the scripted outcome, then release q1 and record which message consumed it. Also verify that after the barrier the entered signal belongs to hang, w2 is rejected specifically for too_many_waits, and cancellation frees the wait slot. Bound channel waits and join the client goroutine during cleanup. A gate on the scripted outcome alone would not prevent q1 from consuming it.

I ran six assertions on a small Python ordering model: 3 of 15 valid baseline schedules admitted the second wait; neither of the two schedules with the q1-before-queue barrier did. This checks the abstract scheduling argument only. I have not run the Go test, race detector, SDK/HTTP integration, or CI; the available go command here did not provide the Go toolchain. The candidate still needs the native regression and Linux/macOS -race checks before being treated as a fix.
