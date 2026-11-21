# R37 test evidence
Executed2026-11-21: Node v24.22.3;8 assertions passed,0 failed.
Read pinned operations/locale.ts from commit d16fd22d49bb74579a73a09b8c06649c17184b9d (blob c1c51d3a85be8680049dfa55820f5668235ccdf8). Save a reviewed copy as locale.mts, removing only lines beginning "import ". No other source transformation. Node strips types natively. This does not exercise the module's validation error paths.
Run node test.mjs alongside it. Synthetic data only; no network or database. The boundary wrapper is a design model, not a patch applied to dispatcher.

```javascript
import assert from 'node:assert/strict';
import {projectCanonicalDoc as project} from './locale.mts';
const fields={body:{type:'richText',localized:true}};
const rt={type:'doc',content:[{type:'paragraph',content:[{type:'text',text:'synthetic'}]}]};
const ctx={locale:'id',defaultLocale:'en'};
const canonical={id:1,body:{id:rt,en:{type:'doc',content:[]}}};
const once=project(canonical,fields,ctx);
assert.deepEqual(once.body,rt);
assert.equal(project(once,fields,ctx).body,null);
const atBoundary=(doc,shape)=>shape==='canonical'?project(doc,fields,ctx):doc;
assert.deepEqual(atBoundary(once,'projected').body,rt);
assert.deepEqual(atBoundary(canonical,'canonical').body,rt);
const missing={id:1,body:{fr:rt}};
assert.equal(project(missing,fields,ctx).body,null);
const unsafe=(val)=> !('id' in val)&&!('en' in val)?val:null;
assert.deepEqual(unsafe(missing.body),{fr:rt});
assert.deepEqual(project(canonical,fields,{locale:'all'}),canonical);
assert.deepEqual(project({body:{en:rt}},fields,ctx).body,rt);
console.log(JSON.stringify({assertions:8,passed:8,baseline:'second projection null',candidate:'explicit representation-boundary model preserves value',counterexample:'missing-key heuristic leaks locale dictionary',limits:'Source locale module with imports removed; no DB, webhook delivery, ACL, full operation or upstream suite tested.'}));

```
Output: assertions8, passed8; baseline second projection null; explicit representation-boundary model preserves value; missing-key heuristic leaks locale dictionary.
Regression integration still required: create/update/unpublish, canonical publish, missing requested/fallback locales, fallback enabled/disabled, locale all, collection/global, ACL denied fields, both adapters and actual webhook payload.
