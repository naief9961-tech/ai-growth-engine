# R31 — one English reply for review

Status: **PENDING_USER_APPROVAL; NOT POSTED.** Recheck the issue, comments and PRs before approved publication. No other draft this round.

## R31-01 — Withings31

Destination: https://github.com/davidmosiah/withings-mcp/issues/31

Copy only the text below after approval:

---

AI-assisted source review: there is one additional boundary in the `data_quality.confidence` calculation, separate from the timezone and empty-data cases in your report.

At [7b0b1ff](https://github.com/davidmosiah/withings-mcp/blob/7b0b1ff9359478d89d7e9484e482df6d49638c86/src/services/summary.ts), `dailyStats()` records `has_heart_error`, and the result exposes it as `missing_or_failed.heart`. However, `buildDailySummary()` computes confidence from only the activity, sleep and measures error flags. A failure of `/v2/heart` alone therefore produces both `heart: true` and `confidence: "high"`.

I reproduced this with the actual summary module and its two runtime helpers, injecting a synthetic `client.get` implementation. No account or API request was used.

A narrow correction is to include all four error flags:

```ts
confidence: [
  stats.has_activity_error,
  stats.has_sleep_error,
  stats.has_measures_error,
  stats.has_heart_error,
].some(Boolean) ? "partial" : "high",
```

The candidate I tested adds `stats.has_heart_error` to the existing `.filter(Boolean).length === 0` expression; the snippet above is the equivalent shorter form. Six isolated assertion groups passed on Node 24.22.1: the baseline heart-only failure, then candidate checks for successful requests and a failure in each of the four domains. Apart from confidence and the creation timestamp, each result matched the baseline.

For regression coverage in `scripts/summary-fixture-test.mjs`, make only `/v2/heart` throw and assert both `missing_or_failed.heart === true` and `confidence === "partial"`. Retain the all-success and other-domain-failure controls.

This only corrects error aggregation. Empty successful responses still need a separate data-coverage policy, and this does not fix timezone selection, `days`, or Windows browser launching. I have not run the upstream build/full suite, an MCP client, or a live Withings account.
