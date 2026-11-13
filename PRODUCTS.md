# NAIF Gravity — Developer tools & product directory

**Find a focused fix for an MCP, JSON, API, webhook, or Docker problem.** Start with a free tool or troubleshooting guide; use an optional, separately scoped service only when you need it.

**[NAIF Gravity storefront](https://naifgravity.com/?utm_source=github&utm_medium=product_directory&utm_campaign=product_discovery)** · **[Live service catalog](https://naifgravity.com/services?utm_source=github&utm_medium=product_directory&utm_campaign=product_discovery)** · **[Free troubleshooting guides](https://naifgravity.com/discover)** · **[أدلة عربية مجانية](https://naifgravity.com/ar/discover)**

## Free developer tools — source and installation

| Product | What it actually does | Start |
| --- | --- | --- |
| **[NAIF Gravity MCP Doctor](https://github.com/naief9961-tech/naif-gravity-mcp-diagnostics)** | Free MIT Python CLI for bounded MCP **Streamable HTTP** `initialize` / session / `tools/list` discovery diagnostics. Turn sanitized reports into local Error Passports; optionally check an endpoint you are authorized to test. No `tools/call`, automated repair, or full conformance certification. | [Python and npm install](https://github.com/naief9961-tech/naif-gravity-mcp-diagnostics#install-from-pypi-or-npm) · [Free local demo](https://github.com/naief9961-tech/naif-gravity-mcp-diagnostics#see-a-healthy-and-a-broken-mcp-response) |
| **[NAIF JSON Rescue Skill](skills/naif-json-rescue/SKILL.md)** | Free local, syntax-only JSON check for coding agents. Does not upload samples, change project files, or purchase anything. Not a schema or duplicate-key validator. | [Skill and local tests](skills/naif-json-rescue/SKILL.md) · [Installation instructions](README.md#install-naif-json-rescue-for-your-agent) |
| **[MCP diagnostic scripts and issue templates](docs/DIAGNOSTIC-QUICKSTART.md)** | Reproducible sample-based diagnostics and privacy-conscious issue templates for MCP, API/Auth, and webhooks in this repository. | [Diagnostic hub](NAIF-GRAVITY.md) · [Quick start](docs/DIAGNOSTIC-QUICKSTART.md) |

MCP Doctor is available via `python3 -m pip install naif-gravity-mcp-doctor`. The npm package (`npm install -g naif-gravity-mcp-doctor`) is a **Node.js launcher of the same Python implementation**, not a separate JavaScript probe. It requires **Node.js 20+ and Python 3.10+**.

## Choose a product by the problem you have

| Problem / search term | Free first step | Optional separately scoped service |
| --- | --- | --- |
| MCP server not responding; `initialize` timeout; `tools/list` fails | [MCP Doctor](https://github.com/naief9961-tech/naif-gravity-mcp-diagnostics) and [MCP failure guides](https://naifgravity.com/discover) | [Current technical services](https://naifgravity.com/services) |
| JSON syntax error, malformed JSON, trailing comma | [Local JSON Rescue Skill](skills/naif-json-rescue/SKILL.md) or [free sample preview](https://naifgravity.com/micro-v2) | [JSON Validity Check](https://naifgravity.com/service/json-validity-check?utm_source=github&utm_medium=product_directory) |
| API response field changed; response schema drift | [Free sample preview](https://naifgravity.com/micro-v2) | [API Response Shape Check](https://naifgravity.com/service/api-response-shape-check?utm_source=github&utm_medium=product_directory) |
| Normalize small JSON objects or arrays | [Free sample preview](https://naifgravity.com/micro-v2) | [JSON Normalize Mini](https://naifgravity.com/service/json-normalizer?utm_source=github&utm_medium=product_directory) |
| CSV missing columns, inconsistent rows | [Free sample preview](https://naifgravity.com/micro-v2) | [CSV Schema Audit Mini](https://naifgravity.com/service/csv-schema-audit?utm_source=github&utm_medium=product_directory) |
| n8n webhook returns HTTP 200, but the next field is empty | [n8n field-mapping troubleshooting](https://naifgravity.com/discover/n8n-webhook-field-mapping) | [Webhook Debug Mini](https://naifgravity.com/service/webhook-debug-mini?utm_source=github&utm_medium=product_directory) |
| One failing API operation or integration | [Troubleshooting guides](https://naifgravity.com/discover) | [API Integration Mini](https://naifgravity.com/service/api-integration-mini?utm_source=github&utm_medium=product_directory) |
| Docker/Compose healthcheck keeps failing | [Collect a minimal, sanitized configuration](docs/TROUBLESHOOTING.md) | [Docker Healthcheck Fix](https://naifgravity.com/service/docker-health-fix?utm_source=github&utm_medium=product_directory) |
| Received an AI-generated or contractor patch; need to spot unexpected file changes before acceptance | Keep an owner-approved reference separate from the received bundle and compare hashes manually | [NAIF Patch Evidence — $9 one-time](https://naifgravity.com/service/naif-patch-evidence?utm_source=github&utm_medium=product_directory&utm_campaign=patch_evidence_launch) — offline inventory, SHA-256, file sizes, POSIX modes and symlink rejection (integrity, not correctness or vulnerability scanning) |
| Need evidence that a proposed patch addresses the reported failure | [Document the failing condition and expected result](NAIF-GRAVITY.md) | [Repair Check Beta](https://naifgravity.com/service/repair-check-beta?utm_source=github&utm_medium=product_directory) |

**Important purchasing distinction:** the **Micro Tools V2 page currently offers free bounded previews only**; a separate paid *Micro V2 report checkout* is not active. The linked standalone service pages are distinct products with their own live scope, eligibility, displayed price, and checkout. Do not assume the preview result is the paid artifact. No subscription, payment or repair is initiated by using these GitHub links.

## For AI agents and integrations

- [Public Agent Card](https://naifgravity.com/.well-known/agent-card.json) — agent identity and advertised interfaces.
- [Remote MCP endpoint](https://naifgravity.com/mcp) — use an MCP-compatible client; an ordinary browser `GET` may return HTTP 405.
- [Agent service catalog](https://naifgravity.com/api/agent/catalog) and [OpenAPI spec](https://naifgravity.com/openapi.json) — check live capabilities, eligibility, current prices, and required approvals.
- [Service catalog for humans](https://naifgravity.com/services) — direct product pages and service boundaries.

**Security and scope:** use only synthetic or redacted examples. Never post tokens, API keys, personal records, payment credentials or private customer payloads in GitHub issues or hosted previews. A discovery result, passing HTTP status, or directory listing is not evidence of a completed paid repair.

## العربية — ابدأ بالمجاني

**NAIF Gravity** يوفر أدوات مجانية لتشخيص مشاكل **MCP وJSON**، بالإضافة إلى صفحات خدمات منفصلة لمشاكل API وWebhooks وDocker. ابدأ بـ[الأدلة العربية](https://naifgravity.com/ar/discover)، ثم اختر المنتج المحدد للمشكلة، وتحقق من نطاق الخدمة وسعرها المباشر قبل أي شراء.

Need to report a security issue? Read [SECURITY.md](SECURITY.md). Want to contribute a reproducible non-sensitive bug report? Use the [issue templates](.github/ISSUE_TEMPLATE/).
