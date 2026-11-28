# R44 review draft — NOT POSTED

Target: https://github.com/IndianOpinion/mcp/issues/27
Status: PENDING_USER_REVIEW. Recheck issue/comments/PRs immediately before any later authorized publication.
AI-assisted source review and isolated reproduction. No production access.

## Full proposed English comment

I checked `src/tools.js` at [`b46fa71`](https://github.com/IndianOpinion/mcp/blob/b46fa71e8ea583bc9b1fc1322b7dd19748e3bc50/src/tools.js). One regression-test gap is that [the REST stub](https://github.com/IndianOpinion/mcp/blob/b46fa71e8ea583bc9b1fc1322b7dd19748e3bc50/test/stub-rest.mjs#L256) always supplies a source URL. That fixture cannot expose the reported production-shaped response with only `outlet` and `headline`.

A narrow fix is to change only the breaking-event source schema, retaining the separate `get_brief` contract:

```js
sources: z.array(z.looseObject({
  outlet: str,
  headline: str.optional(),
  url: str.optional(),
})).optional()
```

Keep the REST object as `structuredContent`; do not invent a link from the outlet name or discard source provenance. Update the breaking-event text rendering too:

```js
...(r.sources || []).map((s) =>
  `- ${s.outlet}${s.headline ? `: ${s.headline}` : ''}${s.url ? ` <${s.url}>` : ''}`
),
```

I ran the pinned public tool-registration/handler code with a synthetic REST client and Zod 4.6.7 on Node 24.22.3. Twelve isolated check groups passed against the candidate: missing-URL, legacy-URL, headline-plus-URL and mixed sources; absent/empty arrays; preserved unknown fields; rejection of numeric URLs and missing outlets; unchanged authentication/404 behavior; and the exported JSON Schema plus unchanged `get_brief` schema. The baseline rejects the missing-URL fixture and renders `<undefined>`.

Before accepting this, add the URL-less fixture to the existing SDK-level tests and assert both a successful `callTool` and the exact source text/structured fields. Retain a URL-present fixture as a compatibility control.

These checks did **not** run the MCP transport, the full repository suite, or the live REST service. The public repository is a mirror, so maintainers still need to validate and deploy through the private source repository.
