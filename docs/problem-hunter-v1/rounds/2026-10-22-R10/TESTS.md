# R10 — executed checks, proposed regressions and limits

## Executed: Northplan complete-schema isolated checks

Python 3.12.14, Pydantic 2.14.0, NumPy 2.3.5, PyYAML 6.0.3. Existing installed packages only; no installs, secrets, network calls during validation, simulation, real accounts or financial operations. Result: **16 assertion groups PASS**, not 16 full-system tests.

Five fetched inputs were checked against their Git blob SHA-1 before execution. Complete schema.py plus moments.py, timeline.py and params/loader.py were loaded unmodified for the baseline; package __init__.py files were empty local scaffolding, not copied from upstream. The candidate only rewrites numeric type annotations and adds a bool guard. No dependency stubs. The fixture is upstream's zero-amount minimal YAML plus clearly synthetic boolean/value mutations; no financial parameters were loaded.

- Eleven paired baseline/candidate groups: seed, n_paths, birth_month, annual money, survivor share, inflation, correlation cell, allocation weight, contribution weight, election age, RRIF fraction.
- One paired grid group rejects False through both numeric union branches and checks located error prefixes.
- Four retention groups: accepted YAML/container and numeric conversions, existing bounds/finiteness, False versus valid numeric zero, frozen model/nested mappings.

Both baseline and candidate are the real Pydantic schema, not a handwritten parser model. This validates the tested input boundary only. Native scenario/editor suites, API integration, financial calculations, all supported dependency versions and pinned ruff 0.16.4 were **NOT RUN**. Existing test_parse_normalises_an_integral_float_and_an_integer_flag was read, not executed; equivalent schema-level coercions were checked. No expected-value tests were modified.

[Machine-readable results](results.json) · [exact candidate diff](NORTHPLAN-CANDIDATE.md).

## Reproduce in a disposable directory

Use Python 3.12+ with the versions above already available. Copy the fetch block into fetch_sources.py, run it once to retrieve public pinned files, then copy the harness below into check.py in the same directory and run python check.py. Fetching is separate from the offline validation. Original fetched files retain their SPDX headers and upstream license. No upstream project entrypoint is run.

```python
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

manifest = json.loads(r'''[
  {
    "path": "engine/scenario/schema.py",
    "blob_sha": "42648c3cbab46aae85b8c8f5b9ae1652957281ed",
    "url": "https://raw.githubusercontent.com/janowoc/northplan/f3b55a5e72a30080ef28cd3066371017ecae1b97/engine/scenario/schema.py"
  },
  {
    "path": "engine/mc/moments.py",
    "blob_sha": "f41411a5fb3e1204e1b9dab77c6ee37dfb8c0118",
    "url": "https://raw.githubusercontent.com/janowoc/northplan/f3b55a5e72a30080ef28cd3066371017ecae1b97/engine/mc/moments.py"
  },
  {
    "path": "engine/core/timeline.py",
    "blob_sha": "1a73d1120443b9ba77e1367934a673f2785255d8",
    "url": "https://raw.githubusercontent.com/janowoc/northplan/f3b55a5e72a30080ef28cd3066371017ecae1b97/engine/core/timeline.py"
  },
  {
    "path": "engine/params/loader.py",
    "blob_sha": "da74368a16d615be779b98879b1b6da108d09a58",
    "url": "https://raw.githubusercontent.com/janowoc/northplan/f3b55a5e72a30080ef28cd3066371017ecae1b97/engine/params/loader.py"
  },
  {
    "path": "scenarios/minimal.yaml",
    "blob_sha": "17252cee15c55a8fb9364525bc993941eddf1e48",
    "url": "https://raw.githubusercontent.com/janowoc/northplan/f3b55a5e72a30080ef28cd3066371017ecae1b97/scenarios/minimal.yaml"
  }
]''')
root = Path.cwd()
for entry in manifest:
    with urlopen(entry["url"], timeout=30) as response:
        data = response.read()
    actual = hashlib.sha1(b"blob " + str(len(data)).encode() + bytes([0]) + data).hexdigest()
    assert actual == entry["blob_sha"], (entry["path"], actual)
    target = root / entry["path"]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    if target.suffix == ".py":
        for parent in target.parents:
            if parent == root:
                break
            (parent / "__init__.py").touch()
```

### Executed harness

```python
import ast
import copy
import difflib
import importlib.util
import json
import pathlib
import platform
import sys
import yaml
import pydantic
import numpy
from pydantic import ValidationError

root = pathlib.Path(__file__).parent
source_path = root / 'engine/scenario/schema.py'
source = source_path.read_text()
tree = ast.parse(source)
# Change only scalar type names within model field annotations and four numeric aliases.
nodes = []
for statement in tree.body:
    if isinstance(statement, ast.Assign) and any(isinstance(t, ast.Name) and t.id in {'Finite','Money','Month','Fraction'} for t in statement.targets):
        nodes.extend(ast.walk(statement.value))
    if isinstance(statement, ast.ClassDef):
        for member in statement.body:
            if isinstance(member, ast.AnnAssign):
                nodes.extend(ast.walk(member.annotation))
lines = source.splitlines(keepends=True)
offsets = [0]
for line in lines:
    offsets.append(offsets[-1] + len(line.encode()))
replacements = []
for n in nodes:
    if isinstance(n, ast.Name) and n.id in {'int','float'}:
        replacements.append((offsets[n.lineno-1]+n.col_offset, offsets[n.end_lineno-1]+n.end_col_offset, 'InputInt' if n.id=='int' else 'InputFloat'))
patched = source.encode()
for start,end,value in sorted(set(replacements), reverse=True):
    patched = patched[:start] + value.encode() + patched[end:]
patched = patched.decode().replace('from pydantic import AfterValidator,', 'from pydantic import AfterValidator, BeforeValidator,',1)
guard = '''def _reject_bool_number(value: Any) -> Any:
    """Refuse booleans before numeric conversion; preserve other input coercions."""
    if isinstance(value, bool):
        raise ValueError("boolean is not a numeric scenario value")
    return value


InputInt = Annotated[int, BeforeValidator(_reject_bool_number)]
InputFloat = Annotated[float, BeforeValidator(_reject_bool_number)]


'''
patched = patched.replace('#: A float that is neither infinite nor nan.', guard+'#: A float that is neither infinite nor nan.',1)
(root/'schema_candidate.py').write_text(patched)
(root/'candidate.diff').write_text(''.join(difflib.unified_diff(source.splitlines(keepends=True),patched.splitlines(keepends=True),fromfile='a/engine/scenario/schema.py',tofile='b/engine/scenario/schema.py')))
def load(name, path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
    return module
baseline=load('baseline_schema',source_path)
candidate=load('candidate_schema',root/'schema_candidate.py')
base=yaml.safe_load((root/'scenarios/minimal.yaml').read_text())
results=[]
def check(name, fn):
    fn(); results.append({'name':name,'result':'PASS'})
def scenario_value(module, path, value):
    d=copy.deepcopy(base);cur=d
    for k in path[:-1]:cur=cur[k]
    cur[path[-1]]=value
    return module.Scenario.model_validate(d)
paths=[
 ('seed',),('n_paths',),('household','persons',0,'birth_month'),
 ('spending','schedule',0,'annual'),('spending','survivor_share'),
 ('assumptions','inflation'),('assumptions','correlation',0,0),
 ('assumptions','allocations','default','cash'),
 ('policies',0,'contribution','weights','tfsa'),
 ('policies',0,'elections','cpp_start_age_years','a'),
 ('policies',0,'elections','rrif_conversion','fraction'),
]
for path in paths:
    def paired(path=path):
        scenario_value(baseline,path,True)
        try: scenario_value(candidate,path,True)
        except ValidationError as exc:
            assert any(tuple(e['loc'])==path and 'boolean is not' in e['msg'] for e in exc.errors()),exc
        else: raise AssertionError('boolean accepted')
    check('baseline accepts / candidate rejects '+repr(path),paired)
def grid_pair():
    d=copy.deepcopy(base);d['grid']={'elections.rrif_conversion.fraction':[False]}
    baseline.Scenario.model_validate(d)
    try:candidate.Scenario.model_validate(d)
    except ValidationError as e:assert all(x['loc'][:3]==('grid','elections.rrif_conversion.fraction',0) for x in e.errors())
    else:raise AssertionError('grid boolean accepted')
check('grid: reject bool in both union branches',grid_pair)
def preserve():
    for mod in (baseline,candidate):
        mod.Scenario.model_validate(base)
        s=scenario_value(mod,('seed',),42.0);assert type(s.seed) is int and s.seed==42
        s=scenario_value(mod,('policies',0,'withdrawal','fill_pension_credit'),1);assert s.policies[0].withdrawal.fill_pension_credit is True
        s=scenario_value(mod,('spending','schedule',0,'annual'),0);assert s.spending.schedule[0].annual==0.0
        s=scenario_value(mod,('policies',0,'elections','rrif_conversion','fraction'),1);assert s.policies[0].elections.rrif_conversion.fraction==1.0
check('preserve YAML list coercion, 42.0 seed, numeric 0/1, existing bool policy',preserve)
def invalid_bounds():
    for path,value in [(('n_paths',),0),(('household','persons',0,'birth_month'),13),(('spending','schedule',0,'annual'),-1),(('assumptions','inflation'),float('nan')),(('policies',0,'elections','rrif_conversion','fraction'),1.1)]:
        try:scenario_value(candidate,path,value)
        except ValidationError:pass
        else:raise AssertionError((path,value))
check('preserve existing numeric bounds and finiteness',invalid_bounds)
def false_numbers():
    for path in [('seed',),('spending','schedule',0,'annual'),('assumptions','inflation')]:
        scenario_value(baseline,path,False)
        try:scenario_value(candidate,path,False)
        except ValidationError:pass
        else:raise AssertionError(path)
check('False rejected where numeric zero remains valid',false_numbers)
def frozen():
    s=candidate.Scenario.model_validate(base)
    try:s.assumptions.allocations['default']['cash']=0.0
    except TypeError:pass
    else:raise AssertionError('mapping mutable')
    try:s.seed=2
    except ValidationError:pass
    else:raise AssertionError('model mutable')
check('frozen model and nested mapping invariants retained',frozen)
result={'python':platform.python_version(),'pydantic':pydantic.__version__,'numpy':numpy.__version__,'pyyaml':yaml.__version__,'groups_passed':len(results),'scalar_annotation_replacements':len(set(replacements)),'results':results,'scope':'Full pinned schema.py and three local dependency modules; empty package initializers; real Pydantic/NumPy/PyYAML, no stubs, no simulator/API/editor/native upstream test suite.'}
(root/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
```

## Proposed only: Casdoor regressions

No Go compiler/runtime available; no native test, DCR request, token exchange or connector login executed. No Python/JS surrogate is reported as a Casdoor regression pass.

1. Unsupported registration/update auth method is rejected as invalid metadata before AddApplication/UpdateApplication is called; use mocked persistence.
2. For every genuinely supported dynamically provisioned method, create → read → update retains the effective method and required key metadata.
3. Missing method has a documented consistent default; unsupported explicit method never silently becomes basic.
4. Existing manually configured certificate/federated client-assertion path retains behavior. A method-discovery change needs explicit compatibility coverage.
5. CIMD unsupported-method rejection remains deterministic until dynamic key provisioning is implemented.
6. Any future JWKS implementation needs separate locally generated keys, bounded key-resolution fixtures and token-validation cases; no real client keys, remote login or disabling auth.

Static comparison only: token_oauth.go, token_oauth_util.go and oauth_dcr.go are byte-identical at v4.23.0 and reviewed master, proving presence of the assertion branch and registration/read mismatch at the reported release source. This does not establish the reporter's actual deployed image or full RFC conformance.

## Other limits

Railway: Rust unavailable; no native JSONC test. Ouroboros: Go unavailable; no cancellation/101-handoff test. Beeper: affected built-in Desktop schema generator not identified in accessible SDK. No reply drafted for these. A2A #1354 final diff read; its tests were not rerun and no release/deployment acceptance was verified.
