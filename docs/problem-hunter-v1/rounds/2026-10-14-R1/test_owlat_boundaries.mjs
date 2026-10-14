// Isolated source-extract tests. No HTTP requests, real secrets or Convex DB.
// Node >=24: built-in TypeScript stripping; no downloaded packages.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {stripTypeScriptTypes} from 'node:module';
import {webcrypto, createHmac} from 'node:crypto';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const root=path.dirname(fileURLToPath(import.meta.url));
const read=f=>fs.readFileSync(path.join(root,'evidence',f),'utf8');
function extract(f,name){
  const src=read(f); const re=new RegExp('^(?:export )?(?:async )?function '+name+'\\(', 'm');
  const start=src.search(re); if(start<0)throw Error('Missing function '+name);
  const end=src.indexOf('\n}',start); if(end<0)throw Error('Missing function end');
  return src.slice(start,end+2).replace(/^export /,'');
}
const secretBytes=Buffer.from('synthetic-test-only-secret-32byte!');
const secret='whsec_'+secretBytes.toString('base64');
const funcs=[
 ['owlat-bytes.ts',['bytesToBase64','bytesToBase64Url','bytesToHex']],
 ['owlat-crypto.ts',['constantTimeEqual','importHmacKey','hmacSignature','hmacSha256Base64']],
 ['owlat-security.ts',['isUnixSecondsTimestamp','clampToleranceSeconds']],
 ['owlat-resend.ts',['verifySvixHeaders']],
 ['owlat-signature.ts',['readSignatureSecret','verifyPluginSvixDelivery','deliveryDigestOf']],
].flatMap(([f,ns])=>ns.map(n=>extract(f,n))).join('\n');
const prelude=`const UNIX_SECONDS_PATTERN=/^\\d{1,15}$/;
const SVIX_TIMESTAMP_TOLERANCE_SECONDS=300;
const PLUGIN_INBOUND_REPLAY_MAX_TOLERANCE_SECONDS=900;
const SVIX_DIGEST_SCHEME='svix';
const getPluginSecret=()=>TEST_SECRET;
const bytesToBinaryString=b=>String.fromCharCode(...new Uint8Array(b));`;
const stable=`async function stableSvixDigest(pluginId,transportKind,id,body){
 const bodyHash=bytesToHex(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(body)));
 return bytesToHex(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(JSON.stringify(['owlat.plugin.webhook.svix.v2',pluginId,transportKind,id,bodyHash]))));
}`;
function build(patched){
 let source=prelude+'\n'+funcs;
 if(patched){
   const original="deliveryDigest: await deliveryDigestOf(delivery.pluginId, delivery.transportKind, [\n\t\t\tSVIX_DIGEST_SCHEME,\n\t\t\tid,\n\t\t\ttimestamp,\n\t\t\tsignature,\n\t\t]),";
   assert(source.includes(original));
   source=source.replace(original,'deliveryDigest: await stableSvixDigest(delivery.pluginId, delivery.transportKind, id, delivery.rawBody),');
   source=source.replace('expiresAtMs: nowMs + 2 * toleranceSeconds * 1000,','expiresAtMs: nowMs + 48 * 60 * 60 * 1000,')+'\n'+stable;
 }
 const ctx=vm.createContext({crypto:webcrypto,TextEncoder,Uint8Array,ArrayBuffer,atob,btoa,TEST_SECRET:secret});
 vm.runInContext(stripTypeScriptTypes(source)+'\nglobalThis.verify=verifyPluginSvixDelivery;',ctx);
 return ctx.verify;
}
const original=build(false), patched=build(true);
const now=1800000000, body='{"type":"email.delivered","id":"synthetic"}';
const contract={scheme:'svix',secretEnvVar:'PLUGIN_SYNTHETIC',toleranceSeconds:300};
const sign=(id,ts,b)=>'v1,'+createHmac('sha256',secretBytes).update(`${id}.${ts}.${b}`).digest('base64');
function delivery({id='msg_synthetic',ts=now,b=body,plugin='plugin_a',transport='email',signature,at=ts}={}){
 return {contract,pluginId:plugin,transportKind:transport,rawBody:b,nowMs:at*1000,headers:new Headers({'svix-id':id,'svix-timestamp':String(ts),'svix-signature':signature||sign(id,ts,b)})};
}
const tests=[];
async function test(name,fn){await fn(); tests.push({name,status:'PASS'});console.log('PASS '+name)}
await test('baseline reproduces distinct identities for authentic re-signed retry',async()=>{
 const a=await original(delivery(),contract),b=await original(delivery({ts:now+60}),contract);
 assert(a.ok&&b.ok);assert.notEqual(a.deliveryDigest,b.deliveryDigest);
 assert.equal(a.expiresAtMs-now*1000,600000);
});
await test('candidate keeps retry identity stable',async()=>{
 const a=await patched(delivery(),contract),b=await patched(delivery({ts:now+60}),contract);
 assert(a.ok&&b.ok);assert.equal(a.deliveryDigest,b.deliveryDigest);
});
await test('signature-list ordering does not change identity after verification',async()=>{
 const good=sign('msg_synthetic',now,body);
 const a=await patched(delivery({signature:good+' v1,bad'}),contract);
 const b=await patched(delivery({signature:'v1,bad '+good}),contract);
 assert(a.ok&&b.ok);assert.equal(a.deliveryDigest,b.deliveryDigest);
});
await test('body id plugin and transport remain distinct',async()=>{
 const variants=[{}, {id:'msg_other'}, {b:body+' '}, {plugin:'plugin_b'}, {transport:'sms'}];
 const out=await Promise.all(variants.map(v=>patched(delivery(v),contract)));
 assert(out.every(x=>x.ok));assert.equal(new Set(out.map(x=>x.deliveryDigest)).size,5);
});
await test('bad signature rejected',async()=>{
 const out=await patched(delivery({signature:'v1,bad'}),contract);assert.equal(out.ok,false);assert.equal(out.status,401);
});
await test('stale signed timestamp still rejected',async()=>{
 assert.equal((await patched(delivery({at:now+301}),contract)).ok,false);
});
await test('unverified raw body alteration rejected',async()=>{
 const d=delivery();d.rawBody+=' ';assert.equal((await patched(d,contract)).ok,false);
});
await test('proposed retention outlives freshness without extending it',async()=>{
 const a=await patched(delivery(),contract);assert.equal(a.expiresAtMs-now*1000,48*60*60*1000);
});
await test('retry after 27.5h retains same identity with a fresh signature',async()=>{
 const a=await patched(delivery(),contract),b=await patched(delivery({ts:now+99000}),contract);
 assert(a.ok&&b.ok);assert.equal(a.deliveryDigest,b.deliveryDigest);assert(a.expiresAtMs>b.expiresAtMs-48*60*60*1000);
});
console.log(JSON.stringify({tests:tests.length,passed:tests.length,scope:'source-extracted verifier/digest; no Convex persistence or concurrency test'},null,2));
