import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { createHash, createHmac, timingSafeEqual } from 'node:crypto';
import { stripTypeScriptTypes } from 'node:module';
import vm from 'node:vm';
import path from 'node:path';

// Run only reviewed source extracts. No imports, network, provider, or database.
const root = process.argv[2] || './input';
const manifest = JSON.parse(readFileSync(new URL('./sources.json', import.meta.url), 'utf8'));
function source(name) {
  const content = readFileSync(path.join(root, name), 'utf8');
  const hash = createHash('sha1').update(`blob ${Buffer.byteLength(content)}\0`).update(content).digest('hex');
  assert.equal(hash, manifest[name].blob_sha, `source drift: ${name}`);
  return content;
}
function between(s, start, end) {
  const a = s.indexOf(start), b = s.indexOf(end, a + start.length);
  assert(a >= 0 && b > a, 'extract markers must exist');
  return s.slice(a, b);
}
function once(s, old, replacement) {
  assert.equal(s.split(old).length, 2, 'patch marker must occur once');
  return s.replace(old, replacement);
}
const results = [];
async function check(name, type, fn) {
  await fn(); results.push({name, type, status:'PASS'}); console.log(`PASS ${name}`);
}
const now = 1792555200;
const payload = '{"id":"evt_synthetic_only","data":{"value":1}}';
const secret = 'synthetic-public-test-key-not-a-credential';
const sign = (t, body = payload) => `t=${t},v1=${createHmac('sha256',secret).update(`${t}.${body}`).digest('hex')}`;
const frame = between(source('framework.ts'), 'export const stripeVerify:', '/**\n * GitHub signature verifier');
const handler = between(source('handler.ts'), 'export class StripeSignatureVerifier', '/**\n * GitHub webhook signature verifier');
function verifiers(f, h) {
  const ctx = vm.createContext({createHmac, timingSafeEqual, Buffer, Date:{now:()=>now*1000}});
  vm.runInContext(stripTypeScriptTypes(f.replace('export const','const') + h.replace('export class','class') + '\nthis.api=[stripeVerify,(...args)=>new StripeSignatureVerifier().verify(...args)];'),ctx);
  return ctx.api;
}
const baseline = verifiers(frame, handler);
const guard = "if (/[^0-9]/.test(timestamp)) return false;\n  const timestampNum = Number(timestamp);\n  if (!Number.isSafeInteger(timestampNum)) return false;";
const fixedFrame = once(frame, 'const now = Math.floor(Date.now() / 1000);', guard + '\n  const now = Math.floor(Date.now() / 1000);').replace('Number.parseInt(timestamp)', 'timestampNum');
const fixedHandler = once(handler, 'const timestampNum = Number.parseInt(timestamp, 10);', guard);
const fixed = verifiers(fixedFrame, fixedHandler);
const finiteFrame = once(frame, 'const now = Math.floor(Date.now() / 1000);', 'const timestampNum = Number.parseInt(timestamp, 10);\n  if (!Number.isFinite(timestampNum)) return false;\n  const now = Math.floor(Date.now() / 1000);').replace('Math.abs(now - Number.parseInt(timestamp))','Math.abs(now - timestampNum)');
const finiteHandler = once(handler, 'const timestampNum = Number.parseInt(timestamp, 10);', 'const timestampNum = Number.parseInt(timestamp, 10);\n    if (!Number.isFinite(timestampNum)) return false;');
const finiteOnly = verifiers(finiteFrame, finiteHandler);
await check('Stripe: both original verifiers accept correctly signed t=abc', 'source-extracted baseline',()=>baseline.forEach(v=>assert.equal(v(payload,sign('abc'),secret),true)));
await check('Stripe: finite-only candidate still accepts a signed numeric prefix with junk', 'candidate counterexample',()=>finiteOnly.forEach(v=>{assert.equal(v(payload,sign('abc'),secret),false);assert.equal(v(payload,sign(now+'junk'),secret),true);}));
await check('Stripe: full grammar rejects malformed signed timestamps in both copies', 'source-extracted candidate',()=>fixed.forEach(v=>['abc','',now+'junk',now+'.5',now+'e0',' '+now,'+'+now,now+'\n'].forEach(t=>assert.equal(v(payload,sign(t),secret),false,t))));
await check('Stripe: valid signatures and original timestamp bytes preserved', 'source-extracted candidate',()=>fixed.forEach(v=>[String(now),'0'+now].forEach(t=>assert.equal(v(payload,sign(t),secret),true,t))));
await check('Stripe: inclusive tolerance boundaries remain unchanged', 'source-extracted candidate',()=>fixed.forEach(v=>[-300,300,-301,301].forEach(delta=>assert.equal(v(payload,sign(now+delta),secret),Math.abs(delta)<=300))));
await check('Stripe: unsafe and out-of-window integers rejected', 'source-extracted candidate',()=>fixed.forEach(v=>['9007199254740993','0'].forEach(t=>assert.equal(v(payload,sign(t),secret),false))));
await check('Stripe: wrong key and mutated raw body rejected', 'source-extracted candidate',()=>fixed.forEach(v=>{assert.equal(v(payload,sign(now),'different-synthetic-key'),false);assert.equal(v(payload+' ',sign(now),secret),false);}));
await check('Stripe: missing timestamp or signature rejected', 'source-extracted candidate',()=>fixed.forEach(v=>{assert.equal(v(payload,'v1=aa',secret),false);assert.equal(v(payload,'t='+now,secret),false);}));

const core = between(source('load.tools.service.ts'), '  coreToolNames() {', '  async agent()');
const relaySource = source('mcp.relay.service.ts');
const connect = between(relaySource,'  async connect(', '  // The same definitions');
const callTool = between(relaySource,'  async callTool(', '  private async withClient');
class HttpException extends Error {}
class StreamableHTTPError extends Error {}
function fixture(optional = false, listed = ['integrationList','integrationSchedulePostTool']) {
  const toolList = [{name:'integrationList'},{name:'integrationSchedulePostTool'},{name:'mediaStatusTool',optionalOnSelfHosted:optional}];
  const ctx = vm.createContext({URL,HttpException,StreamableHTTPError,HttpStatus:{BAD_REQUEST:400},isSafePublicHttpsUrl:async()=>true,requiredTools:['integrationList','integrationSchedulePostTool'],toolList});
  const code = `class Loader { ${core} } class Relay { ${connect} ${callTool} } this.Loader=Loader;this.Relay=Relay;`;
  vm.runInContext(stripTypeScriptTypes(code),ctx);
  const loader = new ctx.Loader(); loader._moduleRef={get:p=>p};
  const relay = new ctx.Relay(); relay._loadToolsService=loader;
  relay.withClient=async (_instance, fn)=>fn({listTools:async()=>({tools:listed.map(name=>({name}))}),callTool:async()=>({isError:true,content:[{type:'text',text:'Unknown tool: mediaStatusTool'}]})});
  relay.text=r=>r.content[0].text;
  return {loader,relay};
}
await check('Postiz: release catalog lacks MediaStatusTool; main registers it without optional flag', 'pinned source assertions',()=>{
  assert(!source('release-tool.list.ts').includes('MediaStatusTool'));
  assert(source('main-tool.list.ts').includes('  MediaStatusTool,'));
  assert(!source('media.status.tool.ts').includes('optionalOnSelfHosted'));
});
await check('Postiz: current extracted gate rejects missing mediaStatusTool with the reported message', 'source-extracted baseline with stubs',async()=>{
  await assert.rejects(fixture().relay.connect('https://fixture.example','synthetic-key'),/missing tools this connection needs \(mediaStatusTool\)/);
});
await check('Postiz: candidate optional metadata permits baseline connection', 'source-extracted gate; candidate metadata',async()=>{
  const result=await fixture(true).relay.connect('https://fixture.example','synthetic-key');assert.equal(result.mcpUrl,'https://fixture.example/api/mcp');
});
await check('Postiz: baseline identity tools remain mandatory', 'source-extracted gate; candidate metadata',async()=>{
  await assert.rejects(fixture(true,[]).relay.connect('https://fixture.example','synthetic-key'),/does not look like a Postiz instance/);
});
await check('Postiz: current catalog passes the original gate', 'source-extracted baseline with stubs',async()=>{
  await fixture(false,['integrationList','integrationSchedulePostTool','mediaStatusTool']).relay.connect('https://fixture.example','synthetic-key');
});
await check('Postiz: absent optional tool still returns explicit call failure', 'source-extracted callTool with stubs',async()=>{
  await assert.rejects(fixture(true).relay.callTool({mcpUrl:'https://fixture.example/api/mcp',apiKey:'synthetic-key'},'mediaStatusTool',{}),/mediaStatusTool is not available/);
});
writeFileSync(new URL('./results.json',import.meta.url),JSON.stringify({node:process.version,run_at:new Date().toISOString(),groups_passed:results.length,results,scope:'Reviewed source extracts and synthetic stubs only. No upstream suite, OAuth, live MCP, deployed image, media processing, database or payment test.'},null,2)+'\n');
