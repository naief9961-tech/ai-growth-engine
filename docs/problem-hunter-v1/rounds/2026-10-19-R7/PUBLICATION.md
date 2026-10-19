# R7 manual publication — 2026-10-19

The user manually published [R7-02](https://github.com/bergbacher/hyde-mcp-gateway/issues/34#issuecomment-6260256914) as **naief9961-tech** at 2026-10-19T05:19:23Z (08:19:23 Asia/Riyadh). Account and full text were fetched and verified; technical content matches the copy-ready conversation reply. No comment was sent by this verification action. No subsequent developer reply was present. No commercial interest or purchase established.

Ledger last_own_comment_id and last_seen_comment_id: **6260256914**. Do not repost. R7-01 remains held due to [upstream PR #573](https://github.com/ktysne/agent-cockpit/pull/573); no publication authorized for it.

## Verified published text

At `3a518f59106ad6597ff27896880b1819ded64ca2`, the report reads `[...schemas.redactedSchemas.keys()]`, while the store inserts each app as its asynchronous read finishes. I reproduced the reversed order deterministically with the extracted SchemaStore: start both apps, release crm's reads first, then shop's. The live map was `["crm", "shop"]`.

If registry order is the intended report contract, this small projection in `src/boot.ts` avoids changing refresh or map semantics:

```ts
redacted: appNames(registry).filter(
  app => schemas.redactedSchemas.has(app),
),
```

The `has` filter matters: a registered app whose first schema load failed must remain absent. The isolated checks returned `["shop", "crm"]` for reversed completion, retained the last-good entries after a failed refresh, and reported only crm when shop had never loaded. The map itself remained in completion order and all reads still started concurrently.

One adjacent assertion deserves review: `test/schema-store.test.ts` also expects log-map keys in `["shop", "crm"]` order, whereas its redacted-map assertion sorts the keys. A report-only fix does not establish ordering for the store's live maps. Compare their membership without order unless that is a separate store contract.

For the boot regression, control completion with deferred promises instead of repeated runs or timing sleeps. I tested source-extracted store/control-flow code with synthetic readers and parser stubs; I did not run Vitest, the full boot integration, or typechecking.
