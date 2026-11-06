# R26 isolated verification
Runtime: Node v24.22.1. All runs exited 0. No external package install, network, secrets or live writes.

## Backlog.md
Save the unchanged [tagged validators.ts](https://github.com/MrLesk/Backlog.md/blob/0cf4fdbc70020327f4366a29d3f405f83d180301/src/mcp/validation/validators.ts) as r26-validators.mts. Blob: 8c8427578231f1cbd3378f2baecddac03ea191ea. Run this harness with `node r26-backlog-check.mts`. The field property was extracted unchanged from the same tag's schema-generators.ts; the outer object is a test fixture, not the full generated schema.

```ts
import assert from 'node:assert/strict';
import {validateInput} from './r26-validators.mts';
const schema={type:'object',properties:{acceptanceCriteriaSet: {
				type: "array",
				description:
					"Replace all acceptance criteria. Matching trimmed text keeps its check state, even after reordering; duplicate texts match old entries in order, once each. New or reworded entries start unchecked, and omitted entries are removed.",
				items: {
					type: "string",
					maxLength: 500,
				},
				maxItems: 50,
			}},additionalProperties:false};
for(const n of [441,500,501,520]){
 const input={acceptanceCriteriaSet:['x'.repeat(n)]};
 const before=JSON.stringify(input);
 const result=validateInput(input,schema);
 assert.equal(result.isValid,n<=500);
 assert.equal(JSON.stringify(input),before);
 if(n<=500) assert.deepEqual(result.sanitizedData,input);
 else {assert.equal(result.sanitizedData,undefined);assert.match(result.errors[0],/acceptanceCriteriaSet\[0\]/);}
 console.log(JSON.stringify({n,...result}));
}
const mixed=validateInput({acceptanceCriteriaSet:['valid','x'.repeat(520)]},schema);
assert.equal(mixed.isValid,false);
assert.equal(mixed.sanitizedData,undefined);
assert.match(mixed.errors[0],/acceptanceCriteriaSet\[1\]/);
console.log('mixed batch rejected; no partial sanitizedData; 5 case groups PASS');


```

Observed: 441/500 accepted unchanged; 501/520 rejected, no sanitizedData; mixed batch rejected with index 1. Five groups. No input mutation. Wrapper/handler, transport, binary, Bun and persistence untested.

## Hatchet
Pinned source extraction: commit 00d4dd2afa601324cf7d219ff04d063509e47419, use-webhooks.tsx blob bf5296e557666d517cf9d26c9199e4067b9ae848. Baseline function unchanged; candidate changes hostname to host and erases its TypeScript annotation for new Function. Run with `node r26-url-check.mts`.

```ts
import assert from 'node:assert/strict';
// Unchanged function extracted from pinned use-webhooks.tsx.
function factory(tenant: any, tenantId: string, window: any) {
  const createWebhookURL = (name: string) => {
    const suffix = `/api/v1/stable/tenants/${tenantId}/webhooks/${name}`;

    // if the tenant has a serverUrl defined, use that to construct the webhook URL. Otherwise, fall back to using the current window location
    if (tenant?.serverUrl) {
      return `${tenant.serverUrl}${suffix}`;
    }

    return `${window.location.protocol}//${window.location.hostname}${suffix}`;
  };
return createWebhookURL;
}
const fixed = new Function('tenant','tenantId','window', "  const createWebhookURL = (name) => {\n    const suffix = `/api/v1/stable/tenants/${tenantId}/webhooks/${name}`;\n\n    // if the tenant has a serverUrl defined, use that to construct the webhook URL. Otherwise, fall back to using the current window location\n    if (tenant?.serverUrl) {\n      return `${tenant.serverUrl}${suffix}`;\n    }\n\n    return `${window.location.protocol}//${window.location.host}${suffix}`;\n  };\nreturn createWebhookURL;");
const suffix='/api/v1/stable/tenants/tenant-test/webhooks/hook-test';
const cases=[
 ['http://localhost:8080/settings',undefined,'http://localhost:8080',true],
 ['https://example.invalid:8443/settings',undefined,'https://example.invalid:8443',true],
 ['http://[::1]:8080/settings',undefined,'http://[::1]:8080',true],
 ['https://example.invalid/settings',undefined,'https://example.invalid',false],
 ['http://example.invalid:80/settings',undefined,'http://example.invalid',false],
 ['http://localhost:8080/settings',{serverUrl:'https://api.example.invalid:9443'},'https://api.example.invalid:9443',false],
 ['http://localhost:8080/settings',{serverUrl:''},'http://localhost:8080',true],
] as const;
for (const [url,tenant,expected,broken] of cases) {
 const window={location:new URL(url)};
 const baseline=factory(tenant,'tenant-test',window)('hook-test');
 const candidate=fixed(tenant,'tenant-test',window)('hook-test');
 assert.equal(baseline===expected+suffix,!broken);
 assert.equal(candidate,expected+suffix);
 console.log(JSON.stringify({url,baseline,candidate,baselinePortLoss:broken,status:'PASS'}));
}
console.log('7 case groups passed; 4 baseline port-loss reproductions; no network or React mount.');


```

Seven groups: HTTP :8080, HTTPS :8443, IPv6 :8080 and empty serverUrl reproduced baseline port loss; normal HTTPS, default HTTP port and explicit tenant.serverUrl are controls. Candidate satisfies all seven. This is URL construction only: no React mounting, real tenant data, webhook delivery, browser or upstream suite. The fix is already suggested publicly; no new draft.
