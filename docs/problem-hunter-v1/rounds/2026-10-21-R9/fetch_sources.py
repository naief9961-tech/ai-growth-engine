"""Download pinned public source files for isolated R9 checks. No dependencies."""
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

root = Path(__file__).resolve().parent
manifest = json.loads((root / "sources.json").read_text())
output = root / "input"
output.mkdir(exist_ok=True)
for name, record in manifest.items():
    parts = record["url"].split("/")
    assert parts[2] == "github.com" and parts[5] == "blob"
    assert len(parts[6]) == 40 and all(c in "0123456789abcdef" for c in parts[6])
    assert Path(name).name == name
    raw = "https://raw.githubusercontent.com/" + "/".join(parts[3:5] + parts[6:])
    with urlopen(Request(raw, headers={"User-Agent": "NAIF-R9-evidence"}), timeout=30) as response:
        data = response.read()
    digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if digest != record["blob_sha"]:
        raise RuntimeError("Source hash mismatch: " + name)
    (output / name).write_bytes(data)
    print("VERIFIED", name, digest)
