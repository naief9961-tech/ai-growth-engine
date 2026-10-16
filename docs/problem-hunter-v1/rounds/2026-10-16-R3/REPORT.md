# الجولة الثالثة — 16 أكتوبر 2026

هذه مراجعة هندسية محدودة؛ لا تعليقات أو PRs خارجية أُرسلت في هذه الجولة. مسودات [DRAFTS.md](DRAFTS.md) تنتظر موافقة المستخدم.

## النطاق والنتيجة

- **215** رابط مشكلة فريد في الفرز الأولي، من سبعة استعلامات: MCP وA2A وx402 وwebhook وJSON Schema وMCP bugs وAPI authentication. سجّلنا العناوين والروابط في [SCREENING.md](SCREENING.md). الفرز ليس قراءة كاملة.
- **9** بلاغات مرشحة قُرئت بالكامل مع جميع التعليقات/الأحداث المتاحة.
- **3** تحقيقات مصدرية مكتملة، مع SHA ومراجعة مساهمات المشروع وبحث PRs والتحديثات. لم نملأ العدد بخمس حالات ضعيفة.
- **16** سلسلة متابعة فُحصت: عشر سابقة وست مسائل ذات مسودات R1/R2. لا منشورات لنا في مسائل R1 الثلاث.
- **8** حالات محلية نجحت: اثنتان لإعادة إنتاج السلوك من كود AGNT المقروء مع بدائل ذاكرة/شبكة، وست حالات نمذجة تصميمية. **صفر** حزم اختبار كاملة للمشاريع الأصلية.
- **3** تعليقات نشرها المستخدم يدويًا أمس تأكدت عبر GitHub، وصُححت حالتها في السجل. لم ننشرها في التشغيل الحالي.
- **6** تعليقات جديدة بعد آخر مؤشر محفوظ أو تعليقنا المؤكد: رد تقني مباشر واحد، وتحديثا Trinity، وثلاثة أحداث مساهمة لشخص آخر في LumenRoute.
- لا طلب شراء أو اهتمام تجاري صريح.

## أفضل الحالات الجديدة

### 1. [agnt-gg/agnt#169](https://github.com/agnt-gg/agnt/issues/169) — سباق OAuth

المبلّغ `agnt-gg`؛ أُنشئت 2026-10-16T03:11:31Z؛ مفتوحة وبلا تعليقات عند الفحص.

**المصدر:** [MCPOAuthService.js](https://github.com/agnt-gg/agnt/blob/52f1a8644bf8f672df660534dc3584fbeb3138fc/backend/src/services/MCPOAuthService.js)، commit `52f1a8644bf8f672df660534dc3584fbeb3138fc`، blob `ef149de39c19a166fc874fd8de0c3b1382ed8b2a`. الدالة `refresh` تبدأ عند السطر 332؛ تحفظ snapshot قبل انتظار الشبكة ثم تكتب المتجر كله عند 351.

**التشخيص المثبت محليًا:** عشرة متصلين متزامنين يستدعون تبادل الرمز عشر مرات. وعند اكتمال تحديث B قبل A، يعيد snapshot الخاص بـA بيانات B القديمة. أُعيد إنتاجهما من الكلاس الأصلي بعد استبعاد imports والتصدير، مع استبدال التخزين وطلب الرمز بعينات ذاكرة فقط. تحققنا من SHA للملف قبل التنفيذ.

**الإصلاح المقترح:** single-flight لكل خادم؛ وقفل يحمي قراءة آخر متجر ودمج الحساب وكتابته معًا، وليس مجرد ترتيب كتابة snapshots قديمة. ينبغي للمالك استكمال الكتابة الذرية وحالات دورة حياة الاعتماد. جرى اختبار نموذج محدود للـsingle-flight والدمج ونجح؛ ليس patch جاهزًا للإنتاج.

**Regression:** 10 متصلين/طلب تبادل واحد؛ ترتيب B ثم A بحواجز promises حتمية؛ بقاء تحديث الحسابين؛ اختبارات لاحقة للملف والصلاحيات والإخفاق والتزامن بين العمليات.

**الثقة/الفائدة:** عالية للسلوكين المحددين؛ عالية لقيمة إعادة الإنتاج. لا إثبات لانقطاع حساب حقيقي أو معالجة session 404.

**سياسة المشروع:** CONTRIBUTING يمنع PRs خارجية في المصادقة والتخزين الاعتمادي، ويسمح ببلاغات الأعطال غير الأمنية. المسودة تضيف أدلة إلى البلاغ العام الموجود فقط؛ لا patch خارجي ولا عرض خدمة مدفوعة.

### 2. [owasp-noir/noir#3078](https://github.com/owasp-noir/noir/issues/3078) — حقول readOnly تظهر في الطلب

المبلّغ `hahwul`؛ أُنشئت 2026-10-16T04:52:09Z؛ مفتوحة وبلا تعليقات أو PR مرتبط ظاهر.

**المصدر:** commit `8d8600bf8aab07c40ee8a75f2b9b4a93d82f626b`:
- [oas3.cr](https://github.com/owasp-noir/noir/blob/8d8600bf8aab07c40ee8a75f2b9b4a93d82f626b/src/analyzer/analyzers/specification/oas3.cr)، blob `6da7f483f2a46c08d30f034c0b398334d6db33e1`، حلقات properties عند 96 و135.
- [oas2.cr](https://github.com/owasp-noir/noir/blob/8d8600bf8aab07c40ee8a75f2b9b4a93d82f626b/src/analyzer/analyzers/specification/oas2.cr)، blob `58061efad5f80055fc252d44807b90b8418681a2`، عند 28 و65.

**التشخيص:** الحلقات الأربع تهمل قيمة تعريف الخاصية وتضيف اسمها دون فحص readOnly. الإضافة الجديدة: المسارات نفسها تجمع حقول form أيضًا، لذا الإصلاح المقيد بـJSON وحده ناقص.

**الإصلاح:** استبعاد boolean readOnly:true عند إصدار خاصية الطلب في النسختين والصيغتين؛ إبقاء writeOnly/false/absent؛ وصول آمن للأنواع؛ عدم تغيير schema المشتركة للاستجابة. تحتاج property-level refs إلى حل مرجع آمن بدل الاكتفاء بالعلم المباشر.

**Regression:** JSON/YAML × OAS2/OAS3، JSON/form، required readOnly مقابل writeOnly، null/scalar، property refs وcomposition والدورات.

**الثقة/الفائدة:** عالية لمسار الخاصية المباشرة، متوسطة للتفاصيل المركبة غير المختبرة؛ فائدة متوسطة إلى عالية.

**الاختبار:** حالة Python اصطناعية لمرشح الخصائص نجحت. Crystal غير متاح؛ لم نشغّل Noir أو resolver أو suite.

### 3. [Gentleman-Programming/engram#1899](https://github.com/Gentleman-Programming/engram/issues/1899) — ملف فارغ يوقف تشخيص بقية MCP

المبلّغ `Taber37`؛ أُنشئت 2026-10-15T19:31:32Z؛ مفتوحة وبلا تعليقات أو PR مرتبط ظاهر.

**المصدر:** [registry.go](https://github.com/Gentleman-Programming/engram/blob/9c4382f60e2fb300c6cb877bb6ff295ecfbdf2ee/internal/setup/registry.go)، commit `9c4382f60e2fb300c6cb877bb6ff295ecfbdf2ee`، blob `24ccbbca81573f64b2768152557fd8121c839062`. `StaleMCPCommands` عند 196؛ Unmarshal عند 214 ثم return عند الخطأ. راجعنا أيضًا `setup.go` و`registry_test.go`.

**التشخيص:** parse لملف فارغ ينهي حلقة فحص جميع adapters. helper المشترك `readJSONConfig` يخدم مسارات كتابة أيضًا، فلا ينبغي توسيع إصلاح doctor إليه بلا حاجة.

**الإصلاح:** guard للملف الفارغ/مسافات JSON بعد نجاح القراءة وقبل Unmarshal داخل الحلقة فقط؛ إبقاء nonempty malformed خطأ. النص الكامل يتضمن اقتراح Go محدودًا غير مجمّع.

**Regression:** ملف فارغ يسبق تسجيلًا يطابق شكل Engram ويشير إلى executable مطلق مفقود؛ يجب أن يبقى اكتشاف الثاني ظاهرًا. absent/whitespace/{}، malformed، وعدم كتابة أي config.

**الثقة/الفائدة:** عالية لمسار المصدر، دون إثبات تشغيل Go؛ متوسطة إلى عالية لفائدة اختبار عبور adapters وعدم الكتابة.

**الاختبار:** ثلاث حالات نموذجية Python نجحت. Go غير متاح؛ لم نشغّل doctor أو suite. CONTRIBUTING يتطلب موافقة maintainer وتعيين مسؤول قبل التنفيذ؛ لم نفتح PR أو ننفذ patch للمشروع.

## الاستبعادات الموثقة

- https://github.com/a2aproject/a2a-dotnet/issues/551 — Author's PR #552 already covers JSON response handling/tests; no additive reply.
- https://github.com/UKGovernmentBEIS/inspect_ai/issues/5891 — Author's PR #5893 covers alias fix and tests; no duplicate advice.
- https://github.com/crewAIInc/crewAI/issues/8216 — PR #8217 plus existing detailed comment already covers pagination and repeated cursors.
- https://github.com/agentscope-ai/agentscope/issues/3337 — Assigned to reporter; source-level BOM remedy already explicit, no additional value.
- https://github.com/openJiuwen-ai/agent-runtime/issues/271 — Reporter supplies exact newline fix and reproduction; mirrored GitCode issue; no incremental source investigation.
- https://github.com/winsznx/routedock/issues/570 — Fix outline already detailed and contributors volunteering; no distinct added value this round.

البحث في PRs للمختارين لم يظهر إصلاحًا مرتبطًا بالرقم؛ timelines فارغة عند الفحص. هذا فحص للحالة المتاحة وليس ضمان عدم وجود عمل خاص أو PR غير مرتبط.

## المتابعة — الجديد فقط

1. **إقرار تقني مباشر:** [parisbs في #143](https://github.com/parisbs/codex-subagent-mcp/issues/143#issuecomment-6201356227)، 2026-10-15T20:14:15Z. شكر مراجعة الحساب صراحة، وذكر نقل مبدأ مصدر إعدادات واحد، واختبار إعدادين معًا، وعدم وصف fallback كإعداد صالح إلى [#180](https://github.com/parisbs/codex-subagent-mcp/issues/180). أُغلقت #143 لصالح البديل؛ لا طلب خدمة أو شراء.
2. **Trinity:** [تحديث الدمج](https://github.com/Abilityai/trinity/issues/3749#issuecomment-6186662739)، 2026-10-15T07:15:00Z. تحققنا من API أن [PR #3750](https://github.com/Abilityai/trinity/pull/3750) مدموج فعلًا إلى `dev` عند `f5fc04fb07afcd6ea62e991016d33849fa9107f1` في 07:13:57Z. أرقام اختبارات PR تخص المساهم وليست اختباراتنا. القبول الحي بعد deploy ما زال مطلوبًا حسب المساهم؛ البلاغ ما زال مفتوحًا. لا دليل يثبت أن تعليقنا سبب الإصلاح.
3. **LumenRoute #8:** اكتملت المسألة بواسطة `chief197` وفق أحداث البرنامج وأُغلقت. هذه مساهمة شخص آخر وليست عميلًا أو مكسبًا لـNAIF. حُدث المؤشر إلى `6195420882` لمنع إعادة إعلانها.
4. لا رد لاحق على تعليقنا في VS Code أو A2A Python. لا تعليق جديد في سلاسل المتابعة الثماني الأخرى.

### توثيق التعليقات اليدوية السابقة

- [VS Code — 6184978396](https://github.com/microsoft/vscode/issues/341683#issuecomment-6184978396)، 2026-10-15T05:15:04Z.
- [A2A Python — 6184993589](https://github.com/a2aproject/a2a-python/issues/1341#issuecomment-6184993589)، 05:16:16Z.
- [Trinity — 6185031732](https://github.com/Abilityai/trinity/issues/3749#issuecomment-6185031732)، 05:19:23Z.

حُفظت روابطها وحالة النشر ومؤشرات آخر تعليق. تاريخ R2 يبقى موثقًا كما حدث وقت الجولة؛ لا يُعاد احتساب هذه المنشورات كعمل نشر آلي اليوم.

## تصحيح دقة الجولة السابقة

- **VS Code:** البلاغ المعدّل يفصل بين redirect وبين تفاصيل v0.1 التي تفتقد packages/remotes؛ صلة ذلك بعطل التعطيل بعد restart لم تثبت. ثقة R2 العالية كانت أوسع من الدليل. اقتراح slash retry يخص عرض التحويل فقط ولا يثبت إصلاح التعطيل عمومًا. لا حاجة لتكرار التعليق.
- **A2A Python:** عبارة R2 التي وصفت كل القراءة بأنها ParseDict غير دقيقة: REST SSE يستخدم Parse. التعليق الذي نشره المستخدم يوضح هذا التمييز بصورة صحيحة.
- اختبارات R2 الاصطناعية تبقى نماذج حدود وليست إثبات إصلاح كامل.

## أدوات NAIF وحدودها

قُرئت https://naifgravity.com/tools وREADME الحالي للمستودع التشخيصي (blob `23361889ae17a26240b25bfdadadfb1a38363bc8`). أدوات الصفحة للفحص المحدود لوصول endpoint عام وبنية JSON المنقحة؛ ليست مدقق توقيع. المسبار يختبر تفاوض MCP/listing محدودًا ولا يدعم OAuth login أو stdio أو إصلاح A2A. لا تطابق مباشر مع الحالات الثلاث؛ لم ندرج روابط دعائية في الردود أو نقترح مدفوعًا.

## النشر والتحقق والقيود

تقتصر تغييرات هذه الجولة على README وledger وتقارير هذه الجولة داخل `docs/problem-hunter-v1/`. فُحص AGENTS.md (دليل onboarding قديم لمكافآت مستودع آخر، لا تعليمات إضافية لهذه الوثائق)، وشجرة الملفات كاملة لا تحتوي AGENTS متداخلًا. روجعت ملفات workflows الثمانية عند base `e038bf760a48516c17cb81285f779fa068ffde62`: push paths لا تشمل هذه الوثائق. لا workflow جرى تشغيله أو تغييره.

التحديث الذري يستخدم parent SHA حديثًا وexpected_sha وforce:false؛ نتيجة commit تُعرض في رسالة الجولة بعد التحقق. الاختبارات كاملة وحدودها وسكربتات إعادة إنتاجها في [TESTS.md](TESTS.md).

- محاولة hash أولى توقفت بسبب newline إضافي أدخله حفظ patch المحلي؛ أزيلت الزيادة فقط بعد مطابقة Git blob، ثم نجحت إعادة التشغيل. لم يُنفذ كود غير مطابق.
- لا Go أو Crystal؛ لا ادعاء باجتياز suites.
- لا اختبار على الإنتاج أو أي نظام خارجي، ولا أسرار أو رموز حقيقية أو مفاتيح أو مدفوعات أو تغيير خادم/V5.
- لا اهتمام تجاري صريح مثبت؛ الشكر التقني ليس طلب شراء.
- المطلوب من المستخدم فقط: مراجعة النصوص الثلاثة وإقرار الردود التي يريد نشرها، إن أراد. لا إجراء عاجل آخر.

## تحديث لاحق — نشر يدوي مؤكد في 16 أكتوبر

بعد انتهاء الجولة، نشر المستخدم رد R3-01 بنفسه في [AGNT #169](https://github.com/agnt-gg/agnt/issues/169#issuecomment-6208715705) عند 2026-10-16T05:23:05Z (08:23:05 بتوقيت السعودية). تأكد الحساب `naief9961-tech` والنص عبر GitHub، وحُدث سجل النشر ومؤشر `last_seen_comment_id` إلى `6208715705`. لم يظهر رد لاحق عند التحقق؛ لا اهتمام تجاري مثبت. هذا نشر يدوي لاحق، ولا يغيّر عدد منشورات التشغيل المجدول (صفر). تبقى R3-02 وR3-03 مسودتين للمراجعة.

### تحديث النشر اليدوي الثاني

نشر المستخدم R3-02 في [Noir #3078](https://github.com/owasp-noir/noir/issues/3078#issuecomment-6208753257) عند 2026-10-16T05:26:11Z (08:26:11 بتوقيت السعودية). تأكد النص وحساب `naief9961-tech` عبر GitHub؛ حُدث السجل ومؤشر آخر تعليق إلى `6208753257`. لا رد لاحق أو اهتمام تجاري ظاهر. تبقى R3-03 للمراجعة؛ لا تعليق آلي أُرسل.


## تحديث توثيق النشر اليدوي — 16 أكتوبر 2026، الجولة R4

تأكد نشر R3-03 يدويًا من حساب naief9961-tech. [التعليق الظاهر حاليًا في Engram #1899](https://github.com/Gentleman-Programming/engram/issues/1899#issuecomment-6208832958) أُنشئ 2026-10-16T05:32:58Z (08:32:58 السعودية). لوحظ أولًا التعليق 6208777198 عند 05:28:14Z، ثم غاب عن قائمة التعليقات اللاحقة؛ حُفظت الملاحظتان دون تخمين سبب التغيير. مؤشر المتابعة الحالي 6208832958. أصبح نشر ردود R3 الثلاثة موثقًا يدويًا؛ لا رد مطور لاحق أو اهتمام تجاري ظاهر عند إعادة الفحص. [تفاصيل R4](../2026-10-16-R4/REPORT.md). لم يرسل الوكيل تعليقًا خارجيًا.
