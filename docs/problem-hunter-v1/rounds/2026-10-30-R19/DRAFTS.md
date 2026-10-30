# R19 — one follow-up for review

Status: AWAITING_USER_APPROVAL. Not posted. Destination: https://github.com/wevm/mppx/pull/1133 (merged). Original issue: https://github.com/wevm/mppx/issues/1113 (closed).

A materially new post-merge false-positive is documented; do not repost the old R16 comment. Re-read PR/issue comments and current source before publication. No commercial links.

## R19-01 — full proposed comment

AI-assisted follow-up to #1133, checked at [c912c79a](https://github.com/wevm/mppx/tree/c912c79a5df2589eadfcadfd30a43b7f7b5ff5c2).

There is a remaining quoted-string boundary in `Challenge.hasPaymentScheme`. Its new bare-scheme fallback uses `.split(',')`, which ignores quoting. For example:

```ts
Challenge.hasPaymentScheme('Bearer realm="alpha, Payment, beta"')
// currently true; there is no actual Payment challenge
```

I reproduced this with the unchanged classifier helpers extracted from `src/Challenge.ts`. The original quote-aware scanner returns no starts for this header, but the fallback sees an isolated `Payment` segment. Reading `Mpp.ts` and `deserializeList`, this routes the response back into the strict parser's “No Payment schemes found.” error. The transport consequence is source analysis; I have not run the complete transport.

A narrow repair is to recognize bare schemes inside the same quote/escape-aware scanner: at a valid top-level start/comma boundary, accept the exact case-insensitive token followed by whitespace, a comma, or end-of-input. An optional presence-detection mode can preserve the strict parser's current default behavior. This retains rejection of real malformed `Payment` challenges without treating quoted text as a scheme.

My isolated candidate passed 13 classification cases plus 13 strict-scanner parity checks. Three quoted-text false positives were reproduced in the baseline; ten controls behaved as expected. No upstream suite, credentials, or payments ran.

For integration validation, add a synthetic 402 with this header plus a valid x402 offer and assert x402 is collected; keep controls for escaped quotes, mixed case, `Paymentish`, actual bare `Payment`, and real mixed-protocol challenges.
