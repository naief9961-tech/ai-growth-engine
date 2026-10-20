// node --test test-woodhouse.cjs
// Baseline: actual Octokit v12.3.2 source, types stripped; only error utilities stubbed.
// Candidate: isolated helper, NOT a full Probot/Express/HMAC integration test.
const assert = require('node:assert/strict');
const { test } = require('node:test');
const { readFileSync } = require('node:fs');
const { stripTypeScriptTypes } = require('node:module');
const vm = require('node:vm');
const { createSubscriptionIndex, logUnmatchedVerified } = require('./subscription-candidate.cjs');
const source = readFileSync(__dirname + '/receiver.fixture.ts', 'utf8');
let js = stripTypeScriptTypes(source);
js = js.replace(/^import .* from .*;\s*$/gm, '').replace('export function receiverHandle', 'function receiverHandle');
const sandbox = { AggregateError: class extends Error {
  constructor(errors) { super('fixture aggregate error'); this.errors = errors; }
}, wrapErrorHandler: (handler, error) => handler(error), Error };
vm.createContext(sandbox);
vm.runInContext(js + '\nthis.receiverHandle = receiverHandle;', sandbox);
const receive = sandbox.receiverHandle;

test('baseline: missing action resolves before transform and guarded listener', async () => {
  let transformed = 0, called = 0;
  await receive({ hooks: { 'pull_request.opened': [() => called++] }, transform: x => {transformed++; return x;} },
    { id: 'synthetic-1', name: 'pull_request', payload: {} });
  assert.equal(transformed, 0); assert.equal(called, 0);
});
test('baseline: matching action dispatches; handler rejection still rejects', async () => {
  let called = 0;
  const state = { hooks: { 'pull_request.opened': [() => { called++; throw new Error('synthetic failure'); }] } };
  await assert.rejects(receive(state, {id:'synthetic-2',name:'pull_request',payload:{action:'opened'}}));
  assert.equal(called, 1);
});
test('baseline: base-event listeners also match action-bearing payloads', async () => {
  let called = 0;
  await receive({hooks:{push:[() => called++]}}, {id:'synthetic-3',name:'push',payload:{action:'extra'}});
  assert.equal(called, 1);
});
test('candidate: array registration, action matching, base matching, missing/unknown action', () => {
  const idx = createSubscriptionIndex();
  idx.register(['pull_request.opened', 'pull_request.reopened']); idx.register('push');
  assert.equal(idx.matches('pull_request','opened'), true);
  assert.equal(idx.matches('pull_request','reopened'), true);
  assert.equal(idx.matches('pull_request','closed'), false);
  assert.equal(idx.matches('pull_request',undefined), false);
  assert.equal(idx.matches('push',undefined), true);
  assert.equal(idx.matches('push','extra'), true);
  assert.equal(idx.matches('ping',undefined), false);
});
test('candidate: app indexes remain isolated', () => {
  const one = createSubscriptionIndex(), two = createSubscriptionIndex();
  one.register('push'); two.register('pull_request.opened');
  assert.equal(two.matches('push'),false); assert.equal(one.matches('pull_request','opened'),false);
});
test('candidate: one unmatched warning contains bounded metadata only', () => {
  const idx=createSubscriptionIndex(), logs=[];
  const log={warn:(...args)=>logs.push(args)};
  const metadata={deliveryId:'synthetic-4',app:'fixture',event:'pull_request',signature:'SECRET_SENTINEL'};
  const payload={privateBody:'PRIVATE_SENTINEL'};
  assert.equal(logUnmatchedVerified(idx,payload,metadata,log),true);
  assert.equal(logs.length,1);
  assert.deepEqual(Object.keys(logs[0][0]).sort(),['action','app','deliveryId','event','outcome']);
  assert.equal(JSON.stringify(logs).includes('SENTINEL'),false);
});
test('candidate: matching subscription is not mislabeled as unmatched', () => {
  const idx=createSubscriptionIndex(); idx.register('pull_request.closed');
  let warnings=0;
  assert.equal(logUnmatchedVerified(idx,{action:'closed'},{event:'pull_request'}, {warn:()=>warnings++}),false);
  assert.equal(warnings,0);
});
test('candidate integration model: verification rejection never reaches success logging', async () => {
  const idx=createSubscriptionIndex(); let warnings=0;
  async function modeledRoute(verify) {
    await verify();
    logUnmatchedVerified(idx,{}, {event:'pull_request'}, {warn:()=>warnings++});
  }
  await assert.rejects(modeledRoute(async()=>{throw new Error('synthetic signature rejection');}));
  assert.equal(warnings,0);
  await modeledRoute(async()=>{}); assert.equal(warnings,1);
});
