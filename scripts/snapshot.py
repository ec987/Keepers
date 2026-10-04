"""Download each source in sources.json to data/raw/, record results in data/status.json.
A failed source never stops the others. Git history shows what changed and when."""
import json, hashlib, time, datetime, urllib.request, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
raw = root / "data" / "raw"; raw.mkdir(parents=True, exist_ok=True)
status = {"run_utc": datetime.datetime.utcnow().isoformat() + "Z", "sources": {}}
for s in json.load(open(root / "sources.json")):
    sid = s["id"]
    try:
        req = urllib.request.Request(s["url"], headers={"User-Agent": "fishing-rules-snapshot/0.1 (personal project)"})
        body = urllib.request.urlopen(req, timeout=60).read()
        (raw / f"{sid}.{s['ext']}").write_bytes(body)
        status["sources"][sid] = {"ok": True, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()[:16]}
    except Exception as e:
        status["sources"][sid] = {"ok": False, "error": str(e)[:200]}
    time.sleep(2)
(root / "data" / "status.json").write_text(json.dumps(status, indent=1))
print(json.dumps(status, indent=1))
