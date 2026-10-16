# R4 local evidence — 2026-10-16

Actual environment: Node v24.19.0; Python 3.12.14; Pydantic 2.13.5. No packages installed. No external network calls, credentials, Git operations, subprocess CLI, disk-full event or payment occurred during the tests.

| Harness | Baseline groups | Candidate groups | Result |
|---|---:|---:|---|
| pi temp-file cleanup | 2 | 5 | 7 PASS |
| MCP Git envelope/params | 2 | 3 | 5 PASS |
| MCP Python reserved-name collision | 2 | 7 | 9 PASS |
| Total | 6 | 15 | 21 PASS |

These are assertion groups; a group may include several inputs. The 24 method/parameter matrix entries are included in one candidate group, not counted as 24 independent project tests. No upstream full suite ran. pi's issue closed after these tests; its candidate is withdrawn from posting.

## Pinned inputs

- mcp-config.ts: [source](https://github.com/markdlabrecque/pi-claude-subscription/blob/e0c9a12ac21be4c197e82795f7207746f3183028/src/mcp-config.ts), Git blob `04854611e280a6dfc3a3ddab76c83c855fa8d801`.
- func_metadata.py: [source](https://github.com/modelcontextprotocol/python-sdk/blob/754254c08fe1c3eda18b69da3d336106fe8d72d6/src/mcp/server/mcpserver/utilities/func_metadata.py), Git blob `96d25ec5ab50261dc303f55c8585cdeeca4db99d`.
- http_jsonrpc.py: [source](https://github.com/MementoRC/mcp-git/blob/648cb467d80311ef83f7246dfa9a07bd930db072/src/mcp_server_git/transport/http_jsonrpc.py), Git blob `730b378f8c68ed0e15c6fa31795607cc23201bea`.
- http_tool_call.py: [source](https://github.com/MementoRC/mcp-git/blob/648cb467d80311ef83f7246dfa9a07bd930db072/src/mcp_server_git/transport/http_tool_call.py), Git blob `2720df013e687d111a2b162350bdb3613cd18393`.
- http_rpc_responses.py: [source](https://github.com/MementoRC/mcp-git/blob/648cb467d80311ef83f7246dfa9a07bd930db072/src/mcp_server_git/transport/http_rpc_responses.py), Git blob `8383fc4f1cb176588b5157d6e8677454908cf55e`.

Source content was retrieved via the GitHub connector and byte-hashed before extraction. Upstream source files are not vendored. To reproduce, place these pinned files and the following harnesses together in a disposable local directory. The optional fetcher below was not used in this run; it describes how another reviewer can retrieve the same bytes.

```python
# Optional reproduction setup: download only the five pinned public source files.
# Tests below execute reviewed extracts, never project entry points.
import hashlib, json, pathlib, urllib.request
manifest = json.loads("[{\"file\":\"mcp-config.ts\",\"repo\":\"markdlabrecque/pi-claude-subscription\",\"path\":\"src/mcp-config.ts\",\"sha\":\"04854611e280a6dfc3a3ddab76c83c855fa8d801\",\"commit\":\"e0c9a12ac21be4c197e82795f7207746f3183028\"},{\"file\":\"func_metadata.py\",\"repo\":\"modelcontextprotocol/python-sdk\",\"path\":\"src/mcp/server/mcpserver/utilities/func_metadata.py\",\"sha\":\"96d25ec5ab50261dc303f55c8585cdeeca4db99d\",\"commit\":\"754254c08fe1c3eda18b69da3d336106fe8d72d6\"},{\"file\":\"http_jsonrpc.py\",\"repo\":\"MementoRC/mcp-git\",\"path\":\"src/mcp_server_git/transport/http_jsonrpc.py\",\"sha\":\"730b378f8c68ed0e15c6fa31795607cc23201bea\",\"commit\":\"648cb467d80311ef83f7246dfa9a07bd930db072\"},{\"file\":\"http_tool_call.py\",\"repo\":\"MementoRC/mcp-git\",\"path\":\"src/mcp_server_git/transport/http_tool_call.py\",\"sha\":\"2720df013e687d111a2b162350bdb3613cd18393\",\"commit\":\"648cb467d80311ef83f7246dfa9a07bd930db072\"},{\"file\":\"http_rpc_responses.py\",\"repo\":\"MementoRC/mcp-git\",\"path\":\"src/mcp_server_git/transport/http_rpc_responses.py\",\"sha\":\"8383fc4f1cb176588b5157d6e8677454908cf55e\",\"commit\":\"648cb467d80311ef83f7246dfa9a07bd930db072\"}]")
for item in manifest:
    url = f"https://raw.githubusercontent.com/{item['repo']}/{item['commit']}/{item['path']}"
    with urllib.request.urlopen(url, timeout=20) as response:
        data = response.read()
    actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert actual == item["sha"], (item["file"], actual)
    pathlib.Path(item["file"]).write_bytes(data)

```

## test_pi_cleanup.mjs

Run: `node test_pi_cleanup.mjs`. In-memory filesystem injection; baseline function body retained except TypeScript signature/export removal and replacement of import.meta.url with a fixture URL. Candidate is a small ownership/cleanup model, not a project patch. Real ENOSPC/EACCES, filesystem atomicity, cleanup success when deletion itself fails, process crashes and CLI lifecycle remain untested.

```javascript
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {join,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import vm from 'node:vm';
const raw=readFileSync(new URL('./mcp-config.ts',import.meta.url));
assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+raw.length+'\0'),raw])).digest('hex'),'04854611e280a6dfc3a3ddab76c83c855fa8d801');
let source=raw.toString().slice(raw.toString().indexOf('export function writeMcpConfig('))
.replace('export function writeMcpConfig(toolDefs: McpToolDef[]): string {','function writeMcpConfig(toolDefs) {')
.replace('import.meta.url','"file:///fixture/mcp-config.ts"');
const results=[];
function fixture(failAt=0, cleanupFails=false){
 const files=new Map([['/tmp/other/keep','sentinel']]);let writes=0,serial=0,cleanupErrors=0;
 const original=new Error('synthetic ENOSPC');
 return {files,original,get cleanupErrors(){return cleanupErrors},
  writeFileSync(path,data){writes++;files.set(path,'partial');if(writes===failAt)throw original;files.set(path,data)},
  mkdtempSync(prefix){return prefix+(++serial)},
  rmSync(dir){if(cleanupFails){cleanupErrors++;throw new Error('synthetic unlink error')}for(const k of files.keys())if(k.startsWith(dir+'/'))files.delete(k)}
 };
}
function baseline(f){const ctx={writeFileSync:f.writeFileSync,join,dirname,fileURLToPath,tmpdir:()=>'/tmp',process:{pid:123}};vm.createContext(ctx);vm.runInContext(source,ctx);return ctx.writeMcpConfig}
function candidate(f){
 const dir=f.mkdtempSync('/tmp/pi-owned-');const schema=join(dir,'schema.json'),config=join(dir,'config.json');
 try{f.writeFileSync(schema,JSON.stringify([{name:'fixture'}]));f.writeFileSync(config,JSON.stringify({schema}));return config}
 catch(original){try{f.rmSync(dir)}catch{/* Preserve original; production should separately report cleanup failure. */}throw original}
}
for(const [n,count]of [[1,2],[2,3]]){const f=fixture(n);assert.throws(()=>baseline(f)([]),e=>e===f.original);assert.equal(f.files.size,count);results.push({test:'baseline partial write '+n,kind:'source-extracted baseline',pass:true});}
for(const n of [1,2]){const f=fixture(n);assert.throws(()=>candidate(f),e=>e===f.original);assert.deepEqual([...f.files],[['/tmp/other/keep','sentinel']]);results.push({test:'candidate cleans partial write '+n,kind:'candidate model',pass:true});}
{const f=fixture(2,true);assert.throws(()=>candidate(f),e=>e===f.original);assert.equal(f.cleanupErrors,1);results.push({test:'cleanup failure preserves original error',kind:'candidate model',pass:true});}
{const f=fixture();const a=candidate(f),before=new Map(f.files),b=candidate(f);assert.notEqual(a,b);for(const[k,v]of before)assert.equal(f.files.get(k),v);results.push({test:'same-process calls keep separate owned files',kind:'candidate model',pass:true});}
{const f=fixture();const path=candidate(f);assert.ok(JSON.parse(f.files.get(path)).schema);assert.equal(f.files.size,3);results.push({test:'successful pair remains for caller',kind:'candidate model',pass:true});}
console.log(JSON.stringify({node:process.version,tests:results,limitations:'In-memory injected writes, no actual disk-full, permissions, crash recovery, CLI or Vitest suite.'},null,2));

```

## test_rpc_boundary.py

Run: `python test_rpc_boundary.py`. AST extraction keeps the reviewed response builders and handler classes; FastAPI Request/JSONResponse and catalog are stand-ins. No real Git session operations. Candidate guard covers ID-bearing requests in the tested matrix; it is not a complete JSON-RPC validation layer. The local choice to reject arrays does not establish batch-policy compliance. Notifications and nested tool-argument schemas remain for integration tests.

```python
import ast
import asyncio
import hashlib
import json
import logging
from pathlib import Path
from typing import Any, Callable, Awaitable
from types import SimpleNamespace
import secrets

ROOT = Path(__file__).parent
EXPECTED = {"http_jsonrpc.py":"730b378f8c68ed0e15c6fa31795607cc23201bea","http_tool_call.py":"2720df013e687d111a2b162350bdb3613cd18393","http_rpc_responses.py":"8383fc4f1cb176588b5157d6e8677454908cf55e"}
sources = {}
for name, expected in EXPECTED.items():
    raw = (ROOT / name).read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest() == expected
    sources[name] = raw.decode()

class JSONResponse:
    def __init__(self, content, status_code=200):
        self.content, self.status_code, self.headers = content, status_code, {}
class Request:
    def __init__(self, value): self.value = value
    async def json(self): return self.value

def load(patched=False):
    ns = dict(Any=Any, Callable=Callable, Awaitable=Awaitable, JSONResponse=JSONResponse,
              Request=Request, json=json, secrets=secrets, PROTOCOL_VERSION="2024-11-05",
              TOOLS_LIST=[], logger=logging.getLogger("fixture"))
    ns["logger"].disabled = True
    for name in ["http_rpc_responses.py","http_tool_call.py","http_jsonrpc.py"]:
        text = sources[name]
        if patched and name == "http_jsonrpc.py":
            text = text.replace('        method = body.get("method")', '''        if not isinstance(body, dict):
            return rpc_error(None, -32600, "Invalid Request")
        method = body.get("method")''')
            text = text.replace('        return await handler(req_id, params, session_id)', '''        if "params" in body and not isinstance(params, dict):
            return rpc_error(req_id, -32602, "Invalid params - object required")
        return await handler(req_id, params, session_id)''')
        tree = ast.parse(text)
        tree.body = [node for node in tree.body if isinstance(node, (ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef))]
        exec(compile(tree,name,"exec"),ns)
    server = SimpleNamespace(default_repo=None)
    return ns["MCPRequestHandler"](server)

results=[]
def passed(name,kind,details=None):
    results.append(dict(test=name,kind=kind,pass_=True,details=details))

async def main():
    original=load()
    for body in [[],[{"jsonrpc":"2.0","method":"tools/list","id":1}],None,42,"text",False]:
        try: await original.handle(Request(body),"fixture")
        except AttributeError: pass
        else: raise AssertionError("expected baseline AttributeError")
    passed("six non-object envelope shapes raise before validation","source-extracted baseline")
    invalid=[None,[],False,0,"",["x"],1,"x"]
    outcomes={}
    for method in ["initialize","tools/list","tools/call"]:
        values=[]
        for param in invalid:
            r=await original.handle(Request({"jsonrpc":"2.0","id":7,"method":method,"params":param}),"fixture")
            values.append(r.content.get("error",{}).get("code","success"))
        outcomes[method]=values
    assert outcomes["initialize"]==["success"]*8
    assert outcomes["tools/list"]==["success"]*8
    assert outcomes["tools/call"]==[-32602]*5+[-32603]*3
    passed("params truthiness and dispatch affect baseline result","source-extracted baseline",outcomes)
    candidate=load(True)
    for body in [[],None,42,"text",False]:
        r=await candidate.handle(Request(body),"fixture")
        assert r.content["error"]["code"]==-32600 and r.content["id"] is None
    passed("candidate rejects five non-object envelopes","local candidate extract")
    for method in ["initialize","tools/list","tools/call"]:
        for param in invalid:
            r=await candidate.handle(Request({"jsonrpc":"2.0","id":7,"method":method,"params":param}),"fixture")
            assert r.content["error"]["code"]==-32602 and r.content["id"]==7
    passed("24 invalid-params matrix entries return -32602 and preserve id","local candidate extract")
    for body in [{"jsonrpc":"2.0","id":"same","method":"tools/list"},
                 {"jsonrpc":"2.0","id":"same","method":"tools/list","params":{}}]:
        r=await candidate.handle(Request(body),"fixture")
        assert r.content == {"jsonrpc":"2.0","id":"same","result":{"tools":[]}}
    passed("omitted and object params keep tools-list success","local candidate extract")
asyncio.run(main())
print(json.dumps({"tests":results,"limitations":"Source classes extracted; request/response/catalog replaced; no FastAPI/ASGI integration, real Git execution, notification validation or full suite. Array rejection is a local candidate policy, not proof of negotiated protocol compliance."},indent=2))

```

## test_reserved_names.py

Run: `python test_reserved_names.py` with already available Pydantic. Only ArgModelBase and the argument-construction prefix execute; return-output logic, AnyIO, resolver binding and transport entry points are not loaded. Public Client(server) schema-and-invocation regression is still required. The first harness attempt raised KeyError('__name__'); adding the normal module name to the synthetic namespace fixed the harness. All nine groups then passed. No claim that this passes the SDK's locked dependency/CI matrix.

```python
import ast
import hashlib
import inspect
import itertools
import json
import sys
from pathlib import Path
from typing import Any, Annotated, Callable, Sequence
import pydantic
from pydantic import BaseModel, ConfigDict, Field, WithJsonSchema, create_model, ValidationError
raw = Path(__file__).with_name("func_metadata.py").read_bytes()
assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="96d25ec5ab50261dc303f55c8585cdeeca4db99d"
source=raw.decode()
def build(patched=False):
    text=source
    if patched:
        old='            field_name = f"field_{field_name}"'
        text=text.replace(old,old+'''
            while field_name in params or field_name in dynamic_pydantic_model_params or hasattr(BaseModel, field_name):
                field_name = f"field_{field_name}"''')
    tree=ast.parse(text)
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=="ArgModelBase")
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="func_metadata")
    end=next(i for i,n in enumerate(fn.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="arguments_model" for t in n.targets))
    fn.body=fn.body[:end+1]+[ast.Return(value=ast.Name(id="arguments_model",ctx=ast.Load()))]
    fn.returns=None
    module=ast.fix_missing_locations(ast.Module(body=[cls,fn],type_ignores=[]))
    ns=dict(__name__=__name__,inspect=inspect,Any=Any,Annotated=Annotated,Callable=Callable,Sequence=Sequence,BaseModel=BaseModel,ConfigDict=ConfigDict,Field=Field,WithJsonSchema=WithJsonSchema,create_model=create_model)
    exec(compile(module,"source_extract.py","exec"),ns)
    return ns["func_metadata"]
baseline,candidate=build(),build(True)
def make(names):
    ns={}
    exec("def target("+", ".join(n+": int" for n in names)+"):\n    return {"+", ".join(repr(n)+": "+n for n in names)+"}",ns)
    return ns["target"]
results=[]
for names in [("model_dump","field_model_dump"),("field_model_dump","model_dump")]:
    fn=make(names);model=baseline(fn)
    props=set(model.model_json_schema()["properties"])
    assert props=={names[-1]}
    results.append(dict(test="baseline order "+",".join(names),kind="source-extracted baseline",pass_=True))
names=("model_dump","field_model_dump","field_field_model_dump")
for order in itertools.permutations(names):
    fn=make(order);model=candidate(fn);values={name:i+1 for i,name in enumerate(order)}
    assert set(model.model_json_schema()["properties"])==set(names)
    assert set(model.model_json_schema()["required"])==set(names)
    assert fn(**model.model_validate(values).model_dump_one_level())==values
    results.append(dict(test="candidate order "+",".join(order),kind="local candidate extract",pass_=True))
def typed(model_dump: Annotated[int,Field(ge=1)],field_model_dump: str="default"):
    return model_dump,field_model_dump
model=candidate(typed)
assert typed(**model.model_validate({"model_dump":2}).model_dump_one_level())==(2,"default")
try:model.model_validate({"model_dump":0})
except ValidationError:pass
else:raise AssertionError("constraint was lost")
schema=model.model_json_schema()
assert schema["properties"]["model_dump"]["minimum"]==1
assert schema["properties"]["field_model_dump"]["type"]=="string"
assert schema["required"]==["model_dump"]
results.append(dict(test="candidate preserves types constraint and default",kind="local candidate extract",pass_=True))
print(json.dumps(dict(python=sys.version.split()[0],pydantic=pydantic.__version__,tests=results,limitations="Only ArgModelBase and argument-construction prefix extracted. No installed MCP SDK, public Client(server) roundtrip, async invocation, full upstream suite or caller-defined aliases tested."),indent=2))

```

