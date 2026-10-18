'use strict';
// Extract reviewed methods only; no imports of upstream modules/provider calls.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = name => fs.readFileSync(`${__dirname}/source/${name}`, 'utf8');
const extract = (s, start, end) => {
  assert.equal(s.split(start).length, 2);
  return s.slice(s.indexOf(start), s.indexOf(end, s.indexOf(start))).trim();
};
const record = extract(source('billing_repository.js'), 'async recordEvent(', '    // Accounts');
const handle = extract(source('billing_service.js'), 'async handleWebhook(', '    async applyEvent(');
async function baseline() {
  let row, applies = 0;
  const BillingEvent = {create: async () => {
    if (row) throw Object.assign(new Error('duplicate'), {name:'SequelizeUniqueConstraintError'});
    row = {status:'received', update: async data => Object.assign(row,data)};
    return row;
  }};
  const repository = vm.runInNewContext(`({${record}})`, {BillingEvent});
  const service = vm.runInNewContext(`({${handle}})`, {repository, providers:{isBillingConfigured:()=>true}});
  service.provider = () => ({parseWebhook: async () => ({id:'synthetic-1', rawType:'synthetic'})});
  service.applyEvent = async () => { applies++; throw new Error('synthetic temporary fault'); };
  await assert.rejects(service.handleWebhook(Buffer.from('{}'), {}), /temporary/);
  assert.equal(row.status,'failed');
  const retry = await service.handleWebhook(Buffer.from('{}'), {});
  assert.equal(retry.duplicate,true);
  assert.equal(applies,1);
  console.log('PASS source-extracted failed redelivery is silently classified duplicate');
}
async function claimModel() {
  // Design model, NOT the production ORM/transaction implementation.
  let status = 'failed', applies = 0;
  const claim = () => { if (status !== 'failed') return false; status='processing'; return true; };
  const workers = Array.from({length:8}, async () => {
    if (!claim()) return false;
    await Promise.resolve(); applies++; status='processed'; return true;
  });
  assert.equal((await Promise.all(workers)).filter(Boolean).length,1);
  assert.equal(applies,1); assert.equal(status,'processed'); assert.equal(claim(),false);
  console.log('PASS candidate state-machine model: one claim across 8 contenders, terminal suppression');
}
(async()=>{await baseline(); await claimModel();})().catch(e=>{console.error(e);process.exitCode=1;});
