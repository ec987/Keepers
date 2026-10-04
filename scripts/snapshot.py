"""Download each source in sources.json to data/raw/ and record results in data/status.json.
A source is saved only if its content looks right. Otherwise the last good copy is kept."""
import json, hashlib, time, datetime, urllib.request, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
raw = root / "data" / "raw"; raw.mkdir(parents=True, exist_ok=True)
status = {"run_utc": datetime.datetime.utcnow().isoformat() + "Z", "sources": {}}

def check(ext, body):
    if ext == "html":
        if len(body) < 20000 or b"<html" not in body.lower():
            return "html too small or not a page"
        return None
    try:
        d = json.loads(body)
    except Exception:
        return "not valid JSON (probably an error page)"
    if isinstance(d, dict) and "error" in d:
        return "service returned an error"
    if isinstance(d, dict) and "features" in d and not d["features"]:
        return "no features returned"
    return None

for s in json.load(open(root / "sources.json")):
    sid = s["id"]
    try:
        req = urllib.request.Request(s["url"], headers={"User-Agent": "fishing-rules-snapshot/0.2 (personal project)"})
        body = urllib.request.urlopen(req, timeout=60).read()
        problem = check(s["ext"], body)
        entry = {"ok": problem is None, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()[:16]}
        if problem:
            entry["problem"] = problem
        else:
            (raw / f"{sid}.{s['ext']}").write_bytes(body)
        status["sources"][sid] = entry
    except Exception as e:
        status["sources"][sid] = {"ok": False, "problem": str(e)[:200]}
    time.sleep(2)
(root / "data" / "status.json").write_text(json.dumps(status, indent=1))
print(json.dumps(status, indent=1))
