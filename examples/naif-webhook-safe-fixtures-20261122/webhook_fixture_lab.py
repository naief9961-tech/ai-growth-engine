#!/usr/bin/env python3
"""Offline webhook signature fixture lab (education only, no network or secrets).

This demo uses a fixed FAKE test key and synthetic payloads. It is not a
production endpoint, an n8n workflow, or crash-safe exactly-once handling.
"""
import hashlib
import hmac
import json

DEMO_KEY = b"NAIF-demo-test-key-DO-NOT-USE-IN-PRODUCTION"
PREFIX = "sha256="


def canonical_payload(event_id="synthetic-001", event_type="ticket.updated"):
    """Serialize one artificial fixture using a deterministic byte representation."""
    return json.dumps(
        {"event_id": event_id, "type": event_type, "test": True},
        separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def sign_fixture(body, key=DEMO_KEY):
    """Sign the EXACT bytes; changing whitespace also changes a signature."""
    return PREFIX + hmac.new(key, body, hashlib.sha256).hexdigest()


def verify_fixture(body, signature, key=DEMO_KEY):
    """Constant-time digest comparison; does NOT verify timestamps or authorization."""
    if not isinstance(signature, str) or not signature.startswith(PREFIX):
        return False
    supplied = signature[len(PREFIX):]
    if len(supplied) != 64 or any(c not in "0123456789abcdef" for c in supplied):
        return False
    expected = hmac.new(key, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, supplied)


def classify_demo_deliveries(deliveries):
    """Simulate signature and duplicate gates within ONE in-memory batch only."""
    accepted_ids = set()
    results = []
    for item in deliveries:
        body = item.get("body")
        signature = item.get("signature")
        event_id = item.get("event_id")
        if not isinstance(body, bytes) or not verify_fixture(body, signature):
            reason = "SIGNATURE_MISSING_OR_INVALID"
        elif not isinstance(event_id, str) or not event_id:
            reason = "MISSING_EVENT_ID"
        elif event_id in accepted_ids:
            reason = "DUPLICATE_WITHIN_THIS_BATCH"
        else:
            accepted_ids.add(event_id)
            reason = "ACCEPTED_SYNTHETIC"
        results.append({"case": item.get("case"), "decision": reason})
    return results


def sample_cases():
    original = canonical_payload()
    good_sig = sign_fixture(original)
    altered = original.replace(b"ticket.updated", b"ticket.deleted")
    return [
        {"case": "valid", "event_id": "synthetic-001", "body": original, "signature": good_sig},
        {"case": "invalid", "event_id": "synthetic-002", "body": altered, "signature": good_sig},
        {"case": "missing", "event_id": "synthetic-003", "body": original, "signature": None},
        {"case": "duplicate", "event_id": "synthetic-001", "body": original, "signature": good_sig},
    ]


def run_demo():
    return classify_demo_deliveries(sample_cases())


if __name__ == "__main__":
    print(json.dumps({"mode": "OFFLINE_SYNTHETIC_ONLY", "cases": run_demo()}, indent=2))
