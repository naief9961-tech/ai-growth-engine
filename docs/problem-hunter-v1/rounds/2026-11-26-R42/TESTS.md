# R42 isolated evidence — not a full application test

Executed2026-11-26 with Node v24.22.3; eight groups passed. Source commit162bffbd2367f39be6c8dd57d8a213d3b225bed6.

Four paired groups execute actual pinned route registration/handler source with stubbed dependencies. Original SQL wire value violates strict ISO shape; candidate maps it to expected UTC ISO. Actual time.ts helper uses real Luxon3.7.2. The harness validates4 source Git blob SHAs before execution. This is not a substitute implementation of date parsing.

Source imports are removed and TypeScript types stripped; route definitions, schemas, authorization and domain/database operations are stubbed. Real Hono, DB drivers, PGlite/Postgres, HTTP, React Native/Hermes, full workspace tests and TypeScript typecheck were NOT run. This establishes response-mapping behavior only. Other routes and aggregated client detail are outside the executed candidate.

Initial harness assertion failed on VM-realm object prototypes when comparing authorization call records. Changed only that assertion to compare serialized records; no product change was inferred from it. Final run exit0. Node emits its normal experimental stripTypeScriptTypes warning.

## Reproduce

In an empty temporary directory, save the following setup as prepare.py and harness as check.mjs. Run python3 prepare.py, then node check.mjs. Setup downloads four pinned source files and one Luxon archive; no dependency installation scripts, application entrypoints, credentials or live application endpoints. Archive SHA512 is copied from the pinned upstream pnpm-lock.yaml. No upstream files are vendored into this report.

```python
import urllib.request, pathlib, hashlib, base64, io, tarfile
base = "https://raw.githubusercontent.com/KhubaibQaiser/fitness-app/162bffbd2367f39be6c8dd57d8a213d3b225bed6/"
for path in ["apps/api/src/routes/clients.ts", "apps/api/src/routes/check-ins.ts", "packages/db/src/time.ts", "packages/contracts/openapi/openapi.v1.json"]:
    pathlib.Path(path.split("/")[-1]).write_bytes(urllib.request.urlopen(base + path).read())
archive = urllib.request.urlopen("https://registry.npmjs.org/luxon/-/luxon-3.7.2.tgz").read()
expected = "vtEhXh/gNjI9Yg1u4jX/0YVPMvxzHuGgCm6tC5kZyb08yjGWGnqAjGJvcXbqQR2P3MyMEFnRbpcdFS6PBcLqew=="
assert base64.b64encode(hashlib.sha512(archive).digest()).decode() == expected
with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tf:
    pathlib.Path("luxon.cjs").write_bytes(tf.extractfile("package/build/node/luxon.js").read())
```

## Executed harness

```javascript
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import { createHash } from 'node:crypto';
import { stripTypeScriptTypes } from 'node:module';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { DateTime } = require('./luxon.cjs');
const pins = { 'clients.ts':'e1ca94d86c68e10bc9b4dcab4f55264165f61d3b', 'check-ins.ts':'3e1f81888813599236308a52bd341dfca335a9a7', 'time.ts':'530ee9b2aab5889c86bd93770bc64c25f2984dd7', 'openapi.v1.json':'7ea447ee250c3905ea33e8cf9ab3357550273ba0' };
const source = {};
for (const [name,sha] of Object.entries(pins)) {
  let s = fs.readFileSync(new URL(name,import.meta.url),'utf8');
  const hash = x => createHash('sha1').update(`blob ${Buffer.byteLength(x)}\0`).update(x).digest('hex');
  if(hash(s)!==sha && hash(s+'\n')===sha) s+='\n';
  assert.equal(hash(s),sha,`source blob ${name}`); source[name]=s;
}
const executable = s => stripTypeScriptTypes(s.replace(/^import\s[\s\S]*?;\n/gm,'').replace(/export /g,''));
const helper = vm.runInNewContext(executable(source['time.ts'])+'\n({toStrictIso});',{DateTime,Date}).toStrictIso;
const ISO = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/;
const raw='2026-11-23 20:14:59.426903+00', expected='2026-11-23T20:14:59.426Z';
const note=Object.freeze({id:'synthetic-note',createdAt:raw,body:raw});
let checkin=Object.freeze({id:'synthetic-checkin',completedAt:raw,scheduledFor:'2026-11-23',coachNotes:raw});
const serializeNote = n => ({...n,createdAt:helper(n.createdAt)});
const serializeCheckIn = row => ({...row,completedAt:row.completedAt===null?null:helper(row.completedAt)});
const schema = new Proxy(function(){},{get:()=>schema,apply:()=>schema});
function routes(candidate) {
  const handlers={}, auth=[];
  const app={openapi:(route,fn)=>{handlers[route.operationId]=fn;}};
  const bind={db:{},authorize:(_c,permission,resource)=>auth.push({permission,resource}),asCoach:p=>p};
  const globals={createRoute:x=>x,z:schema,dto:schema,json:()=>({}),problemDocs:()=>({}),serializeNote,serializeCheckIn,listNotes:async()=>[note],createNote:async()=>note,listCheckIns:async()=>[checkin],getCheckInDetail:async()=>checkin,ProblemError:class extends Error {}};
  for (const [file,name] of [['clients.ts','registerClientRoutes'],['check-ins.ts','registerCheckInRoutes']]) {
    let s=source[file];
    if(candidate){
      const pairs = file==='clients.ts' ? [
        ['return c.json({ items: await listNotes(db, clientId) });','return c.json({ items: (await listNotes(db, clientId)).map(serializeNote) });'],
        ["await createNote(db, asCoach(c.get('principal')), clientId, c.req.valid('json').body),","serializeNote(await createNote(db, asCoach(c.get('principal')), clientId, c.req.valid('json').body)),"]
      ] : [
        ['return c.json({ items: await listCheckIns(db, clientId) });','return c.json({ items: (await listCheckIns(db, clientId)).map(serializeCheckIn) });'],
        ['return c.json(detail);','return c.json(serializeCheckIn(detail));']
      ];
      for(const [a,b] of pairs){assert.equal(s.split(a).length,2);s=s.replace(a,b);}
    }
    vm.runInNewContext(executable(s)+`\n${name};`,globals)(app,bind);
  }
  const context={req:{valid:kind=>kind==='param'?{clientId:'synthetic-client',id:'synthetic-checkin'}:{body:raw}},get:()=>({coachId:'synthetic-coach'}),json:x=>JSON.parse(JSON.stringify(x))};
  return {run:async id=>handlers[id](context),auth};
}
const results=[];
async function group(name,fn){await fn();results.push({name,status:'PASS'});}
for(const [id,field,key] of [['listNotes','createdAt','items'],['createNote','createdAt',null],['listClientCheckIns','completedAt','items'],['getCheckIn','completedAt',null]]){
  await group(id+' paired route boundary',async()=>{
    const b=routes(false),c=routes(true),bv=await b.run(id),cv=await c.run(id);
    const before=key?bv.items[0]:bv,after=key?cv.items[0]:cv;
    assert.equal(before[field],raw);assert.equal(ISO.test(before[field]),false);
    assert.equal(after[field],expected);assert.match(after[field],ISO);
    assert.equal(after.body??after.coachNotes,raw);
    if(after.scheduledFor)assert.equal(after.scheduledFor,'2026-11-23');
    assert.equal(JSON.stringify(c.auth),JSON.stringify(b.auth));assert.equal(c.auth.length,1);
    assert.equal((field==='createdAt'?note:checkin)[field],raw);
  });
}
await group('nullable completion remains null',async()=>{
  checkin={...checkin,completedAt:null};
  const c=routes(true);assert.equal((await c.run('getCheckIn')).completedAt,null);assert.equal((await c.run('listClientCheckIns')).items[0].completedAt,null);
});
await group('real helper offset and millisecond normalization',()=>{
  assert.equal(helper('2026-08-06 22:48:12.345+05'),'2026-08-06T17:48:12.345Z');
  assert.equal(helper('2026-08-05T23:00:00.000-04:00'),'2026-08-06T03:00:00.000Z');
  assert.equal(helper(new Date('2026-08-06T17:48:12.345Z')),'2026-08-06T17:48:12.345Z');
});
await group('real helper rejects malformed timestamp',()=>assert.throws(()=>helper('not-a-date'),/unparseable timestamp/));
await group('OpenAPI response audit cannot enumerate these timestamp fields',()=>{
  const spec=JSON.parse(source['openapi.v1.json']);
  for(const [path,method,list] of [['/v1/clients/{clientId}/notes','get',true],['/v1/clients/{clientId}/notes','post',false],['/v1/clients/{clientId}/check-ins','get',true],['/v1/check-ins/{id}','get',false]]){
    let s=spec.paths[path][method].responses['200'].content['application/json'].schema;
    if(list)s=s.properties.items.items;
    assert.equal(s.type,'object');assert.deepEqual(s.additionalProperties,{});assert.equal(s.properties,undefined);
  }
});
console.log(JSON.stringify({runtime:process.version,dependency:'Luxon 3.7.2, lockfile integrity verified',groups:results.length,results,limits:'Real source registration/handler bodies and timestamp helper; stubbed Hono/schema/auth/domain/db. No real HTTP, Postgres/PGlite, native Hermes, full workspace or TypeScript check.'},null,2));

```

## Actual final output

```json
{
  "runtime": "v24.22.3",
  "dependency": "Luxon 3.7.2, lockfile integrity verified",
  "groups": 8,
  "results": [
    {
      "name": "listNotes paired route boundary",
      "status": "PASS"
    },
    {
      "name": "createNote paired route boundary",
      "status": "PASS"
    },
    {
      "name": "listClientCheckIns paired route boundary",
      "status": "PASS"
    },
    {
      "name": "getCheckIn paired route boundary",
      "status": "PASS"
    },
    {
      "name": "nullable completion remains null",
      "status": "PASS"
    },
    {
      "name": "real helper offset and millisecond normalization",
      "status": "PASS"
    },
    {
      "name": "real helper rejects malformed timestamp",
      "status": "PASS"
    },
    {
      "name": "OpenAPI response audit cannot enumerate these timestamp fields",
      "status": "PASS"
    }
  ],
  "limits": "Real source registration/handler bodies and timestamp helper; stubbed Hono/schema/auth/domain/db. No real HTTP, Postgres/PGlite, native Hermes, full workspace or TypeScript check."
}

```

## Required upstream regressions — not executed here

Use the existing PGlite-backed notifications test pattern for the four route responses. Seed SQL timestamps with UTC and nonzero offsets, null completedAt, date-only scheduledFor, and date-looking free text. Assert exact UTC instants plus strict wire shape; Node Date acceptance alone is inadequate. Keep authorization negative tests. Add explicit response schemas if changing the public contract, regenerate OpenAPI and run workspace typecheck/tests plus native consumer verification. Preserve project merge gates.
