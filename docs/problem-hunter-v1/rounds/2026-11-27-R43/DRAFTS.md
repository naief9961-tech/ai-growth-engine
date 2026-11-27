# R43 historical copy — RETIRED, DO NOT POST

## Publication follow-up — 2026-11-27T10:23:57Z

**R43-01 is retired: DO NOT POST.** The user approved the reviewed reply in chat. The pre-publication check found [PR499](https://github.com/abhi478jeetur-rgb/env-saaf/pull/499) merged at 2026-11-27T07:18:19Z (10:18:19 Asia/Riyadh), merge commit `c0154b947ba81ca1b6564140885e062b05cd0af6`, and [issue494](https://github.com/abhi478jeetur-rgb/env-saaf/issues/494) closed. The exact CLI diff was read: selected-file extras, exit/scaffold gates, per-file text labels and deduplicated JSON union are implemented. No third-party comment was attempted or posted; the issue has0comments. No repair credit or commercial interest claimed. Upstream runtime tests were not rerun. The earlier R43 evidence and original draft below are historical, not current publication advice.

Destination: https://github.com/abhi478jeetur-rgb/env-saaf/issues/494

Original status at investigation: pending review. Subsequently approved in chat, then retired after the pre-publication check. No third-party comment posted.

## R43-01 — historical English text (do not post)

I reproduced this against `0b9a97dcb87badf5d198314df0617e716a34214b` using the actual CLI in temporary synthetic projects.

There is one regression trap worth covering: copying both sides of the existing `.env` diff into the `--values` path would turn omitted optional/defaulted keys into `envMissing` failures. A values file can legitimately omit those keys; required omissions should continue through `validateEnv`.

The current split is in [cli.js](https://github.com/abhi478jeetur-rgb/env-saaf/blob/0b9a97dcb87badf5d198314df0617e716a34214b/cli.js#L1185): key comparison always reads `.env`, while the later `targetName` branch reads the selected values file only for validation.

A narrow fix is to collect only the selected file's extra keys immediately after reading `rawValues`:

```js
// Declare valuesExtra = [] in runCheck(), before the schema branch.
if (valuesOpt !== null) {
  valuesExtra = diffEnv(Object.keys(rawValues), documented).usedNotDocumented;
}
```

Combine those keys into `envExtra` **before** calculating `scaffoldAhead` and `ok`, so a project with no code usage cannot incorrectly pass. Keep `validateEnv` and the existing missing-key handling unchanged. Use the parsed raw keys, before any example-secret guard strips values.

In my candidate I preserved the existing local `.env` findings, deduplicated the JSON `envExtra` union, and retained separate key lists for text output: local findings say `.env`, selected-file findings say `valuesOpt`, and both use `fileOpt` for the template name. Selecting `./.env` does not print the same finding twice. This deliberately preserves current local-file checking; replacing that policy would be a separate behavior change.

Verification: 12 paired scenarios passed on Node 24.22.3, each running baseline/candidate in text and JSON modes (48 CLI subprocesses). They cover extras with/without a local `.env`, clean values, invalid values, required omissions, optional/default omissions, a custom template, simultaneous local/selected-file findings, `--values ./.env`, a missing values file, grouped schema keys, and the no-`--values` path. The extra-only reproductions changed from exit 0 to exit 1 with populated `envExtra`; clean and optional/default cases stayed at exit 0. The repository's existing `node test-cli.js` also passed on both copies.

I have not run the complete `npm test` pipeline, other Node versions, Windows, watch mode, or `--fix` interactions. These checks establish the bounded CLI behavior, not a deployment validation. The focused cases should be added to `test-cli.js`, with the requested README/CHANGELOG updates, before merging.
