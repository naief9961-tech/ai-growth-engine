# R11 isolated evidence — OpenViking #6471

Checked 2026-10-23T05:07:40Z. Source commit: `0d546854b4be4b24a277c1b3ca7cf06c02d61a14`. Node **v24.19.0**. No dependency installation.

## What actually ran

The full canonical `createOpenVikingMcpProxy` module and its three actual imported dependencies were loaded, without source extraction or replacement dependencies. Only the documented `readConfig`, `loggerFactory`, `stdout` and `fetchImpl` seams were supplied by the harness. Configuration and messages are synthetic; no credentials, remote requests, wallets or payments were used. The `.invalid` URL is never contacted.

**21 before/after assertion groups passed (42 complete-core `handleMessage` executions).** Sixteen response cases produced the expected spurious error in baseline and zero stdout messages in the local candidate. Five request/notification controls retained their behavior. Every execution asserted exactly one forwarded POST body equal to its input. Failed response deliveries still reached the injected diagnostic logger.

| Input matrix | Transport result | Original stdout | Candidate stdout |
| --- | --- | --- | --- |
| Result/error response × ID 0/string (4 cases each row) | 202 empty | -32003 | none |
| Same | 403 | -32001 | none |
| Same | 500 | -32002 | none |
| Same | injected AbortError | -32004 | none |
| Request `ping`, ID 0 | 200 JSON / 202 empty / 500 | result / -32003 / -32002 | unchanged |
| Notification | 202 / 500 | none | none |

This is a regression matrix, not 21 upstream tests. The baseline reproduction assertions intentionally expect the broken behavior, so the harness exits successfully after proving the before/after difference.

## Scope limits

NOT RUN: upstream test suite, live HTTP or stdio processes, real clients, real timer expiry, session reinitialization/replay (including 400/404), credential rotation, packaging/release checks, or malformed-message/schema validation. This does not prove an end-to-end repair. No upstream file was modified. The candidate is only a two-line classifier change in a temporary local copy.

The existing upstream `mcp-proxy-core.test.mjs` was inspected for its test seam; its tests were **not** run. Do not inherit author-reported test results from any issue/PR.

## Pinned sources

- [examples/memory-plugin-shared/lib/mcp-proxy-core.mjs](https://github.com/volcengine/OpenViking/blob/0d546854b4be4b24a277c1b3ca7cf06c02d61a14/examples/memory-plugin-shared/lib/mcp-proxy-core.mjs) — Git blob `5891599e68dfea801aca2f3e542a7b4b25601d46`.
- [examples/memory-plugin-shared/lib/ov-http.mjs](https://github.com/volcengine/OpenViking/blob/0d546854b4be4b24a277c1b3ca7cf06c02d61a14/examples/memory-plugin-shared/lib/ov-http.mjs) — Git blob `b359783916df8832ede27dc7346f641bf307829c`.
- [examples/memory-plugin-shared/lib/mcp-proxy-config.mjs](https://github.com/volcengine/OpenViking/blob/0d546854b4be4b24a277c1b3ca7cf06c02d61a14/examples/memory-plugin-shared/lib/mcp-proxy-config.mjs) — Git blob `74573ff78fbf5acb40bcb82cf5d9577cba0fb570`.
- [examples/memory-plugin-shared/lib/credentials.mjs](https://github.com/volcengine/OpenViking/blob/0d546854b4be4b24a277c1b3ca7cf06c02d61a14/examples/memory-plugin-shared/lib/credentials.mjs) — Git blob `d47a448ff5b19268cf9236884163627b8f3385e9`.
- [agent-plugins/servers/shared/mcp-proxy-core.mjs](https://github.com/volcengine/OpenViking/blob/0d546854b4be4b24a277c1b3ca7cf06c02d61a14/agent-plugins/servers/shared/mcp-proxy-core.mjs) — Git blob `495819f85dc369a27936606c750222d1a943e183`.
- [examples/memory-plugin-shared/sync.mjs](https://github.com/volcengine/OpenViking/blob/0d546854b4be4b24a277c1b3ca7cf06c02d61a14/examples/memory-plugin-shared/sync.mjs) — Git blob `180bb738e8ee82cd203e45ce73560fc820df0a10`.

Actual content bytes of the four loaded original modules were verified against the listed Git blob SHA-1 values. The committed core copy under `agent-plugins/servers/shared` is identical to the canonical core after removing its generated banner. The recursive tree shows that the Claude Code and Codex copies share that same generated blob, `495819f85dc369a27936606c750222d1a943e183`. The existing sync script declares these committed targets; it was read, not executed.

Protocol reference: [MCP 2025-06-18 transport](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports), the revision used by the reviewed core. Accepted response/notification POSTs return an empty 202. No assertion is made about conformance to every newer MCP revision.

## Reproduce

During this run sources were fetched through the connected GitHub reader and exported byte-for-byte. For independent reproduction, the equivalent acquisition script below fetches the same pinned public files and refuses a blob mismatch. This alternative downloader itself was not executed in this run. Save it as `prepare.py` in a new temporary directory, run `python3 prepare.py`, then save the following harness as `checks.mjs` alongside `original/` and run `node checks.mjs` with Node 24. No packages are required.

```python
from pathlib import Path
import hashlib
import urllib.request
import json

commit = "0d546854b4be4b24a277c1b3ca7cf06c02d61a14"
manifest = [
  {
    "path": "examples/memory-plugin-shared/lib/mcp-proxy-core.mjs",
    "blob": "5891599e68dfea801aca2f3e542a7b4b25601d46"
  },
  {
    "path": "examples/memory-plugin-shared/lib/ov-http.mjs",
    "blob": "b359783916df8832ede27dc7346f641bf307829c"
  },
  {
    "path": "examples/memory-plugin-shared/lib/mcp-proxy-config.mjs",
    "blob": "74573ff78fbf5acb40bcb82cf5d9577cba0fb570"
  },
  {
    "path": "examples/memory-plugin-shared/lib/credentials.mjs",
    "blob": "d47a448ff5b19268cf9236884163627b8f3385e9"
  }
]
out = Path("original")
out.mkdir(exist_ok=True)
for item in manifest:
    url = f"https://raw.githubusercontent.com/volcengine/OpenViking/{commit}/{item['path']}"
    with urllib.request.urlopen(url, timeout=30) as response:
        data = response.read()
    actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert actual == item["blob"], (item["path"], actual)
    (out / Path(item["path"]).name).write_bytes(data)
source = (out / "mcp-proxy-core.mjs").read_text()
old = 'return Object.prototype.hasOwnProperty.call(message || {}, "id");'
assert source.count(old) == 1
candidate = source.replace(old, 'return typeof message?.method === "string"\n    && Object.prototype.hasOwnProperty.call(message, "id");')
(out / "candidate-core.mjs").write_text(candidate)

```

```js
import assert from "node:assert/strict";
import { Writable } from "node:stream";
import { createOpenVikingMcpProxy as original } from "./original/mcp-proxy-core.mjs";
import { createOpenVikingMcpProxy as candidate } from "./original/candidate-core.mjs";
import { writeFileSync } from "node:fs";

const rows = [];
async function run(factory, message, transport) {
  const calls = [], out = [], logs = [];
  const proxy = factory({
    stdout: new Writable({ write(chunk, _enc, cb) { out.push(chunk.toString()); cb(); } }),
    readConfig: () => ({ mcpUrl: "https://fixture.invalid/mcp", timeoutMs: 1000, watchedPaths: [] }),
    loggerFactory: () => ({ log(...v) { logs.push(v); }, logError(...v) { logs.push(v); } }),
    fetchImpl: async (url, init) => {
      assert.equal(url, "https://fixture.invalid/mcp");
      assert.equal(init.method, "POST");
      assert.equal(init.headers.Authorization, undefined);
      calls.push(JSON.parse(init.body));
      if (transport === "abort") throw Object.assign(new Error("synthetic abort"), { name: "AbortError" });
      if (transport === "json") return new Response(JSON.stringify({ jsonrpc: "2.0", id: message.id, result: {} }), { status: 200, headers: { "content-type": "application/json" } });
      const status = Number(transport);
      return new Response(null, { status });
    },
  });
  await proxy.handleMessage(message);
  await proxy.closeSession();
  assert.deepEqual(calls, [message]);
  return { messages: out.join("").trim().split("\n").filter(Boolean).map(JSON.parse), logs };
}
for (const id of [0, "server-ping"]) {
  for (const kind of ["result", "error"]) {
    const message = { jsonrpc: "2.0", id, ...(kind === "result" ? { result: {} } : { error: { code: -32603, message: "synthetic failure" } }) };
    for (const transport of ["202", "403", "500", "abort"]) {
      const before = await run(original, message, transport);
      const after = await run(candidate, message, transport);
      assert.equal(before.messages.length, 1);
      assert.equal(before.messages[0].id, id);
      const code = { "202": -32003, "403": -32001, "500": -32002, abort: -32004 }[transport];
      assert.equal(before.messages[0].error.code, code);
      assert.deepEqual(after.messages, []);
      if (transport !== "202") assert(after.logs.length > 0);
      rows.push({ id, kind, transport, baseline_spurious_code: code, candidate_stdout: 0, status: "PASS" });
    }
  }
}
for (const transport of ["json", "202", "500"]) {
  const message = { jsonrpc: "2.0", id: 0, method: "ping" };
  for (const factory of [original, candidate]) {
    const r = await run(factory, message, transport);
    assert.equal(r.messages.length, 1);
    assert.equal(r.messages[0].id, 0);
    if (transport === "json") assert.deepEqual(r.messages[0].result, {});
    else assert.equal(r.messages[0].error.code, transport === "202" ? -32003 : -32002);
  }
  rows.push({ kind: "request-id-zero-control", transport, status: "PASS" });
}
for (const transport of ["202", "500"]) {
  for (const factory of [original, candidate]) {
    const r = await run(factory, { jsonrpc: "2.0", method: "notifications/initialized" }, transport);
    assert.deepEqual(r.messages, []);
    if (transport === "500") assert(r.logs.length > 0);
  }
  rows.push({ kind: "notification-control", transport, status: "PASS" });
}
const result = { node: process.version, groups_passed: rows.length, full_core_executions: rows.length * 2, baseline_response_failures_reproduced: 16, upstream_full_suite_run: false, real_network_requests: 0, rows };
writeFileSync(new URL("./results.json", import.meta.url), JSON.stringify(result, null, 2) + "\n");
console.log(JSON.stringify(result, null, 2));
```

[Actual result data](results.json). Harness is NAIF-authored; upstream source is linked/fetched rather than republished here and retains its original license.
