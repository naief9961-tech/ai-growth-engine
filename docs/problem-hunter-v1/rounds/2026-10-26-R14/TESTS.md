# R14 isolated test evidence

Source: https://github.com/agentscope-ai/QwenPaw/blob/b501aca97f8e13c730669fa1c6365f4f053895b6/src/qwenpaw/drivers/handlers/mcp_streamable_http.py
Git blob SHA: 184c594799f0b733b12c69b52e8fb5b6e85e733c (verified before execution).

Final command: `python test_r14_final.py`, exit 0. Ten paired groups / twenty executions; see results.json. The harness executes the complete extracted _negotiate and its actual classification helpers/classes. _rpc is injected. httpx is unavailable; only its HTTPStatusError exception type is replaced, and no HTTPStatusError case is tested. No native MCP imports, network, tokens or upstream suite.

The initial source write added a newline; hash verification stopped execution. Removing only that extra newline restored the exact Git blob. A harness substring-indentation assertion also stopped setup; corrected to match the AST-unparsed guard exactly once. Neither setup failure is counted as a tested product case.

To reproduce: download the pinned source byte-for-byte as qwen_source_r14.py next to this harness. Run with Python 3.10+; no third-party packages needed. The harness verifies the source hash and changes only the special 404 guard. This does not establish cleanup, retry-count, OAuth or complete transport compatibility.

```python
import ast, asyncio, hashlib, json, types
from pathlib import Path
source=Path(__file__).with_name("qwen_source_r14.py").read_bytes()
assert hashlib.sha1(b"blob "+str(len(source)).encode()+b"\0"+source).hexdigest()=="184c594799f0b733b12c69b52e8fb5b6e85e733c"
tree=ast.parse(source)
names={"_LegacyProtocolError","_OAuthRequiredError","_JsonRpcError","_supported_versions_from_payload","_is_legacy_protocol_evidence","_discover_rpc_error"}
nodes=[n for n in tree.body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name in names]
method=next(m for c in tree.body if isinstance(c,ast.ClassDef) for m in c.body if isinstance(m,ast.AsyncFunctionDef) and m.name=="_negotiate")
env={"Any":object,"httpx":types.SimpleNamespace(HTTPStatusError=type("HTTPStatusError",(Exception,),{})),"_MODERN_PROTOCOL_VERSION":"2026-07-28","_HANDSHAKE_PROTOCOL_VERSIONS":frozenset(["2025-03-26","2025-06-18","2025-11-25"]),"_JSONRPC_METHOD_NOT_FOUND":-32601,"_JSONRPC_HEADER_MISMATCH":-32020,"_JSONRPC_MISSING_REQUIRED_CLIENT_CAPABILITY":-32021,"_JSONRPC_UNSUPPORTED_PROTOCOL_VERSION":-32022}
exec(compile(ast.fix_missing_locations(ast.Module(body=[ast.ImportFrom(module="__future__",names=[ast.alias(name="annotations")],level=0)]+nodes+[method],type_ignores=[])),"source-extract","exec"),env)
baseline=env["_negotiate"]
candidate=ast.unparse(method)
import re
candidate, count = re.subn(r"if exc\.http_status == 404:\s+raise _discover_rpc_error\(exc\) from exc", "pass # Use existing legacy signal for method-not-found", candidate)
assert count == 1
exec(compile(candidate,"candidate-extract","exec"),env)
patched=env["_negotiate"]
cases=[
("404_method_not_found",-32601,404,None,"RuntimeError","_LegacyProtocolError"),
("200_method_not_found",-32601,200,None,"_LegacyProtocolError","_LegacyProtocolError"),
("400_method_not_found",-32601,400,None,"_LegacyProtocolError","_LegacyProtocolError"),
("404_header_mismatch",-32020,404,None,"RuntimeError","RuntimeError"),
("404_missing_capability",-32021,404,None,"RuntimeError","RuntimeError"),
("unsupported_modern",-32022,404,{"supported":["2026-07-28"]},"RuntimeError","RuntimeError"),
("unsupported_legacy",-32022,404,{"supported":["2025-06-18"]},"_LegacyProtocolError","_LegacyProtocolError"),
("discover_modern",None,None,{"supportedVersions":["2026-07-28"]},"ok","ok"),
("discover_legacy",None,None,{"supportedVersions":["2025-06-18"]},"_LegacyProtocolError","_LegacyProtocolError"),
("malformed_discover",None,None,{},"RuntimeError","RuntimeError"),
]
async def run(fn,code,status,data):
 async def rpc(method,params):
  assert method=="server/discover" and params=={}
  if code is not None: raise env["_JsonRpcError"](code,"synthetic",data,http_status=status)
  return data
 try: await fn(types.SimpleNamespace(_rpc=rpc)); return "ok"
 except Exception as e: return type(e).__name__
async def main():
 results=[]
 for name,code,status,data,b,p in cases:
  actual_b=await run(baseline,code,status,data)
  actual_p=await run(patched,code,status,data)
  assert (actual_b,actual_p)==(b,p),(name,actual_b,actual_p)
  results.append({"case":name,"baseline":actual_b,"candidate":actual_p})
 print(json.dumps({"passed_groups":len(results),"function_executions":2*len(results),"results":results},indent=2))
asyncio.run(main())

```
