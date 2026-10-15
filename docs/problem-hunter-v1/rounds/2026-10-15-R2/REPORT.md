# الجولة الثانية — 15 أكتوبر 2026

> **الحالة:** تحقيق موثق ومقترحات إصلاح. لم يُنشر أي تعليق أو PR في مستودعات الآخرين. الردود الثلاثة في [DRAFTS.md](DRAFTS.md) تنتظر موافقة المستخدم.

## نطاق الجولة

- الفرز الأولي: **393** رابط مشكلة فريد من استعلامات MCP/A2A/x402/API/Webhooks/JSON/Schema/GitHub Actions، مع أولوية لما نُشر خلال 24–72 ساعة.
- القراءة الكاملة: **12** بلاغًا فريدًا مع التعليقات المتاحة.
- التحقيقات المختارة المكتملة: **5** مع قراءة المصدر وتثبيت SHA والتحقق من PRs المرتبطة.
- المتابعة: **10** سلاسل سابقة؛ لا تعليق أحدث من `last_seen_comment_id`.
- الاختبار: **5** اختبارات حدود اصطناعية معزولة نجحت. لم تُشغّل حزم الاختبار الكاملة لأي مشروع خارجي.
- تحقق PR: لا PR مرتبط ظاهر للخمسة المختارين. استُبعد `turnstonelabs/turnstone#1391` بعد ظهور PR #1395 الذي يعالج حد 16 MiB، واستُبعد `LanternOps/breeze#8798` لأن السجل الجاري يشير صراحة إلى PR خاص به.

## أفضل خمس مشكلات

### 1) [microsoft/vscode#341683](https://github.com/microsoft/vscode/issues/341683) — سجل MCP على GitHub Pages

- المبلّغ: `Yamano-Yuki`؛ مفتوحة منذ 2026-10-15 04:48Z؛ بلا تعليقات عند الفحص.
- الدليل: عند SHA [`9ebdca5c...`](https://github.com/microsoft/vscode/tree/9ebdca5c15f666ab336ca0b0421f5ee25bf1cbe0)، يتحقق `getMcpServerUrlInGallery()` من الأصل ومسار السجل ثم يستدعي `getMcpServer()` الطلب مع `followRedirects: 0` في [mcpGalleryService.ts](https://github.com/microsoft/vscode/blob/9ebdca5c15f666ab336ca0b0421f5ee25bf1cbe0/src/vs/platform/mcp/common/mcpGalleryService.ts).
- التشخيص: رابط الدليل بلا الشرطة الختامية يصطدم بتحويل GitHub Pages إلى المسار القانوني؛ منع التحويلات يجعل الاستجابة غير قابلة للاستخدام، وقد تظهر في renderer بالحالة 0.
- الإصلاح: إعادة محاولة واحدة فقط بإضافة `/`، ثم إعادة فحص الأصل ومسار السجل، مع إبقاء `followRedirects: 0`.
- Regression: canonical slash، عدم تكرار الرابط القانوني، 404، أخطاء 401/403/429/5xx، ومنع التحويل خارج الأصل/المسار.
- الثقة/الفائدة: **عالية / عالية**.
- الاختبار: تحقق اصطناعي لنفس الأصل ومسار السجل نجح؛ لم يُعاد إنتاج opaque response ولم تُشغّل حزمة VS Code.

### 2) [a2aproject/a2a-python#1341](https://github.com/a2aproject/a2a-python/issues/1341) — رفض حقول A2A الجديدة

- المبلّغ: `fpt-long-hd`؛ مفتوحة منذ 2026-10-15 03:28Z؛ بلا تعليقات.
- الدليل: عند SHA [`a4c4fc91...`](https://github.com/a2aproject/a2a-python/tree/a4c4fc91a22778f3d805e5e592bf690915a33033)، كل مسارات الاستجابة في [jsonrpc.py](https://github.com/a2aproject/a2a-python/blob/a4c4fc91a22778f3d805e5e592bf690915a33033/src/a2a/client/transports/jsonrpc.py) و[rest.py](https://github.com/a2aproject/a2a-python/blob/a4c4fc91a22778f3d805e5e592bf690915a33033/src/a2a/client/transports/rest.py) تستخدم `ParseDict` الصارم.
- التشخيص: السياسة الصارمة تشمل unary وstreaming وTask/list/push-config/card، فتخالف قابلية التوسع الواردة في spec 5.7.
- الإصلاح: helper مركزي لقراءة الاستجابة مع `ignore_unknown_fields=True` فقط في جهة العميل المستقبِلة.
- Regression: JSON-RPC وREST وSSE، حقول عليا ومتداخلة، وبقاء الحقول المعروفة غير الصحيحة مرفوضة، وتوثيق سلوك enum غير المعروف.
- الثقة/الفائدة: **عالية / عالية**.
- الاختبار: نموذج parser اصطناعي strict/ignore نجح؛ إعادة SDK المباشرة تعذرت لغياب `google.protobuf`؛ لا suite upstream.

### 3) [Abilityai/trinity#3749](https://github.com/Abilityai/trinity/issues/3749) — ضياع نتيجة A2A الطويلة

- المبلّغ: `vybe`؛ مفتوحة منذ 2026-10-15 04:06Z؛ بلا تعليقات.
- الدليل: عند SHA [`43576279...`](https://github.com/Abilityai/trinity/tree/43576279b43d27cca67559a66f47f33e6ddedb56)، [a2a.py](https://github.com/Abilityai/trinity/blob/43576279b43d27cca67559a66f47f33e6ddedb56/src/backend/routers/a2a.py) ينتظر `dispatch_and_await_terminal` كاملًا قبل إرجاع id، بينما `tasks/get` يترجم أصلًا running/queued إلى working/submitted.
- التشخيص: مسار poll موجود لكن `message/send` لا يسلم المقبض قبل مهلة عميل 30 ثانية.
- الإصلاح: فصل durable dispatch عن الانتظار، تثبيت الملكية/الدافع فور إنشاء التنفيذ، انتظار shielded بميزانية أقل من العميل، وإرجاع الحالة الحالية؛ تخزين idempotency كـ messageId→executionId وعدم كتابة audit نهائي عند الرد المبكر.
- Regression: fast path مطابق، slow path، bearer/AAuth/paid ownership، replay في الحالتين، disconnect، وعدم مضاعفة audit.
- الثقة/الفائدة: **عالية / عالية**.
- الاختبار: asyncio اصطناعي أثبت أن shielded task يستمر بعد مهلة الخادم؛ لم تُشغّل DB/billing/audit integrations.

### 4) [php-mcp/laravel#50](https://github.com/php-mcp/laravel/issues/50) — جلسة منتهية تتحول من 404 إلى 500

- المبلّغ: `gms8994`؛ مفتوحة منذ 2026-10-15 01:08Z؛ بلا تعليقات.
- الدليل: عند SHA [`39c23334...`](https://github.com/php-mcp/laravel/tree/39c233348dbea594305da56ffc4ef03036fc226f)، [StreamableHttpServerTransport.php](https://github.com/php-mcp/laravel/blob/39c233348dbea594305da56ffc4ef03036fc226f/src/Transports/StreamableHttpServerTransport.php) يرسل عبر queue ثم يحوّل القائمة الفارغة إلى 500. وفي [php-mcp/server 3.3.0 SessionManager.php](https://github.com/php-mcp/server/blob/3.3.0/src/Session/SessionManager.php) تعود `queueMessage` بصمت إذا لم توجد الجلسة.
- التشخيص: خطأ 404 الصحيح يعتمد على queue لا تقبل session منتهية، فيُفقد ثم يُصنع 500.
- الإصلاح: فحص session في transport قبل queue-based JSON response وإرجاع 404 JSON-RPC مباشرة؛ يفضل عدم توسيع SessionManager إلى طابور مؤقت.
- Regression: invalid/expired id، جلسة صحيحة، initialize، JSON mode وSSE mode، والتحقق من عدم كتابة log مضلل.
- الثقة/الفائدة: **عالية / عالية**.
- الاختبار: نموذج state-machine اصطناعي أعاد drop→500 والإصلاح→404؛ لم تُشغّل Laravel/PHP tests.

### 5) [tidynotebook/tidynotebook#389](https://github.com/tidynotebook/tidynotebook/issues/389) — Bearer challenge ناقص

- المبلّغ: `bkhanale`؛ مفتوحة منذ 2026-10-15 04:50Z؛ بلا تعليقات.
- الدليل: عند SHA [`c92e2324...`](https://github.com/tidynotebook/tidynotebook/tree/c92e23248770b04fba5c246684460a8250252f60)، [protocol.ts](https://github.com/tidynotebook/tidynotebook/blob/c92e23248770b04fba5c246684460a8250252f60/apps/server/src/mcp/protocol.ts) يضيف `error="insufficient_scope"` للـ403، لكنه يستخدم فرع 401 واحدًا للحالة المفقودة والرمز غير الصالح ولا يضيف `invalid_token`.
- التشخيص: missing credentials وinvalid/expired/revoked token مدمجة في helper واحد رغم اختلاف RFC 6750.
- الإصلاح: challenge kind صريح: missing بلا error، invalid/expired/revoked مع `invalid_token`، scope مع `insufficient_scope`.
- Regression: مصفوفة الحالات الخمس مع body/status/header.
- الثقة/الفائدة: **عالية / متوسطة-عالية**.
- الاختبار: مصفوفة header اصطناعية نجحت؛ لم تُشغّل Fastify/integration suites.

## الردود الجاهزة للمراجعة

- `R2-01`: VS Code — إعادة محاولة canonical slash آمنة مع اختبارات SSRF/redirect.
- `R2-02`: A2A Python — توحيد parse leniency وتغطية كل transports.
- `R2-03`: Trinity — hand-off دائم، ownership، idempotency، audit.

النصوص الإنجليزية الكاملة في [DRAFTS.md](DRAFTS.md). حالتها `PENDING_USER_APPROVAL`، ولم تُرسل.

## المتابعة والفرص

- فُحصت سلاسل المتابعة العشر المسجلة. **لا رد جديد** بعد آخر `last_seen_comment_id`، لذلك لم يتغير أي cursor.
- **لا اهتمام تجاري صريح ولا طلب شراء** في هذه الجولة.
- لم تُقترح خدمة مدفوعة.
- روجعت [صفحة الأدوات المجانية](https://naifgravity.com/tools) وREADME للمسبار عند `28f09cc8...`. لم نضع رابطًا في الردود: أدوات الويب تفحص reachability/headers أو JSON sanitized فقط، ومسبار MCP لا يدعم stdio أو OAuth ولا يصلح A2A أو هذه الإصلاحات المصدرية.

## ما نُشر في مستودعاتنا

هذه الجولة تحدّث README و`ledger.json` وتضيف هذا التقرير ومسودات الردود تحت `docs/problem-hunter-v1/rounds/2026-10-15-R2/`. لا workflow يُشغّل على تغييرات هذا المسار وفق triggers الحالية. لم يتغير production أو الدفع أو V5 أو server أو workflows.

## القيود

- تعذر تشغيل إعادة A2A Python المباشرة لعدم توفر `google.protobuf` محليًا؛ سُجلت محاولة الاستيراد الفاشلة ولم تُحسب PASS.
- البحث في GitHub أعاد ضوضاء وإعلانات كثيرة؛ العدد 393 هو الفرز الفريد، وليس تحقيقًا كاملًا.
- اختبارات الحدود الاصطناعية لا تثبت أن الإصلاح سيعمل داخل المشاريع كاملة.
- لا صلاحية كتابة في المستودعات الخارجية؛ ولم تُحاول أي كتابة خلال هذه الجولة المجدولة.
