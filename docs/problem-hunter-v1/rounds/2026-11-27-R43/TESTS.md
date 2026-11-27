# R43 executed evidence

Date: 2026-11-27T05:10:25Z. Issue: https://github.com/abhi478jeetur-rgb/env-saaf/issues/494

## Source identity

Pinned commit: `0b9a97dcb87badf5d198314df0617e716a34214b`. Downloaded source files' Git blob hashes were verified locally after removing the transfer-added final blank line, then all checks below reran on the exact bytes.

| File | Git blob SHA |
|---|---|
| cli.js | `e5f6404e5d4fd34f8620c34b91b03c243c97cceb` |
| index.js | `0d063dcda619fd77211677a931f06b3d7df8e093` |
| package.json | `674ac1c7c0ee9156c4a3c0e470fc005aafda8407` |
| test-cli.js | `a17f59d3560d95537e25df63b7dcd3c75eca84f5` |

Node v24.22.3; no dependency install. Real `cli.js` and `index.js` subprocesses, no function mocks. Temporary directories and synthetic values only; minimal child environment containing PATH only for our harness; each temporary fixture removed after use. The existing upstream CLI suite uses its own environment scrubber. No provider, wallet, network endpoint or customer data.

## Observed results

12 paired fixture groups; 48 CLI subprocesses (baseline/candidate × text/JSON). All assertions passed. Existing upstream `node test-cli.js` passed separately on baseline and candidate. This is one upstream test file, **not the full npm test suite**.

```json
{
  "node": "v24.22.3",
  "groups": 12,
  "cliProcesses": 48,
  "results": [
    {
      "name": "extra keys, no local env",
      "baseline": {
        "exit": 0,
        "envExtra": [],
        "envMissing": [],
        "invalidCount": 0
      },
      "candidate": {
        "exit": 1,
        "envExtra": [
          "EXTRA",
          "PORTT"
        ],
        "envMissing": [],
        "invalidCount": 0
      }
    },
    {
      "name": "extra keys, clean local env",
      "baseline": {
        "exit": 0,
        "envExtra": [],
        "envMissing": [],
        "invalidCount": 0
      },
      "candidate": {
        "exit": 1,
        "envExtra": [
          "EXTRA"
        ],
        "envMissing": [],
        "invalidCount": 0
      }
    },
    {
      "name": "clean values",
      "baseline": {
        "exit": 0,
        "envExtra": [],
        "envMissing": [],
        "invalidCount": 0
      },
      "candidate": {
        "exit": 0,
        "envExtra": [],
        "envMissing": [],
        "invalidCount": 0
      }
    },
    {
      "name": "invalid values preserved",
      "baseline": {
        "exit": 1,
        "envExtra": [],
        "envMissing": [],
        "invalidCount": 1
      },
      "candidate": {
        "exit": 1,
        "envExtra": [],
        "envMissing": [],
        "invalidCount": 1
      }
    },
    {
      "name": "required omission preserved",
      "baseline": {
        "exit": 1,
        "envExtra": [],
        "envMissing": [],
        "invalidCount": 1
      },
      "candidate": {
        "exit": 1,
        "envExtra": [],
        "envMissing": [],
        "invalidCount": 1
      }
    },
    {
      "name": "optional and default omission stays allowed",
      "baseline": {
        "exit": 0,
        "envExtra": [],
        "envMissing": [],
        "invalidCount": 0
      },
      "candidate": {
        "exit": 0,
        "envExtra": [],
        "envMissing": [],
        "invalidCount": 0
      }
    },
    {
      "name": "custom template label",
      "baseline": {
        "exit": 0,
        "envExtra": [],
        "envMissing": [],
        "invalidCount": 0
      },
      "candidate": {
        "exit": 1,
        "envExtra": [
          "EXTRA"
        ],
        "envMissing": [],
        "invalidCount": 0
      }
    },
    {
      "name": "local findings retained with source labels",
      "baseline": {
        "exit": 1,
        "envExtra": [
          "LOCAL_ONLY"
        ],
        "envMissing": [
          "PORT"
        ],
        "invalidCount": 0
      },
      "candidate": {
        "exit": 1,
        "envExtra": [
          "EXTRA",
          "LOCAL_ONLY"
        ],
        "envMissing": [
          "PORT"
        ],
        "invalidCount": 0
      }
    },
    {
      "name": "same .env path produces one extra line",
      "baseline": {
        "exit": 1,
        "envExtra": [
          "EXTRA"
        ],
        "envMissing": [],
        "invalidCount": 0
      },
      "candidate": {
        "exit": 1,
        "envExtra": [
          "EXTRA"
        ],
        "envMissing": [],
        "invalidCount": 0
      }
    },
    {
      "name": "missing values file remains usage error",
      "baseline": {
        "exit": 2
      },
      "candidate": {
        "exit": 2
      }
    },
    {
      "name": "grouped schema uses documented flat key",
      "baseline": {
        "exit": 0,
        "envExtra": [],
        "envMissing": [],
        "invalidCount": 0
      },
      "candidate": {
        "exit": 1,
        "envExtra": [
          "DB_PORRT"
        ],
        "envMissing": [],
        "invalidCount": 0
      }
    },
    {
      "name": "plain .env behavior unchanged",
      "baseline": {
        "exit": 1,
        "envExtra": [
          "EXTRA"
        ],
        "envMissing": [],
        "invalidCount": 0
      },
      "candidate": {
        "exit": 1,
        "envExtra": [
          "EXTRA"
        ],
        "envMissing": [],
        "invalidCount": 0
      }
    }
  ]
}
```

## Candidate diff

Documentation-only inline candidate; not installed or posted upstream. The candidate preserves existing local .env checks and unions extras for JSON. Text output retains each file's provenance. Whether --values should replace local .env checking is a separate policy choice, not silently changed here. Path normalization deduplicates the tested ./\.env spelling; symlink equivalence was not tested.

```diff
--- a/cli.js
+++ b/cli.js
@@ -1200,6 +1200,7 @@
   // is skipped. Failures land in the existing `invalid` field (the library's
   // errors already name the key) and fail the check like a missing key.
   let invalid = [];
+  let valuesExtra = [];
   // Issue #358: the schema is a third source of truth; report both directions
   // against the example file, using flattened group names.
   let schemaNotDocumented = [];
@@ -1227,6 +1228,9 @@
     }
     if (targetName) {
       const rawValues = readEnvFile(path.join(dir, targetName));
+      if (valuesOpt !== null) {
+        valuesExtra = diffEnv(Object.keys(rawValues), documented).usedNotDocumented;
+      }
       // Any example finding protects the schema report, whichever file (the
       // template, .env, --values) supplies the values or an alias resolves to.
       const guard = secrets.length > 0 ? buildExampleGuard(schema, secrets, isolatedExample) : null;
@@ -1271,6 +1275,8 @@
   // when UNUSED is the *only* finding: any MISSING, EXTRA or INVALID still
   // fails the check exactly as before (#113 is unchanged for a project that
   // already reads at least one variable).
+  const localEnvExtra = envExtra;
+  envExtra = [...new Set([...localEnvExtra, ...valuesExtra])].sort();
   const scaffoldAhead = used.length === 0 && documentedNotUsed.length > 0
     && usedNotDocumented.length === 0 && secrets.length === 0
     && envExtra.length === 0 && envMissing.length === 0 && invalid.length === 0
@@ -1314,7 +1320,10 @@
     usedNotDocumented.forEach(k => console.log(`MISSING in ${fileOpt}: ${k} (used in code)`));
     documentedNotUsed.forEach(k => console.log(`UNUSED: ${k} (in ${fileOpt}, never used in code)`));
     secrets.forEach(k => console.log(`SECRET in ${fileOpt}: ${k} (value [REDACTED] looks like a real secret; use an empty value or placeholder)`));
-    envExtra.forEach(k => console.log(`EXTRA in .env: ${k} (not in ${fileOpt})`));
+    localEnvExtra.forEach(k => console.log(`EXTRA in .env: ${k} (not in ${fileOpt})`));
+    if (valuesOpt !== null && path.resolve(dir, valuesOpt) !== path.resolve(envPath)) {
+      valuesExtra.forEach(k => console.log(`EXTRA in ${valuesOpt}: ${k} (not in ${fileOpt})`));
+    }
     envMissing.forEach(k => console.log(`MISSING in .env: ${k} (in ${fileOpt}, not set locally)`));
     invalid.forEach(e => console.log(`INVALID${valuesOpt !== null ? ` in ${valuesOpt}` : ''}: ${e}`));
     schemaNotDocumented.forEach(k => console.log(`NOT DOCUMENTED: ${k} (in schema, missing from ${fileOpt})`));

```

## Reproduction

Retrieve the four pinned files above into `baseline/`, verify Git blob hashes, copy to `candidate/`, apply the diff to candidate/cli.js, and place this script next to both directories. Run `node regression.cjs`, then each copy's `node test-cli.js`. The script uses Node built-ins only.

```js
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const schema = "module.exports = { PORT: { type: 'port', required: true } };\n";
const defaults = { '.env.example': 'PORT=\n', 'env.schema.js': schema, 'prod.env': 'PORT=3000\n' };
const cases = [
  {name:'extra keys, no local env', files:{'prod.env':'PORT=3000\nEXTRA=synthetic-value\nPORTT=4000\n'}, old:0, next:1, extras:['EXTRA','PORTT']},
  {name:'extra keys, clean local env', files:{'.env':'PORT=3000\n','prod.env':'PORT=3000\nEXTRA=synthetic-value\n'}, old:0, next:1, extras:['EXTRA']},
  {name:'clean values', files:{}, old:0, next:0, extras:[]},
  {name:'invalid values preserved', files:{'prod.env':'PORT=not-a-port\n'}, old:1, next:1, extras:[], invalid:true},
  {name:'required omission preserved', files:{'prod.env':''}, old:1, next:1, extras:[], invalid:true},
  {name:'optional and default omission stays allowed', files:{'.env.example':'PORT=\nNAME=\n','env.schema.js':"module.exports={PORT:{type:'port',default:3000},NAME:{type:'string'}};\n",'prod.env':''},old:0,next:0,extras:[]},
  {name:'custom template label',files:{'deploy.example':'PORT=\n','prod.env':'PORT=3000\nEXTRA=synthetic-value\n'},flags:['--file','deploy.example'],old:0,next:1,extras:['EXTRA'],template:'deploy.example'},
  {name:'local findings retained with source labels',files:{'.env':'LOCAL_ONLY=synthetic-value\n','prod.env':'PORT=3000\nEXTRA=synthetic-value\n'},old:1,next:1,extras:['EXTRA','LOCAL_ONLY'],missing:['PORT']},
  {name:'same .env path produces one extra line',files:{'.env':'PORT=3000\nEXTRA=synthetic-value\n'},values:'./.env',old:1,next:1,extras:['EXTRA']},
  {name:'missing values file remains usage error',files:{},values:'absent.env',old:2,next:2},
  {name:'grouped schema uses documented flat key',files:{'.env.example':'DB_PORT=\n','env.schema.js':"module.exports={db:{prefix:'DB_',schema:{PORT:{type:'port',required:true}}}};\n",'prod.env':'DB_PORT=3000\nDB_PORRT=synthetic-value\n'},old:0,next:1,extras:['DB_PORRT']},
  {name:'plain .env behavior unchanged',files:{'.env':'PORT=3000\nEXTRA=synthetic-value\n'},noValues:true,old:1,next:1,extras:['EXTRA']},
];
const results=[];
for (const c of cases) {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'r43-env-'));
  try {
    for(const [name,content] of Object.entries({...defaults,...c.files}))fs.writeFileSync(path.join(dir,name),content);
    const pair={name:c.name};
    for(const variant of ['baseline','candidate']){
      const args=['check','.', '--schema','env.schema.js', ...(c.noValues?[]:['--values',c.values||'prod.env']),...(c.flags||[])];
      const run=(json)=>spawnSync(process.execPath,[path.join(__dirname,variant,'cli.js'),...args,...(json?['--json']:[])],{cwd:dir,env:{PATH:path.dirname(process.execPath)},encoding:'utf8',timeout:10000});
      const r=run(true), plain=run(false);
      assert.ifError(r.error);assert.ifError(plain.error);
      assert.equal(r.status,variant==='baseline'?c.old:c.next,`${c.name}: ${variant}: ${r.stdout}${r.stderr}`);
      assert.equal(plain.status,r.status);
      const data=JSON.parse(r.stdout);
      assert.equal(data.ok,r.status===0);
      assert.ok(!r.stdout.includes('synthetic-value')&&!plain.stdout.includes('synthetic-value'));
      if(c.extras && variant==='candidate')assert.deepEqual(data.envExtra,c.extras);
      if(c.invalid)assert.ok(data.invalid.length>0);
      if(c.missing)assert.deepEqual(data.envMissing,c.missing);
      if(c.name.startsWith('optional'))assert.deepEqual(data.envMissing,[]);
      if(c.name==='same .env path produces one extra line')assert.equal((plain.stdout.match(/EXTRA in /g)||[]).length,1);
      if(variant==='candidate'&&c.name==='local findings retained with source labels'){
        assert.match(plain.stdout,/EXTRA in \.env: LOCAL_ONLY/);
        assert.match(plain.stdout,/EXTRA in prod.env: EXTRA/);
        assert.match(plain.stdout,/MISSING in \.env: PORT/);
      }
      if(variant==='candidate'&&c.next===1&&c.old===0){
        assert.match(plain.stdout,/EXTRA in prod.env:/);
        assert.ok(plain.stdout.includes(`not in ${c.template||'.env.example'}`));
        assert.ok(!plain.stdout.includes('no process.env usage found'));
      }
      pair[variant]={exit:r.status,envExtra:data.envExtra,envMissing:data.envMissing,invalidCount:data.invalid?.length};
    }
    results.push(pair);
  } finally { fs.rmSync(dir,{recursive:true,force:true}); }
}
console.log(JSON.stringify({node:process.version,groups:results.length,cliProcesses:results.length*4,results},null,2));

```

## Not established

No full npm test, scanner/validator fuzz suites, packaging/export tests, TypeScript check, Node 16/other versions, Windows, watch mode, --fix interactions, alias policy or real deployment. No upstream patch, README or CHANGELOG was changed. Isolated filesystem CLI tests do not establish every supported deployment/configuration combination.
