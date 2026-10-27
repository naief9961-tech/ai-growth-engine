# R16-01 — mppx #1113

**POSTED MANUALLY AND VERIFIED — DO NOT REPOST.**
Published by naief9961-tech at 2026-10-27T05:35:38Z; verified at 2026-10-27T05:36:14Z.
Comment: https://github.com/wevm/mppx/issues/1113#issuecomment-6434639013
No subsequent developer reply at verification. Historical text retained below; this publication does not authorize future comments.
Destination: https://github.com/wevm/mppx/issues/1113

---

AI-assisted source review at [dd2c3e3b](https://github.com/wevm/mppx/tree/dd2c3e3b21006b80f4de65b218967a0490eaa218).

There is already a useful building block in [Challenge.ts](https://github.com/wevm/mppx/blob/dd2c3e3b21006b80f4de65b218967a0490eaa218/src/Challenge.ts): `findSchemeStarts` ignores quoted-string contents and handles escaped quotes. I ran that unmodified scanner in isolation against nine synthetic headers, including a quoted `, Payment ...`, mixed-case scheme names, two Payment challenges, and `Paymentish`; all nine assertions passed. This checks scheme detection only, not payment handling.

For the repair, distinguish **no Payment scheme** from **a present but invalid Payment challenge**. The MPP adapter currently delegates every 402 with WWW-Authenticate to `fromResponseList`; `deserializeList` throws when the scanner returns no starts, aborting the collector before x402.

A narrow option is an internal/tolerant list-parsing entry point that returns an empty list only for zero matching scheme starts, reusing the existing scanner and retaining the current deserialization errors for matching challenges. Keep the existing public strict API behavior unless an API change is intended. Avoid catching every parsing error or testing a raw substring.

Suggested regressions at `Transport.http().getChallenges`:

- X402-only and quoted Payment text: the x402 offer is still collected.
- Real mixed-case Payment plus x402: both protocols' offers remain available.
- Malformed actual Payment challenge plus x402: preserve the explicit parsing failure, rather than silently treating malformed MPP as absent.
- Non-402 and missing-header controls retain their previous behavior.

These can use synthetic Responses and inspect collected challenges without creating credentials or making payments. I have not run those transport regressions, the full suite, or a payment flow.
