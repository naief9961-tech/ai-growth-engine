#!/usr/bin/env python3
"""Offline regression tests for the entirely synthetic fixture lab."""
import unittest
import webhook_fixture_lab as demo


class SyntheticWebhookTests(unittest.TestCase):
    def test_valid_signature(self):
        payload = demo.canonical_payload()
        self.assertTrue(demo.verify_fixture(payload, demo.sign_fixture(payload)))

    def test_changed_bytes_are_rejected(self):
        payload = demo.canonical_payload()
        changed = payload + b" "
        self.assertFalse(demo.verify_fixture(changed, demo.sign_fixture(payload)))

    def test_missing_or_malformed_signature(self):
        payload = demo.canonical_payload()
        self.assertFalse(demo.verify_fixture(payload, None))
        self.assertFalse(demo.verify_fixture(payload, "sha256=invalid"))
        self.assertFalse(demo.verify_fixture(payload, "0" * 64))

    def test_duplicate_is_not_new_delivery(self):
        outcomes = demo.run_demo()
        self.assertEqual(
            [i["decision"] for i in outcomes],
            ["ACCEPTED_SYNTHETIC", "SIGNATURE_MISSING_OR_INVALID",
             "SIGNATURE_MISSING_OR_INVALID", "DUPLICATE_WITHIN_THIS_BATCH"]
        )

    def test_replay_state_is_not_durable(self):
        # Re-running recreates the in-memory set: this does NOT prove crash safety.
        self.assertEqual(demo.run_demo(), demo.run_demo())


if __name__ == "__main__":
    unittest.main()
