# R17 isolated verification

Actual command: `python r17_check.py`; exit 0.
Python 3.12.14; Pydantic 2.14.1. 29 check groups passed.

- 6 original source annotation groups reject object input and accept JSON string input.
- 4 unmodified _vdom_params groups reproduce AttributeError for decoded non-object truthy JSON values.
- 4 candidate normalizer groups accept objects/equivalent JSON text including empty objects.
- 9 candidate groups reject malformed JSON or decoded non-object shapes.
- 4 required-union validation groups reject native list/scalar/None.
- 1 optional None/default group.
- 1 Pydantic JSON-schema object/string group.

The 10 baseline groups and 19 candidate/type/helper groups are not upstream tests. The two source blobs are hash-verified. Only an AST-extracted method and type annotations are executed; no upstream imports, server entrypoint or network. The helper is a candidate, not installed into all six handlers. No FastMCP, httpx, MCP dispatch, Claude Code, FortiGate, HTTP, secrets, real payment, or full suite.

## Input preparation

The run obtained both files through the GitHub connector at commit `5c82a1e6e2b7a336cd9b22881d50a658d8bdcb06` and wrote a temporary r17_sources.json. To reproduce, retrieve tools/generic.py and fortios_client.py at that exact commit, then form:

```python
import json
from pathlib import Path
Path("r17_sources.json").write_text(json.dumps({
    "generic": Path("generic.py").read_text(),
    "client": Path("fortios_client.py").read_text(),
    "shas": {
        "generic": "8ca014c5e241867b3d7bd13a81d7618f95e2b420",
        "client": "9fdd7140e28a5a13f2ce108db8f17be84720c593"
    }
}))
```

This preparation snippet documents the input format; the executed run used connector-provided text directly. Save the following executed harness next to r17_sources.json. It requires Pydantic already available; no install was performed in the run.

## Executed harness

```python
"""Isolated source/type boundaries, NOT FastMCP or a live FortiGate test."""
import ast
import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Annotated, Any
import pydantic
from pydantic import Field, TypeAdapter, ValidationError

src = json.loads(Path(__file__).with_name('r17_sources.json').read_text())
for name in ('generic', 'client'):
    b = src[name].encode()
    assert hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == src['shas'][name]
results = []
def passed(name):
    results.append(name)

functions = {n.name: n for n in ast.walk(ast.parse(src['generic'])) if isinstance(n, ast.AsyncFunctionDef)}
params = {'cmdb_create': 'data', 'cmdb_update': 'data', 'monitor_get': 'extra_params', 'monitor_action': 'body', 'log_get': 'extra_params', 'service_call': 'body'}
for name, param in params.items():
    node = next(a for a in functions[name].args.args if a.arg == param)
    annotation = eval(compile(ast.Expression(node.annotation), '<annotation>', 'eval'))
    adapter = TypeAdapter(annotation)
    try:
        adapter.validate_python({'count': 20})
    except ValidationError as exc:
        assert exc.errors()[0]['type'] == 'string_type'
    else:
        raise AssertionError(name)
    assert adapter.validate_python('{"count":20}') == '{"count":20}'
    passed('baseline annotation rejects object: ' + name)

node = next(n for n in ast.walk(ast.parse(src['client'])) if isinstance(n, ast.FunctionDef) and n.name == '_vdom_params')
env = {'Any': Any}
exec(compile(ast.Module(body=[node], type_ignores=[]), '<unmodified _vdom_params>', 'exec'), env)
vdom = env['_vdom_params']
for raw in ('[1]', '1', 'true', json.dumps('{"count":20}')):
    try:
        vdom(SimpleNamespace(vdom='root'), json.loads(raw))
    except AttributeError as exc:
        assert 'items' in str(exc)
    else:
        raise AssertionError(raw)
    passed('baseline decoded non-object reaches items: ' + raw)

# Candidate helper only; no patch is installed into upstream handlers.
def json_object(value: dict[str, Any] | str, field: str) -> dict[str, Any]:
    parsed = json.loads(value) if isinstance(value, str) else value
    if not isinstance(parsed, dict):
        raise ValueError(f'{field} must be a JSON object')
    return parsed

candidate = TypeAdapter(dict[str, Any] | str)
for raw in ({'count': 20}, '{"count":20}', {}, '{}'):
    got = json_object(candidate.validate_python(raw), 'extra_params')
    expected = {'count': 20} if raw in ({'count': 20}, '{"count":20}') else {}
    assert got == expected
    assert vdom(SimpleNamespace(vdom='root'), got) == {'vdom': 'root', **expected}
    passed('candidate valid object form: ' + repr(raw))
for raw in ('[]', '[1]', 'null', 'false', '0', '1', '""', json.dumps('{"count":20}'), '{'):
    try:
        json_object(candidate.validate_python(raw), 'extra_params')
    except ValueError:
        pass
    else:
        raise AssertionError(raw)
    passed('candidate rejects malformed/non-object: ' + raw)
for raw in ([], 0, False, None):
    try:
        candidate.validate_python(raw)
    except ValidationError:
        pass
    else:
        raise AssertionError(raw)
    passed('candidate required type rejects: ' + repr(raw))
optional = TypeAdapter(dict[str, Any] | str | None)
assert optional.validate_python(None) is None
assert vdom(SimpleNamespace(vdom='root'), None) == {'vdom': 'root'}
passed('optional None remains absence; caller preserves defaults')
assert {x['type'] for x in candidate.json_schema()['anyOf']} == {'object', 'string'}
passed('candidate Pydantic schema advertises object and string')
print(json.dumps({'python': sys.version.split()[0], 'pydantic': pydantic.__version__, 'passed_groups': len(results), 'groups': results, 'scope': 'Pydantic annotation validation, unmodified _vdom_params extract, candidate helper only; no FastMCP, HTTP, FortiGate, full suite, or installed handler patch'}, indent=2))
```

## Proposed regressions NOT run

For all six handlers, exercise actual FastMCP registration/tools/list/tools/call with a mocked FortiOS client. Compare dict and JSON-string forms; assert malformed JSON, lists, scalars, double-encoded strings never invoke that client. Check optional omission, None, legacy empty strings, empty objects, method routing and error formatting. Reconcile PR #2 paging semantics. Run the upstream suite before claiming integrated success.
