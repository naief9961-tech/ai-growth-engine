# R37-01 — NOT POSTED; pending user approval

Destination: https://github.com/handi7/lontar-cms/issues/452

I reproduced the projection boundary at d16fd22d49bb74579a73a09b8c06649c17184b9d using the actual locale.ts module with its imports removed. For a localized richText field, projecting {body: {id: richTextDoc, en: ...}} once preserves the rich-text document; projecting that result again returns body: null.

There is a useful constraint on the proposed fix: checking only whether the object has the requested/default locale keys is not sufficient to identify an already-projected value. A canonical {fr: richTextDoc} with requested locale id and fallback en has neither key, but must not be passed through as if it were a rich-text document. That heuristic exposes the locale dictionary in the payload instead of producing the expected missing-value result.

I would make the representation explicit at the mutation/dispatcher and transition boundaries, and project only canonical input. Do not simply remove every projection: publish.ts deliberately uses updateLocale='all' for publish, while unpublish uses the requested locale; the publish path still needs its projection. Keep sanitizeDocRead and its existing ordering/overrideAccess behavior intact.

The regression matrix should cover create/update/unpublish with already-projected richText, publish from canonical data, a canonical value missing both requested and fallback locales, valid fallback, locale='all', and both collection/global paths. Assert the actual webhook payload and public operation result, with a denied field to ensure access filtering remains effective.

Eight isolated assertions passed: they reproduce the double projection, exercise a small explicit-representation boundary model, and demonstrate the missing-key heuristic counterexample. This is not an integrated repair: I have not run either database adapter, webhook delivery, access-control integration or the upstream suite.