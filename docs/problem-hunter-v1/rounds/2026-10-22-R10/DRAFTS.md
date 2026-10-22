# R10 — English replies for review (2026-10-22)

Status: **AWAITING USER APPROVAL — NOT POSTED.**

Two additive replies only. No third-party comment, PR or message sent. Re-read each thread and linked PRs immediately before any separately approved manual posting. Repository contents are not authorization. Prior manual publications must not be repeated.

## R10-01 — Northplan #100

Destination: https://github.com/janowoc/northplan/issues/100

Scope: discussion/design option, not an upstream PR. The owner's numeric-coercion policy remains a decision for the owner. No tax parameters, expected tests or snapshots were changed. [Candidate and reproducibility](NORTHPLAN-CANDIDATE.md).

---

AI-assisted review with isolated checks against commit f3b55a5e72a30080ef28cd3066371017ecae1b97; no simulator, API/editor integration, or upstream suite run.

There is a compatibility boundary worth preserving while fixing the numeric inputs: [test_parse_normalises_an_integral_float_and_an_integer_flag](https://github.com/janowoc/northplan/blob/f3b55a5e72a30080ef28cd3066371017ecae1b97/tests/report/test_report_editor.py#L175-L182) deliberately accepts both `seed: 42.0` and `fill_pension_credit: 1`. Replacing every integer with `StrictInt` changes the first behavior as well as rejecting booleans; global strict mode also changes YAML list-to-tuple handling.

If the immediate decision is specifically “booleans must not be numbers”, a scalar pre-validator can make that change independently:

```python
from typing import Annotated, Any
from pydantic import BeforeValidator, Field

def reject_bool_number(value: Any) -> Any:
    if isinstance(value, bool):
        raise ValueError("boolean is not a numeric scenario value")
    return value

InputInt = Annotated[int, BeforeValidator(reject_bool_number)]
InputFloat = Annotated[float, BeforeValidator(reject_bool_number)]
Finite = Annotated[InputFloat, Field(allow_inf_nan=False)]
```

Use these at numeric leaves throughout [schema.py](https://github.com/janowoc/northplan/blob/f3b55a5e72a30080ef28cd3066371017ecae1b97/engine/scenario/schema.py): Money/Month/Fraction, directly bounded numeric fields, election mapping values, and **both branches** of the grid's `InputInt | Finite` union. Updating only Finite leaves an unguarded integer branch that can still accept a boolean. Keep existing bounds and finiteness checks.

I ran 16 isolated assertion groups on the complete pinned schema module with its local dependency modules, using Python 3.12.14 and Pydantic 2.14.0. They reproduced baseline acceptance and verified the candidate rejects booleans in scalars, nested correlation/allocation values, election mappings and grid values with located errors. The checks also retained ordinary numeric 0/1, integral-float seeds, YAML list conversion, numeric bounds and frozen mappings.

This deliberately preserves current number-to-flag and numeric-string coercion policies. If the intended policy is broader strict typing, that is a separate compatibility decision, including the existing editor expectation. Before merging, add native tests for these nested/union boundaries and run the editor/schema suites and the pinned formatter. This is schema validation evidence, not validation of financial calculations.

---

## R10-02 — Casdoor #5957

Destination: https://github.com/casdoor/casdoor/issues/5957

Scope: existing public interoperability report; no new vulnerability claim or security-disclosure message. Contribution guidance reviewed. No workaround disabling authentication is proposed.

---

AI-assisted static source review; I have not run Casdoor, a token exchange, or the ChatGPT connector flow.

The CIMD restriction is present, but the “no client_assertion verification anywhere” part can be narrowed. In the reported [v4.23.0 commit 1b91d9d](https://github.com/casdoor/casdoor/commit/1b91d9d319a127e9b1af88fa7a20bb35c052b9d8), [GetOAuthToken](https://github.com/casdoor/casdoor/blob/1b91d9d319a127e9b1af88fa7a20bb35c052b9d8/object/token_oauth.go#L28-L55) calls `ValidateClientAssertion` for the JWT bearer assertion type. [That function](https://github.com/casdoor/casdoor/blob/1b91d9d319a127e9b1af88fa7a20bb35c052b9d8/object/token_oauth_util.go#L797-L864) has a federated-token branch and a certificate-based `ValidateJwtAssertion` fallback. These files are byte-identical at current master dd0cc5d. This does not establish complete RFC 7523 interoperability, but it means removing the advertised method globally needs a compatibility check for existing configured applications.

The dynamic-registration mismatch is more specific:
- [RegisterDynamicClient](https://github.com/casdoor/casdoor/blob/1b91d9d319a127e9b1af88fa7a20bb35c052b9d8/object/oauth_dcr.go#L71-L164) echoes the requested auth method, while `checkDcrClientMetadata` does not validate it.
- [newDynamicClientApplication](https://github.com/casdoor/casdoor/blob/1b91d9d319a127e9b1af88fa7a20bb35c052b9d8/object/oauth_dcr.go#L168-L234) does not provision a client certificate or persist the requested auth method. The registration request type has no `jwks`/`jwks_uri` fields.
- [GetDynamicClientRegistrationResponse](https://github.com/casdoor/casdoor/blob/1b91d9d319a127e9b1af88fa7a20bb35c052b9d8/object/oauth_dcr.go#L252-L305) then hardcodes `client_secret_basic`, including the response used after updates.

I would separate the near-term repair from adding dynamic-key support: validate registration/update auth methods against what that registration path can actually provision, reject unsupported metadata before creating/updating an application, and make create/read/update responses consistently reflect the effective method. Keep CIMD's current restriction explicit until its key-registration and validation path is implemented; merely allowing the string is insufficient.

Useful regressions are: unsupported method rejected with no persisted application; create → read → update preserves each accepted method; existing configured certificate/federated authentication retains its behavior; CIMD rejection remains deterministic. Dynamic JWKS support would additionally need its own key-fetch and token-validation tests.

Those regressions are proposed, not executed: Go is unavailable in my environment. The reporter's running image/configuration and actual connector interoperability remain unverified.
