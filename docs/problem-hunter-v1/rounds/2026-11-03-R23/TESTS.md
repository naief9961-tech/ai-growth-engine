# R23 isolated evidence

The following harness was run with Node on synthetic inputs. Output columns: JavaScript UTF-16 units, code points, UTF-8 bytes. Output: 10000 9999 10002; 10001 10000 10003. Exit 0. AJV stub counts calls; not a real schema compilation, deployment or SDK request.

```ts
import assert from 'node:assert/strict';
type AnySchema=unknown;
let compiled=0;const createAjvInstanceInternal=()=>({compile(_s:unknown){compiled++}});
export const MAX_JSON_SCHEMA_CHARACTERS = 10_000;
export const JSON_SCHEMA_SIZE_ERROR = `Schema exceeds the ${MAX_JSON_SCHEMA_CHARACTERS.toLocaleString("en-US")}-character limit`;
export const INVALID_JSON_SCHEMA_ERROR = "Must be a valid JSON Schema";

export function getJSONSchemaValidationError(schema: unknown): string | null {
  try {
    const stringified = JSON.stringify(schema);
    if (stringified.length > MAX_JSON_SCHEMA_CHARACTERS) {
      return JSON_SCHEMA_SIZE_ERROR;
    }

    const ajv = createAjvInstanceInternal();
    // This will throw an error if the schema is invalid
    ajv.compile(schema as AnySchema);

    return null;
  } catch {
    return INVALID_JSON_SCHEMA_ERROR;
  }
}
const schema={type:'string',description:''};schema.description='a'.repeat(10000-JSON.stringify(schema).length-2);
for(const [suffix,expected,shouldCompile] of [['😀',null,true],['😀a',JSON_SCHEMA_SIZE_ERROR,false]] as const){
 const x={...schema,description:schema.description+suffix};const serialized=JSON.stringify(x),before=compiled;
 assert.equal(getJSONSchemaValidationError(x),expected);assert.equal(compiled-before,Number(shouldCompile));
 console.log(serialized.length,[...serialized].length,Buffer.byteLength(serialized));}

```

PriceStalker: repeated the six R21 vectors using the actual UI helpers and provider at merge 33c8e3e2ccb7093efb8a5477d27921652f9e8dfd, no predicate replacement. Same fake axios.post, logger and literal interpolation fixture as R21; checked UI/provider agreement, send count and payload shape. Node --experimental-transform-types: 6 cases, zero wrong. No upstream suite or real delivery.
