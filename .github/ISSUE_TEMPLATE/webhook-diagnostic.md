---
name: Webhook diagnostic request
about: Report delivery, signature, parsing, retry or idempotency failures
title: "[Webhook] "
labels: ""
assignees: ""
---

## Problem
Describe the webhook failure briefly.

## Provider / stack
- Provider:
- Framework/runtime:
- Delivery status:
- Handler status:
- Sanitized event type:

## Signature / payload
- Signature verification result:
- Raw-body handling checked?:
- Timestamp tolerance checked?:
- Payload shape (redacted):

## Reproduction
Describe the smallest safe reproduction.

## Expected behavior
What should happen?

## Security checklist
- [ ] Signing secrets and tokens are removed.
- [ ] Payload contains no customer/private data.
- [ ] I am authorized to test this webhook.

Commercial repair path: https://naifgravity.com/?utm_source=github&utm_medium=issue_template&utm_campaign=webhook
