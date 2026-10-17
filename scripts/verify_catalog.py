"""Check that each catalog entry's evidence lines still appear in the saved FWC page text.
Writes data/app/catalog_status.json. A changed page marks its species 'check' on the phone page."""
import json, pathlib, re, datetime
root = pathlib.Path(__file__).resolve().parent.parent
norm = lambda s: re.sub(r"\s+", " ", s).strip()
cat = json.load(open(root / "data" / "app" / "catalog.json"))
res = {"run_utc": datetime.datetime.utcnow().isoformat() + "Z", "species": {}}
for e in cat["species"]:
    f = root / "data" / "raw" / "species" / f"{e['slug']}.txt"
    if not f.exists():
        res["species"][e["id"]] = {"ok": False, "problem": "page text missing"}; continue
    t = norm(f.read_text(errors="ignore"))
    missing = [x for x in e["evidence"] if norm(x) not in t]
    res["species"][e["id"]] = {"ok": not missing, "missing": missing}
(root / "data" / "app" / "catalog_status.json").write_text(json.dumps(res, indent=1))
bad = {k: v for k, v in res["species"].items() if not v["ok"]}
print(len(res["species"]) - len(bad), "ok,", len(bad), "changed or missing")
for k, v in bad.items(): print(" ", k, v)
