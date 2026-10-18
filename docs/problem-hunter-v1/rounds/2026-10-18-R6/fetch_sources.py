"""Fetch pinned public sources into local source/ and verify Git blob hashes."""
import hashlib, json, urllib.request
from pathlib import Path
root = Path(__file__).parent
(root / 'source').mkdir(exist_ok=True)
for item in json.loads((root / 'manifest.json').read_text()):
    data = urllib.request.urlopen(item['url'], timeout=30).read()
    actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    if actual != item['blob_sha']: raise ValueError(f"Hash mismatch: {item['name']}")
    (root / 'source' / item['name']).write_bytes(data)
print('PASS: five pinned source hashes')
