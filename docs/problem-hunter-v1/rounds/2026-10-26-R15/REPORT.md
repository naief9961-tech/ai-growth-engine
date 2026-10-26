# R15 — 2026-10-26: فرص إضافية بطلب المستخدم

وقت التحقق: 2026-10-26T05:26:30Z. **حالة ثانية مناسبة للمراجعة: SDRangel #3039؛ لم يُنشر رد خارجي.**

## النتائج

- فُرزت **179 مشكلة فريدة** من 180 نتيجة عبر 6 استعلامات منذ 2026-10-23؛ 104 روابط لم تظهر في فرز R14. هذه أعداد فرز وليست تحقيقات أو تغطية شاملة.
- قُرئت **4 بلاغات بالكامل** مع جميع التعليقات والتحديثات. اكتمل **تحقيق مصدر ثابت واحد**، إضافة إلى قراءة استكشافية لـ Camber استُبعدت بعد اكتشاف تنفيذ قائم.
- **صفر اختبارات تشغيلية** في هذه المتابعة: لا Qt أو pkg-config متاحين. لم تُنشأ اختبارات تحاكي المنطق وتُقدّم كإثبات لإصلاح التطبيق.
- **مسودة إنجليزية واحدة**، ولا حاجة لملء العدد بحالات ضعيفة. لم تُعد متابعة جميع الردود؛ حالة QwenPaw المنشورة ورقم تعليقها محفوظان كما هما.

## الحالة المختارة

[SDRangel #3039](https://github.com/f4exb/sdrangel/issues/3039)، أبلغ عنها melanders-utv في 2026-10-25T19:44:17Z: Copilot يرفض تعريف tune_gain.values بسبب غياب items. راجعنا الرأس 24ac61389837c63dedd61fed762d74d5860c3430.

الدليل: prop يضع type وdescription فقط، وتسجيل tune_gain يستخدمه لإنشاء values، ثم listTools يعيد المخطط دون تعديل. يوجد في scan نمط جاهز لإضافة items.type=number. إضافة جديدة للتحقق: toolsdump.cpp يأخذ نفس listTools وCMake يولد server/tools.json للحزمة؛ يجب التحقق من التعريف المباشر والمرفق معًا.

الإصلاح المرشح: إنشاء gainValues وإضافة items.number مع إبقاء الوصف وكون values اختياريًا، ثم توليد الملف المرفق مجددًا. هذا توافق مع العميل؛ [JSON Schema العام يسمح بمصفوفة دون items](https://json-schema.org/understanding-json-schema/reference/array).

الثقة عالية في سبب المخطط ومسار توليد الحزمة من المصدر؛ نجاح البناء والعميل غير مثبت. لا اختبار Copilot، أو خادم حي، أو عتاد راديو، ولا تشغيل أدوات تغيّر إعداداته.

- [plugins/feature/mcpserver/mcptools.cpp](https://github.com/f4exb/sdrangel/blob/24ac61389837c63dedd61fed762d74d5860c3430/plugins/feature/mcpserver/mcptools.cpp) — blob 4b7992bbac4d7e6e5e71a7a923c3fd74c99ed702
- [plugins/feature/mcpserver/toolsdump.cpp](https://github.com/f4exb/sdrangel/blob/24ac61389837c63dedd61fed762d74d5860c3430/plugins/feature/mcpserver/toolsdump.cpp) — blob 5e5c886e8bae89bdd963cdb9813d4d8697157ebf
- [plugins/feature/mcpserver/bridge/CMakeLists.txt](https://github.com/f4exb/sdrangel/blob/24ac61389837c63dedd61fed762d74d5860c3430/plugins/feature/mcpserver/bridge/CMakeLists.txt) — blob 10b89c41a876d944c4010e2a77572fd62dfed8f4

فُحص الوصف والتعليقات والتحديثات مرتين؛ لا تعليقات أو PR مرتبط في السجل. بحث MCP أعاد ستة PRs؛ البحث برقم البلاغ وبـ tune_gain لم يُعد إصلاحًا. هذه حدود البحث وليست ادعاء فحص جميع PRs.

## المستبعدون

- [Code-Hex #1622](https://github.com/Code-Hex/graphql-codegen-typescript-validation-schema/issues/1622): دعوة ترويجية، لا خطأ تقني.
- [CyberChain #2](https://github.com/bisite/cyberchain-smart-contract-wrapper/issues/2): مساهم آخر نشر بالفعل التشخيص وإعادة الإنتاج واختبارات IDs؛ لا نكرر.
- [Camber #300](https://github.com/yroussev/camber/issues/300): [PR #305](https://github.com/yroussev/camber/pull/305) قيد العمل ويحتوي الإصلاح وتحديث اختبارات البروتوكول؛ ليس إصدارًا مثبتًا ولم نُعد اختباراته.

## النشر والمتابعة

[النص الإنجليزي الكامل](DRAFTS.md) و[خطة التحقق غير المنفذة](CHECKS.md). بانتظار موافقة منفصلة؛ لا تعليق أو PR خارجي أُرسل. لا اهتمام تجاري مثبت في الحالة المختارة ولا طلب شراء. لا أداة NAIF موصى بها لأن الحاجة هنا تعديل تعريف C++ والتحقق من توافق العميل.

تحديث docs/problem-hunter-v1/ فقط، على الرأس 9026b914512a87ede0bedee75b258cabc16179f2. أعيد التحقق من أن AGENTS.md وworkflows الثمانية لها نفس SHA التي فُحصت في هذه الجلسة؛ لا push trigger يطابق هذه الوثائق. لا تغيير أو تشغيل workflows، أو إنتاج/دفع/V5/سيرفر، أو إنفاق.

المطلوب من المستخدم: مراجعة R15-01 فقط إن أراد المساهمة. عدم توفر بيئة Qt يمنع ادعاء اختبار الإصلاح.
