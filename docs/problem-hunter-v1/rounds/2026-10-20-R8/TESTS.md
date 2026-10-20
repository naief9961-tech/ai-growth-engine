# R8 — Tests, source evidence and limits

Checked: 2026-10-20T05:04:25.754Z. Runtime: Node v24.19.0.

## Woodhouse #29

- Issue: https://github.com/recursive-cloud/woodhouse/issues/29
- Reporter: gunzy83; created 2026-10-20T04:33:49Z.
- Woodhouse main commit: `9ab881d47d35105fee4a3d1e2fea5a248f13db63`.
- Lockfile pins Probot 13.4.7 and @octokit/webhooks 12.3.2.
- Octokit v12.3.2 commit: `fa60c1a589c026ad41e4db360f80dac6db4518e0`.
- Probot v13.4.7 commit: `c4c67c3c3d83ea8e2cc01e8b43b91e8fe7d4f91b`.

Source review:
- [HTTP verification and 200 response](https://github.com/recursive-cloud/woodhouse/blob/9ab881d47d35105fee4a3d1e2fea5a248f13db63/src/server.ts)
- [Actual subscriptions](https://github.com/recursive-cloud/woodhouse/blob/9ab881d47d35105fee4a3d1e2fea5a248f13db63/src/app.ts)
- [GuardedApp registration and allowlist](https://github.com/recursive-cloud/woodhouse/blob/9ab881d47d35105fee4a3d1e2fea5a248f13db63/src/security/guard.ts)
- [Dependency lock](https://github.com/recursive-cloud/woodhouse/blob/9ab881d47d35105fee4a3d1e2fea5a248f13db63/package-lock.json)
- [Receiver selection and empty-hook early return](https://github.com/octokit/webhooks.js/blob/fa60c1a589c026ad41e4db360f80dac6db4518e0/src/event-handler/receive.ts)
- [Signature then JSON parse then receive](https://github.com/octokit/webhooks.js/blob/fa60c1a589c026ad41e4db360f80dac6db4518e0/src/verify-and-receive.ts)
- [Probot webhook construction](https://github.com/probot/probot/blob/c4c67c3c3d83ea8e2cc01e8b43b91e8fe7d4f91b/src/octokit/get-webhooks.ts)
- [Probot transform](https://github.com/probot/probot/blob/c4c67c3c3d83ea8e2cc01e8b43b91e8fe7d4f91b/src/octokit/octokit-webhooks-transform.ts)

No linked repair PR in the full issue timeline. All 23 repository PR entries inspected for overlap; none targets this case. Zero issue comments at final refresh. AGENTS.md and TODO.md reviewed; no direct unguarded business listener proposed. The acceptance-report path referenced in the issue is absent from the inspected tree; fetching it returned 404. The original acceptance fixture was therefore not reproduced.

### Executed

```sh
node --test test-woodhouse.cjs
```

**8 passed / 0 failed**. The command emitted Node's experimental stripTypeScriptTypes warning.

| Group | Scope | Result |
|---|---|---|
| Missing action skips transform and action listener | Actual pinned Octokit receiver, dependency error helpers stubbed | PASS |
| Matching action dispatches; thrown handler still rejects | Same extracted receiver | PASS |
| Base event also matches an action-bearing payload | Same extracted receiver | PASS |
| Array/base/action/missing/unknown matching | Proposed pure helper | PASS |
| Independent per-App indexes | Proposed pure helper | PASS |
| One warning, selected metadata only, no sentinel payload/signature | Proposed helper | PASS |
| Matching subscription emits no unmatched warning | Proposed helper | PASS |
| Rejected verification does not reach success logging | Candidate orchestration model; NOT HMAC verification | PASS |

`receiver.fixture.ts` is the unmodified upstream receiver file, with [MIT notice](OCTOKIT-LICENSE.md). The harness strips types and imports, injects local AggregateError/wrapErrorHandler substitutes, and executes the receiver in a VM. No network, credentials, real webhook delivery or external process is involved. `subscription-candidate.cjs` is a proposed helper, not a patch applied to Woodhouse.

### Not tested / remaining work

No Probot/Express install, full suite, real signature check, HTTP status acceptance test, real installation allowlist test, authentication or deployment. The per-App index still needs wiring through GuardedApp and AppRegistry. The log helper accepts selected fields; production structured logging should retain normal input-size and log-volume controls. A subscription match is not payload validation or proof of execution. Expected unhandled events may deserve debug rather than warn, a maintainer decision.

Confidence: **high** for the empty-hook dispatch mechanism and isolated reproduction; **moderate** for applicability to the unavailable original fixture and the complete integration. Benefit: moderate, concrete observability improvement with no repair/purchase claim.

## Other source reads (not completed investigations)

- Linkid #900: inspected `lib/webhookDelivery.ts` and its tests at `53a48f6d826f7696d872c699277ba43a00e1ecf5`. [PR #912](https://github.com/vishnukothakapu/linkid/pull/912) already covers TimeoutError/AbortError and a never-responding receiver. No new draft; tests not rerun.
- Paperless #14502: views (main and v3.3.0), serializers, permissions, filters, schema and existing schema tests inspected. No proven evaluation trigger or isolated reproduction; **no root cause claimed, no draft**. Main inspected at `a5c8b82da5b392c812a05289c0d13aeec843d644`. CONTRIBUTING requires AI disclosure, observed-behavior-only AI issue reports, and does not accept mostly AI-derived PRs. Do not publish speculative diagnosis or an AI-generated PR. The report's large deployment/OOM behavior was not reproduced.
- A2A #1341 follow-up: reviewed all four files in [PR #1354](https://github.com/a2aproject/a2a-python/pull/1354) at `27bd15979b99a5198eea1358729d449f4e32c958`. Both REST `Parse` SSE and JSON-RPC `ParseDict` streaming changes and tests are present. No duplicate suggestion; SDK tests not run here.
