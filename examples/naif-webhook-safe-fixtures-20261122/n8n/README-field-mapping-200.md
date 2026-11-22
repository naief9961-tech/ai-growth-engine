# n8n Webhook returns HTTP 200, but the next node shows empty fields

**Free, offline-first troubleshooting checklist — NAIF Gravity (23 November 2026)**

HTTP 200 means that some HTTP handler replied successfully. It does **not** prove a workflow ran to completion, an order was saved, or a downstream node received the expected fields. Determine *where* the failure occurs before changing mappings or buying any repair.

## Three distinct branches

| Observation | Check first | Avoid |
| --- | --- | --- |
| No corresponding n8n execution | Test URL vs Production URL, method, webhook path, publishing state, proxy routing | Assuming a field-mapping issue because HTTP returned 200 |
| Execution exists; Webhook node has data; next node is empty or `undefined` | Inspect the actual **Webhook node output JSON** and the field path used by the next node | Guessing that `order_id` is always at the root |
| The provider says its signature was rejected before processing | Original **raw** request bytes, provider-specific headers, timestamp, signing key version | Reserializing JSON or pasting live secrets into a shared debug tool |

Official n8n references: [Webhook Test vs Production URLs](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/workflow-development/) and [data mapping in the UI](https://docs.n8n.io/data/data-mapping/data-mapping-ui/).

## Tiny example: the Webhook fired, but a mapping is wrong

Suppose the Webhook node's **observed output** contains the following synthetic item:

```json
{
  "headers": {"content-type": "application/json"},
  "body": {
    "order_id": "DEMO_A",
    "quantity": 2
  }
}
```

An Edit Fields (Set) node trying to read the root fields may return empty values:

```text
{{ $json.order_id }}
{{ $json.quantity }}
```

For the *specific output shape shown above*, the correct n8n expressions refer to `body`:

```text
{{ $json.body.order_id }}
{{ $json.body.quantity }}
```

If your actual execution's output differs, **do not copy those expressions blindly**. Instead, open the Webhook node output and drag the correct field into the expression editor. Check item linking and branches when a downstream node changes the current item.

Try two non-customer fixtures:

| Fixture | `body.order_id` | `body.quantity` | Expected |
| --- | --- | --- | --- |
| A | `DEMO_A` | `2` | Both fields present |
| B | `DEMO_B` | `3` | Both fields present |

A local **structure-only** regression check is included here:

```bash
python3 n8n_field_mapping_fixture.py
```

Expected: `PASS_OFFLINE_SYNTHETIC_ONLY`, `old_root_mapping_passes: 0`, `corrected_body_mapping_passes: 2`. It uses the Python standard library and never contacts n8n, a provider, or the store. It is **not** a full n8n workflow execution test.

## Before you deploy or spend money

1. Prove which n8n endpoint received the event and find its execution record.
2. Verify the exact JSON output of the Webhook node using **sanitized** test data. Don't expose customer payloads, authorization headers, signing keys, account IDs, or payment details.
3. Change only the specific field reference after comparing two independent fixtures, including a missing-field case.
4. Re-run the workflow in a controlled test environment and confirm that the next node receives the expected values.
5. Treat signature verification and duplicate deliveries as separate checks: the output path change does **not** verify the provider or guarantee idempotency.

### Free guide or optional paid help?

If the event never reaches n8n, start with the [n8n Webhook node troubleshooting documentation](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/workflow-development/). For a visible execution with wrong downstream fields, see NAIF Gravity's [free n8n field-mapping guide](https://naifgravity.com/discover/n8n-webhook-field-mapping?utm_source=github&utm_medium=organic&utm_campaign=naif-n8n-mapping-20261123&utm_content=field-guide).

If the problem remains and you want a **separately scoped, optional** repair, review [Automation Rescue — scope and current price](https://naifgravity.com/service/automation-rescue?utm_source=github&utm_medium=organic&utm_campaign=naif-n8n-mapping-20261123&utm_content=optional-mapping-repair). The published scope covers bounded synthetic mapping examples and before/after evidence, **not live deployment or a guaranteed payment outcome**. Check eligibility and terms on that page before placing any order.

If signature validation is failing, use the separate [free raw-body signing checklist](https://naifgravity.com/discover/webhook-signature-mismatch?utm_source=github&utm_medium=organic&utm_campaign=naif-webhook-checklist-20261122&utm_content=n8n-triage-signature) instead. Do not confuse a valid JSON payload with a verified signature.

**بالعربية:** إذا رجع Webhook رمز 200 والخطوة التالية في n8n فارغة، تأكد أولًا من وجود تنفيذ داخل n8n، ثم افتح مخرجات عقدة Webhook. ربما البيانات داخل `body` وليس في المستوى الرئيسي. جرّب المثال الصناعي المجاني أعلاه قبل طلب إصلاح مدفوع. لا تُدخل أسرار التوقيع أو بيانات العملاء.

*Original NAIF Gravity educational text. Free first, no credentials or external requests, no claim of customer results or increased sales.*
