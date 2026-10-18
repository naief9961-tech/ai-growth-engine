# R6 — English replies for review (2026-10-18)

Status: PUBLISHED_VERIFIED after the user's subsequent explicit instruction on 2026-10-18. The scheduled round itself sent no comments. These texts are now historical copies; DO NOT POST AGAIN. No advertising or commercial offer.

- R6-01: https://github.com/reeenatamc/wp-content-agent/issues/6#issuecomment-6246051674 (2026-10-18T05:21:34Z)
- R6-02: https://github.com/opena2a-org/agent-identity-management/issues/772#issuecomment-6246052455 (2026-10-18T05:21:41Z)
- R6-03: https://github.com/Danathar/tududi/issues/263#issuecomment-6246053246 (2026-10-18T05:21:48Z)

## R6-01 — WordPress Retry-After

Target: https://github.com/reeenatamc/wp-content-agent/issues/6

Begin proposed comment:

One detail worth preserving when adding a cap: if the server asks for 600 seconds and the client budget is 120 seconds, sleeping 120 seconds would still retry earlier than requested. I would stop/defer that attempt and return the rate-limit error, rather than truncate a valid server delay.

I checked `_request` at [e1cc22b](https://github.com/reeenatamc/wp-content-agent/blob/e1cc22b4fbb34033ee3da91e901f8167bffa9a22/src/wp_mcp/client.py). PR #3 is now merged; its updated request loop still sleeps at the start of the next iteration without consulting the response headers. With that method extracted into a fake-transport harness, a synthetic 429 carrying `Retry-After: 60` followed by 200 recorded a 0.5-second sleep.

Suggested implementation:

1. Compute the next delay from the failed response and carry it to the next iteration; do not add an unconditional exponential sleep on top of it.
2. Accept non-negative decimal seconds and HTTP-date values ([RFC 9110 §10.2.3](https://www.rfc-editor.org/rfc/rfc9110.html#section-10.2.3)). Use an injected UTC clock for date tests, clamp past dates to zero, and fall back to backoff for malformed/missing values.
3. If the valid delay exceeds the configured wait budget, stop/defer. Validate the setting as finite and non-negative, and bound oversized numeric header values before integer conversion.
4. Leave retry eligibility unchanged: parsing this header must not make POST 5xx/read-timeout failures retryable. Do not sleep after the final attempt.

Regression cases: seconds/date/past-date; missing, invalid and oversized headers; over-budget delay yields no additional request; 429 then success sleeps once; attempt exhaustion; and POST 500/read timeout remains one request. If jitter is added, it must not reduce the chosen server delay.

The extracted baseline and standalone delay-policy tests passed locally. The POST-500 no-retry baseline also passed. I have not integrated the helper into the retry loop, run the project's pytest suite, or tested WordPress/MCP end to end.

End proposed comment.

## R6-02 — AIM current-agent skills route

Target: https://github.com/opena2a-org/agent-identity-management/issues/772

Begin proposed comment:

The existing agent-scoped route also preserves a useful authorization boundary. At [ad332f2](https://github.com/opena2a-org/agent-identity-management/blob/ad332f24c1321beff97a617bc41d0e8eacc98471/apps/backend/cmd/server/main.go), `GET /agents/:id/skills` is registered on `a2aHeld`; [GetAgentSkills](https://github.com/opena2a-org/agent-identity-management/blob/ad332f24c1321beff97a617bc41d0e8eacc98471/apps/backend/internal/interfaces/http/handlers/a2a_handler.go) additionally checks the caller's organization and loads the owned agent before returning the existing `skills` envelope.

For the documented “current agent” behavior, the SDK-only change can therefore remain small:

```python
response = self._make_request(
    "GET", f"/api/v1/a2a/agents/{self.agent_id}/skills"
)
return response.get("skills", [])
```

Keep this through `_make_request`: the signing branch incorporates the endpoint into the signed message, so changing only the final URL outside that method would risk a signature/path mismatch. A new global skills-list endpoint is unnecessary for this method.

I ran an extracted-method check reproducing the old GET path and confirmed the registered agent route in the pinned server source. With the candidate path substitution, populated/empty skill lists were preserved and a synthetic authorization error still propagated.

For an upstream regression, assert the exact method/path for two distinct agent IDs, then exercise the mounted Go route with owned-agent, unauthorized and cross-organization cases. A mock returning 200 for any URL would miss this contract mismatch. My checks used a fake request boundary; I have not run the Go authorization tests, signed HTTP integration, or the full SDK suite.

End proposed comment.

## R6-03 — Tududi failed webhook redelivery

Target: https://github.com/Danathar/tududi/issues/263

Review note: another agent claimed this issue at 04:59:59Z. Before posting, inspect its resulting work and omit this reply if the same boundaries are covered. Do not take over its claim.

Begin proposed comment:

There are two extra boundaries to consider when making failed events retryable.

At [69f0887](https://github.com/Danathar/tududi/blob/69f08879b80b4eca651c32fd7176aa145a18b8cc/backend/modules/billing/service.js), I reproduced the failure using the extracted `handleWebhook` and `recordEvent` methods with an in-memory model stub: the first application fails and records `failed`; the second delivery is reported as a duplicate without a second application attempt. This confirms the reported control-flow problem, not database or provider behavior.

First, merely returning the existing nonterminal record lets two redeliveries both enter `applyEvent`. Use a database-backed exclusive claim for retryable events (or a transaction design appropriate to both supported database dialects). Suppress only terminal `processed`/`skipped` records. For an actively owned claim, do not acknowledge completion unless another durable mechanism guarantees recovery. If using a processing state/lease, add crash recovery and ownership/fencing checks for completion.

The [BillingEvent model](https://github.com/Danathar/tududi/blob/69f08879b80b4eca651c32fd7176aa145a18b8cc/backend/models/billing_event.js) currently validates only `received`, `processed`, `skipped`, and `failed`. Adding `processing` only in the service would fail model validation; model validation and any claim/lease storage must change together.

Second, `applyEvent` can update the account before `seats.reconcile` or event-status persistence fails. Replaying after such a partial success needs idempotent side effects or a durable outbox/deduplication boundary. An exclusive claim alone cannot guarantee exactly-once external effects.

Suggested regressions: fail-before-apply then retry; successful duplicate suppression; simultaneous redeliveries; crash after claim; account update succeeds but a later step fails; and event-status write fails after application. Retain signature verification before event recording and clear stale error metadata after successful recovery.

A small exclusive-claim state-machine model admitted one of eight contenders locally. This was not a Sequelize concurrency test. The actual ORM implementation, both database dialects, provider signature integration, crash recovery and external side effects remain untested.

End proposed comment.
