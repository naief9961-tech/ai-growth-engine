# R41-01 — review draft, NOT POSTED

Destination: https://github.com/Mag1cFall/Antigravity2API/issues/11

Approval: awaiting the user's review. Re-read the issue and PRs before publication.

---

I checked v0.1.12 at `8caff896859499b86398c1e3e75c964c40dca6f3`. One distinction may help narrow this down: the late `request.progress` in the log is not itself a `type: "request"` SSE event.

In `internal/app/events.go`, `logHandler.Handle` routes it through `hub.log`, which publishes `type: "log"`. In `web/src/app/events.ts`, that branch only updates the logs cache. I exercised the extracted `apply` function with a mocked QueryClient: running → cancelled → late progress log leaves the running list empty; running → cancelled → a late **request/running** event brings the entry back. So the log sequence alone does not prove which event resurrected the card.

There is a separate source-level ordering gap worth testing: `Trace.SetAccount` calls its watch callback after releasing the trace lock; the callback is `hub.begin`, which publishes unconditionally. `hub.end` removes the active ID and publishes the terminal row under `hub.mu`. A delayed begin can therefore publish after end. A candidate guard is to check active membership and publish within that same hub lock:

```go
func (h *hub) begin(row requestdb.Row) {
    h.mu.Lock()
    defer h.mu.Unlock()
    if _, ok := h.active[row.ID]; !ok {
        return
    }
    h.publishLocked(event{Type: "request", Data: row})
}
```

This is an uncompiled candidate, not a confirmed reproduction of the reported cancellation path. Also, `Trace.done` currently means an upstream finish event was observed; it is not a general finalization flag.

For verification, add a deterministic hub test that holds a captured running update until after `end`, then releases it: existing subscribers must receive no subsequent running row, and a fresh subscription must contain no such request. Keep a control where updates to a still-active request are delivered. Run the native tests with the race detector.

The pre-ready reducer should also replace entries by ID and remove terminal rows instead of appending blindly. Three paired extracted-function checks reproduced duplicate/terminal snapshot entries and passed with that change. The server currently queues its initial snapshot and ready under one lock, so those are defensive reducer checks, not proof of a live pre-ready race. This change does **not** repair a late live running event; an empty reconnect snapshot does clear stale state.

Eight isolated assertion groups passed in Node 24.22.3. QueryClient, refresh and log merging were stubbed. No Go hub/race test, React/EventSource, WebView2, provider call or full application test was run. A synthetic SSE sequence identifying whether the offending message is `log` or `request` would resolve the remaining causal gap.
