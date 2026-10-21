# R9 isolated tests — 2026-10-21

Actual execution: 2026-10-21T05:04:52.642Z, Node v24.19.0. **14 groups PASS.**
Eight cover both IntelliFlow timestamp verifier extracts; six cover Postiz catalog assertions and relay extracts.

## Reproduce

With Node 24 supporting `node:module.stripTypeScriptTypes` and Python 3:

```sh
python3 fetch_sources.py
node checks.mjs input
```

The downloader fetches only the seven pinned public sources in sources.json and verifies Git blob SHA-1. No npm installation. In this run source bytes were obtained through the GitHub connector, then the same blob checks ran locally; the standalone download helper was supplied for reproduction and was not network-executed here. Upstream source files are not vendored and retain their owners' rights.

The harness fails if extraction markers, patch markers or source hashes drift. It strips TypeScript types and executes only explicitly selected function/method extracts, never repository entrypoints or imported dependencies.

## Scope of stubs

- IntelliFlow: real Node HMAC and timing-safe comparison; fixed-clock Date stub. Synthetic public test key, synthetic body and generated headers; no provider or customer data.
- Postiz: real extracted coreToolNames, connect and callTool; synthetic DI, tool catalogs, list/call responses, URL-safety success, exception classes. No DNS/HTTP, OAuth, persistence, media job or ChatGPT connection. The optional flag is candidate fixture metadata, not a patch merged into Postiz.
- Source assertions compare the pinned main and release catalogs and absence of the optional flag.

## Results

1. **PASS** Stripe: both original verifiers accept correctly signed t=abc — source-extracted baseline.
2. **PASS** Stripe: finite-only candidate still accepts a signed numeric prefix with junk — candidate counterexample.
3. **PASS** Stripe: full grammar rejects malformed signed timestamps in both copies — source-extracted candidate.
4. **PASS** Stripe: valid signatures and original timestamp bytes preserved — source-extracted candidate.
5. **PASS** Stripe: inclusive tolerance boundaries remain unchanged — source-extracted candidate.
6. **PASS** Stripe: unsafe and out-of-window integers rejected — source-extracted candidate.
7. **PASS** Stripe: wrong key and mutated raw body rejected — source-extracted candidate.
8. **PASS** Stripe: missing timestamp or signature rejected — source-extracted candidate.
9. **PASS** Postiz: release catalog lacks MediaStatusTool; main registers it without optional flag — pinned source assertions.
10. **PASS** Postiz: current extracted gate rejects missing mediaStatusTool with the reported message — source-extracted baseline with stubs.
11. **PASS** Postiz: candidate optional metadata permits baseline connection — source-extracted gate; candidate metadata.
12. **PASS** Postiz: baseline identity tools remain mandatory — source-extracted gate; candidate metadata.
13. **PASS** Postiz: current catalog passes the original gate — source-extracted baseline with stubs.
14. **PASS** Postiz: absent optional tool still returns explicit call failure — source-extracted callTool with stubs.

## Not established

These tests do not establish a fixed deployment, a complete supported-version compatibility matrix, a real Stripe exploit, or completion of either repository's native lint/typecheck/unit/integration gates. Postiz adjustment/status capability handling still needs implementation and integrated validation; optional metadata alone is not a complete repair. IntelliFlow's configurable tolerance and real HTTP raw-body handling need native regression coverage.

Initial source export appended a newline and failed the hash precondition before any test ran. Re-exporting exact connector bytes corrected this harness-preparation error; the final successful run is recorded verbatim in results.json.
