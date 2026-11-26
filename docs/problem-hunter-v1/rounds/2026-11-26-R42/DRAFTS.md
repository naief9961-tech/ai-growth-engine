# R42-01 — fitness-app131 · PENDING USER REVIEW · NOT POSTED

Destination: https://github.com/KhubaibQaiser/fitness-app/issues/131

One new draft only. Recheck the issue and related PRs immediately before any approved posting. Prior approvals and remote file values do not approve this reply.

---

I checked `162bffbd` and found a concrete starting scope beyond notifications:

| Route | Timestamp currently passed through |
| --- | --- |
| GET /v1/clients/{clientId}/notes | items[].createdAt |
| POST /v1/clients/{clientId}/notes | createdAt |
| GET /v1/clients/{clientId}/check-ins | items[].completedAt |
| GET /v1/check-ins/{id} | completedAt |

The [notes handlers](https://github.com/KhubaibQaiser/fitness-app/blob/162bffbd2367f39be6c8dd57d8a213d3b225bed6/apps/api/src/routes/clients.ts) and [check-in handlers](https://github.com/KhubaibQaiser/fitness-app/blob/162bffbd2367f39be6c8dd57d8a213d3b225bed6/apps/api/src/routes/check-ins.ts) serialize these domain results directly. The [notes queries](https://github.com/KhubaibQaiser/fitness-app/blob/162bffbd2367f39be6c8dd57d8a213d3b225bed6/packages/modules/src/coaching/notes.ts) return database rows, while the [check-in projection](https://github.com/KhubaibQaiser/fitness-app/blob/162bffbd2367f39be6c8dd57d8a213d3b225bed6/packages/modules/src/coaching/checkins.ts#L451-L493) selects completedAt unchanged.

One audit trap: these responses currently use generic `anyObject`/`objectList` schemas. Their committed OpenAPI response objects have no named timestamp properties, so searching only for `format: date-time` will miss them. Cross-check route projections and DB columns as well as OpenAPI.

A bounded fix is explicit serializers using the existing `toStrictIso`, applied to both list and single/create responses:

```ts
const serializeNote = <T extends { createdAt: string | Date }>(row: T) => ({
  ...row,
  createdAt: toStrictIso(row.createdAt),
});

const serializeCheckIn = <
  T extends { completedAt: string | Date | null }
>(row: T) => ({
  ...row,
  completedAt: row.completedAt === null ? null : toStrictIso(row.completedAt),
});
```

Map list rows through the relevant serializer and wrap the corresponding single-row response. Preserve `scheduledFor` as its date-only value and leave free text untouched; avoid recursively converting every date-looking string. Also audit `recentCheckIns` in the aggregated client-detail response separately.

I ran eight isolated assertion groups using the pinned route-handler bodies, the actual timestamp helper and Luxon 3.7.2. All four baseline handlers passed through the synthetic Postgres string unchanged; the candidate mappings emitted `2026-11-23T20:14:59.426Z`. Checks also covered null completion, offset conversion, malformed input rejection, unchanged date-only/free-text fields, and the generic OpenAPI response shape.

These tests stubbed Hono, authorization and domain/database calls. They do **not** establish real database or Hermes integration, and no workspace typecheck/full suite ran. Before merging, add PGlite-backed route tests following the notification test in #120, assert both exact instants and wire shape, preserve null/date-only values, and verify the native consumer.
