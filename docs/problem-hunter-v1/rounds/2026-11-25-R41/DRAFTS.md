# R41-01 — updated after isolated Go tests; NOT POSTED

Destination: https://github.com/Mag1cFall/Antigravity2API/issues/11

Pending user review. Evidence: [Go test harness and results](GO-TESTS.md). No third-party comment sent.

---

I checked v0.1.12 (`8caff896859499b86398c1e3e75c964c40dca6f3`) and tested the event-ordering boundary in an isolated Go fixture.

First, the late `request.progress` log alone does not prove that the request was resurrected. `logHandler.Handle` routes it through `hub.log` as `type: "log"`; the frontend's log branch only updates the logs cache. The extracted frontend handler confirms that running → cancelled → late log stays empty, whereas a late `type: "request"` with `state: "running"` restores the entry.

A concrete ordering gap exists in `hub.begin`: it publishes unconditionally. If a previously captured running update reaches it after `hub.end`, existing subscribers receive running after terminal even though the active map no longer contains the request. `Trace.SetAccount` invokes its watch after releasing the trace lock, making that callback boundary worth checking.

The candidate is to check membership and publish under the same lock used by `end`:

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

I extracted seven hub methods from the SHA-verified source, with minimal Row/Trace/supporting-type stubs, and ran Go 1.27.4 with `go test -race -count=1`:

- Original: delayed-begin-after-end failed for cancelled, failed and completed states; the concurrent begin/end test also failed.
- Candidate: all six top-level test groups passed, including 200 concurrent begin/end iterations, still-active updates, unrelated requests, fresh subscriptions and full-subscriber cleanup.
- Neither fixture run reported a memory data race; this is a logical event-ordering defect.

This validates the guard at the isolated hub boundary, not the reported production cancellation path. The full Go application, real Trace callback path, React/EventSource and WebView2 were not tested. A synthetic SSE capture identifying an actual late request/running frame would close the remaining causal gap.

Separately, pre-ready snapshot handling should upsert by ID and remove terminal entries rather than append blindly. Paired frontend checks cover that, but it does not fix late live events. The server currently queues snapshot and ready under one lock, so those are defensive reducer checks.

Also avoid using `Trace.done` as a general finalization flag: it currently represents an observed upstream finish event.
