# Noir #3078 — inline readOnly candidate (2026-10-17)

**CANDIDATE_NATIVE_VALIDATION_PENDING — NOT SUBMITTED.** This is a review document containing a patch, not a deployed fix. No fork, branch, PR, comment or upstream change was created.

## Scope and evidence

- Issue: https://github.com/owasp-noir/noir/issues/3078
- Maintainer scope: https://github.com/owasp-noir/noir/issues/3078#issuecomment-6228187553
- Base: `8372858c86e2ffd17123214641174f59f0a3828b`, rechecked at 2026-10-17T06:13:41Z.
- [OAS2 source](https://github.com/owasp-noir/noir/blob/8372858c86e2ffd17123214641174f59f0a3828b/src/analyzer/analyzers/specification/oas2.cr): blob `58061efad5f80055fc252d44807b90b8418681a2`.
- [OAS3 source](https://github.com/owasp-noir/noir/blob/8372858c86e2ffd17123214641174f59f0a3828b/src/analyzer/analyzers/specification/oas3.cr): blob `add09afd846d500fda4d19bec9e12d44b9be1e51`.
- Read root AGENTS.md, spec/AGENTS.md, .github/CONTRIBUTING.md, justfile, both analyzers, existing tests, SpecificationEngine and FunctionalTester. The full issue has two comments; no newer reply. Open PR collection has only unrelated #2244; search for PR #3078 found none.

The four property-emission loops discard the property value. The candidate retains it and skips only an explicitly boolean readOnly:true using guarded hash/boolean access. It leaves absent/false annotations and writeOnly fields in place. It mutates neither the shared schema nor its required list. Body collection uses the existing param_type for JSON and form.

This intentionally implements the maintainer-permitted inline first pass. Existing traversal still reaches inline properties inside root-referenced/composed object schemas. **Annotations hidden behind a property-level $ref or composition are not newly resolved.** Remote refs, cycle behavior and resolver policy are untouched. OAS2 form cases exercise Noir's existing consumes/body-schema mapping; they are not a claim that body-schema form input is standard OpenAPI 2 formData syntax.

## Regression design

Twenty functional cases: two versions × two encodings × five routes (JSON, URL-encoded form, multipart form, shared root schema, composed root schema). All compare the exact list of (name, param_type), because FunctionalTester only checks expected-field presence and would otherwise miss unwanted id/status fields.

Eight unit cases: two versions × two encodings × two output parameter types. They include true/false/missing/non-boolean flags, writeOnly, null/scalar property nodes followed by writable fields, required read-only id, repeated calls and a shared parsed-node snapshot.

**These 28 Crystal test cases were authored but NOT RUN.** They are not passing-test evidence.

## Actual local checks

```json
{
  "scope": "artifact and fixture validation only; no Crystal/Noir execution",
  "source_hashes_verified": 2,
  "fixtures_parsed": [
    "oas2/json",
    "oas2/yaml",
    "oas3/json",
    "oas3/yaml"
  ],
  "json_yaml_parity_pairs": 2,
  "patch_applies": true,
  "applied_files_match_candidate_and_manifest": 8,
  "whitespace_errors": 0,
  "native_tests_run": 0,
  "native_test_cases_prepared": 28
}
```

Commands executed: `python noir3078/prepare_candidate.py`, `python noir3078/check_artifact.py`, and `git apply --check` (the checker also uses --whitespace=error). The checker applied the patch only inside a disposable local temporary directory and compared all eight resulting files with their manifest. Source fetched via GitHub connector; no upstream binary or tool was executed.

Crystal, shards, just and Docker are unavailable. No compiler/toolchain was installed and no heavy build was attempted. AGENTS.md requires build/test/format before code commit, and the maintainer requests just test before submitting. Those gates remain pending; this document is not an upstream code commit or submission. No claim of RED/GREEN, syntax/type correctness, functional scan success, full-suite success or production repair.

## Native validation before any submission

On a suitable isolated checkout at the pinned SHA, first apply only the six new fixture/spec files and run the two new specs to observe the intended baseline failures. Then apply the two source hunks and repeat the same specs. Confirm failures concern read-only fields, not fixture/runtime problems. Run the existing OAS2/OAS3 functional tests as well, then the maintainer-required build, format check and `just test`. Retain actual output. Full-suite execution is pending a permitted environment and the user's light-work constraint; no server or Mac resources were used.

Proposed commands (NOT RUN here):

```sh
crystal spec spec/unit_test/analyzer/specification/oas_read_only_spec.cr
crystal spec spec/functional_test/testers/specification/oas_read_only_spec.cr
crystal spec spec/functional_test/testers/specification/oas2_spec.cr spec/functional_test/testers/specification/oas3_spec.cr
just build
crystal tool format --check src/analyzer/analyzers/specification/oas2.cr src/analyzer/analyzers/specification/oas3.cr spec/unit_test/analyzer/specification/oas_read_only_spec.cr spec/functional_test/testers/specification/oas_read_only_spec.cr
just test
```

## Review-only PR description

Title: fix(oas): omit inline read-only properties from request parameters

Shared request/response schemas currently expose inline readOnly:true fields as request inputs. This patch filters those fields in all four OAS2/OAS3 JSON/YAML property collectors, including the existing form-body paths. Writable fields and shared schema contents stay unchanged.

The regression specs assert exact parameter lists for JSON/form input, encoding/version parity, required read-only fields, shared/composed root schemas, and malformed property metadata without losing later writable fields. Property-level reference/composition annotation resolution is deferred to a separate change, as discussed in #3078.

Validation: patch application, fixture parsing/parity and file hashes checked locally. Crystal compilation, regression execution, format check and just test are still pending. Do not submit this draft as a tested fix.

## Eight-file manifest

```json
[
  {
    "path": "src/analyzer/analyzers/specification/oas2.cr",
    "sha256": "af480515add836b25ad5f58fa8cea309a879642a3cfc5a18570f16dec678a760",
    "new_file": false
  },
  {
    "path": "src/analyzer/analyzers/specification/oas3.cr",
    "sha256": "914600c62cc7ccadbb9c40f5d9e30945ae2c493154ebf13ad2673692005e894f",
    "new_file": false
  },
  {
    "path": "spec/functional_test/fixtures/specification/oas2_read_only/json/doc.json",
    "sha256": "929ebb1d630e2d45b1ca1edcf2e95ed49a15029706013b1720e6bf3be0f0d4bd",
    "new_file": true
  },
  {
    "path": "spec/functional_test/fixtures/specification/oas2_read_only/yaml/doc.yaml",
    "sha256": "c86d0a7c485ee2ba7335e7929615bad77292045bfab1f61503524d99a89cfccf",
    "new_file": true
  },
  {
    "path": "spec/functional_test/fixtures/specification/oas3_read_only/json/doc.json",
    "sha256": "41aba3b1d0bb3b3392667a1db55bf27626cefe78c106769049b9bfc9b72a64a9",
    "new_file": true
  },
  {
    "path": "spec/functional_test/fixtures/specification/oas3_read_only/yaml/doc.yaml",
    "sha256": "cc3c9d1c08b0b877b5daee043acfaf5902f34959f71768da3db57bf82ea2e440",
    "new_file": true
  },
  {
    "path": "spec/functional_test/testers/specification/oas_read_only_spec.cr",
    "sha256": "cb373b2a51ccdb525090324116d41aca42e238466606a9af4c96d2c366b32633",
    "new_file": true
  },
  {
    "path": "spec/unit_test/analyzer/specification/oas_read_only_spec.cr",
    "sha256": "5364277ece94473cf25cb93036b2b8f94f4289924ef441684de4d037abf884f8",
    "new_file": true
  }
]
```

## Complete candidate patch

Save this block as `noir3078-inline.patch` for review in an isolated checkout. It changes only two analyzer files and adds six test/fixture files; no CI changes.

```diff
--- a/src/analyzer/analyzers/specification/oas2.cr
+++ b/src/analyzer/analyzers/specification/oas2.cr
@@ -25,7 +25,8 @@
       end
 
       if props = schema["properties"]?.try(&.as_h?)
-        props.each do |name, _|
+        props.each do |name, property|
+          next if property.as_h?.try(&.["readOnly"]?).try(&.as_bool?) == true
           add_param(params, name.to_s, param_type)
         end
       end
@@ -62,7 +63,8 @@
 
       if props_node = schema[YAML::Any.new("properties")]?
         if props = props_node.as_h?
-          props.each do |name, _|
+          props.each do |name, property|
+            next if property.as_h?.try(&.[YAML::Any.new("readOnly")]?).try(&.as_bool?) == true
             add_param(params, name.to_s, param_type)
           end
         end
--- a/src/analyzer/analyzers/specification/oas3.cr
+++ b/src/analyzer/analyzers/specification/oas3.cr
@@ -82,7 +82,8 @@
       end
 
       if props = schema["properties"]?.try(&.as_h?)
-        props.each do |name, _|
+        props.each do |name, property|
+          next if property.as_h?.try(&.["readOnly"]?).try(&.as_bool?) == true
           add_param(params, name.to_s, param_type)
         end
       end
@@ -121,7 +122,8 @@
 
       if props_node = schema[YAML::Any.new("properties")]?
         if props = props_node.as_h?
-          props.each do |name, _|
+          props.each do |name, property|
+            next if property.as_h?.try(&.[YAML::Any.new("readOnly")]?).try(&.as_bool?) == true
             add_param(params, name.to_s, param_type)
           end
         end
--- /dev/null
+++ b/spec/functional_test/fixtures/specification/oas2_read_only/json/doc.json
@@ -0,0 +1,239 @@
+{
+  "swagger": "2.0",
+  "info": {
+    "title": "OAS2 inline readOnly regression",
+    "version": "1.0.0"
+  },
+  "paths": {
+    "/inline-json": {
+      "post": {
+        "responses": {
+          "200": {
+            "description": "ok",
+            "schema": {
+              "$ref": "#/definitions/Shared"
+            }
+          }
+        },
+        "consumes": [
+          "application/json"
+        ],
+        "parameters": [
+          {
+            "name": "body",
+            "in": "body",
+            "required": true,
+            "schema": {
+              "type": "object",
+              "required": [
+                "id",
+                "name"
+              ],
+              "properties": {
+                "id": {
+                  "type": "string",
+                  "readOnly": true
+                },
+                "name": {
+                  "type": "string"
+                },
+                "editable": {
+                  "type": "string",
+                  "readOnly": false
+                },
+                "password": {
+                  "type": "string",
+                  "writeOnly": true
+                }
+              }
+            }
+          }
+        ]
+      }
+    },
+    "/inline-urlencoded": {
+      "post": {
+        "responses": {
+          "200": {
+            "description": "ok",
+            "schema": {
+              "$ref": "#/definitions/Shared"
+            }
+          }
+        },
+        "consumes": [
+          "application/x-www-form-urlencoded"
+        ],
+        "parameters": [
+          {
+            "name": "body",
+            "in": "body",
+            "required": true,
+            "schema": {
+              "type": "object",
+              "required": [
+                "id",
+                "name"
+              ],
+              "properties": {
+                "id": {
+                  "type": "string",
+                  "readOnly": true
+                },
+                "name": {
+                  "type": "string"
+                },
+                "editable": {
+                  "type": "string",
+                  "readOnly": false
+                },
+                "password": {
+                  "type": "string",
+                  "writeOnly": true
+                }
+              }
+            }
+          }
+        ]
+      }
+    },
+    "/inline-multipart": {
+      "post": {
+        "responses": {
+          "200": {
+            "description": "ok",
+            "schema": {
+              "$ref": "#/definitions/Shared"
+            }
+          }
+        },
+        "consumes": [
+          "multipart/form-data"
+        ],
+        "parameters": [
+          {
+            "name": "body",
+            "in": "body",
+            "required": true,
+            "schema": {
+              "type": "object",
+              "required": [
+                "id",
+                "name"
+              ],
+              "properties": {
+                "id": {
+                  "type": "string",
+                  "readOnly": true
+                },
+                "name": {
+                  "type": "string"
+                },
+                "editable": {
+                  "type": "string",
+                  "readOnly": false
+                },
+                "password": {
+                  "type": "string",
+                  "writeOnly": true
+                }
+              }
+            }
+          }
+        ]
+      }
+    },
+    "/shared": {
+      "post": {
+        "responses": {
+          "200": {
+            "description": "ok",
+            "schema": {
+              "$ref": "#/definitions/Shared"
+            }
+          }
+        },
+        "consumes": [
+          "application/json"
+        ],
+        "parameters": [
+          {
+            "name": "body",
+            "in": "body",
+            "required": true,
+            "schema": {
+              "$ref": "#/definitions/Shared"
+            }
+          }
+        ]
+      }
+    },
+    "/composed": {
+      "post": {
+        "responses": {
+          "200": {
+            "description": "ok",
+            "schema": {
+              "$ref": "#/definitions/Shared"
+            }
+          }
+        },
+        "consumes": [
+          "application/json"
+        ],
+        "parameters": [
+          {
+            "name": "body",
+            "in": "body",
+            "required": true,
+            "schema": {
+              "allOf": [
+                {
+                  "$ref": "#/definitions/Shared"
+                },
+                {
+                  "type": "object",
+                  "properties": {
+                    "status": {
+                      "type": "string",
+                      "readOnly": true
+                    },
+                    "note": {
+                      "type": "string"
+                    }
+                  }
+                }
+              ]
+            }
+          }
+        ]
+      }
+    }
+  },
+  "definitions": {
+    "Shared": {
+      "type": "object",
+      "required": [
+        "id",
+        "name"
+      ],
+      "properties": {
+        "id": {
+          "type": "string",
+          "readOnly": true
+        },
+        "name": {
+          "type": "string"
+        },
+        "editable": {
+          "type": "string",
+          "readOnly": false
+        },
+        "password": {
+          "type": "string",
+          "writeOnly": true
+        }
+      }
+    }
+  }
+}
--- /dev/null
+++ b/spec/functional_test/fixtures/specification/oas2_read_only/yaml/doc.yaml
@@ -0,0 +1,151 @@
+swagger: '2.0'
+info:
+  title: OAS2 inline readOnly regression
+  version: 1.0.0
+paths:
+  /inline-json:
+    post:
+      responses:
+        '200':
+          description: ok
+          schema:
+            $ref: '#/definitions/Shared'
+      consumes:
+      - application/json
+      parameters:
+      - name: body
+        in: body
+        required: true
+        schema:
+          type: object
+          required:
+          - id
+          - name
+          properties:
+            id:
+              type: string
+              readOnly: true
+            name:
+              type: string
+            editable:
+              type: string
+              readOnly: false
+            password:
+              type: string
+              writeOnly: true
+  /inline-urlencoded:
+    post:
+      responses:
+        '200':
+          description: ok
+          schema:
+            $ref: '#/definitions/Shared'
+      consumes:
+      - application/x-www-form-urlencoded
+      parameters:
+      - name: body
+        in: body
+        required: true
+        schema:
+          type: object
+          required:
+          - id
+          - name
+          properties:
+            id:
+              type: string
+              readOnly: true
+            name:
+              type: string
+            editable:
+              type: string
+              readOnly: false
+            password:
+              type: string
+              writeOnly: true
+  /inline-multipart:
+    post:
+      responses:
+        '200':
+          description: ok
+          schema:
+            $ref: '#/definitions/Shared'
+      consumes:
+      - multipart/form-data
+      parameters:
+      - name: body
+        in: body
+        required: true
+        schema:
+          type: object
+          required:
+          - id
+          - name
+          properties:
+            id:
+              type: string
+              readOnly: true
+            name:
+              type: string
+            editable:
+              type: string
+              readOnly: false
+            password:
+              type: string
+              writeOnly: true
+  /shared:
+    post:
+      responses:
+        '200':
+          description: ok
+          schema:
+            $ref: '#/definitions/Shared'
+      consumes:
+      - application/json
+      parameters:
+      - name: body
+        in: body
+        required: true
+        schema:
+          $ref: '#/definitions/Shared'
+  /composed:
+    post:
+      responses:
+        '200':
+          description: ok
+          schema:
+            $ref: '#/definitions/Shared'
+      consumes:
+      - application/json
+      parameters:
+      - name: body
+        in: body
+        required: true
+        schema:
+          allOf:
+          - $ref: '#/definitions/Shared'
+          - type: object
+            properties:
+              status:
+                type: string
+                readOnly: true
+              note:
+                type: string
+definitions:
+  Shared:
+    type: object
+    required:
+    - id
+    - name
+    properties:
+      id:
+        type: string
+        readOnly: true
+      name:
+        type: string
+      editable:
+        type: string
+        readOnly: false
+      password:
+        type: string
+        writeOnly: true
--- /dev/null
+++ b/spec/functional_test/fixtures/specification/oas3_read_only/json/doc.json
@@ -0,0 +1,246 @@
+{
+  "openapi": "3.0.3",
+  "info": {
+    "title": "OAS3 inline readOnly regression",
+    "version": "1.0.0"
+  },
+  "paths": {
+    "/inline-json": {
+      "post": {
+        "responses": {
+          "200": {
+            "description": "ok",
+            "content": {
+              "application/json": {
+                "schema": {
+                  "$ref": "#/components/schemas/Shared"
+                }
+              }
+            }
+          }
+        },
+        "requestBody": {
+          "required": true,
+          "content": {
+            "application/json": {
+              "schema": {
+                "type": "object",
+                "required": [
+                  "id",
+                  "name"
+                ],
+                "properties": {
+                  "id": {
+                    "type": "string",
+                    "readOnly": true
+                  },
+                  "name": {
+                    "type": "string"
+                  },
+                  "editable": {
+                    "type": "string",
+                    "readOnly": false
+                  },
+                  "password": {
+                    "type": "string",
+                    "writeOnly": true
+                  }
+                }
+              }
+            }
+          }
+        }
+      }
+    },
+    "/inline-urlencoded": {
+      "post": {
+        "responses": {
+          "200": {
+            "description": "ok",
+            "content": {
+              "application/json": {
+                "schema": {
+                  "$ref": "#/components/schemas/Shared"
+                }
+              }
+            }
+          }
+        },
+        "requestBody": {
+          "required": true,
+          "content": {
+            "application/x-www-form-urlencoded": {
+              "schema": {
+                "type": "object",
+                "required": [
+                  "id",
+                  "name"
+                ],
+                "properties": {
+                  "id": {
+                    "type": "string",
+                    "readOnly": true
+                  },
+                  "name": {
+                    "type": "string"
+                  },
+                  "editable": {
+                    "type": "string",
+                    "readOnly": false
+                  },
+                  "password": {
+                    "type": "string",
+                    "writeOnly": true
+                  }
+                }
+              }
+            }
+          }
+        }
+      }
+    },
+    "/inline-multipart": {
+      "post": {
+        "responses": {
+          "200": {
+            "description": "ok",
+            "content": {
+              "application/json": {
+                "schema": {
+                  "$ref": "#/components/schemas/Shared"
+                }
+              }
+            }
+          }
+        },
+        "requestBody": {
+          "required": true,
+          "content": {
+            "multipart/form-data": {
+              "schema": {
+                "type": "object",
+                "required": [
+                  "id",
+                  "name"
+                ],
+                "properties": {
+                  "id": {
+                    "type": "string",
+                    "readOnly": true
+                  },
+                  "name": {
+                    "type": "string"
+                  },
+                  "editable": {
+                    "type": "string",
+                    "readOnly": false
+                  },
+                  "password": {
+                    "type": "string",
+                    "writeOnly": true
+                  }
+                }
+              }
+            }
+          }
+        }
+      }
+    },
+    "/shared": {
+      "post": {
+        "responses": {
+          "200": {
+            "description": "ok",
+            "content": {
+              "application/json": {
+                "schema": {
+                  "$ref": "#/components/schemas/Shared"
+                }
+              }
+            }
+          }
+        },
+        "requestBody": {
+          "required": true,
+          "content": {
+            "application/json": {
+              "schema": {
+                "$ref": "#/components/schemas/Shared"
+              }
+            }
+          }
+        }
+      }
+    },
+    "/composed": {
+      "post": {
+        "responses": {
+          "200": {
+            "description": "ok",
+            "content": {
+              "application/json": {
+                "schema": {
+                  "$ref": "#/components/schemas/Shared"
+                }
+              }
+            }
+          }
+        },
+        "requestBody": {
+          "required": true,
+          "content": {
+            "application/json": {
+              "schema": {
+                "allOf": [
+                  {
+                    "$ref": "#/components/schemas/Shared"
+                  },
+                  {
+                    "type": "object",
+                    "properties": {
+                      "status": {
+                        "type": "string",
+                        "readOnly": true
+                      },
+                      "note": {
+                        "type": "string"
+                      }
+                    }
+                  }
+                ]
+              }
+            }
+          }
+        }
+      }
+    }
+  },
+  "components": {
+    "schemas": {
+      "Shared": {
+        "type": "object",
+        "required": [
+          "id",
+          "name"
+        ],
+        "properties": {
+          "id": {
+            "type": "string",
+            "readOnly": true
+          },
+          "name": {
+            "type": "string"
+          },
+          "editable": {
+            "type": "string",
+            "readOnly": false
+          },
+          "password": {
+            "type": "string",
+            "writeOnly": true
+          }
+        }
+      }
+    }
+  }
+}
--- /dev/null
+++ b/spec/functional_test/fixtures/specification/oas3_read_only/yaml/doc.yaml
@@ -0,0 +1,152 @@
+openapi: 3.0.3
+info:
+  title: OAS3 inline readOnly regression
+  version: 1.0.0
+paths:
+  /inline-json:
+    post:
+      responses:
+        '200':
+          description: ok
+          content:
+            application/json:
+              schema:
+                $ref: '#/components/schemas/Shared'
+      requestBody:
+        required: true
+        content:
+          application/json:
+            schema:
+              type: object
+              required:
+              - id
+              - name
+              properties:
+                id:
+                  type: string
+                  readOnly: true
+                name:
+                  type: string
+                editable:
+                  type: string
+                  readOnly: false
+                password:
+                  type: string
+                  writeOnly: true
+  /inline-urlencoded:
+    post:
+      responses:
+        '200':
+          description: ok
+          content:
+            application/json:
+              schema:
+                $ref: '#/components/schemas/Shared'
+      requestBody:
+        required: true
+        content:
+          application/x-www-form-urlencoded:
+            schema:
+              type: object
+              required:
+              - id
+              - name
+              properties:
+                id:
+                  type: string
+                  readOnly: true
+                name:
+                  type: string
+                editable:
+                  type: string
+                  readOnly: false
+                password:
+                  type: string
+                  writeOnly: true
+  /inline-multipart:
+    post:
+      responses:
+        '200':
+          description: ok
+          content:
+            application/json:
+              schema:
+                $ref: '#/components/schemas/Shared'
+      requestBody:
+        required: true
+        content:
+          multipart/form-data:
+            schema:
+              type: object
+              required:
+              - id
+              - name
+              properties:
+                id:
+                  type: string
+                  readOnly: true
+                name:
+                  type: string
+                editable:
+                  type: string
+                  readOnly: false
+                password:
+                  type: string
+                  writeOnly: true
+  /shared:
+    post:
+      responses:
+        '200':
+          description: ok
+          content:
+            application/json:
+              schema:
+                $ref: '#/components/schemas/Shared'
+      requestBody:
+        required: true
+        content:
+          application/json:
+            schema:
+              $ref: '#/components/schemas/Shared'
+  /composed:
+    post:
+      responses:
+        '200':
+          description: ok
+          content:
+            application/json:
+              schema:
+                $ref: '#/components/schemas/Shared'
+      requestBody:
+        required: true
+        content:
+          application/json:
+            schema:
+              allOf:
+              - $ref: '#/components/schemas/Shared'
+              - type: object
+                properties:
+                  status:
+                    type: string
+                    readOnly: true
+                  note:
+                    type: string
+components:
+  schemas:
+    Shared:
+      type: object
+      required:
+      - id
+      - name
+      properties:
+        id:
+          type: string
+          readOnly: true
+        name:
+          type: string
+        editable:
+          type: string
+          readOnly: false
+        password:
+          type: string
+          writeOnly: true
--- /dev/null
+++ b/spec/functional_test/testers/specification/oas_read_only_spec.cr
@@ -0,0 +1,32 @@
+require "../../func_spec.cr"
+
+# Exact parameter lists matter here: FunctionalTester checks expected fields
+# but does not reject unexpected fields such as the response-only id.
+["oas2", "oas3"].each do |version|
+  ["json", "yaml"].each do |format|
+    tester = FunctionalTester.new("fixtures/specification/#{version}_read_only/#{format}/", {
+      :techs     => 1,
+      :endpoints => 5,
+    }, nil)
+
+    describe "#{version} #{format} inline readOnly request fields", tags: "functional" do
+      {
+        "/inline-json"       => "json",
+        "/inline-urlencoded" => "form",
+        "/inline-multipart"  => "form",
+        "/shared"            => "json",
+        "/composed"          => "json",
+      }.each do |path, param_type|
+        it "omits response-only fields at #{path} without dropping writable fields" do
+          tester.endpoints.size.should eq(5)
+          endpoint = tester.endpoints.find { |e| e.url == path && e.method == "POST" }.not_nil!
+          names = ["name", "editable", "password"]
+          names << "note" if path == "/composed"
+          endpoint.params.map { |p| {p.name, p.param_type} }.sort.should eq(
+            names.map { |name| {name, param_type} }.sort
+          )
+        end
+      end
+    end
+  end
+end
--- /dev/null
+++ b/spec/unit_test/analyzer/specification/oas_read_only_spec.cr
@@ -0,0 +1,107 @@
+require "../../../spec_helper"
+require "../../../../src/analyzer/analyzers/specification/oas2"
+require "../../../../src/analyzer/analyzers/specification/oas3"
+
+# Test-only entrypoints keep shared parsed nodes observable across collection.
+
+class Analyzer::Specification::Oas2
+  def read_only_regression_params(root : JSON::Any, param_type : String)
+    params = [] of Param
+    doc = Analyzer::Specification::SpecDoc.new(root, "fixture.json")
+    collect_body_props_json(doc, root, param_type, params)
+    params
+  end
+
+  def read_only_regression_params(root : YAML::Any, param_type : String)
+    params = [] of Param
+    doc = Analyzer::Specification::SpecDoc.new(root, "fixture.yaml")
+    collect_body_props_yaml(doc, root, param_type, params)
+    params
+  end
+
+end
+
+class Analyzer::Specification::Oas3
+  def read_only_regression_params(root : JSON::Any, param_type : String)
+    params = [] of Param
+    doc = Analyzer::Specification::SpecDoc.new(root, "fixture.json")
+    collect_schema_props_json(doc, root, param_type, params)
+    params
+  end
+
+  def read_only_regression_params(root : YAML::Any, param_type : String)
+    params = [] of Param
+    doc = Analyzer::Specification::SpecDoc.new(root, "fixture.yaml")
+    collect_schema_props_yaml(doc, root, param_type, params)
+    params
+  end
+
+end
+
+describe "OpenAPI inline readOnly collection" do
+  # Malformed/non-object schemas retain previous behavior; they must not
+  # abort the loop and erase writable properties that occur after them.
+  fixture = %({"type":"object","required":["id","name"],"properties":{"id":{"type":"string","readOnly":true},"nullable":null,"scalar":7,"boolean":false,"string_flag":{"readOnly":"true"},"number_flag":{"readOnly":1},"null_flag":{"readOnly":null},"editable":{"readOnly":false},"password":{"writeOnly":true},"name":{"type":"string"}}})
+  expected = ["nullable", "scalar", "boolean", "string_flag", "number_flag", "null_flag", "editable", "password", "name"].sort
+
+  ["json", "form"].each do |param_type|
+    it "OAS2 JSON filters only boolean true for #{param_type} and preserves the shared node" do
+      root = JSON.parse(fixture)
+      before = root.to_json
+      analyzer = Analyzer::Specification::Oas2.new(create_test_options)
+
+      2.times do
+        params = analyzer.read_only_regression_params(root, param_type)
+        params.map(&.name).sort.should eq(expected)
+        params.all? { |p| p.param_type == param_type }.should be_true
+        root.to_json.should eq(before)
+      end
+    end
+  end
+
+  ["json", "form"].each do |param_type|
+    it "OAS2 YAML filters only boolean true for #{param_type} and preserves the shared node" do
+      root = YAML.parse(fixture)
+      before = root.to_json
+      analyzer = Analyzer::Specification::Oas2.new(create_test_options)
+
+      2.times do
+        params = analyzer.read_only_regression_params(root, param_type)
+        params.map(&.name).sort.should eq(expected)
+        params.all? { |p| p.param_type == param_type }.should be_true
+        root.to_json.should eq(before)
+      end
+    end
+  end
+
+  ["json", "form"].each do |param_type|
+    it "OAS3 JSON filters only boolean true for #{param_type} and preserves the shared node" do
+      root = JSON.parse(fixture)
+      before = root.to_json
+      analyzer = Analyzer::Specification::Oas3.new(create_test_options)
+
+      2.times do
+        params = analyzer.read_only_regression_params(root, param_type)
+        params.map(&.name).sort.should eq(expected)
+        params.all? { |p| p.param_type == param_type }.should be_true
+        root.to_json.should eq(before)
+      end
+    end
+  end
+
+  ["json", "form"].each do |param_type|
+    it "OAS3 YAML filters only boolean true for #{param_type} and preserves the shared node" do
+      root = YAML.parse(fixture)
+      before = root.to_json
+      analyzer = Analyzer::Specification::Oas3.new(create_test_options)
+
+      2.times do
+        params = analyzer.read_only_regression_params(root, param_type)
+        params.map(&.name).sort.should eq(expected)
+        params.all? { |p| p.param_type == param_type }.should be_true
+        root.to_json.should eq(before)
+      end
+    end
+  end
+
+end
```

## Reproduce artifact checks only

This verifier uses Python, PyYAML and git; it does not compile Crystal. In a disposable directory, save the patch and manifest blocks above as `noir3078-inline.patch` and `manifest.json`. Copy the two analyzer files from the pinned upstream commit under `base/`, preserving their source paths and exact bytes. Copy `base/` to `candidate/`, then apply the patch inside `candidate/`. Save the following as `check_artifact.py` alongside those directories and run `python check_artifact.py`. No new package installation was performed in this run.

```python
"""Validate patch/fixture packaging only. Does NOT execute Crystal or Noir."""
from pathlib import Path
import hashlib, json, shutil, subprocess, tempfile
import yaml

root = Path(__file__).parent
source_count = 0
sources = [
    {'path': 'src/analyzer/analyzers/specification/oas2.cr', 'sha': '58061efad5f80055fc252d44807b90b8418681a2'},
    {'path': 'src/analyzer/analyzers/specification/oas3.cr', 'sha': 'add09afd846d500fda4d19bec9e12d44b9be1e51'},
]
for source in sources:
    raw = (root / 'base' / source['path']).read_bytes()
    assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == source['sha']
    source_count += 1

fixtures = []
for version in (2, 3):
    folder = root / 'candidate/spec/functional_test/fixtures/specification' / f'oas{version}_read_only'
    json_doc = json.loads((folder / 'json/doc.json').read_text())
    yaml_doc = yaml.safe_load((folder / 'yaml/doc.yaml').read_text())
    assert json_doc == yaml_doc
    for fmt, document in [('json', json_doc), ('yaml', yaml_doc)]:
        assert set(document['paths']) == {'/inline-json', '/inline-urlencoded', '/inline-multipart', '/shared', '/composed'}
        for route in ('/inline-json', '/inline-urlencoded', '/inline-multipart'):
            operation = document['paths'][route]['post']
            if version == 2:
                schema = operation['parameters'][0]['schema']
            else:
                schema = next(iter(operation['requestBody']['content'].values()))['schema']
            assert schema['properties']['id']['readOnly'] is True
            assert schema['properties']['editable']['readOnly'] is False
            assert 'readOnly' not in schema['properties']['name']
            assert schema['properties']['password']['writeOnly'] is True
            assert schema['required'] == ['id', 'name']
        fixtures.append(f'oas{version}/{fmt}')

subprocess.run(['git', 'apply', '--check', '--whitespace=error', '../noir3078-inline.patch'], cwd=root / 'base', check=True)
manifest = json.loads((root / 'manifest.json').read_text())
with tempfile.TemporaryDirectory(prefix='noir3078_patch_') as directory:
    target = Path(directory)
    for source in sources:
        destination = target / source['path']
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / 'base' / source['path'], destination)
    subprocess.run(['git', 'apply', str((root / 'noir3078-inline.patch').resolve())], cwd=target, check=True)
    for item in manifest:
        raw = (target / item['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == item['sha256']
        assert raw == (root / 'candidate' / item['path']).read_bytes()
result = {'scope': 'artifact and fixture validation only; no Crystal/Noir execution', 'source_hashes_verified': source_count, 'fixtures_parsed': fixtures, 'json_yaml_parity_pairs': 2, 'patch_applies': True, 'applied_files_match_candidate_and_manifest': len(manifest), 'whitespace_errors': 0, 'native_tests_run': 0, 'native_test_cases_prepared': 28}
(root / 'artifact-check-results.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
```
