"""Source-extracted AIM + WP checks; fake transport, no SDK dependencies/network."""
import ast
import asyncio
import hashlib
import json
import re
import types
import unittest
from pathlib import Path
from typing import Any, Dict, List
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone

ROOT = Path(__file__).parent
for item in json.loads((ROOT / 'manifest.json').read_text()):
    data = (ROOT / 'source' / item['name']).read_bytes()
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == item['blob_sha']

def method(file, cls, name, replace=None):
    source = (ROOT / 'source' / file).read_text()
    node = next(n for c in ast.parse(source).body if isinstance(c, ast.ClassDef) and c.name == cls for n in c.body if getattr(n, 'name', None) == name)
    code = ast.get_source_segment(source, node)
    if replace:
        assert replace[0] in code
        code = code.replace(*replace)
    ns = dict(Any=Any, Dict=Dict, List=List)
    exec('from __future__ import annotations\n' + code, ns)
    return ns[name], ns

class Failure(Exception):
    def __init__(self, *args, **kwargs): super().__init__(*args)
    @classmethod
    def from_payload(cls, status, payload): return cls(str(status))

class Response:
    def __init__(self, status, headers=None):
        self.status_code, self.headers = status, headers or {}
        self.is_success = 200 <= status < 300
    def json(self): return {'ok': True}

class TransportError(Exception): pass
class TimeoutException(TransportError): pass

def retry_delay(value, fallback, ceiling, now):
    """Candidate policy only: None means stop/defer; never shorten server wait."""
    if value is None:
        delay = fallback
    elif re.fullmatch(r'[0-9]+', value.strip(), flags=re.ASCII):
        # Avoid converting unbounded attacker-controlled integer strings.
        digits = value.strip().lstrip('0') or '0'
        if len(digits) > 12: return None
        delay = int(digits)
    else:
        try:
            date = parsedate_to_datetime(value)
            if date.tzinfo is None: raise ValueError('timezone required')
            delay = max(0, (date - now).total_seconds())
        except (ValueError, TypeError, OverflowError):
            delay = fallback
    return delay if delay <= ceiling else None

class Boundaries(unittest.TestCase):
    def test_aim_baseline_missing_route(self):
        fn, _ = method('aim_a2a.py', 'A2AClient', 'list_skills')
        calls = []
        obj = types.SimpleNamespace(_make_request=lambda *a: calls.append(a) or {'skills': []})
        fn(obj)
        self.assertEqual(calls, [('GET', '/api/v1/a2a/skills')])
        routes = (ROOT / 'source/aim_server.go').read_text()
        self.assertNotIn('a2a.Get("/skills",', routes)
        self.assertIn('a2aHeld.Get("/agents/:id/skills", h.A2A.GetAgentSkills)', routes)

    def test_aim_candidate_route_and_results(self):
        fn, _ = method('aim_a2a.py', 'A2AClient', 'list_skills', ('"/api/v1/a2a/skills"', 'f"/api/v1/a2a/agents/{self.agent_id}/skills"'))
        for skills in ([], [{'name': 'synthetic'}]):
            calls = []
            obj = types.SimpleNamespace(agent_id='00000000-0000-4000-8000-000000000001', _make_request=lambda *a: calls.append(a) or {'skills': skills})
            self.assertEqual(fn(obj), skills)
            self.assertEqual(calls, [('GET', f'/api/v1/a2a/agents/{obj.agent_id}/skills')])

    def test_aim_candidate_does_not_swallow_authorization_error(self):
        fn, _ = method('aim_a2a.py', 'A2AClient', 'list_skills', ('"/api/v1/a2a/skills"', 'f"/api/v1/a2a/agents/{self.agent_id}/skills"'))
        def fail(*a): raise Failure('403 synthetic')
        with self.assertRaises(Failure): fn(types.SimpleNamespace(agent_id='synthetic', _make_request=fail))

    def test_wp_baseline_ignores_retry_after(self):
        fn, ns = method('wp_client.py', 'WordPressClient', '_request')
        sleeps, calls = [], []
        responses = iter([Response(429, {'Retry-After': '60'}), Response(200)])
        async def sleep(n): sleeps.append(n)
        async def request(*a, **kw): calls.append(a); return next(responses)
        ns.update(asyncio=types.SimpleNamespace(sleep=sleep), httpx=types.SimpleNamespace(TransportError=TransportError, TimeoutException=TimeoutException), WordPressError=Failure, _json_or_none=lambda r:r.json(), _TRANSIENT_STATUS={429,500,502,503,504}, _NOT_SENT_ERRORS=(), logger=types.SimpleNamespace(warning=lambda *a:None))
        obj = types.SimpleNamespace(_http=types.SimpleNamespace(request=request), _settings=types.SimpleNamespace(max_retries=1, backoff_s=.5))
        self.assertEqual(asyncio.run(fn(obj, 'GET', '/posts')), {'ok':True})
        self.assertEqual(sleeps, [.5])
        self.assertEqual(len(calls), 2)

    def test_wp_post_500_is_not_retried(self):
        fn, ns = method('wp_client.py', 'WordPressClient', '_request')
        calls = []
        async def request(*a, **kw): calls.append(a); return Response(500)
        ns.update(httpx=types.SimpleNamespace(TransportError=TransportError), WordPressError=Failure, _json_or_none=lambda r:r.json(), _TRANSIENT_STATUS={429,500}, logger=types.SimpleNamespace(warning=lambda *a:None))
        obj = types.SimpleNamespace(_http=types.SimpleNamespace(request=request), _settings=types.SimpleNamespace(max_retries=3, backoff_s=.5))
        with self.assertRaises(Failure): asyncio.run(fn(obj, 'POST', '/posts'))
        self.assertEqual(len(calls), 1)

    def test_policy_delta_seconds(self):
        now = datetime(2026,10,18,tzinfo=timezone.utc)
        self.assertEqual(retry_delay('60', .5, 120, now), 60)
        self.assertEqual(retry_delay('0', .5, 120, now), 0)

    def test_policy_dates(self):
        now = datetime(2026,10,18,tzinfo=timezone.utc)
        self.assertEqual(retry_delay('Sun, 18 Oct 2026 00:01:00 GMT', .5, 120, now), 60)
        self.assertEqual(retry_delay('Sat, 17 Oct 2026 00:00:00 GMT', .5, 120, now), 0)

    def test_policy_invalid_and_missing_fallback(self):
        now = datetime(2026,10,18,tzinfo=timezone.utc)
        for value in (None, 'garbage', '-1', '1.5', 'NaN', 'Infinity', '６０'):
            self.assertEqual(retry_delay(value, .5, 120, now), .5)

    def test_policy_over_budget_defers_instead_of_shortening(self):
        now = datetime(2026,10,18,tzinfo=timezone.utc)
        self.assertIsNone(retry_delay('600', .5, 120, now))
        self.assertIsNone(retry_delay('9' * 5000, .5, 120, now))

if __name__ == '__main__': unittest.main(verbosity=2)
