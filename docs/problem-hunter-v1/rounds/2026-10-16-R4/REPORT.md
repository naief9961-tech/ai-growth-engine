# الجولة الإضافية R4 — 16 أكتوبر 2026

بدأت بطلب المستخدم بعد نشر ردود R3 يدويًا. لا تعليق أو PR خارجي أُرسل في هذه الجولة.

## النتيجة الفعلية

- فرز أولي لـ **398 رابط مشكلة فريدًا** من 14 استعلامًا. منها 86 ظهرت في فرز R3؛ الفرز ليس تحقيقًا كاملًا ولا يعني أن 398 مشكلة جديدة اكتُشفت لأول مرة. 4 روابط سبق تسجيلها في السجل/الرادار.
- **11** بلاغًا قُرئ مع جميع التعليقات والأحداث المتاحة؛ **3** تحقيقات مصدرية مكتملة.
- عند المراجعة النهائية: **رد واحد جاهز للمراجعة**، وتحقيق مفتوح موقوف عن توصية النشر بسبب شروط مساهمات المستودع، ومرشح سُحب بعد أن أغلقه صاحبه أثناء العمل.
- **21 مجموعة اختبار محلية PASS**: 6 مجموعات تثبت السلوك الأصلي و15 للنماذج/المقاطع المرشحة. المصفوفات الداخلية لا تُحسب كتحقيقات إضافية. لا suite كامل لأي مشروع.
- قُرئت سلاسل ردود R3 الثلاثة من جديد: لا رد مطور أو اهتمام تجاري ظاهر عند آخر تحقق.
- المنشور الخارجي في هذه الجولة بواسطة الوكيل: **صفر**. النص الكامل للرد المقترح في [DRAFTS.md](DRAFTS.md).

## التحقيقات

### 1. [MementoRC/mcp-git#298](https://github.com/MementoRC/mcp-git/issues/298)

المبلّغ: `MementoRC`؛ أُنشئت: 2026-10-16T01:07:07Z؛ حالة المراجعة النهائية: **open / DRAFT_ONLY**.

**التشخيص:** Top-level non-object bodies hit .get before validation. Parameter validation is dispatch-dependent: initialize/list ignore non-objects; tools/call coerces falsey values with params or {} and produces -32603 for truthy wrong types.

**الحل/الحدود:** Validate envelope before .get; for methods requiring object params validate explicit params before dispatch, retaining absent versus null and request ID. Batch and notification policy need separate integration checks.

**الاختبار:** 5 groups PASS: 2 baseline source-extracted groups and 3 candidate-extract groups; includes 24 invalid-param method/value combinations. No FastAPI/ASGI, live HTTP, Git operations, notification or full-suite tests.

**الثقة:** high for source-extracted dispatch behavior; integration and batch policy unverified. **الفائدة:** high: adds falsey/truthy and method-dispatch boundaries absent from existing characterization pair.

**المصدر المثبت:**
- [src/mcp_server_git/transport/http_jsonrpc.py](https://github.com/MementoRC/mcp-git/blob/648cb467d80311ef83f7246dfa9a07bd930db072/src/mcp_server_git/transport/http_jsonrpc.py) — commit `648cb467d80311ef83f7246dfa9a07bd930db072`؛ blob `730b378f8c68ed0e15c6fa31795607cc23201bea`.
- [src/mcp_server_git/transport/http_tool_call.py](https://github.com/MementoRC/mcp-git/blob/648cb467d80311ef83f7246dfa9a07bd930db072/src/mcp_server_git/transport/http_tool_call.py) — commit `648cb467d80311ef83f7246dfa9a07bd930db072`؛ blob `2720df013e687d111a2b162350bdb3613cd18393`.
- [src/mcp_server_git/transport/http_rpc_responses.py](https://github.com/MementoRC/mcp-git/blob/648cb467d80311ef83f7246dfa9a07bd930db072/src/mcp_server_git/transport/http_rpc_responses.py) — commit `648cb467d80311ef83f7246dfa9a07bd930db072`؛ blob `8383fc4f1cb176588b5157d6e8677454908cf55e`.

### 2. [modelcontextprotocol/python-sdk#3710](https://github.com/modelcontextprotocol/python-sdk/issues/3710)

المبلّغ: `inanna-malick`؛ أُنشئت: 2026-10-14T22:07:26Z؛ حالة المراجعة النهائية: **open / HELD_REPOSITORY_AI_POLICY**.

**التشخيص:** Reserved-name prefixing collides with a literal parameter name and overwrites the model-field dictionary before Pydantic. Declaration order changes the lost field.

**الحل/الحدود:** Allocate an internal name against all original parameter names plus already generated names; preserve alias/original kwargs binding and constraints. Test both orders and repeated-prefix names via public MCP Client/server before upstream use.

**الاختبار:** 9 groups PASS using extracted ArgModelBase and argument-construction prefix: 2 baseline orders, 6 candidate permutations and 1 annotation/default/constraint control. Python 3.12.14/Pydantic 2.13.5; no MCP package, public roundtrip or suite.

**الثقة:** high for construction-time collision; candidate end-to-end compatibility unverified. **الفائدة:** medium to high: order-independent allocation and repeated-prefix regression boundary.

**المصدر المثبت:**
- [src/mcp/server/mcpserver/utilities/func_metadata.py](https://github.com/modelcontextprotocol/python-sdk/blob/754254c08fe1c3eda18b69da3d336106fe8d72d6/src/mcp/server/mcpserver/utilities/func_metadata.py) — commit `754254c08fe1c3eda18b69da3d336106fe8d72d6`؛ blob `96d25ec5ab50261dc303f55c8585cdeeca4db99d`.

### 3. [markdlabrecque/pi-claude-subscription#22](https://github.com/markdlabrecque/pi-claude-subscription/issues/22)

المبلّغ: `markdlabrecque`؛ أُنشئت: 2026-10-16T05:24:29Z؛ حالة المراجعة النهائية: **closed / WITHDRAWN_ISSUE_CLOSED**.

**التشخيص:** At inspected default-branch snapshot two unguarded writes can leave schema and partial config artifacts. PID-only file names do not identify individual call ownership.

**الحل/الحدود:** Investigation suggested owned per-call paths, cleanup covering both writes and preserving original error. Withdrawn from posting when owner closed issue citing fix/pr-17-review-followups; branch now has UUID paths and second-write schema cleanup.

**الاختبار:** 7 groups PASS: 2 baseline injected partial-write failures and 5 limited cleanup/ownership candidate-model groups. Memory filesystem; no actual ENOSPC/EACCES, CLI, Vitest or crash recovery. Maintainer branch tests were not run by us.

**الثقة:** high for historical pinned source; closure verified, complete maintainer fix not independently integration-tested. **الفائدة:** WITHDRAWN: issue closed during investigation.

**المصدر المثبت:**
- [src/mcp-config.ts](https://github.com/markdlabrecque/pi-claude-subscription/blob/e0c9a12ac21be4c197e82795f7207746f3183028/src/mcp-config.ts) — commit `e0c9a12ac21be4c197e82795f7207746f3183028`؛ blob `04854611e280a6dfc3a3ddab76c83c855fa8d801`.
- [index.ts](https://github.com/markdlabrecque/pi-claude-subscription/blob/e0c9a12ac21be4c197e82795f7207746f3183028/index.ts) — commit `e0c9a12ac21be4c197e82795f7207746f3183028`؛ blob `4b77482487cff70296081e8e80e6fdcda5b9e597`.

## تفاصيل هندسية تمنع ادعاء إصلاح كامل

**MCP Git:** المصفوفة المحلية تضمنت `null` و`[]` و`false` و`0` و`""` و`["x"]` و`1` و`"x"`، لكل من initialize وtools/list وtools/call، مع request ID صريح. أول طريقتين قبلتا الأنواع الثمانية؛ tools/call يبدل الخمس falsey بـ{}، فتظهر رسالة missing name، بينما الثلاث truthy تعيد internal error. الدليل الجديد هو اختلاف السلوك حسب الطريقة والقيمة، فوق وصف البلاغ الأصلي. يجب أن تتحقق اختبارات المشروع لاحقًا من عدم دخول handler أو إنشاء session عند فشل التحقق، ومن notifications دون response، ومن سياسة batch المتوافقة مع البروتوكول. معلن المصدر `2024-11-05`؛ نموذج رفض arrays المحلي لا يثبت توافق batch. [PR #297](https://github.com/MementoRC/mcp-git/pull/297) مدموج لكنه refactor يحافظ عمدًا على الخطأين، وليس إصلاحًا لهما. لم يظهر PR مفتوح للمشروع عند المراجعة. اختبارات characterization الحالية قُرئت ولم تُشغّل.

**MCP Python:** المشكلة تحدث عند بناء قاموس الحقول قبل create_model؛ عكس ترتيب model_dump وfield_model_dump يعكس الحقل المفقود. يتعين حجز كل الأسماء الأصلية قبل اختيار اسم داخلي مولّد وتجاوز سلسلة field_ كاملة، مع إبقاء aliases والأنواع والقيم الافتراضية. نجحت ستة ترتيبات لثلاثة أسماء في المقاطع المعزولة. [PR #3416](https://github.com/modelcontextprotocol/python-sdk/pull/3416) مغلق وغير مدموج، ويعالج إعادة ربط alias مختلفة؛ لا يرد حقلًا كُتب فوقه. مراجعة مستقلة قرأت المشكلة دون الحل المقترح وأكدت السبب وحدود الاختبار؛ لم تشغّل اختبارات مستقلة. بيئتنا Python 3.12.14 وPydantic 2.13.5 تختلف عن بيئة المبلّغ، ولم يُثبت public MCP roundtrip.

**سياسة MCP Python:** قُرئت [CONTRIBUTING](https://github.com/modelcontextprotocol/python-sdk/blob/754254c08fe1c3eda18b69da3d336106fe8d72d6/CONTRIBUTING.md)، وAGENTS، وtest-quality، و[AI_POLICY](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/AI_POLICY.md). الترحيب بالتحليل لا يلغي شرط الإفصاح والفهم الشخصي ووجود إنسان واجه المشكلة وقرأ الناتج. هذا غير مثبت من مجرد طلب فرز مشكلات أطراف أخرى؛ لذلك حُفظ التحقيق ولم يُجهز نص يُطلب نسخه مباشرة. لا PR بلا assignment/help wanted، ولا طلب تعيين آلي.

**pi-claude:** أُعيد إنتاج إخفاق الكتابة الجزئي بعينات ذاكرة فقط. أثناء الفحص أُغلقت #22، و[ذكر صاحبها الإصلاح](https://github.com/markdlabrecque/pi-claude-subscription/issues/22#issuecomment-6208910728) على branch `fix/pr-17-review-followups` عند `c861e737a52248db020051f874efa7572e564682`. قرأنا mcp-config.ts في ذلك الفرع (blob `64fbc4dad0a23ce1dbe22974929e8ecfeb724b99`): UUID لكل نداء وcatch يحذف schema إذا فشلت كتابة config. لم نشغّل اختبارات المساهم أو نزعم دمج/نشر هذا الفرع. نتائجنا مرتبطة بالمصدر الأقدم المثبت فقط. سُحب التعليق؛ لم نستغل حدودًا إضافية لتكرار التواصل مع بلاغ مغلق.

## المستبعدون بعد القراءة الكاملة

- [volcengine/OpenViking#6158](https://github.com/volcengine/OpenViking/issues/6158) — Reporter already supplies source-level cause and eight wire-level cases; no distinct added value established.
- [aotter/mantle#1693](https://github.com/aotter/mantle/issues/1693) — PR #1694 already implements normalized issuer verification with regression coverage; no duplicate comment.
- [neatlogs/neatroots#154](https://github.com/neatlogs/neatroots/issues/154) — PR #155 verified merged; excluded as already repaired upstream.
- [bmorton/temporal-operator#223](https://github.com/bmorton/temporal-operator/issues/223) — Owner already supplies detailed causal chain and remediation; no additional independently tested fix.
- [modelcontextprotocol/python-sdk#3711](https://github.com/modelcontextprotocol/python-sdk/issues/3711) — Existing targeted dataclass reproductions; source read was preliminary, not a completed additional investigation.
- [modelcontextprotocol/python-sdk#3714](https://github.com/modelcontextprotocol/python-sdk/issues/3714) — Reporter already supplies deterministic delayed-error reproduction; no new contribution completed.
- [modelcontextprotocol/typescript-sdk#3019](https://github.com/modelcontextprotocol/typescript-sdk/issues/3019) — PR #3021 already covers null-prototype registries and tests; no duplicate.
- [FreeTWAI/freedom-platform#827](https://github.com/FreeTWAI/freedom-platform/issues/827) — PR #828 already covers exact media-type parsing and native HTTP regressions; no duplicate.

## توثيق نشر R3 اليدوي

- [AGNT](https://github.com/agnt-gg/agnt/issues/169#issuecomment-6208715705): 08:23:05 السعودية.
- [Noir](https://github.com/owasp-noir/noir/issues/3078#issuecomment-6208753257): 08:26:11 السعودية.
- [Engram — التعليق الظاهر حاليًا](https://github.com/Gentleman-Programming/engram/issues/1899#issuecomment-6208832958): 08:32:58 السعودية. رأينا أولًا التعليق 6208777198 عند 08:28:14 ثم لم يعد موجودًا في قائمة التعليقات الأخيرة؛ حُفظت الملاحظتان دون افتراض سبب التغيير. مؤشر المتابعة الحالي 6208832958.
- لا تعليق لاحق من مطور في السلاسل الثلاثة، ولا طلب تجاري أو شراء مثبت. لا تعاد أخبار R3 القديمة كأنها ردود جديدة.

## الحفظ والقيود

- التغييرات وثائق وسجل فقط داخل docs/problem-hunter-v1. فُحص AGENTS والشجرة كاملة وworkflows الثمانية في سلسلة commits الحالية؛ لا AGENTS متداخل. push paths لا تشمل هذه الوثائق. استُخدم expected_sha مع force:false و[skip ci]، ولم تُشغّل workflow يدويًا.
- لم يُغيّر أي نظام إنتاج أو دفع أو V5 أو خادم، ولم تُستخدم مفاتيح أو بيانات عملاء أو مدفوعات أو خدمات إضافية.
- لم تُوصَ أداة NAIF مجانية لعدم تطابق مباشر مع العيوب المكتشفة؛ لا رابط دعائي في المسودة. حدود الأدوات المقروءة في R3 ما زالت معتمدة؛ لا ادعاء بفحص توقيع أو OAuth/stdio.
- تفاصيل إعادة الإنتاج وحدودها في [TESTS.md](TESTS.md)، والفرز في [SCREENING.md](SCREENING.md).
- اختبار collision توقف في محاولة أولى بسبب نقص __name__ في namespace لحاضنة الاختبار فقط؛ أُصلح إعداد الحاضنة وأُعيد بنجاح. لم يكن هذا فشلًا إضافيًا في المشروع الأصلي.
- المطلوب من المستخدم: مراجعة رد R4-01 إذا أراد نشره. لا طلب إعادة نشر أي من ردود R3 ولا تكرار التعليق على #22 المغلقة.

