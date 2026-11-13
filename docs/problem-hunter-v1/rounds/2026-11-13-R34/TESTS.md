# R34 — Offline transport experiment

Commit: `4782e389daf2b05f9fd762a65dec8c0cdade5177`. Python3.12.14. Nine check groups passed; not a full system fix. No network/API keys/real endpoints/commands/packages/registry initialization/config writes. `example.invalid` is synthetic.

## Source provenance
- [src/apm_cli/adapters/client/base.py](https://github.com/microsoft/apm/blob/4782e389daf2b05f9fd762a65dec8c0cdade5177/src/apm_cli/adapters/client/base.py): Git blob `4659cb43b84cb536771aa2092845428122c88337`
- [src/apm_cli/adapters/client/gemini.py](https://github.com/microsoft/apm/blob/4782e389daf2b05f9fd762a65dec8c0cdade5177/src/apm_cli/adapters/client/gemini.py): Git blob `b889fc66b94aae27987e5a73125b27a07060bdea`
- [src/apm_cli/adapters/client/antigravity.py](https://github.com/microsoft/apm/blob/4782e389daf2b05f9fd762a65dec8c0cdade5177/src/apm_cli/adapters/client/antigravity.py): Git blob `53a52c61e621638afa0e709d28ec89546a8e1694`

Download the three pinned original files as base.py, gemini.py, antigravity.py beside probe.py; preserve bytes. The harness checks their Git blob hashes before AST extraction. Source code is not vendored here. Save the following harness as probe.py and run `python3 probe.py` in an isolated directory. It extracts the real class definitions without imports/initializers and only the two base helper methods needed by these fixtures. Paths are computed, not written. Nonempty _extra, environment/header resolution and package branches are outside scope.

## Harness and local candidate
```python
"""Offline source-extracted experiment; not APM/agy integration tests."""
import ast, hashlib, json, platform
from pathlib import Path

ROOT = Path(__file__).parent
MANIFEST = [{"local":"base.py","blob_sha":"4659cb43b84cb536771aa2092845428122c88337","path":"src/apm_cli/adapters/client/base.py","commit":"4782e389daf2b05f9fd762a65dec8c0cdade5177"},{"local":"gemini.py","blob_sha":"b889fc66b94aae27987e5a73125b27a07060bdea","path":"src/apm_cli/adapters/client/gemini.py","commit":"4782e389daf2b05f9fd762a65dec8c0cdade5177"},{"local":"antigravity.py","blob_sha":"53a52c61e621638afa0e709d28ec89546a8e1694","path":"src/apm_cli/adapters/client/antigravity.py","commit":"4782e389daf2b05f9fd762a65dec8c0cdade5177"}]

def tree(name):
    raw = (ROOT / name).read_bytes()
    expected = next(x["blob_sha"] for x in MANIFEST if x["local"] == name)
    actual = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    assert actual == expected, (name, actual, expected)
    return ast.parse(raw, filename=name)

base = tree("base.py")
gemini = tree("gemini.py")
antigravity = tree("antigravity.py")
base_class = next(n for n in base.body if isinstance(n, ast.ClassDef) and n.name == "MCPClientAdapter")
helpers = [n for n in base_class.body if isinstance(n, ast.FunctionDef) and n.name in {"_select_remote_with_url", "_merge_extra"}]
# No registry client, adapter initializer, package installation or external imports.
minimal_base = ast.ClassDef(name="CopilotClientAdapter", bases=[], keywords=[], body=helpers, decorator_list=[])
gclass = next(n for n in gemini.body if isinstance(n, ast.ClassDef))
aclass = next(n for n in antigravity.body if isinstance(n, ast.ClassDef))
ns = {"Path": Path}
exec(compile(ast.fix_missing_locations(ast.Module(body=[minimal_base, gclass, aclass], type_ignores=[])), "pinned_extract", "exec"), ns)
Gemini = ns["GeminiClientAdapter"]
Antigravity = ns["AntigravityClientAdapter"]

class Candidate(Antigravity):
    """Illustrative local experiment only; no upstream implementation."""
    def _format_server_config(self, server_info, env_overrides=None, runtime_vars=None):
        remotes = server_info.get("remotes", [])
        if not server_info.get("_raw_stdio") and remotes:
            remote = self._select_remote_with_url(remotes) or remotes[0]
            if (remote.get("transport_type") or "").strip() == "sse":
                raise ValueError("Antigravity CLI requires Streamable HTTP; legacy SSE is unsupported")
        config = super()._format_server_config(server_info, env_overrides, runtime_vars)
        if "httpUrl" in config:
            config["serverUrl"] = config.pop("httpUrl")
        return config

def adapter(cls, user=False):
    a = object.__new__(cls)
    a.user_scope = user
    a.project_root = Path("/synthetic/project")
    return a

a, g, c = adapter(Antigravity), adapter(Gemini), adapter(Candidate)
rows = []
url = "https://example.invalid/mcp"
# Four HTTP spellings/defaults: actual source emits Gemini's unsupported key.
for label, extra in [("http", {"transport_type": "http"}), ("streamable-http", {"transport_type": "streamable-http"}), ("empty-default", {"transport_type": ""}), ("omitted-default", {})]:
    info = {"name":"synthetic", "remotes":[{"url":url, **extra}]}
    before = a._format_server_config(info)
    after = c._format_server_config(info)
    assert before == {"httpUrl":url}
    assert after == {"serverUrl":url}
    assert g._format_server_config(info) == before
    rows.append({"case":label,"baseline":before,"candidate":after,"gemini_unchanged":True})
info = {"remotes":[{"url":url, "transport_type":"sse"}]}
assert a._format_server_config(info) == g._format_server_config(info) == {"url":url}
try:
    c._format_server_config(info)
    raise AssertionError("candidate accepted legacy SSE")
except ValueError:
    pass
rows.append({"case":"legacy-sse","baseline":"accepted as url","candidate":"rejected","gemini_unchanged":True})
info = {"remotes":[{"url":url, "transport_type":"unsupported"}]}
for instance in (a,g,c):
    try:
        instance._format_server_config(info)
        raise AssertionError("invalid transport accepted")
    except ValueError:
        pass
rows.append({"case":"invalid-transport","baseline":"rejected","candidate":"rejected","gemini_unchanged":True})
info = {"_raw_stdio":{"command":"synthetic-never-executed","args":[]}}
for instance in (a,g,c):
    assert instance._format_server_config(info) == {"command":"synthetic-never-executed","args":[]}
rows.append({"case":"stdio-no-arguments","baseline":"preserved","candidate":"preserved","gemini_unchanged":True})
for user in (False, True):
    expected = Path.home()/".gemini"/"config"/"mcp_config.json" if user else Path("/synthetic/project/.agents/mcp_config.json")
    for cls in (Antigravity, Candidate):
        assert Path(adapter(cls,user).get_config_path()) == expected
    rows.append({"case":"user-path" if user else "project-path","baseline":"expected path","candidate":"unchanged"})
result={"python":platform.python_version(),"commit":MANIFEST[0]["commit"],"checks_passed":len(rows),"cases":rows,"limitations":["AST-extracted actual formatter, path methods, selection and extra-field helpers; no adapter initialization or CLI integration.","No agy binary, network, credentials, package installation, config writes, header/env resolution, _extra payloads, local-package branch or full suite tested.","Candidate is a local experiment and does not establish complete repair or runtime discovery."]}
print(json.dumps(result,indent=2))
(ROOT/"results.json").write_text(json.dumps(result,indent=2)+"\n")

```

## Observed output
```json
{
  "python": "3.12.14",
  "commit": "4782e389daf2b05f9fd762a65dec8c0cdade5177",
  "checks_passed": 9,
  "cases": [
    {
      "case": "http",
      "baseline": {
        "httpUrl": "https://example.invalid/mcp"
      },
      "candidate": {
        "serverUrl": "https://example.invalid/mcp"
      },
      "gemini_unchanged": true
    },
    {
      "case": "streamable-http",
      "baseline": {
        "httpUrl": "https://example.invalid/mcp"
      },
      "candidate": {
        "serverUrl": "https://example.invalid/mcp"
      },
      "gemini_unchanged": true
    },
    {
      "case": "empty-default",
      "baseline": {
        "httpUrl": "https://example.invalid/mcp"
      },
      "candidate": {
        "serverUrl": "https://example.invalid/mcp"
      },
      "gemini_unchanged": true
    },
    {
      "case": "omitted-default",
      "baseline": {
        "httpUrl": "https://example.invalid/mcp"
      },
      "candidate": {
        "serverUrl": "https://example.invalid/mcp"
      },
      "gemini_unchanged": true
    },
    {
      "case": "legacy-sse",
      "baseline": "accepted as url",
      "candidate": "rejected",
      "gemini_unchanged": true
    },
    {
      "case": "invalid-transport",
      "baseline": "rejected",
      "candidate": "rejected",
      "gemini_unchanged": true
    },
    {
      "case": "stdio-no-arguments",
      "baseline": "preserved",
      "candidate": "preserved",
      "gemini_unchanged": true
    },
    {
      "case": "project-path",
      "baseline": "expected path",
      "candidate": "unchanged"
    },
    {
      "case": "user-path",
      "baseline": "expected path",
      "candidate": "unchanged"
    }
  ],
  "limitations": [
    "AST-extracted actual formatter, path methods, selection and extra-field helpers; no adapter initialization or CLI integration.",
    "No agy binary, network, credentials, package installation, config writes, header/env resolution, local-package branch or full suite tested.",
    "Candidate is a local experiment and does not establish complete repair or runtime discovery.",
    "Nonempty _extra payloads are not exercised."
  ]
}
```

## Additional regressions for maintainers (not executed here)
- Native APM tests should assert remote HTTP formatting for both scopes and preserve headers/options.
- Keep Gemini HTTP and SSE behavior; do not alter the shared formatter globally.
- Validate supported-transport selection when registry metadata offers several remotes.
- Run agy with a known Streamable HTTP fixture and confirm discovery; confirm selected legacy SSE gives an actionable rejection.
- Re-run existing atomic-write/preservation tests and package stdio tests.
