# R5 isolated checks

Node v24.19.0. Command actually run: `node r5/test_schema_boundary.mjs`; exit 0. Eight assertion groups PASS: three original-source loss reproductions and five candidate groups. Full project suites, tsc, model calls, desktop behavior, and general JSON Schema validation NOT RUN. No packages installed, credentials used, network calls or tool execution during tests. Node emitted its usual experimental stripTypeScriptTypes warning.

The source wrapper and request-definition builder were fetched through the GitHub connector, then verified against Git blob hashes by the harness before execution. Type annotations and imports were removed; the policy dependency was stubbed to allow construction. This does not test approval policy, transport or model acceptance. The local JSON Pointer helper is only a fixture assertion, not a schema validator.

## Pinned source inputs
- [src/mcp/wrapper.ts](https://raw.githubusercontent.com/huiliyi37/Tianshu-harness/76a968a6b0a927cd2408882641baab4f7563b61b/src/mcp/wrapper.ts): blob `6f430637bfd5d4a42eb3646fda87fc0f00dd1e7a`
- [src/prompt/oai-tool-definitions.ts](https://raw.githubusercontent.com/huiliyi37/Tianshu-harness/76a968a6b0a927cd2408882641baab4f7563b61b/src/prompt/oai-tool-definitions.ts): blob `da519cb05a5e52791abf21af6bd5a4ebb0a328d7`

## Reproduction setup
Save the setup script and harness in the same disposable directory. Setup fetches only two pinned public files and verifies hashes; source is not vendored here. This optional downloader was not used in the actual run.

```python
# Optional setup for a reviewer; not executed during this round.
import hashlib, json, pathlib, urllib.request
manifest = [{"path":"src/mcp/wrapper.ts","sha":"6f430637bfd5d4a42eb3646fda87fc0f00dd1e7a","url":"https://raw.githubusercontent.com/huiliyi37/Tianshu-harness/76a968a6b0a927cd2408882641baab4f7563b61b/src/mcp/wrapper.ts"},{"path":"src/prompt/oai-tool-definitions.ts","sha":"da519cb05a5e52791abf21af6bd5a4ebb0a328d7","url":"https://raw.githubusercontent.com/huiliyi37/Tianshu-harness/76a968a6b0a927cd2408882641baab4f7563b61b/src/prompt/oai-tool-definitions.ts"}]
bundle = []
for item in manifest:
    with urllib.request.urlopen(item["url"], timeout=20) as response:
        raw = response.read()
    actual = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    assert actual == item["sha"]
    bundle.append({"path": item["path"], "sha": item["sha"], "content": raw.decode("utf-8")})
pathlib.Path("pinned-inputs.json").write_text(json.dumps(bundle), encoding="utf-8")
```

## test_schema_boundary.mjs
```js
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { createHash } from 'node:crypto'
import { stripTypeScriptTypes } from 'node:module'
import vm from 'node:vm'

const bundle = JSON.parse(readFileSync(new URL('./pinned-inputs.json', import.meta.url), 'utf8'))
for (const f of bundle) {
  const b = Buffer.from(f.content)
  assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob ' + b.length + '\0'), b])).digest('hex'), f.sha)
}
const wrapper = bundle.find(f => f.path.endsWith('/wrapper.ts')).content
const builder = bundle.find(f => f.path.endsWith('/oai-tool-definitions.ts')).content
const old = "input_schema: {\n        type: 'object',\n        properties: mcpDef.inputSchema.properties ?? {},\n        required: mcpDef.inputSchema.required,\n      },"
assert.equal(wrapper.split(old).length, 2)
const patch = "input_schema: {\n        ...structuredClone(mcpDef.inputSchema),\n        properties: structuredClone(mcpDef.inputSchema.properties ?? {}),\n      },"
function load(src, exported) {
  const js = stripTypeScriptTypes(src.replace(/^import .*$/gm, ''), {mode:'strip'})
    .replace(/^export /gm, '')
  const sandbox = {
    structuredClone,
    evaluateMcpPolicy: () => ({action:'allow',capability:'read'}),
    classifyMcpError: () => {throw Error('unexpected execution')},
    resolveSubAgentWorkspace: () => {throw Error('unexpected execution')},
    readWorkspaceReceipt: () => {throw Error('unexpected execution')},
  }
  return vm.runInNewContext(js + '\n' + exported, sandbox)
}
const baseline = load(wrapper, 'createMcpToolWrapper')
const candidate = load(wrapper.replace(old, patch), 'createMcpToolWrapper')
const toOai = load(builder, 'buildOaiToolDefinitions')
const plain = x => JSON.parse(JSON.stringify(x))
const def = (fn, schema) => plain(fn('fixture', {name:'probe',inputSchema:schema}, async()=>{throw Error('must not execute')}).definition)
function pointer(root, ref) {
  assert.ok(ref.startsWith('#/'))
  return ref.slice(2).split('/').map(s=>s.replaceAll('~1','/').replaceAll('~0','~')).reduce((o,k)=>{
    assert.ok(o && Object.hasOwn(o,k), 'missing pointer component '+k)
    return o[k]
  }, root)
}
const fixtures = {
  modern: {type:'object',properties:{item:{$ref:'#/$defs/Thing'}},required:['item'],$defs:{Thing:{type:'object',properties:{value:{type:'string'}}}}},
  legacy: {type:'object',properties:{item:{$ref:'#/definitions/Thing'}},definitions:{Thing:{type:'integer'}}},
  constraints: {type:'object',properties:{a:{type:'string'},b:{type:'integer'}},additionalProperties:false,oneOf:[{required:['a']},{required:['b']}],minProperties:1},
}
let n = 0
function test(label, fn){fn();n++;console.log('PASS '+n+' '+label)}
test('baseline: modern reference loses target',()=>{
 const s=def(baseline,fixtures.modern).input_schema
 assert.equal(s.$defs,undefined)
 assert.throws(()=>pointer(s,s.properties.item.$ref),/missing pointer/)
})
test('baseline: legacy reference loses target',()=>{
 const s=def(baseline,fixtures.legacy).input_schema
 assert.equal(s.definitions,undefined)
 assert.throws(()=>pointer(s,s.properties.item.$ref),/missing pointer/)
})
test('baseline: root constraints lost even without references',()=>{
 const s=def(baseline,fixtures.constraints).input_schema
 for(const k of ['additionalProperties','oneOf','minProperties'])assert.equal(s[k],undefined)
})
test('candidate: modern and legacy refs resolve at outgoing request boundary',()=>{
 for(const input of [fixtures.modern,fixtures.legacy]){
   const out=plain(toOai([def(candidate,input)]))[0].function.parameters
   assert.deepEqual(out,input)
   assert.deepEqual(pointer(out,out.properties.item.$ref),{...(input.$defs??input.definitions).Thing})
 }
})
test('candidate: nested escaped pointer and recursive definition preserved without expansion',()=>{
 const s={type:'object',properties:{items:{type:'array',items:{$ref:'#/$defs/a~1b~0c'}}},$defs:{'a/b~c':{type:'object',properties:{next:{$ref:'#/$defs/a~1b~0c'}}}}}
 const out=plain(toOai([def(candidate,s)]))[0].function.parameters
 assert.deepEqual(pointer(out,out.properties.items.items.$ref),s.$defs['a/b~c'])
 assert.deepEqual(out,s)
})
test('candidate: independent root constraints survive JSON serialization',()=>{
 const out=plain(toOai([def(candidate,fixtures.constraints)]))[0].function.parameters
 assert.deepEqual(out,fixtures.constraints)
})
test('candidate: source schema remains unchanged including after output mutation',()=>{
 const s=structuredClone(fixtures.modern),before=JSON.stringify(s)
 const out=def(candidate,s).input_schema
 out.$defs.Thing.properties.value.type='number'
 assert.equal(JSON.stringify(s),before)
 // Also check original live object before conversion through JSON
 const live=candidate('fixture',{name:'probe',inputSchema:s},async()=>{throw Error('must not execute')})
 live.definition.input_schema.$defs.Thing.properties.value.type='boolean'
 assert.equal(JSON.stringify(s),before)
})
test('candidate: no-property controls retain existing object fallback and empty-tool behavior',()=>{
 assert.deepEqual(def(candidate,{type:'object'}).input_schema,{type:'object',properties:{}})
 assert.deepEqual(def(candidate,{type:'object',properties:{}}).input_schema,{type:'object',properties:{}})
 assert.equal(toOai([]),undefined)
})
console.log(JSON.stringify({groups:n,baseline:3,candidate:5,node:process.version,fullSuite:false,networkCalls:0}))
```

## Observed output
```text
PASS 1 baseline: modern reference loses target
PASS 2 baseline: legacy reference loses target
PASS 3 baseline: root constraints lost even without references
PASS 4 candidate: modern and legacy refs resolve at outgoing request boundary
PASS 5 candidate: nested escaped pointer and recursive definition preserved without expansion
PASS 6 candidate: independent root constraints survive JSON serialization
PASS 7 candidate: source schema remains unchanged including after output mutation
PASS 8 candidate: no-property controls retain existing object fallback and empty-tool behavior
{"groups":8,"baseline":3,"candidate":5,"node":"v24.19.0","fullSuite":false,"networkCalls":0}
```

The source is public main at 76a968a6b0a927cd2408882641baab4f7563b61b, not the reporter's installed desktop build. Candidate-only edit replaces the schema projection; no upstream source was modified. Input type widening remains a proposed upstream task requiring real typecheck. A check for Python jsonschema reported ModuleNotFoundError; it was not installed and no validation claim is made.

