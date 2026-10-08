# NAIF Gravity — GitHub Diagnostic Hub

NAIF Gravity helps developers and AI agents diagnose bounded integration failures without handing over private keys or rebuilding an entire stack.

## Start here

1. **MCP problem** — run `python3 tools/mcp_health_check.py https://your-mcp.example/mcp` against an endpoint you own or are authorized to test.
2. **API / Auth problem** — collect the HTTP status, sanitized error code, auth method and expected behavior.
3. **Webhook problem** — collect the provider, delivery status, signature-verification result and a redacted payload shape.
4. If the failure is reproducible, open the matching GitHub diagnostic request template.

## Direct diagnostic paths

Use the narrowest matching destination instead of sending every visitor to the home page:

- [API integration diagnostic](https://naifgravity.com/service/api-integration-mini?utm_source=github&utm_medium=diagnostic_hub&utm_campaign=seo_discovery) — API integration errors, request/response mismatch, small integration failures.
- [JSON validity check](https://naifgravity.com/service/json-validity-check?utm_source=github&utm_medium=diagnostic_hub&utm_campaign=seo_discovery) — malformed JSON, payload validity, and structured-data checks.
- [Automation factory](https://naifgravity.com/service/automation-factory?utm_source=github&utm_medium=diagnostic_hub&utm_campaign=seo_discovery) — automation workflow failures and broken handoffs.
- [Data factory](https://naifgravity.com/service/data-factory?utm_source=github&utm_medium=diagnostic_hub&utm_campaign=seo_discovery) — structured data transformation and pipeline repair.
- [Docker health fix](https://naifgravity.com/service/docker-health-fix?utm_source=github&utm_medium=diagnostic_hub&utm_campaign=seo_discovery) — container health, startup, and deployment diagnostics.
- [Repair check](https://naifgravity.com/service/repair-check-beta?utm_source=github&utm_medium=diagnostic_hub&utm_campaign=seo_discovery) — bounded repair verification.

Canonical home: https://naifgravity.com

## Guardian subscriptions for agent operators

Teams that need continued visibility into agents rather than a one-time fix can use [NAIF Guardian's 30-day prepaid plans](https://naifgravity.com/subscriptions?utm_source=github&utm_medium=diagnostic_hub&utm_campaign=guardian_30day_plans):

- **Agent Health & Rescue — $9 USD / 30 days:** one agent.
- **Guardian Pro — $29 USD / 30 days:** up to five agents.
- **Guardian Agency — $59 USD / 30 days:** up to fifteen agents.

Plans provide bounded, agent-reported health summaries and signed health passports; issue triage and expert review availability depend on tier. **Renewal is manual, with no automatic card or wallet debits currently enabled.** The existing free diagnostics and paid repair flows remain separate.

## What to include

Include only what is needed to reproduce the failure: public repository link if applicable, client/server versions, transport, sanitized error text, expected behavior, and a minimal reproduction.

**Do not include:** API keys, bearer tokens, cookies, private keys, seed phrases, payment credentials, or customer data.

## Commercial repair path

GitHub issues are for bounded triage and reproducible technical evidence. Paid repair, checkout and delivery are handled by NAIF Gravity:

https://naifgravity.com/?utm_source=github&utm_medium=diagnostic_hub&utm_campaign=github_funnel

The goal is a short path:

**problem → diagnostic evidence → smallest suitable repair → verified delivery**
