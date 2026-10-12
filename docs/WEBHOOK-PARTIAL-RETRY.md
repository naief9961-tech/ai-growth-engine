# Webhook retries after partial success

A delivery can match several workflow registrations. If registration A starts successfully and B fails, retrying the whole delivery can start A again. A single delivery-level processed flag does not describe each effect's outcome.

This guide is a design and diagnostic checklist, not an implementation or a claim that any external service has been repaired.

## Collect sanitized evidence

Record only the workspace identifier, stable delivery identifier, registration identifier, attempt number, durable run identifier, and outcome. Use synthetic identifiers in public reports. Do not publish webhook bodies, signing secrets, authorization headers, customer data, or internal production URLs.

Distinguish three outcomes: no run created, run durably created, and creation outcome unknown after a timeout or crash. Unknown must not be treated as proof of failure.

## Bound the effect

- Deduplicate each intended start with a stable delivery/registration identity, including tenant or workspace scope where needed.
- Preserve that identity on queue redelivery. A new attempt identifier is for observability, not the deduplication key.
- Where claim state and run creation share one transactional database, commit them together and enforce uniqueness on the logical effect.
- Across independent stores or services, make the receiving run-creation operation idempotent and reconcile using the stable identity. An outbox alone does not eliminate duplicate delivery.
- Define recovery for unfinished claims: after a crash, find an existing run before deciding to start another. Locks and leases must not erase durable evidence of completed effects.
- Retain deduplication records for the actual queue retry/redelivery window, including delayed and dead-letter replay policies.

## Failure-injection matrix

Use a disposable local or staging system with synthetic payloads. Do not send live callbacks or create production jobs.

| Case | Expected invariant |
| --- | --- |
| A starts; B fails before creating a run; delivery retries | A remains one run; B eventually becomes one run. |
| Worker crashes after A's durable run creation but before claim completion | Recovery finds A's run; no second A run is created. |
| Two workers process the same delivery concurrently | One durable run per delivery/registration identity. |
| Same delivery ID appears in different tenants | Isolation is preserved; unrelated deliveries are not suppressed. |
| Retry arrives after the normal retention window | Behavior follows the documented replay policy; no accidental deduplication guarantee. |
| Remote create times out after the receiver accepted it | Reconcile by identity before another create attempt. |

Assert persisted run counts and identities after recovery, not only HTTP responses or mock invocation counts. Record the tested commit, queue behavior, retention window, and the first observed failure; report untested cases explicitly.

## Public example that motivated the checklist

[Wbskt issue #293](https://github.com/wbskt/Wbskt/issues/293) describes a callback fan-out with partial success and proposes per-registration claims. This guide adds the crash-between-create-and-completion boundary and recovery checks. We have not executed Wbskt's engine or verified an external fix.

For a reproducible diagnostic request, use the repository's [webhook issue template](../.github/ISSUE_TEMPLATE/webhook-diagnostic.md).
