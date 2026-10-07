# NAIF Gravity — GitHub Diagnostic Hub

NAIF Gravity helps developers and AI agents diagnose bounded integration failures without handing over private keys or rebuilding an entire stack.

## Start here

1. **MCP problem** — run `python3 tools/mcp_health_check.py https://your-mcp.example/mcp` against an endpoint you own or are authorized to test.
2. **API / Auth problem** — collect the HTTP status, sanitized error code, auth method and expected behavior.
3. **Webhook problem** — collect the provider, delivery status, signature-verification result and a redacted payload shape.
4. If the failure is reproducible, open the matching GitHub diagnostic request template.

## What to include

Include only what is needed to reproduce the failure: public repository link if applicable, client/server versions, transport, sanitized error text, expected behavior, and a minimal reproduction.

**Do not include:** API keys, bearer tokens, cookies, private keys, seed phrases, payment credentials, or customer data.

## Commercial repair path

GitHub issues are for bounded triage and reproducible technical evidence. Paid repair, checkout and delivery are handled by NAIF Gravity:

https://naifgravity.com/?utm_source=github&utm_medium=diagnostic_hub&utm_campaign=github_funnel

The goal is a short path:

**problem → diagnostic evidence → smallest suitable repair → verified delivery**
