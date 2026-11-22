# Safe webhook incident fixtures — NAIF Gravity

A **free, offline, synthetic** mini-lab for developers troubleshooting webhook signatures and retries. This is a practical way to classify failures before requesting a paid repair.

**No API keys, customer information, external HTTP calls, paid software, or production access.**

## What it shows

- A valid HMAC-SHA256 signature over the **exact original bytes** of a synthetic event.
- Why changing just one byte makes the signature invalid.
- A missing-signature case, which must not be treated as verified.
- A duplicate delivery rejected only **within one in-memory batch**, not guaranteed across restarts or multiple workers.

This is an educational fixture, **not a production-ready webhook receiver or security certification**. Real systems need provider-specific signature headers, timestamp/replay policy, secret rotation, bounded request bodies, durable deduplication, and error handling. HTTP 200 never proves that downstream processing or billing completed.

## Run locally

Python 3.10+; standard library only.

```bash
python3 webhook_fixture_lab.py
python3 -m unittest -v test_webhook_fixture_lab.py
```

Expected demo classifications, in order:

```text
valid      -> ACCEPTED_SYNTHETIC
invalid    -> SIGNATURE_MISSING_OR_INVALID
missing    -> SIGNATURE_MISSING_OR_INVALID
duplicate  -> DUPLICATE_WITHIN_THIS_BATCH
```

The sample key is intentionally fake and hard-coded. **Never reuse it in production.** No credentials are loaded, no actual webhook is received, and the tests do not contact the internet.

## NAIF n8n importable demo

The same four **synthetic** cases are also available as an [importable n8n JSON workflow](n8n/NAIF_n8n_Offline_Webhook_Fixture_Lab.json) — tested on n8n 2.43.7 in a network-isolated local container, including a clean re-import. It uses a **Manual Trigger** and the native Crypto HMAC node, so it does not open any public Webhook endpoint.

Import the JSON into a new n8n workflow. Create a Crypto credential with the **public fake test key** `NAIF-demo-test-key-DO-NOT-USE-IN-PRODUCTION`, then select it in the **Calculate synthetic HMAC** node. Click **Execute workflow** and check the four expected classifications. Do not use this credential or workflow to accept production webhooks. It is not currently an officially approved n8n Creator Hub listing.

## A safe debugging checklist

1. Record the provider and the failed step (receipt, signature verification, routing, retry, downstream job). Do not copy bearer tokens or private payloads.
2. Verify the raw request bytes **before JSON parsing** using the provider's documented signature format.
3. Confirm whether the delivery is retried, and whether its event ID is stable.
4. Separate an accepted HTTP request from a successfully completed downstream task.
5. Check idempotency against **durable** storage if multiple processes, restarts, or queue retries are possible.
6. Keep only redacted failure evidence and run the smallest relevant test.

For a detailed free guide, see:

[Webhook signature mismatch — free NAIF Gravity diagnostic](https://naifgravity.com/discover/webhook-signature-mismatch?utm_source=github&utm_medium=organic&utm_campaign=naif-webhook-checklist-20261122&utm_content=github-guide)

For a **separate, optional** bounded service with current live terms:

[Webhook Debug Mini — scope and current price](https://naifgravity.com/service/webhook-debug-mini?utm_source=github&utm_medium=organic&utm_campaign=naif-webhook-checklist-20261122&utm_content=optional-paid-scope)

The free guide and fixture require no purchase. The optional paid service is not triggered by clicking the link and is subject to live scope, eligibility, and checkout policies. **No price or conversion result is promised here.**

## بالعربية

تجربة مجانية وآمنة لتوضيح الفرق بين التوقيع الصحيح والتوقيع المعدّل وغياب التوقيع وتكرار إرسال Webhook. جميع الأمثلة صناعية وتعمل دون إنترنت أو بيانات عملاء. التجربة لا تضمن الحماية من إعادة الإرسال بعد إعادة تشغيل الخدمة، ولا تُعدّ إصلاحًا تلقائيًا للأنظمة الحقيقية.

## Publication and measurement notes

This free resource is published in an **owned NAIF Gravity GitHub repository**. The tagged links above label the *intended* campaign source. A UTM label alone is **not proof of a human visit or a conversion**. Verified paid orders require independent checkout/payment evidence, excluding owner tests. No analytics data, client IDs, cookies, or visitor details are embedded in this kit.

*Original educational sample by NAIF Gravity. 22 November 2026.*
