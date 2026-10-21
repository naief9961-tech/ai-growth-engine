# R8 — English reply for review (2026-10-20)

Status: **POSTED_MANUALLY_VERIFIED — HISTORICAL DRAFT — DO NOT REPOST**.

Verified on 2026-10-21: the user posted a shortened version at [comment 6283913029](https://github.com/recursive-cloud/woodhouse/issues/29#issuecomment-6283913029) on 2026-10-20T05:12:50Z. It is not byte-identical to the draft below. No subsequent developer reply at verification. The ledger cursor is updated; this does not authorize any other comment. Original draft retained as history.

## R8-01 — Woodhouse #29

Destination: https://github.com/recursive-cloud/woodhouse/issues/29

Historical text follows; do not copy it into another comment. No NAIF promotion is included.

---

AI-assisted source review; I ran isolated checks, not a full Woodhouse deployment.

There is a concrete no-listener path in the versions pinned by this repository: Probot 13.4.7 / @octokit/webhooks 12.3.2. In [Octokit's receiver](https://github.com/octokit/webhooks.js/blob/fa60c1a589c026ad41e4db360f80dac6db4518e0/src/event-handler/receive.ts), listeners are selected by event name and optional `payload.action`. If that selection is empty, it returns a resolved promise **before** the Probot transform and any guarded handler run. [Woodhouse's HTTP handler](https://github.com/recursive-cloud/woodhouse/blob/9ab881d47d35105fee4a3d1e2fea5a248f13db63/src/server.ts) then returns 200 after `verifyAndReceive` resolves.

That is subscription matching, not general payload-schema validation. For example, `pull_request` with no `action` does not match the action-specific registrations in [app.ts](https://github.com/recursive-cloud/woodhouse/blob/9ab881d47d35105fee4a3d1e2fea5a248f13db63/src/app.ts). Conversely, malformed data that *does* match a subscription can reach the guard/handler and take a different path. The acceptance-report path mentioned above is not present in the inspected main tree, so I cannot assert that this was the exact synthetic payload used in that run.

A bounded fix would be:

1. Record registered event names in a per-App subscription index inside `GuardedApp.on`, using the same single-name/array input as the existing registration. This avoids a second hand-maintained event list.
2. After successful `verifyAndReceive`, compare the verified event/action with that index. Base-event subscriptions must match regardless of action; action-specific subscriptions require that action.
3. If there is no match, emit one structured diagnostic containing only App label, delivery ID, event, action and `outcome: "unmatched-subscription"`. Preserve the current 200 response and all existing signature/unknown-App/handler-error paths. Do not log the raw payload, signature or secret.
4. Keep the installation allowlist on every business handler. A matching subscription does not prove that the guard allowed the delivery or that business work ran.

The matching core can be small:

```js
function matchesSubscription(names, event, action) {
  return names.has(event) ||
    (typeof action === "string" &&
     action.length > 0 &&
     names.has(`${event}.${action}`));
}
```

I would avoid adding a direct unguarded `onAny` listener as the first fix: it conflicts with this repository's guarded-registration rule and changes the formerly empty-listener path to run Probot's transform. A post-verification diagnostic can observe the case without changing dispatch.

Verification should cover: missing/unknown action, matching action, base-event subscription, per-App isolation, and one metadata-only warning for an unmatched delivery. In the full HTTP tests also assert that invalid signatures never produce this success-path warning, unknown Apps stay 404, allowlist rejection remains guarded, handler failures remain failures, and a valid unmatched delivery stays 200. Decide separately whether expected unhandled events such as `ping` should be warn or debug.

My eight isolated checks passed: three execute the pinned receiver source with TypeScript types stripped and error utilities stubbed; five exercise the proposed helper/integration-order model. They do not test real HMAC verification, Express, Probot authentication, live GitHub delivery, or the complete application.

---
