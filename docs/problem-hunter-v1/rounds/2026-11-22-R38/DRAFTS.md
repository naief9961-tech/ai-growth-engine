> **RETIRED on 2026-11-24 — DO NOT POST.** Issue243 closed after [upstream commit ca45ed9](https://github.com/GoodOlClint/CrossTalk/commit/ca45ed9e144b4776736861a676bb13c88ff767b2). The text below is preserved only as historical evidence; its original pending-review label no longer applies. No comment was posted and no causal credit is claimed.

# R38-01 — NOT POSTED; pending user approval

Destination: https://github.com/GoodOlClint/CrossTalk/issues/243

One draft only. Recheck issue/comments/PRs before any authorized publication. Native Go regression remains unrun.

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
