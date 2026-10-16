# R3 local evidence — 2026-10-16

Runtime: Node v24.19.0; Python 3.12.14. No installs, no credentials, no network calls by tests.

## Results and scope

| Case | Evidence | Result |
|---|---|---|
| Ten expiring-session callers | Original AGNT class; in-memory cloned store and deferred token promises | PASS: baseline makes 10 exchanges |
| A completes after B | Same original class and stubs | PASS: baseline overwrites B's new token with old snapshot |
| Ten callers with single-flight | Candidate concurrency model replacing refresh | PASS: 1 exchange, 10 new-token results |
| A/B commit-time merge | Candidate concurrency model | PASS: both updates retained |
| readOnly boolean predicate | Python design model, not Crystal | PASS |
| Blank file then later finding | Python scan model, not Go | PASS |
| Absent/empty object | Python scan model | PASS |
| Nonblank malformed data/BOM/NBSP | Python scan model | PASS: errors retained |

Eight cases passed, two executing upstream source behavior under stubs and six testing candidate/design models. Assertions observing a defect are reproductions, not successful fixes.

No real OAuth token exchange, token-file write, rotation/revocation, filesystem permissions, restart recovery, MCP HTTP transport, Noir parser/resolver, Engram CLI, Go or Crystal execution. No full upstream suites. No deployment or purchase.

An initial source-hash check FAILED because the local patch writer added one final newline. The exact original bytes were restored only after comparing candidate bytes against the Git blob hash. The subsequent hash check and all tests passed. That failed preflight was not counted as a test pass.

## Reproduce the AGNT boundary checks

Retrieve the pinned file below as `r3-agnt-source.js`, preserving its exact bytes. The test refuses a different Git blob:

https://raw.githubusercontent.com/agnt-gg/agnt/52f1a8644bf8f672df660534dc3584fbeb3138fc/backend/src/services/MCPOAuthService.js

Expected Git blob SHA1: `ef149de39c19a166fc874fd8de0c3b1382ed8b2a`.

Save the following harness alongside it as `r3-test-oauth.mjs`, then run `node r3-test-oauth.mjs`. Only the inspected class is evaluated; imports/singleton are excluded. Storage and token exchange are overridden before calling methods. Source retains its upstream license and is not vendored here. This is evidence for the already public issue, not a supported patch.

```js
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
const raw = fs.readFileSync(new URL('./r3-agnt-source.js', import.meta.url), 'utf8');
assert.equal(crypto.createHash('sha1').update(`blob ${Buffer.byteLength(raw)}\0`).update(raw).digest('hex'), 'ef149de39c19a166fc874fd8de0c3b1382ed8b2a');
// Run only the inspected class. Imports, singleton and real I/O are excluded.
const code = raw.slice(raw.indexOf('class MCPOAuthService {'), raw.indexOf('export default'));
const Class = vm.runInNewContext('const REFRESH_SKEW_MS=60000;\n'+code+'\nMCPOAuthService', {console, Date, Map});
const copy = x => JSON.parse(JSON.stringify(x));
const entry = name => ({resource:'https://example.invalid/'+name,authServer:{},client:{},session:{access_token:name+'0',refresh_token:'synthetic-'+name,obtained_at:1,expires_in:1}});
function fixture() {
  let data={a:entry('a'), b:entry('b')};
  const pending=[];
  const s=new Class();
  s._readAll=()=>copy(data);
  s._writeAll=async x=>{ data=copy(x); };
  s._token=async (_as,_c,p)=>new Promise(resolve=>pending.push({p,resolve}));
  return {s,pending,get:()=>copy(data)};
}
function resolve(req, token) {req.resolve({access_token:token,refresh_token:'synthetic-'+token,expires_in:3600});}
{
 const f=fixture(); const calls=Array.from({length:10},()=>f.s.getAccessToken('a'));
 assert.equal(f.pending.length,10);
 f.pending.forEach((r,i)=>resolve(r,'a'+(i+1))); await Promise.all(calls);
 console.log('PASS baseline: 10 parallel callers issue 10 token requests');
}
{
 const f=fixture(); const a=f.s.refresh('a'), b=f.s.refresh('b');
 resolve(f.pending[1],'b1'); await b; assert.equal(f.get().b.session.access_token,'b1');
 resolve(f.pending[0],'a1'); await a; assert.equal(f.get().b.session.access_token,'b0');
 console.log('PASS baseline: delayed A snapshot overwrites completed B refresh');
}
// Candidate concurrency model only: not a patch to upstream OAuth/storage.
function candidate(f) {
 const inflight=new Map(); let writes=Promise.resolve();
 f.s.refresh=function(name) {
  if(inflight.has(name)) return inflight.get(name);
  const p=(async()=>{
   const e=this._readAll()[name];
   const next=await this._token(e.authServer,e.client,{refresh_token:e.session.refresh_token});
   const w=writes.then(async()=>{const latest=this._readAll();latest[name]={...e,session:{...next,obtained_at:Date.now()}};await this._writeAll(latest);});
   writes=w.catch(()=>{});await w;return true;
  })();
  inflight.set(name,p);p.finally(()=>inflight.delete(name));return p;
 };
}
{
 const f=fixture();candidate(f);const calls=Array.from({length:10},()=>f.s.getAccessToken('a'));
 assert.equal(f.pending.length,1);resolve(f.pending[0],'a1');
 assert.deepEqual(await Promise.all(calls),Array(10).fill('a1'));
 console.log('PASS candidate model: 10 parallel callers share one request');
}
{
 const f=fixture();candidate(f);const a=f.s.refresh('a'),b=f.s.refresh('b');
 resolve(f.pending[1],'b1');await b;resolve(f.pending[0],'a1');await a;
 assert.equal(f.get().a.session.access_token,'a1');assert.equal(f.get().b.session.access_token,'b1');
 console.log('PASS candidate model: commit-time merge retains both updates');
}
console.log('4 cases passed. No real token endpoint, disk token store, rotation revocation, or upstream suite tested.');

```

Actual output after matching source bytes:

```text
PASS baseline: 10 parallel callers issue 10 token requests
PASS baseline: delayed A snapshot overwrites completed B refresh
PASS candidate model: 10 parallel callers share one request
PASS candidate model: commit-time merge retains both updates
4 cases passed. No real token endpoint, disk token store, rotation revocation, or upstream suite tested.
```

## Synthetic schema and blank-file design models

Save as `r3-test-boundaries.py`; run `python3 r3-test-boundaries.py`. The scan's synthetic marker represents a later finding; it does not implement Engram's registration-shape or executable checks. The schema test examines only direct properties, not YAML parsing, references or composition.

```python
"""Synthetic design models, NOT Crystal/Go source execution or upstream tests."""
import json
import unittest

def collect_direct(schema, filter_read_only):
    return [name for name, prop in schema['properties'].items()
            if not (filter_read_only and isinstance(prop, dict)
                    and prop.get('readOnly') is True)]

def scan_model(files, skip_blank):
    findings = []
    for name, raw in files:
        if raw is None:
            continue
        if skip_blank and not raw.strip(b' \t\r\n'):
            continue
        config = json.loads(raw.decode('utf-8'))
        if config.get('synthetic_stale'):
            findings.append(name)
    return findings

class BoundaryTests(unittest.TestCase):
    def test_read_only_direct_and_boolean_guard(self):
        schema={'properties':{'id':{'readOnly':True},'name':{'type':'string'},
            'secret':{'writeOnly':True},'mutable':{'readOnly':False},
            'invalid_string':{'readOnly':'true'},'scalar':None}}
        self.assertIn('id',collect_direct(schema,False))
        self.assertEqual(collect_direct(schema,True),['name','secret','mutable','invalid_string','scalar'])
    def test_blank_file_does_not_hide_later_finding(self):
        for raw in (b'',b' \r\n\t'):
            files=[('empty',raw),('later',b'{"synthetic_stale":true}')]
            with self.assertRaises(json.JSONDecodeError):scan_model(files,False)
            self.assertEqual(scan_model(files,True),['later'])
    def test_absent_and_empty_object(self):
        self.assertEqual(scan_model([('absent',None),('object',b'{}')],True),[])
    def test_nonblank_malformed_remains_error(self):
        for raw in (b'{', b'\xef\xbb\xbf', '\u00a0'.encode()):
            with self.assertRaises(json.JSONDecodeError):scan_model([('bad',raw)],True)

if __name__=='__main__':unittest.main(verbosity=2)

```

Actual result: all four unittest methods reported `ok`; `Ran 4 tests`, `OK`.

## Upstream regression work still required

- AGNT: maintainer-owned auth changes only; real persistence, callback/disconnect lifecycle, retry/error taxonomy, process lifetime and rotating mock authorization server. The model is not a production credential-store design.
- Noir: Crystal tests across JSON/YAML, OAS2/OAS3, supported form and JSON media, refs/compositions/cycles; shared response schema unchanged.
- Engram: Go test at pinned current head; fake adapter ordering, exact managed registration shape, absent executable, unchanged file bytes and no created files; CLI result verified.
