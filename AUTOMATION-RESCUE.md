# Automation Rescue — webhook mapping repair for agents and automation teams

Your webhook receives the right data, but the next step reads the wrong field path.

**[Run a free eligibility check](https://naifgravity.com/service/automation-rescue?utm_source=github&utm_medium=announcement&utm_campaign=automation_rescue_launch)**

Automation Rescue is a live NAIF Gravity service. It checks 2–5 synthetic webhook examples and identifies uniquely matching field paths. Supported repairs cost **$19 USD per mapping**, with up to 12 output fields and no subscription.

After verified payment, the service delivers:

- Corrected dotted field paths.
- n8n expressions.
- Before/after checks against the supplied synthetic examples.

The customer or their agent applies the repair. This version does not deploy changes, accept credentials, execute supplied scripts, or repair arbitrary workflows. Passing examples does not guarantee all future inputs. Checkout availability follows regional and connection eligibility rules.

## Example

A workflow reads `order_id`, but the webhook now puts it under `body.order_id`. Submit the failing mapping and at least two synthetic examples with different expected values. A supported case gets a quote; ambiguous or unsupported cases are declined before a paid quote is created.

## Integrate

- [Product and free checker](https://naifgravity.com/service/automation-rescue)
- [Machine-readable input example and delivery contract](https://naifgravity.com/.well-known/naif-automation-rescue.json)
- [Troubleshooting guide](https://naifgravity.com/discover/n8n-webhook-field-mapping)

## Validation

On 2026-10-04, 19 isolated end-to-end checks passed, including quote/checkout, denied unpaid delivery, verified synthetic payment evidence, idempotent delivery, token checks and regional restrictions. This was a mocked-network test, not a live purchase or proof of revenue. The live browser free check also passed.

This service is separate from the repository's bounty program.
