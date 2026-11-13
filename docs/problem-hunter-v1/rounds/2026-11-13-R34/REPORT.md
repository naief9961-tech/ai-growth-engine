# R34 — تحقيق موجّه إضافي، 13 نوفمبر 2026

طلب المستخدم مشكلة أخرى بعد R33. الأساس: `2bd1d833d4c2c52e3210a127e5b744d7ed02ecdf`. وقت التحقق 2026-11-13T05:12:10Z.

## النتيجة
58 بلاغًا فريدًا من60 نتيجة في3 استعلامات محدودة بأحدث20 لكل منها؛ قراءة ثلاثة بلاغات وتعليقاتها وتحديثاتها بالكامل؛ تحقيق واحد مع9 مجموعات تحقق معزولة ناجحة. رد واحد للمراجعة؛ لا نشر لدى الآخرين ولا طلب تجاري. لم نكرر فحص48 متابعة الذي اكتمل قبل دقائق فيR33.

## المختارة: Microsoft APM #3711
[البلاغ](https://github.com/microsoft/apm/issues/3711) — DimashOne، أنشئ 2026-11-13T04:46:14Z، مفتوح. غير مسجل سابقًا.

**تصحيح مهم:** أثناء التحقيق أضاف صاحبه [تعليق6844713314](https://github.com/microsoft/apm/issues/3711#issuecomment-6844713314)، يؤكد أن مسار .agents/mcp_config.json يعمل وأن تحويل httpUrl إلى url عالج اتصاله. لم نكرر هذه المعلومة كاكتشاف لنا. [التوثيق الرسمي الحالي](https://antigravity.google/docs/mcp#global-and-workspace-server-configs) يوافق على المسار ويدعم serverUrl أو url للـStreamable HTTP، ولا يدعم SSE القديم. لا ندعي تاريخ إصدار دعم المسار أو اختبار نسخة صاحب البلاغ.

**الإضافة:** Antigravity يرث formatter الخاص بـGemini كاملًا، ولذلك يقبل transport_type=sse ويخرجه url رغم أن Antigravity CLI لا يدعم هذا البروتوكول. ينبغي أن يكون التغيير خاصًا بـAntigravity، مع رفض SSE المحدد برسالة واضحة والمحافظة على سلوك Gemini الذي يميز SSE/url وHTTP/httpUrl. تغيير اسم المفتاح لا يغير بروتوكول السيرفر.

المصدر عند `4782e389daf2b05f9fd762a65dec8c0cdade5177`: base.py وgemini.py وantigravity.py؛ قائمة SHA للملفات داخل [TESTS.md](TESTS.md). قُرئت اختبارات test_antigravity_target.py القائمة؛ تغطي المسار والكتابة الذرية، ولم نُشغّلها. الثقة عالية في ملاحظة التحويل؛ تكامل CLI غير مثبت.

[النص الكامل للمراجعة](DRAFTS.md). اقتراح محدود مع تجربة محلية، وليس PR جاهزًا للدمج. CONTRIBUTING.md يسمح بالتحقيق والنقاش، ويطلب موافقة مشرف بشري على نطاق التنفيذ قبل إدراج تغيير جوهري؛ لا نشر أو تنفيذ في مستودعهم.

## التحقق وحدوده
تسع مجموعات: http، streamable-http، transport فارغ، transport محذوف، sse، نوع غير مدعوم، stdio بأمر اصطناعي ومعاملات فارغة، مسار المشروع، مسار المستخدم. المصدر الأساسي يكرر المفتاح غير المدعوم وقبول SSE؛ المرشح المحلي يغيّر نتيجة الحالتين، مع ضوابط Gemini وبقاء المسارين.
Python3.12.14؛ AST extraction للطرائق الفعلية ومساعدي الاختيار/دمج إضافات فارغة؛ تحقق Git blob hashes. لا إنشاء عميل سجل أو تشغيل أوامر أو اتصال. أول تجميع للحاضنة أخفق لأنه بحث عن ثابت مستورد داخل الملف؛ أُزيل البحث غير المستخدم ثم نجحت المجموعات التسع. هذا خطأ حاضنة، لا عيب جديد في المنتج.
لم يُختبر agy أو الحزمة الكاملة أو headers/env أو _extra payloads أو stdio من سجل الحزم أو كتابة إعدادات أو اكتشاف أدوات حي. تفاصيل إعادة الإنتاج محفوظة.

## فحص PRs ومنع التكرار
13 عنوان PR مفتوح؛ بحث جميع الحالات عن Antigravity أعاد34 وعن httpUrl أعاد2، وعن3711 صفر عند إعادة الفحص. راجعت تغيير gemini.py فيPR3709 وPR3672؛ يتناولان سلامة الكتابة/تسمية مساعد، ولا يضيفان تحويل Antigravity المستهدف. فهرسا الملفات مقيدان بأول100 عنصر؛ لا ادعاء مسح كامل لكل PR تاريخي. تسلسل البلاغ وتعليقه الوحيد قُرئا مرة أخرى قبل الحفظ، ولا تعليق لنا.

المستبعدان بعد القراءة الكاملة:
- [GAIA #7972](https://github.com/amd/gaia/issues/7972): تعليقات موجودة تشير إلى تكرار7335 وإصلاح7536؛ لا إضافة.
- [GAIA #7969](https://github.com/amd/gaia/issues/7969): تشخيص موجود حول مهلة npx وتزامن التثبيت؛ لا إثبات جديد على Windows.

## النشر
وثائق داخل docs/problem-hunter-v1 فقط مع تحديث ذري وexpected SHA. AGENTS.md وworkflows الثمانية تطابق SHA التي راجعت فيR33؛ مسارات push لا تشمل الوثائق. لا workflow يدوي، لا تغييرات متجر أو إنتاج أو دفع أوV5 أو سيرفر، ولا إنفاق. لا إحالة إلى أدوات NAIF لأن ملاءمتها غير متحققة لهذه المشكلة.

## Search inventory (initial screening only)

Queries: is:issue is:open created:>=2026-11-10 with (MCP AND bug), (webhook AND retry), (schema AND error); sort created desc, top20 each. Not an exhaustive search. Unselected search entries are not completed investigations.

- [Invite picker no longer lists owner's Sutando agent @sutando-huazhengwang:s.space](https://github.com/sonichi/sutando/issues/6413)
- [Resume rebuilds the request prefix from current files, causing full prompt-cache misses; replay the persisted prefix and append diffs instead](https://github.com/can1357/oh-my-pi/issues/19121)
- [(Bug) Shell Link pre-1970 fractional timestamps round into the following millisecond](https://github.com/morluto/rea/issues/10303)
- [The MCP lockfiles resolve vulnerable hono packages](https://github.com/OpenRAE/lilrae/issues/1771)
- [QA run · touched:5fb79bc0 (70/147) · ee9ad834 · 2026-11-13 · 56 PASS / 9 PARTIAL / 5 FAIL / 0 BLOCKED / 77 NOT-RUN](https://github.com/objectstack-ai/objectstack/issues/33025)
- [(Stunna / iPhone UX) Render strength warm-ups outside narrow Set column](https://github.com/New2Dis12/eric-health-hub/issues/38)
- [虚拟屏跑真实脚本实测（v1.2.0）：input 无焦点谎报成功、虚拟屏双建、过渡帧双层等 5 项（附微信 OCR 脚本）](https://github.com/BUGJI/IzukiJS/issues/28)
- [ci: the PyPI publish job fails to create the GitHub release after a successful upload](https://github.com/assistant-ui/assistant-ui/issues/10543)
- [(BUG) Antigravity target writes project MCP config to ignored path and uses unsupported httpUrl key](https://github.com/microsoft/apm/issues/3711)
- [Return else.bot-side MCP failures in the same JSON envelope as results](https://github.com/else-bot/else/issues/327)
- [(Bug): Scheduled routine cannot consistently access enabled Brave MCP tool](https://github.com/nightly-labs/openbot/issues/8709)
- [Proxx Specs: Breakdown, Priorities & Roadmap](https://github.com/open-hax/proxx/issues/525)
- [Agent evals and agent telemetry (dsh evals, trace contract, OpenObserve)](https://github.com/ycchoo28/garden/issues/9)
- [PR review follow-up: #146 — Close tracker follow-ups: doctor handshake, flag combos, merge_json safety, guard docs, statusline omp, CI](https://github.com/bitskc/jev-agent-kit/issues/160)
- [Tracking: CPA Accordion v1 (Accordion as a CLIProxyAPI plugin)](https://github.com/aadityad12/Accordion/issues/2)
- [Runner 容器对宿主机无资源上限 + 残留进程 sweep 漏 ruby —— 单个 Flutter job 能拖垮宿主机](https://github.com/baizhiheizi/gh-sr/issues/640)
- [Cycle 0127: a reduxjs/redux library test is explained live, saved and replayed in both editors (P03 L, R)](https://github.com/laststance/codebook/issues/323)
- [`gaia mcp code-index` started in the home folder exits with a raw Python traceback](https://github.com/amd/gaia/issues/7972)
- [Memory MCP connector never starts on a first connect: 'mcp-server-memory is not recognized', and Personalize then claims](https://github.com/amd/gaia/issues/7969)
- [(Bug) 本地 CLI Agent：选项/审批回答后不开启新回合；steer 缺 expectedTurnId 且失败被静默吞掉](https://github.com/Fei2411/DS-Bot/issues/1513)
- [(Aspire South) TEST sponsor checkout — public donor capability and secure integration plan (planning only)](https://github.com/Aspirefutbol/aspire-raffle-hub/issues/46)
- [delcore: stop a failed-payment subscription intent from blocking deletion](https://github.com/delinoio/apps/issues/1539)
- [Start the API server when an admission webhook for a bootstrap object is unreachable](https://github.com/garamsh/gaon/issues/242)
- [Roadmap: notify administrators when AI is enabled but the saved API key is missing or cannot be decrypted (roadmap A/J producer)](https://github.com/StealthCat/MrPatchy/issues/769)
- [Spec: consumer contract, so every app uses t6-core for Notion, LLM, privacy, Frame.io, Resolve and the fleet](https://github.com/mclbautista/t6-core/issues/115)
- [App Integrations: "app only" mode — no AI-agent fallback when the app webhook is unreachable](https://github.com/chattermate/chattermate.chat/issues/454)
- [forge-cli test: webhook gh stub uses GNU-only stat -c (macOS fails)](https://github.com/sympoies/nils-cli/issues/3652)
- [Import forwarded store receipts by email](https://github.com/Sussman-Club/group-split/issues/521)
- [design(pm-orchestration): leases, fencing, transactional outbox & direct verified completion](https://github.com/developing-today/code/issues/9209)
- [design(pm-orchestration): direct dispatch, slash commands & event routing](https://github.com/developing-today/code/issues/9203)
- [(Lion BI Pass 5 / B) QuickBooks and Outlook end-to-end sandbox reconciliation](https://github.com/Hectorg0827/SecretaryAI/issues/116)
- [(Feature): Prepare a PR review workspace and open its linked Linear issue on review requests](https://github.com/stablyai/orca/issues/41780)
- [(BE) Implement Near-Expiry Discount Pricing](https://github.com/hoaifpt/Fruit_Vending_Machine/issues/61)
- [P0→P1 | Assistente inteligente autenticado, trilha auditável, funil e Mercado Pago — plano faseado](https://github.com/hrq16000-a11y/encontreumtecnico/issues/261)
- [(Bug)(WhatsApp)(NyxBot) Reply is delivered, then subsequent plain-text messages remain unanswered](https://github.com/ChronoAIProject/NyxID/issues/2434)
- [Audit Quokka AI architecture and design Claude vs OpenAI evaluation (investigation only)](https://github.com/ryakel/boomerang/issues/1018)
- [feat(shipping): Biteship Sandbox Booking v0.2 — fail-closed SBX booking & reconciliation](https://github.com/one2pret/onetone-store/issues/73)
- [(FIN-02)(P2) Domínio de pagamentos, PSP, webhook assinado e conciliação](https://github.com/FATEC-BOYS/sansa-os-backend-/issues/16)
- [(FEAT): Build Outgoing Webhook Notification Gateway with HMAC Signatures and Exponential Retries](https://github.com/code-with-abhi-i5/CodePulse/issues/163)
- [(MOD-007 / M7-01b1 BUILD) Strict read-only POS products, customer directory and standing adapters + tests](https://github.com/shuvodelux-commits/hisabiq_ui/issues/394)
- [feat(resume): clamp role summaries to four lines and show "More" only when cut](https://github.com/juliolmuller/portfolio/issues/47)
- [feat(frontend): add the page resolver and named layouts](https://github.com/yutna/rafelo/issues/226)
- [MCP query_dataset with an empty selection.measures reaches the SQL driver and answers 500 DATABASE_ERROR, while the REST twin refuses it 400](https://github.com/objectstack-ai/objectstack/issues/33028)
- [(리팩토링) RAG generation 계약과 실제 형식 테스트의 소유 분리](https://github.com/Kims-DeveloperGroup/story-writing-agents/issues/1025)
- [(DocDB) Object lock release for a finished DDL transaction can be lost on master leader change](https://github.com/yugabyte/yugabyte-db/issues/37808)
- [Look up: fill in missing band details from public sources](https://github.com/rainbows4dinos/Seeens/issues/321)
- [feat(board)!: rename board scan --since DAYS to --updated-since DAYS](https://github.com/jpshackelford/tickster/issues/136)
- [feat(canvas): Canvas References, one "Add reference" tool for Notes, Books, Chapters, Canvases, and Plugin sources](https://github.com/M4ss1ck/maibuk/issues/785)
- [Spec: Give calling agents evidence-linked results and truthful progress](https://github.com/mihaiiova/toad/issues/34)
- [Spec: Return actionable preflight and runtime failures through existing interfaces](https://github.com/mihaiiova/toad/issues/33)
- [docs: establish repository agent operating contract](https://github.com/EltonZhang777/Blasphemous.EditorMode/issues/38)
- [Spec: Make first agent delegation discoverable and executable](https://github.com/mihaiiova/toad/issues/31)
- [Created email: an incident held by a process that stopped is never sent](https://github.com/OneUptime/oneuptime/issues/7571)
- [无法打开 GitBash 命令行](https://github.com/qiu7824/zsdesk/issues/23)
- [(Bug): Relational comparison between TIME and DOUBLE columns is rejected](https://github.com/matrixorigin/matrixone/issues/32672)
- [(xCluster) Automatic mode resolves SESSION_USER in replayed DDL to the target's internal login; OWNER TO / AUTHORIZATION SESSION_USER pause DDL replication](https://github.com/yugabyte/yugabyte-db/issues/37806)
- [UX: page create errors say transaction owner when the page's pack lacks a one-collection schema](https://github.com/gents-ai/gents/issues/3740)
- [Workout Tracker v1: exercise library, templates, session logging, body weight, analytics](https://github.com/bennettsteg/workout-tracker/issues/1)
