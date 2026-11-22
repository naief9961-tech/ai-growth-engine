#!/usr/bin/env python3
"""Free offline n8n field-mapping fixtures by NAIF Gravity.

Synthetic data only. This program does not connect to n8n or HTTP, use
credentials, write files, or execute a workflow. It proves two JSON-path
assumptions for a sample *WebHook node output shape*, not for all providers.
"""
from __future__ import annotations

import json


SYNTHETIC_WEBHOOK_ITEMS = (
    {"body": {"order_id": "DEMO_A", "quantity": 2}},
    {"body": {"order_id": "DEMO_B", "quantity": 3}},
)
EXPECTED = (
    {"order_id": "DEMO_A", "quantity": 2},
    {"order_id": "DEMO_B", "quantity": 3},
)


def read_path(obj: dict, dotted: str):
    """Read a fixed example path. Missing fields never silently invent values."""
    value = obj
    for field in dotted.split("."):
        if not isinstance(value, dict) or field not in value:
            return None
        value = value[field]
    return value


def main() -> None:
    observations = []
    for sample, expected in zip(SYNTHETIC_WEBHOOK_ITEMS, EXPECTED):
        wrong = {
            "order_id": read_path(sample, "order_id"),
            "quantity": read_path(sample, "quantity"),
        }
        corrected = {
            "order_id": read_path(sample, "body.order_id"),
            "quantity": read_path(sample, "body.quantity"),
        }
        assert wrong != expected
        assert corrected == expected
        assert corrected["order_id"].startswith("DEMO_")
        assert isinstance(corrected["quantity"], int)
        observations.append(
            {
                "old_root_mapping_matches": wrong == expected,
                "corrected_body_mapping_matches": corrected == expected,
            }
        )

    assert len(observations) == 2
    assert sum(item["corrected_body_mapping_matches"] for item in observations) == 2
    print(
        json.dumps(
            {
                "status": "PASS_OFFLINE_SYNTHETIC_ONLY",
                "cases": len(observations),
                "old_root_mapping_passes": 0,
                "corrected_body_mapping_passes": 2,
                "n8n_executions": 0,
                "network_requests": 0,
                "credential_access": 0,
                "real_customer_data": False,
                "paid_api_cost_usd": 0,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
