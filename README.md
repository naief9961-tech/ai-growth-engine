# NAIF Gravity — MCP & Integration Diagnostics

[![GitHub stars](https://img.shields.io/github/stars/naief9961-tech/ai-growth-engine?style=flat)](https://github.com/naief9961-tech/ai-growth-engine/stargazers)
[![Diagnostic requests](https://img.shields.io/github/issues/naief9961-tech/ai-growth-engine)](https://github.com/naief9961-tech/ai-growth-engine/issues)

NAIF Gravity provides bounded diagnostics and repair workflows for MCP, AI-agent integrations, APIs, authentication, and webhooks, with reproducible developer-facing diagnostics and machine-readable agent discovery.

**Start with the [Diagnostic Hub](NAIF-GRAVITY.md)** or visit [NAIF Gravity](https://naifgravity.com).

This repository contains public diagnostic guidance, a small Python MCP health-check script, issue templates, and discovery metadata. It is not a complete source distribution of the hosted service.

## Try the MCP health check

Requires Python 3 and uses only the standard library. Run against a server you own or are authorized to test:

```bash
git clone https://github.com/naief9961-tech/ai-growth-engine.git
cd ai-growth-engine
python3 tools/mcp_health_check.py https://your-mcp.example/mcp
```

Replace the example URL with your endpoint. The script requests `initialize` and `tools/list`; it never calls a tool. It reports HTTP status, JSON-RPC results or errors, and the returned tool count when a JSON response can be parsed.

See the [quick start and limitations](docs/DIAGNOSTIC-QUICKSTART.md) before interpreting the result. This is a basic probe, not an MCP conformance suite.

## Find the right diagnostic path

| Failure | Useful evidence | Start here |
| --- | --- | --- |
| MCP connection, session, or schema | Transport, client/server versions, sanitized JSON-RPC error | [MCP diagnostic template](.github/ISSUE_TEMPLATE/mcp-diagnostic.md) |
| API authorization or OAuth | HTTP status, auth scheme, expected behavior, sanitized error code | [API/Auth diagnostic template](.github/ISSUE_TEMPLATE/api-auth-diagnostic.md) |
| Webhook delivery or processing | Provider, delivery and handler status, signature result, redacted payload shape | [Webhook diagnostic template](.github/ISSUE_TEMPLATE/webhook-diagnostic.md) |

Read the [troubleshooting index](docs/TROUBLESHOOTING.md) for common `401`, `403`, `invalid_grant`, raw-body signature, retry, and idempotency failures. Open an issue using the matching template once you have a minimal reproduction.

**GitHub issues are public.** Remove tokens, cookies, signing secrets, private keys, payment credentials, and customer data before sharing evidence.

## For AI-agent builders

[Agent discovery documentation](AGENT-DISCOVERY.md) describes the hosted MCP transport, A2A Agent Card, and canonical domain. [server.json](server.json) contains the provider's MCP registry metadata.

Documentation and discovery metadata describe the provider's interfaces; they do not guarantee current availability or certify protocol conformance. Diagnostic discovery does not automatically execute a production repair.

## Contribute

Useful contributions include reproducible sanitized examples, clearer troubleshooting steps, and corrections to diagnostic documentation. Explain the problem, expected behavior, and how to reproduce or verify your change. Never include private production logs.

This repository also contains material from the earlier AI Growth Engine project. See [the historical README](docs/LEGACY-GROWTH-ENGINE.md) and [the existing contribution guide](CONTRIBUTING.md) for that context. Historical bounty amounts, payout automation, and endpoint status are not current commitments.

If these diagnostics help you debug an integration, consider starring the repository so other builders can find it.

## Service boundary

The hosted service is available at https://naifgravity.com. Public GitHub diagnostic guidance and optional commercial repair workflows are separate; an issue or contribution does not purchase a service or guarantee a repair.
