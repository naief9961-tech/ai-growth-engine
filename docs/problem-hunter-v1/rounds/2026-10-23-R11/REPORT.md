# NAIF Gravity — R11 — 2026-10-23

## النتيجة

- **156 مشكلة فريدة في الفرز الأولي** من 160 نتيجة مقيدة، عبر 8 استعلامات. لا تمثل بحثًا شاملًا في GitHub.
- **6 بلاغات قُرئت بالكامل** مع التعليقات والتحديثات؛ **تحقيق مصدر مكتمل واحد** وفحص استكشافي إضافي واحد. لا نكمل العدد بخمس حالات ضعيفة.
- **رد إنجليزي واحد جديد جاهز للمراجعة**، ولم يُرسل أي تعليق أو PR أو رسالة إلى مستودعات الآخرين.
- **21 مجموعة تحقق معزولة ناجحة**، شملت 42 تشغيلًا للدالة في المصدر الكامل قبل التعديل وبعده. لا اختبار شامل للنظام أو نشر إصلاح.

## المرشح المختار

### 1. [OpenViking #6471](https://github.com/volcengine/OpenViking/issues/6471)

صاحب البلاغ: **ktz03**. فُتح في 2026-10-23T04:11:07Z، وكان مفتوحًا بلا تعليقات عند آخر قراءة. اكتشاف الجولة: 2026-10-23.

السبب: `isRequest()` يكتفي بوجود `id`. لذلك يعامل استجابة العميل كطلب، ويرسل خطأ إضافيًا سواء عادت HTTP 202 فارغة أو فشل النقل. المصدر المثبت: [mcp-proxy-core.mjs](https://github.com/volcengine/OpenViking/blob/0d546854b4be4b24a277c1b3ca7cf06c02d61a14/examples/memory-plugin-shared/lib/mcp-proxy-core.mjs) عند SHA `0d546854b4be4b24a277c1b3ca7cf06c02d61a14`، خصوصًا الدالة عند السطر 68 وفرعي كتابة الأخطاء عند 459 و467.

القيمة الجديدة: البلاغ الأصلي عرض استجابة نجاح و202؛ تحققنا أيضًا من استجابات الخطأ و403 و500 وخطأ إلغاء اصطناعي. ثبت السلوك الخاطئ في 16 حالة استجابة. حافظت خمسة اختبارات ضابطة على الطلب ذي `id: 0` وعلى الإشعارات.

الإصلاح المرشح: يشترط تصنيف الطلب وجود `method` نصية و`id` خاص بالكائن، مع إبقاء إخفاقات تسليم الاستجابة في التشخيص. هذا ليس مدقق JSON-RPC كاملًا. تحديث النسخ المولدة يتم عبر آلية المزامنة الموجودة، لا بتعديلات منفصلة عليها.

الثقة **مرتفعة في السبب والحالات المعزولة**؛ التكامل والجلسات وإعادة المحاولة والإصدار لم تُثبت. فرصة الاستفادة التقنية جيدة لأن الرد يضيف حدود تحقق مستقلة، ولا توجد دلالة تجارية.

فحص PRs: 30 طلبًا حديثًا، و91 نتيجة للاستعلام `repo:volcengine/OpenViking is:pr mcp proxy`، واستعلام مباشر عن 6471 أعاد صفرًا. لا إصلاح مرتبط ظاهر في timeline. هذا لا يعني مراجعة كل PR في المستودع.

- [النص الإنجليزي الكامل للمراجعة](DRAFTS.md)
- [الاختبار القابل لإعادة الإنتاج وحدوده](TESTS.md)
- [نتائج التشغيل الفعلية](results.json)

## حالات استُبعدت أو أُوقفت بعد القراءة

- [vpetersson/agent-iap #118](https://github.com/vpetersson/agent-iap/issues/118): Open PR #119 already supplies the path-join repair and regression controls. Author's live Slack test was not run by us. No duplicate draft.
- [druxt/druxt.js #957](https://github.com/druxt/druxt.js/issues/957): PR #958 merged at 2026-10-23T04:59:07Z (c340e25ec4d710da8d5146bc44970b065b4923d6) during review. Excluded as repaired upstream; tests not independently rerun.
- [strapi/strapi #28196](https://github.com/strapi/strapi/issues/28196): Linked open PR #28197 already proposes shared validation/UI bounds and tests. No duplicate solution or independent test claim.
- [GopherSecurity/gopher-mcp #334](https://github.com/GopherSecurity/gopher-mcp/issues/334): Reporter already provides detailed four-boundary source diagnosis, reproduction and repair design. No distinct lightweight addition established; no native C++/sanitizer build performed. Related closed PR #333 is not asserted to fix these four findings.
- [Yesifan/pi-packages #33](https://github.com/Yesifan/pi-packages/issues/33): Exploratory source mismatch: at main 35c03605cb069a4ed360c9239ea054df208d2052, rpc-server already buffers decoded UTF-8 data and gates dispatch with handled; rpc-client writes LF. This differs from the described per-chunk implementation and PR #32's older client context. Need affected-revision/runtime evidence before proposing a repair. No test or draft; not declared resolved.

لا نجزم بحل Pi #33: المصدر الحالي يختلف عن تنفيذ البلاغ؛ يلزم تثبيت النسخة المتأثرة قبل توصية أخرى. لم تُشغّل اختبارات هذا المشروع.

## متابعة المساهمات

تمت مراجعة **28 سلسلة متابعة**. لا رد جديد على مساهمات NAIF ولا تعليق جديد موثق لنا ولا طلب تجاري صريح.

ظهر [تعليق Paraphern الجديد على Casdoor #5957](https://github.com/casdoor/casdoor/issues/5957#issuecomment-6351091617) في 2026-10-22T20:54:26Z، ويقترح اختبارات توافق لطرق المصادقة المُعلنة. هو **نقاش تقني من طرف ثالث، وليس ردًا علينا**: لم يُنشر تعليق NAIF هناك. رُفع المؤشر إلى `6351091617` لمنع تكرار الإبلاغ. احتُفظ بموافقة R10 وسجل رفض GitHub 403 كما هما، دون إعادة محاولة أو التفاف.

[تفاصيل المتابعة والمؤشرات](FOLLOWUPS.json). لا شكر أو اهتمام تقني محسوب شراءً، ولا فرصة عميل مثبتة في هذه الجولة.

## ملاءمة أدوات NAIF

تمت مراجعة [صفحة الأدوات](https://naifgravity.com/tools) و[README المستودع التشخيصي الحالي](https://github.com/naief9961-tech/naif-gravity-mcp-diagnostics) في 2026-10-23. الأدوات العامة تفحص وصول HTTP أو بنية عينة JSON؛ والمسبار التشخيصي يختبر اكتشاف Streamable HTTP لإصدارات handshake المحددة، ولا يدعم stdio أو OAuth. لا يعيد إنتاج مسار الوسيط المختار، لذلك لم يوضع رابط منتج في الرد ولم تُقترح خدمة مدفوعة.

## تحديث مستودعنا وضوابط التنفيذ

التغييرات المُعدّة للنشر الذري هي README والسجل ووثائق هذه الجولة فقط تحت `docs/problem-hunter-v1/`. قاعدة القراءة `b60744d0a90d166e09c2e4c8e2ca81ce95c14970`؛ يُراجع الرأس مجددًا قبل نقل الفرع مع expected SHA. مرجع النشر الدقيق هو commit الذي أضاف هذا التقرير؛ لا يُعلن نجاحه في المحادثة قبل التحقق.

قُرئ AGENTS.md وشجرة المستودع، وفُحصت ملفات workflow الثمانية. تقتصر مشغلات push على ملفات اكتشاف/manifest أو workflow محددة، ولا تشمل ملفات هذه الجولة. لا تعديل workflow ولا تشغيل يدوي ولا PR. لا إنتاج أو دفع أو V5 أو سيرفر أو إنفاق أو عمل ثقيل.

## العوائق والمطلوب

لا عائق منع التحقيق أو الاختبار المحلي. حدود الإثبات: مصدر Pi لا يطابق البلاغ، وثلاث حالات لها إصلاحات موجودة، والمصفوفة المختارة معزولة وليست اختبار نظام كامل. صلاحيات التعليق السابقة لا تزال مسجلة كعائق؛ لم نختبرها مجددًا في هذه الجولة.

المطلوب من المستخدم لاحقًا: **مراجعة المسودة R11-01 والموافقة عليها إن أراد نشرها**. لا حاجة إلى مفاتيح أو بيانات خاصة. لا يُعد هذا التقرير إذنًا بالنشر.
