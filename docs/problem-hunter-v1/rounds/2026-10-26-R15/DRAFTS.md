# R15-01 — SDRangel #3039

Status: **POSTED MANUALLY AND VERIFIED — DO NOT REPOST**.
Published by naief9961-tech at 2026-10-26T05:33:35Z; verified at 2026-10-26T05:37:19Z.
Comment: https://github.com/f4exb/sdrangel/issues/3039#issuecomment-6409005409
No subsequent developer reply at verification.
Destination: https://github.com/f4exb/sdrangel/issues/3039
Static review only; no native/client/hardware validation. Historical text retained below; this publication does not authorize future comments.

---

AI-assisted source review at [24ac6138](https://github.com/f4exb/sdrangel/blob/24ac61389837c63dedd61fed762d74d5860c3430/plugins/feature/mcpserver/mcptools.cpp).

The missing `items` comes from `prop("array", ...)`: that helper only sets `type` and `description`. The nearby `scan` registration already shows the appropriate pattern: create the array property, then attach a numeric `items` schema. Apply that same pattern to `tune_gain.values`, keeping its existing description and optional status:

```cpp
QJsonObject gainValues = prop("array",
    "For a device type this does not know: the gain values to try, in the key's own units, lowest first");
gainValues["items"] = QJsonObject{{"type", "number"}};
// In tune_gain's schema initializer:
{"values", gainValues}
```

One additional regression boundary is the packaged tool list. [toolsdump.cpp](https://github.com/f4exb/sdrangel/blob/24ac61389837c63dedd61fed762d74d5860c3430/plugins/feature/mcpserver/toolsdump.cpp) serializes the same `MCPTools::listTools()`, and [the bundle build](https://github.com/f4exb/sdrangel/blob/24ac61389837c63dedd61fed762d74d5860c3430/plugins/feature/mcpserver/bridge/CMakeLists.txt) writes it to `server/tools.json`. Regenerate that file from the corrected source so a client starting before SDRangel does not receive the old schema.

Suggested checks:
- Inspect `tune_gain.inputSchema.properties.values.items.type` in both live `tools/list` and the generated bundle: it should be `number`.
- Confirm `values` remains optional and other tool definitions are unchanged.
- Start the client with SDRangel stopped and then running; verify tool discovery in both paths without invoking `tune_gain`.

Also, [a bare array is valid generic JSON Schema](https://json-schema.org/understanding-json-schema/reference/array); the reported rejection is a stricter client compatibility requirement. A generic schema-validity check alone will not catch this omission.

This is static source analysis. I have not compiled the Qt plugin, generated the bundle, tested Copilot, or exercised radio hardware.
