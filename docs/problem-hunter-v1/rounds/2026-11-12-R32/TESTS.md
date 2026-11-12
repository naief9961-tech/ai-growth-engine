# R32 — isolated evidence, candidate and reproduction

## Scope

Original issue: https://github.com/weyucou/wyc6k-task-runner/issues/83 (ellen-goc, created2026-11-12T04:51:04Z). Source commit `b0bc11c3e4c2ce7c5419175326026f0ab1694f17`. Actual reviewed module text, not reimplemented baseline. Six blob hashes checked locally before execution. No third-party changes or provider requests.

Python3.12.14/Pydantic2.13.4. Project declares Python>=3.14,<3.15; **Python3.14 unavailable**. The loader enables future-annotations compiler flag for both baseline/candidate to defer forward-reference evaluation on3.12. Empty package modules avoid unrelated package entrypoints; the six listed module bodies execute. No claim of native target-runtime validation. Fake provider returns one tool call then final text and records actual `generate()`/request-model `messages.create` kwargs.

## Sources

| File | Git blob SHA |
|---|---|
| [marvin/definitions.py](https://github.com/weyucou/wyc6k-task-runner/blob/b0bc11c3e4c2ce7c5419175326026f0ab1694f17/marvin/definitions.py) | `5cdf2fd22bdfa16b5b4b88289d8685259b2839dd` |
| [marvin/llm/base.py](https://github.com/weyucou/wyc6k-task-runner/blob/b0bc11c3e4c2ce7c5419175326026f0ab1694f17/marvin/llm/base.py) | `a98be6609c72eb92b6ea4a5ff638159675c874e0` |
| [marvin/llm/definitions.py](https://github.com/weyucou/wyc6k-task-runner/blob/b0bc11c3e4c2ce7c5419175326026f0ab1694f17/marvin/llm/definitions.py) | `fce0b4c404d3fcb56fe48fd11053bf737acf0dfa` |
| [marvin/llm/anthropic_client.py](https://github.com/weyucou/wyc6k-task-runner/blob/b0bc11c3e4c2ce7c5419175326026f0ab1694f17/marvin/llm/anthropic_client.py) | `cab921b1498a06bc173eef7877a19aea595f6f3d` |
| [marvin/tools/base.py](https://github.com/weyucou/wyc6k-task-runner/blob/b0bc11c3e4c2ce7c5419175326026f0ab1694f17/marvin/tools/base.py) | `447151194280766719c7b9a14beacc74358595bf` |
| [marvin/tools/registry.py](https://github.com/weyucou/wyc6k-task-runner/blob/b0bc11c3e4c2ce7c5419175326026f0ab1694f17/marvin/tools/registry.py) | `6e59aca2f447437e12a3b48795bc0f0084b913e4` |

Additional reads: [tests/test_tools.py](https://github.com/weyucou/wyc6k-task-runner/blob/b0bc11c3e4c2ce7c5419175326026f0ab1694f17/tests/test_tools.py), blob8bbe8c6e5f963d687ee082b8a684952dce69a85e; [pyproject.toml](https://github.com/weyucou/wyc6k-task-runner/blob/b0bc11c3e4c2ce7c5419175326026f0ab1694f17/pyproject.toml), blob0549d84ace44e95bf6b0a596a2a4c1ce424768b3. Tests here assert registry errors but the inspected test module does not establish the final provider request.

Issue83 body/all0comments/all4timeline label/assignment events read and rechecked. Dependency82 body read; it explicitly calls for shared loop first. All3 current open PRs75,76,78 and complete file lists checked; none changes affected source. Latest30 all-state PR summaries also read, not proof of exhaustive historical PR absence. Complete tree returned untruncated; no AGENTS.md or CONTRIBUTING file found for this repository. No unsolicited claim or message.

## Diagnosis and bounded solution

`ToolRegistry.execute` returns `ToolResult.from_error` for unknown tools, parameter rejection and tool exceptions. That constructor leaves output empty. `generate_with_tools` reads only output on the registry route. More specifically, the live carrier is `LLMMessage`; changing the separate `ToolResultMessage.is_error` cannot fix its absent field or the Anthropic serializer. The callable route currently stringifies a ToolResult representation; direct executor exceptions get text but no error flag.

The two-file candidate below is an **illustrative Anthropic boundary patch**, not a complete issue83 solution/PR. Normalize in the future shared loop rather than multiplying four loops. Keep error detection status-based; retain partial output, tool call ID, callable errors and a fallback for empty failures. Other provider serializers, available-tool listings, validation reissue wording, nonzero exec behavior, persistent message replay and Python3.14 CI still require integration work. Updating AnthropicToolResultBlock separately would not fix the current conversion path; AnthropicMessage.content accepts dictionaries.

## Actual results

8 paired cases: baseline observations and candidate verification =16 executions. Baseline is not a passing-fix claim: it confirms failures as specified by the reproduction harness. Candidate passes all8 request-boundary checks; generic message to_dict error flag also asserted. First local harness attempt stopped on module load order before candidate cases; ordering was corrected and final command exited0.

| Case | Baseline request | Candidate request |
|---|---|---|
| Unknown tool | Empty content, no flag | Names missing tool, true |
| Missing parameter | Empty content, no flag | Names missing mode, true |
| Tool raises | Empty content, no flag | Synthetic error, true |
| Partial output + error | Partial output only | Both text parts, true |
| Successful text includes Error | Exact successful text, no flag | Exact text, false |
| Callable returns ToolResult error | Dataclass representation, no flag | Normalized text, true |
| Executor raises directly | Error text, no flag | Error text, true |
| Empty failure message | Empty content, no flag | Nonempty generic fallback, true |

No upstream full suite, Python3.14, real SDK/network, AWS, shell subprocess, other providers, Docker or deployment ran. No secrets, wallets or payments. The isolated test does not prove the full system fixed.

## Candidate diff (not applied upstream)

```diff
--- a/marvin/llm/base.py
+++ b/marvin/llm/base.py
@@ -61,6 +61,7 @@
     tool_calls: list[ToolCall] | None = None
     tool_call_id: str | None = None
     name: str | None = None  # For tool results
+    is_error: bool = False
 
     def to_dict(self) -> dict[str, Any]:
         """Convert to dictionary."""
@@ -68,6 +69,8 @@
             "role": self.role.value,
             "content": self.content,
         }
+        if self.role == MessageRole.TOOL:
+            result["is_error"] = self.is_error
         if self.tool_calls:
             result["tool_calls"] = [tc.to_dict() for tc in self.tool_calls]
         if self.tool_call_id:
@@ -92,13 +95,14 @@
         return cls(role=MessageRole.ASSISTANT, content=content, tool_calls=tool_calls)
 
     @classmethod
-    def tool_result(cls, tool_call_id: str, content: str, name: str | None = None) -> LLMMessage:
+    def tool_result(cls, tool_call_id: str, content: str, name: str | None = None, *, is_error: bool = False) -> LLMMessage:
         """Create a tool result message."""
         return cls(
             role=MessageRole.TOOL,
             content=content,
             tool_call_id=tool_call_id,
             name=name,
+            is_error=is_error,
         )
 
 
--- a/marvin/llm/anthropic_client.py
+++ b/marvin/llm/anthropic_client.py
@@ -1,5 +1,6 @@
 """Anthropic Claude LLM client with tool support."""
 
+from marvin.tools.base import ToolResult, ToolStatus
 import logging
 import os
 from typing import Any
@@ -76,6 +77,7 @@
                                 "type": AnthropicContentTypes.TOOL_RESULT.value,
                                 "tool_use_id": msg.tool_call_id,
                                 "content": msg.content,
+                                "is_error": msg.is_error,
                             }
                         ],
                     }
@@ -220,6 +222,7 @@
             for tool_call in response.tool_calls:
                 logger.info("Executing tool: %s", tool_call.name)
 
+                is_error = False
                 try:
                     # Execute tool via registry
                     if hasattr(tool_executor, "execute"):
@@ -229,8 +232,15 @@
                         # Assume it's a callable
                         result = await tool_executor(tool_call.name, tool_call.arguments)
                         tool_output = str(result)
+                    if isinstance(result, ToolResult):
+                        is_error = result.status == ToolStatus.ERROR
+                        if is_error:
+                            tool_output = "\n".join(part for part in (result.output, result.error) if part) or "Tool execution failed"
+                        else:
+                            tool_output = result.output
                 except Exception as e:  # noqa: BLE001
                     logger.exception("Tool execution failed: %s", tool_call.name)
+                    is_error = True
                     tool_output = f"Error executing tool: {e}"
 
                 # Add tool result to conversation
@@ -239,6 +249,7 @@
                         tool_call_id=tool_call.id,
                         content=tool_output,
                         name=tool_call.name,
+                        is_error=is_error,
                     )
                 )
 
```

## Reproduce in a disposable local directory

Save the bootstrap below as fetch_sources.py and the harness below as check.py in the same empty directory. Use an already-provisioned Python3.12 environment with Pydantic2.13.4 to reproduce our bounded run. These instructions do not install packages. Bootstrap reads six public pinned source files; the test itself has no network path. Command: `python3 fetch_sources.py`, then `python3 check.py`. Port the tests to the project's3.14 before integration; this harness is not their CI suite.

```python
import hashlib, json, pathlib, urllib.request
repo = "weyucou/wyc6k-task-runner"
revision = "b0bc11c3e4c2ce7c5419175326026f0ab1694f17"
manifest = {
  "marvin/definitions.py": "5cdf2fd22bdfa16b5b4b88289d8685259b2839dd",
  "marvin/llm/base.py": "a98be6609c72eb92b6ea4a5ff638159675c874e0",
  "marvin/llm/definitions.py": "fce0b4c404d3fcb56fe48fd11053bf737acf0dfa",
  "marvin/llm/anthropic_client.py": "cab921b1498a06bc173eef7877a19aea595f6f3d",
  "marvin/tools/base.py": "447151194280766719c7b9a14beacc74358595bf",
  "marvin/tools/registry.py": "6e59aca2f447437e12a3b48795bc0f0084b913e4"
}
records = {}
for path, expected in manifest.items():
    url = f"https://raw.githubusercontent.com/{repo}/{revision}/{path}"
    data = urllib.request.urlopen(url, timeout=20).read()
    actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert actual == expected, (path, actual, expected)
    records[path] = {"content": data.decode(), "sha": expected}
pathlib.Path("sources.json").write_text(json.dumps(records))
```

```python
import __future__, asyncio, hashlib, json, logging, sys, types
from pathlib import Path
from types import SimpleNamespace as NS
import pydantic

ROOT = Path(__file__).parent
sources = json.loads((ROOT / 'sources.json').read_text())
logging.disable(logging.CRITICAL)
for path, record in sources.items():
    data = record['content'].encode()
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == record['sha'], path

def load(candidate):
    for key in list(sys.modules):
        if key == 'marvin' or key.startswith('marvin.'):
            del sys.modules[key]
    for name in ('marvin', 'marvin.llm', 'marvin.tools'):
        module = types.ModuleType(name)
        module.__path__ = []
        sys.modules[name] = module
    order = ['marvin/definitions.py', 'marvin/tools/base.py', 'marvin/tools/registry.py', 'marvin/llm/base.py', 'marvin/llm/definitions.py', 'marvin/llm/anthropic_client.py']
    for path in order:
        record = sources[path]
        source = record['content']
        if candidate and path == 'marvin/llm/base.py':
            source = source.replace('    name: str | None = None  # For tool results', '    name: str | None = None  # For tool results\n    is_error: bool = False')
            source = source.replace('        if self.tool_calls:\n', '        if self.role == MessageRole.TOOL:\n            result["is_error"] = self.is_error\n        if self.tool_calls:\n', 1)
            source = source.replace('def tool_result(cls, tool_call_id: str, content: str, name: str | None = None)', 'def tool_result(cls, tool_call_id: str, content: str, name: str | None = None, *, is_error: bool = False)')
            source = source.replace('            name=name,\n', '            name=name,\n            is_error=is_error,\n')
        if candidate and path == 'marvin/llm/anthropic_client.py':
            source = source.replace('import logging', 'from marvin.tools.base import ToolResult, ToolStatus\nimport logging', 1)
            source = source.replace('                                "content": msg.content,', '                                "content": msg.content,\n                                "is_error": msg.is_error,', 1)
            source = source.replace('                try:\n                    # Execute', '                is_error = False\n                try:\n                    # Execute', 1)
            source = source.replace('                        tool_output = str(result)\n                except', '''                        tool_output = str(result)
                    if isinstance(result, ToolResult):
                        is_error = result.status == ToolStatus.ERROR
                        if is_error:
                            tool_output = "\\n".join(part for part in (result.output, result.error) if part) or "Tool execution failed"
                        else:
                            tool_output = result.output
                except''', 1)
            source = source.replace('                    tool_output = f"Error executing tool: {e}"', '                    is_error = True\n                    tool_output = f"Error executing tool: {e}"', 1)
            source = source.replace('                        name=tool_call.name,', '                        name=tool_call.name,\n                        is_error=is_error,', 1)
        module_name = path[:-3].replace('/', '.')
        module = types.ModuleType(module_name)
        sys.modules[module_name] = module
        # Annotation evaluation compatibility only: project requires 3.14;
        # this isolated environment is 3.12. No package entrypoints imported.
        exec(compile(source, path, 'exec', flags=__future__.annotations.compiler_flag), module.__dict__)
        if candidate:
            out = ROOT / 'candidate' / path
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(source)

async def exercise(candidate):
    load(candidate)
    from marvin.llm.anthropic_client import AnthropicClient
    from marvin.tools.base import BaseTool, ToolParameter, ToolResult
    from marvin.tools.registry import ToolRegistry
    class SyntheticTool(BaseTool):
        name = 'sample'
        description = 'Synthetic in-memory tool'
        parameters = [ToolParameter('mode', 'string', 'Synthetic mode')]
        async def execute(self, mode):
            if mode == 'raise':
                raise ValueError('synthetic failure')
            if mode == 'partial':
                return ToolResult.from_error('synthetic failure', output='partial output')
            if mode == 'empty-error':
                return ToolResult.from_error('')
            return ToolResult.success('Error is just a word')
    cases = [
        ('unknown', 'missing', {}, 'registry', ["Tool 'missing' not found"], True),
        ('validation', 'sample', {}, 'registry', ['Missing required parameter: mode'], True),
        ('exception', 'sample', {'mode': 'raise'}, 'registry', ['synthetic failure'], True),
        ('partial', 'sample', {'mode': 'partial'}, 'registry', ['partial output', 'synthetic failure'], True),
        ('success', 'sample', {'mode': 'ok'}, 'registry', ['Error is just a word'], False),
        ('callable', 'sample', {}, 'callable', ['partial output', 'synthetic failure'], True),
        ('direct-exception', 'sample', {}, 'raising', ['synthetic executor failure'], True),
        ('empty-error', 'sample', {'mode': 'empty-error'}, 'registry', ['Tool execution failed'], True),
    ]
    results = []
    for label, name, arguments, kind, expected, error in cases:
        registry = ToolRegistry()
        registry.register(SyntheticTool())
        async def callable_executor(*args):
            return ToolResult.from_error('synthetic failure', output='partial output')
        async def raising_executor(*args):
            raise ValueError('synthetic executor failure')
        executor = {'registry': registry, 'callable': callable_executor, 'raising': raising_executor}[kind]
        requests = []
        async def create(**kwargs):
            requests.append(kwargs)
            if len(requests) == 1:
                content = [NS(type='tool_use', id='synthetic-1', name=name, input=arguments)]
                stop = 'tool_use'
            else:
                content = [NS(type='text', text='done')]
                stop = 'end_turn'
            return NS(content=content, stop_reason=stop, usage=NS(input_tokens=0, output_tokens=0), model='synthetic')
        client = AnthropicClient(model='synthetic')
        client._client = NS(messages=NS(create=create))
        response, history = await client.generate_with_tools([], [], executor)
        assert len(requests) == 2 and response.content == 'done'
        block = requests[1]['messages'][-1]['content'][0]
        assert block['tool_use_id'] == 'synthetic-1'
        if candidate:
            assert all(text in block['content'] for text in expected), (label, block)
            assert block['is_error'] is error, (label, block)
            assert history[-1].to_dict()['is_error'] is error
        else:
            assert 'is_error' not in block
            if label in ('unknown', 'validation', 'exception', 'empty-error'):
                assert block['content'] == ''
            elif label == 'partial':
                assert block['content'] == 'partial output'
            elif label == 'success':
                assert block['content'] == 'Error is just a word'
        results.append({'case': label, 'content': block['content'], 'is_error': block.get('is_error'), 'pass': True})
    return results

result = {'python': sys.version.split()[0], 'pydantic': pydantic.__version__, 'baseline': asyncio.run(exercise(False)), 'candidate': asyncio.run(exercise(True)), 'limitations': 'Isolated source modules with deferred annotations for Python 3.12; target Python 3.14 not available. Fake provider captures actual generate request, no SDK/network. No other providers, real exec, upstream suite, deployment, AWS or credentials.'}
(ROOT / 'results.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
```

## Captured output

```json
{
  "python": "3.12.14",
  "pydantic": "2.13.4",
  "baseline": [
    {
      "case": "unknown",
      "content": "",
      "is_error": null,
      "pass": true
    },
    {
      "case": "validation",
      "content": "",
      "is_error": null,
      "pass": true
    },
    {
      "case": "exception",
      "content": "",
      "is_error": null,
      "pass": true
    },
    {
      "case": "partial",
      "content": "partial output",
      "is_error": null,
      "pass": true
    },
    {
      "case": "success",
      "content": "Error is just a word",
      "is_error": null,
      "pass": true
    },
    {
      "case": "callable",
      "content": "ToolResult(status=<ToolStatus.ERROR: 'error'>, output='partial output', data={}, error='synthetic failure')",
      "is_error": null,
      "pass": true
    },
    {
      "case": "direct-exception",
      "content": "Error executing tool: synthetic executor failure",
      "is_error": null,
      "pass": true
    },
    {
      "case": "empty-error",
      "content": "",
      "is_error": null,
      "pass": true
    }
  ],
  "candidate": [
    {
      "case": "unknown",
      "content": "Tool 'missing' not found",
      "is_error": true,
      "pass": true
    },
    {
      "case": "validation",
      "content": "Missing required parameter: mode",
      "is_error": true,
      "pass": true
    },
    {
      "case": "exception",
      "content": "synthetic failure",
      "is_error": true,
      "pass": true
    },
    {
      "case": "partial",
      "content": "partial output\nsynthetic failure",
      "is_error": true,
      "pass": true
    },
    {
      "case": "success",
      "content": "Error is just a word",
      "is_error": false,
      "pass": true
    },
    {
      "case": "callable",
      "content": "partial output\nsynthetic failure",
      "is_error": true,
      "pass": true
    },
    {
      "case": "direct-exception",
      "content": "Error executing tool: synthetic executor failure",
      "is_error": true,
      "pass": true
    },
    {
      "case": "empty-error",
      "content": "Tool execution failed",
      "is_error": true,
      "pass": true
    }
  ],
  "limitations": "Isolated source modules with deferred annotations for Python 3.12; target Python 3.14 not available. Fake provider captures actual generate request, no SDK/network. No other providers, real exec, upstream suite, deployment, AWS or credentials."
}
```
