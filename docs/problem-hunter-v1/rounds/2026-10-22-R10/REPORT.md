# NAIF Gravity — R10 — 22 October 2026

Reviewed at 2026-10-22T05:12:18Z. Scope: fresh issue discovery, additive engineering evidence, follow-up reconciliation. No third-party publication.

## النتائج

- **154 مشكلة فريدة** في الفرز الأولي من 160 نتيجة عبر 8 استعلامات محدودة بـ20 نتيجة لكل استعلام. هذا ليس حصرًا شاملًا لـGitHub.
- **7 بلاغات قُرئت كاملة** مع التعليقات والتحديثات وفحص طلبات الدمج؛ **تحقيقان مكتملان** و3 قراءات مصدر استكشافية. لا تُحتسب الحالات الاستكشافية تحقيقات مكتملة.
- **ردّان إنجليزيان جاهزان للمراجعة**، لا حاجة لملء العدد بحالات ضعيفة: [النص الكامل](DRAFTS.md).
- **16 مجموعة تحقق معزولة نجحت** على مخطط Northplan الكامل ونسخته المرشحة. اختبارات Casdoor التشغيلية لم تُنفذ؛ Go غير متاح.
- تمت متابعة 26 خيطًا سابقًا. تعليق يدوي واحد جديد لنا تأكد نشره، بلا ردود جديدة من المطورين بعد المؤشرات المحفوظة. لا اهتمام تجاري صريح ولا دليل شراء.

## الحالتان المختارتان

| الحالة | الدليل والحل | الثقة والحدود |
|---|---|---|
| [Northplan #100](https://github.com/janowoc/northplan/issues/100) | قبول true/false كأرقام. إصلاح محدود بحارس قبل التحويل على الأوراق الرقمية، بما فيها فرعا اتحاد قيم grid، يحافظ على التحويلات المقبولة سابقًا. | عالية للمخطط والاختبار المعزول؛ لا تشغيل للمحاكي أو واجهة API أو المحرر أو المجموعة الكاملة. سياسة الأرقام داخل الحقول المنطقية تبقى بقرار المالك. |
| [Casdoor #5957](https://github.com/casdoor/casdoor/issues/5957) | التحقق من client_assertion موجود فعلًا في v4.23.0 وmaster؛ الخلل المحدد في مسار التسجيل الديناميكي واتساق method بين الإنشاء والقراءة والتحديث، مع قيد CIMD. | عالية للقراءة المصدرية، متوسطة لربطها ببيئة المبلّغ. توصية تحقق مبكر واتساق metadata؛ لا إصلاح OAuth مُختبر. |

كلا البلاغين مفتوح وبلا تعليقات عند آخر مراجعة. Northplan أُنشئ 2026-10-22T04:42:28Z بواسطة janowoc؛ Casdoor أُنشئ 2026-10-22T04:49:56Z بواسطة aiastia.

## Engineering findings

### Northplan

At `f3b55a5e72a30080ef28cd3066371017ecae1b97`, numeric aliases/fields are lax. The original minimal fixture plus synthetic boolean mutations reproduce acceptance. A narrow BeforeValidator option rejects bool before numeric conversion across 29 scalar annotation sites, retaining bounds, finiteness and mapping immutability. A finite-only fix misses the raw integer branch in grid. Existing editor tests deliberately normalize seed 42.0 to int and integer 1 to a flag; broad strict typing is a compatibility choice, not a mechanically equivalent repair.

[Candidate diff](NORTHPLAN-CANDIDATE.md) and [reproduction/limits](TESTS.md). No upstream file, golden expectation, financial parameter or snapshot changed. CLAUDE.md/README reviewed. This is an isolated design probe and discussion draft, not a commissioned upstream implementation/PR. The owner must choose any broader coercion policy; formatter/native integration still pending. All two repository PRs are closed and unrelated; no linked repair in complete issue timeline.

### Casdoor

Master `dd0cc5d7af104d7feeacd3b5859402bf0bc4d1f7`; reported v4.23.0 resolves to `1b91d9d319a127e9b1af88fa7a20bb35c052b9d8`. `object/token_oauth.go`, `object/token_oauth_util.go`, and `object/oauth_dcr.go` have identical blob hashes at both commits. GetOAuthToken calls ValidateClientAssertion, which supports a federated branch and certificate fallback. This is evidence against the blanket “no verifier exists” claim, not certification of RFC conformance.

DCR's request shape has no jwks/jwks_uri; the constructor does not provision ClientCert or persist auth method; the initial response echoes requested auth method, whereas read/update response hardcodes client_secret_basic. checkDcrClientMetadata validates other metadata but not that method. CIMD explicitly permits only none. Recommend capability validation before persistence and consistent create/read/update serialization; dynamic-key support needs a separate design. Removing global discovery support could affect configured applications, so it is not proposed as a proven universal fix.

All five open PRs and thirty recent all-state entries checked; no matching repair observed. README and [contribution guide](https://casdoor.ai/docs/contributing/) reviewed. This is a comment on an existing public interoperability report, not disclosure of a newly verified vulnerability. No security email sent.

## Held or excluded after deeper review

- [misaalanshori/lca #454](https://github.com/misaalanshori/lca/issues/454): Reporter already provides measured decode failure, fix/alias option and exact regression; related PR #453 active. No additive independently tested result.
- [NVIDIA/NeMo-Agent-Toolkit #2419](https://github.com/NVIDIA/NeMo-Agent-Toolkit/issues/2419): Open PR #2420 explicitly closes the issue and covers failure/follow-up text; no duplicate solution drafted. Author's tests not rerun.
- [railwayapp/cli #1312](https://github.com/railwayapp/cli/issues/1312): Exploratory source confirms byte-to-char JSONC corruption; reporter already supplies mechanism/workaround. Rust unavailable, additional scanner-boundary ideas unverified; held without draft.
- [herox215/ouroboros #55](https://github.com/herox215/ouroboros/issues/55): Exploratory source confirms cancellation watcher stopped before 200 body read. Reporter already identifies timing; Go unavailable to validate safe 101 handoff/callback race handling. No untested fix presented as proven.
- [beeper/desktop-api-js #48](https://github.com/beeper/desktop-api-js/issues/48): Accessible SDK MCP server is not proven to be Desktop's built-in /v0/mcp schema generator. Affected source boundary unavailable; do not patch the wrong server.

Exploratory source pins: Railway `b62467ef1b5303e3e340283ed96425dcf9612993`; Ouroboros `67042af7c348586d644be25fbd3384a033e15f97`; Beeper SDK `9d2d14d0eef05ef0c2cf6368f58d84489c56487a`. These are not completed fix validations. Other search results were initially screened only; see [discovery audit](SCREENING.json). No previously recorded issue among the 154 was advanced as new.

## New follow-up evidence only

1. **IntelliFlow #940:** verified [our manual comment 6308670609](https://github.com/talyssonoliver/IntelliFlow-CRM/issues/940#issuecomment-6308670609), created 2026-10-21T05:18:24Z. Advanced last_seen_comment_id and last_own_comment_id; marked R9-02 historical. No subsequent developer response. Postiz's earlier manual publication was already recorded; it is not a new result.
2. **A2A Python:** [PR #1354](https://github.com/a2aproject/a2a-python/pull/1354) merged 2026-10-21T10:46:00Z at `91929cda989caba089584ceafa7796583f25bec4`; [#1341](https://github.com/a2aproject/a2a-python/issues/1341) closed at 10:46:02Z. Final five-file diff includes shared parse_lenient, REST SSE parsing and transport regression tests. No new comment; cursor remains 6274826969. We did not rerun those tests, verify a deployed release, or claim our comment caused the change.
3. Other 24 tracked threads: no comments newer than saved cursors. No newly verified commercial request. Technical implementation progress is not a purchase.

## Own publication and safety scope

Prepared as one atomic documentation update in ai-growth-engine, based on `a8409bac636f5f257664f07b1b76732531b4d389`; the resulting commit is returned after the compare-and-swap write. Only docs/problem-hunter-v1/ paths change. All eight existing workflow definitions and root AGENTS.md reviewed. Three push workflows filter server.json, .well-known/agent.json or their own workflow paths; none match these documentation paths. Other workflows have no push trigger. No workflow dispatch or modification; commit uses [skip ci]. No external comments/PRs/messages, production/payment/V5/server changes, payments, wallet actions or dependency installations.

The source's unrelated bounty/wallet onboarding is outside this task and was not executed. The scheduled task remains unchanged.

## Free-tool fit

NAIF homepage and [/tools](https://naifgravity.com/tools) retrieved on 22 October; the page describes public endpoint reachability/status and sanitized payload-structure diagnostics. Existing [diagnostic repository README](https://github.com/naief9961-tech/naif-gravity-mcp-diagnostics) reviewed. Neither is an appropriate proof for numeric coercion or dynamic OAuth registration. No NAIF link or paid offer is inserted in either reply. The MCP probe does not support stdio/OAuth; /tools is not a signature verifier or an A2A repair.

## What remains

Only review/approval of the two new replies is needed before any later publication. Re-check live comments/PRs then. There is no request for credentials, payment data or production access. Go/Rust unavailable; no runtime claim for Casdoor/Ouroboros/Railway. Northplan's pinned formatter and native suites were not run. Limited search coverage is explicit; candidates are not presented as globally best.

## Pinned source evidence

### janowoc/northplan #100

- [engine/scenario/schema.py](https://github.com/janowoc/northplan/blob/f3b55a5e72a30080ef28cd3066371017ecae1b97/engine/scenario/schema.py) — commit `f3b55a5e72a30080ef28cd3066371017ecae1b97`, blob `42648c3cbab46aae85b8c8f5b9ae1652957281ed`.
- [engine/mc/moments.py](https://github.com/janowoc/northplan/blob/f3b55a5e72a30080ef28cd3066371017ecae1b97/engine/mc/moments.py) — commit `f3b55a5e72a30080ef28cd3066371017ecae1b97`, blob `f41411a5fb3e1204e1b9dab77c6ee37dfb8c0118`.
- [engine/core/timeline.py](https://github.com/janowoc/northplan/blob/f3b55a5e72a30080ef28cd3066371017ecae1b97/engine/core/timeline.py) — commit `f3b55a5e72a30080ef28cd3066371017ecae1b97`, blob `1a73d1120443b9ba77e1367934a673f2785255d8`.
- [engine/params/loader.py](https://github.com/janowoc/northplan/blob/f3b55a5e72a30080ef28cd3066371017ecae1b97/engine/params/loader.py) — commit `f3b55a5e72a30080ef28cd3066371017ecae1b97`, blob `da74368a16d615be779b98879b1b6da108d09a58`.
- [scenarios/minimal.yaml](https://github.com/janowoc/northplan/blob/f3b55a5e72a30080ef28cd3066371017ecae1b97/scenarios/minimal.yaml) — commit `f3b55a5e72a30080ef28cd3066371017ecae1b97`, blob `17252cee15c55a8fb9364525bc993941eddf1e48`.
- [tests/report/test_report_editor.py](https://github.com/janowoc/northplan/blob/f3b55a5e72a30080ef28cd3066371017ecae1b97/tests/report/test_report_editor.py) — commit `f3b55a5e72a30080ef28cd3066371017ecae1b97`, blob `5f437da16b12e60af35192286d063b0771547d28`.
- [pyproject.toml](https://github.com/janowoc/northplan/blob/f3b55a5e72a30080ef28cd3066371017ecae1b97/pyproject.toml) — commit `f3b55a5e72a30080ef28cd3066371017ecae1b97`, blob `312e7ba3759130618902f4fd981d01cf290bc112`.

### casdoor/casdoor #5957

- [object/token_oauth.go](https://github.com/casdoor/casdoor/blob/dd0cc5d7af104d7feeacd3b5859402bf0bc4d1f7/object/token_oauth.go) — commit `dd0cc5d7af104d7feeacd3b5859402bf0bc4d1f7`, blob `4e4752457ead34654a01fb017a2899969e2b298b`.
- [object/token_oauth_util.go](https://github.com/casdoor/casdoor/blob/dd0cc5d7af104d7feeacd3b5859402bf0bc4d1f7/object/token_oauth_util.go) — commit `dd0cc5d7af104d7feeacd3b5859402bf0bc4d1f7`, blob `39ce0fa394a42ce72c808154c59722ee9d88c09d`.
- [object/oauth_dcr.go](https://github.com/casdoor/casdoor/blob/dd0cc5d7af104d7feeacd3b5859402bf0bc4d1f7/object/oauth_dcr.go) — commit `dd0cc5d7af104d7feeacd3b5859402bf0bc4d1f7`, blob `92ad8acd305fe2d26ad0d064a5ff7402a3d1a39b`.
- [object/oauth_cimd.go](https://github.com/casdoor/casdoor/blob/dd0cc5d7af104d7feeacd3b5859402bf0bc4d1f7/object/oauth_cimd.go) — commit `dd0cc5d7af104d7feeacd3b5859402bf0bc4d1f7`, blob `a9e13033b536a7ea81fca8d0f1476b855f9e1c42`.
- [object/wellknown_oidc_discovery.go](https://github.com/casdoor/casdoor/blob/dd0cc5d7af104d7feeacd3b5859402bf0bc4d1f7/object/wellknown_oidc_discovery.go) — commit `dd0cc5d7af104d7feeacd3b5859402bf0bc4d1f7`, blob `c7785b271323e415e33d5d3d57a259de9ec447d4`.
