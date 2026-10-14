"""Isolated execution of reviewed upstream functions, NOT upstream integration tests.

Run: python3 test_python_boundaries.py
Sources are in evidence/; source versions and hashes are recorded in manifest.json.
Only selected AST nodes are compiled; upstream modules/install hooks are not imported.
Content is a minimal stub. Pydantic conversion uses the installed pydantic BaseModel.
"""
import ast
import copy
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast
from pydantic import BaseModel
import unittest

ROOT = Path(__file__).parent

class Content:
    def __init__(self, type='text', **kw):
        self.type = type
        self.__dict__.update(kw)
    @staticmethod
    def from_text(text, **kw):
        return Content(text=text, **kw)
    def to_dict(self, **kw):
        return {'type': self.type, 'text': self.text}

def find_node(file, name):
    tree = ast.parse((ROOT/'evidence'/file).read_text())
    return next(n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name)

def compile_nodes(nodes, env, patched=False):
    nodes = copy.deepcopy(nodes)
    for node in nodes:
        if isinstance(node, ast.FunctionDef):
            node.decorator_list = []
        # Replace only relative Content imports with the explicit local stub.
        if hasattr(node, 'body'):
            node.body = [n for n in node.body if not isinstance(n, ast.ImportFrom)]
    if patched:
        for node in nodes:
            for n in ast.walk(node):
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name) and n.func.value.id == 'json' and n.func.attr == 'dumps':
                    if not any(k.arg == 'ensure_ascii' for k in n.keywords):
                        n.keywords.append(ast.keyword(arg='ensure_ascii', value=ast.Constant(False)))
    mod = ast.Module(body=[ast.ImportFrom(module='__future__', names=[ast.alias('annotations')], level=0)]+nodes, type_ignores=[])
    exec(compile(ast.fix_missing_locations(mod), '<reviewed-source-extract>', 'exec'), env)
    return env

def function_tool(patched):
    e = {'json':json, 'Content':Content, 'BaseModel':BaseModel, 'cast':cast, 'Any':Any}
    compile_nodes([find_node('maf-tools.py','_make_dumpable'),find_node('maf-tools.py','parse_result')],e,patched)
    e['FunctionTool'] = SimpleNamespace(_make_dumpable=e['_make_dumpable'])
    return e['parse_result']

class UnicodeCases(unittest.TestCase):
    def test_dict_before_after_and_roundtrip(self):
        data={'columns':['Año','Género','علوم','東京','😀']}
        before=function_tool(False)(data)[0].text
        after=function_tool(True)(data)[0].text
        self.assertIn('\\u00f1',before)
        self.assertIn('علوم',after)
        self.assertNotIn('\\u',after)
        self.assertEqual(json.loads(before),json.loads(after))
        self.assertLess(len(after.encode()),len(before.encode()))
    def test_mixed_content_preserved(self):
        media=Content(type='image',text='unchanged')
        out=function_tool(True)([media, {'city':'طريف'}])
        self.assertIs(out[0],media)
        self.assertEqual(json.loads(out[1].text), {'city':'طريف'})
        self.assertIn('طريف',out[1].text)
    def test_list_preserves_json_types(self):
        v=[{'a':'Año'}, 1, None, False]
        self.assertEqual(json.loads(function_tool(True)(v)[0].text), v)
    def test_model_conversion(self):
        class Sample(BaseModel):
            name: str
        self.assertEqual(json.loads(function_tool(True)(Sample(name='نايف'))[0].text),{'name':'نايف'})
    def test_none_string_content_unchanged(self):
        f=function_tool(True)
        self.assertEqual(f(None)[0].text,'')
        self.assertEqual(f('\\u literal')[0].text,'\\u literal')
        c=Content(text='plain'); self.assertIs(f(c)[0],c)
    def test_default_str_and_escaping(self):
        class Value:
            def __str__(self): return 'Año'
        s=function_tool(True)({'v':Value(),'quote':'"\n\\'})[0].text
        self.assertEqual(json.loads(s),{'v':'Año','quote':'"\n\\'})
    def test_mcp_structured_expression(self):
        t=ast.parse((ROOT/'evidence/maf-mcp.py').read_text())
        expr=next(n for n in ast.walk(t) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and ast.unparse(n.func)=='json.dumps' and n.args and ast.unparse(n.args[0])=='mcp_type.structuredContent')
        env={'json':json,'mcp_type':SimpleNamespace(structuredContent={'name':'Año'})}
        before=eval(compile(ast.Expression(expr),'<source-json-expression>','eval'),env)
        changed=copy.deepcopy(expr); changed.keywords.append(ast.keyword(arg='ensure_ascii',value=ast.Constant(False)))
        after=eval(compile(ast.fix_missing_locations(ast.Expression(changed)),'<patched-json-expression>','eval'),env)
        self.assertIn('\\u00f1',before); self.assertIn('Año',after)
        self.assertEqual(json.loads(before),json.loads(after))
    def test_content_from_function_result_dict(self):
        fn=find_node('maf-types.py','from_function_result')
        e=compile_nodes([fn],{'Content':Content,'json':json},True)
        r=e['from_function_result'](Content,'synthetic-call',result={'name':'Año'})
        self.assertIn('Año',r.result)
        self.assertEqual(r.call_id,'synthetic-call')

class OAuthGateCases(unittest.TestCase):
    def gate(self,cap):
        env={'MAX_STATE_LENGTH':cap,'open_gateway_dcr_client':lambda x: SimpleNamespace(redirect_uris=('https://example.test/cb',)) if x=='synthetic' else None,
             '_oauth_error':lambda *a:a}
        return compile_nodes([find_node('litellm-gateway.py','_rejected_authorize_request')],env)['_rejected_authorize_request']
    def call(self,cap,state,**kw):
        args=dict(client_id='synthetic',redirect_uri='https://example.test/cb',state=state,code_challenge='x'*43,code_challenge_method='S256',response_type='code');args.update(kw)
        return self.gate(cap)(**args)
    def test_reported_1112_boundary(self):
        self.assertEqual(self.call(1024,'x'*1112)[0],400)
        self.assertIsNone(self.call(2048,'x'*1112))
    def test_limit_edges(self):
        self.assertIsNone(self.call(1024,'x'*1024))
        self.assertIsNotNone(self.call(1024,'x'*1025))
        self.assertIsNone(self.call(2048,'x'*2048))
        self.assertIsNotNone(self.call(2048,'x'*2049))
    def test_guards_retained(self):
        for kwargs in ({'client_id':'bad'}, {'redirect_uri':'https://other.test'}, {'code_challenge_method':'plain'}, {'response_type':'token'}):
            self.assertIsNotNone(self.call(2048,'x'*1112,**kwargs))

class DifyGateCases(unittest.TestCase):
    def gate(self,version,supported=None):
        fn=find_node('dify-session.py','initialize')
        idx=next(i for i,n in enumerate(fn.body) if isinstance(n,ast.If) and 'SUPPORTED_PROTOCOL_VERSIONS' in ast.unparse(n.test))
        events=[]
        e={'result':SimpleNamespace(protocolVersion=version), 'SUPPORTED_PROTOCOL_VERSIONS':supported or ['2024-11-05','2025-03-26','2025-06-18'],
           'self':SimpleNamespace(send_notification=lambda n:events.append(n)), 'types':SimpleNamespace(ClientNotification=lambda x:x,InitializedNotification=lambda **kw:kw)}
        compile_nodes(fn.body[idx:idx+2],e)
        return events
    def test_current_rejects_new_version_before_notification(self):
        with self.assertRaisesRegex(RuntimeError,'Unsupported protocol version'):
            self.gate('2025-11-25')
    def test_old_versions_notify(self):
        for v in ['2024-11-05','2025-03-26','2025-06-18']:
            self.assertEqual(self.gate(v),[{'method':'notifications/initialized'}])
    def test_proposed_allowlist_still_rejects_unknown(self):
        supported=['2024-11-05','2025-03-26','2025-06-18','2025-11-25']
        self.assertEqual(len(self.gate('2025-11-25',supported)),1)
        with self.assertRaises(RuntimeError): self.gate('2099-01-01',supported)

if __name__=='__main__':
    unittest.main(verbosity=2)
