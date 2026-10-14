"""Fetch public pinned source snapshots for the isolated documentation tests.

No credentials, package installation, subprocesses, or upstream entrypoints.
Original sources remain governed by their upstream licenses.
"""
import hashlib
import json
from pathlib import Path
import urllib.request

root = Path(__file__).parent
manifest = json.loads((root / 'manifest.json').read_text())
destination = root / 'evidence'
destination.mkdir(exist_ok=True)
for item in manifest:
    url = item['url']
    if not url.startswith('https://raw.githubusercontent.com/'):
        raise ValueError('Only pinned public GitHub source URLs are allowed')
    filename = item['local']
    if Path(filename).name != filename:
        raise ValueError('Source filename must be a basename')
    path = destination / filename
    data = path.read_bytes() if path.exists() else None
    def blob_sha(content):
        return hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
    if data is None or blob_sha(data) != item['blob_sha']:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read(2_000_001)
        if len(data) > 2_000_000 or blob_sha(data) != item['blob_sha']:
            raise ValueError('Source size/hash mismatch: ' + filename)
        path.write_bytes(data)
    print('verified ' + filename)
