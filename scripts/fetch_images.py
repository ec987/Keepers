"""Download one freely licensed photo per fish from Wikimedia Commons (via Wikipedia's lead image).
Reads scripts/fish_images.json. Writes data/app/fish/<id>.<ext> and data/app/fish.json (credits).
Only CC0, public domain, CC BY and CC BY-SA images are kept. Already-downloaded fish are skipped.
To force a specific picture, add "pick": "File:Name.jpg" to that fish in fish_images.json.
A failure for one fish never stops the others."""
import json, pathlib, re, sys, time, html, urllib.request, urllib.parse
root = pathlib.Path(__file__).resolve().parent.parent
cfg = json.loads((root/"scripts"/"fish_images.json").read_text())
outdir = root/"data"/"app"/"fish"; outdir.mkdir(parents=True, exist_ok=True)
manp = root/"data"/"app"/"fish.json"
man = json.loads(manp.read_text()) if manp.exists() else {}
UA = "KeepersFishingApp/1.0 (https://github.com/ec987/Keepers; personal fishing-rules page)"
def get(url):
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30) as r: return r.read()
        except Exception as e:
            err = e; time.sleep(2 + 3*i)
    raise err
def api(host, **p):
    p.update(format="json", formatversion="2")
    return json.loads(get(f"https://{host}/w/api.php?" + urllib.parse.urlencode(p)))
GOOD = re.compile(r"^(cc0|public domain|pd\b|pdm|cc[ -]by(-sa)?\b)", re.I)
BAD = re.compile(r"(^|[\s-])(nc|nd)([\s-]|$)|fair use|non-?commercial|no deriv", re.I)
def strip(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s or ""))).strip()
def one(fid, c):
    fname = c.get("pick")
    if not fname:
        d = api("en.wikipedia.org", action="query", titles=c["title"], prop="pageimages", piprop="name", redirects="1")
        pg = d["query"]["pages"][0]
        if "pageimage" not in pg: return None, "no lead image"
        fname = "File:" + pg["pageimage"]
    d = api("commons.wikimedia.org", action="query", titles=fname, prop="imageinfo", iiprop="url|mime|extmetadata", iiurlwidth="400")
    pg = d["query"]["pages"][0]
    if "imageinfo" not in pg: return None, "file not found: " + fname
    ii = pg["imageinfo"][0]; md = ii.get("extmetadata", {})
    lic = strip(md.get("LicenseShortName", {}).get("value", ""))
    if not lic or BAD.search(lic) or not GOOD.search(lic): return None, f"license not accepted ({lic or 'unknown'}) for {fname}"
    if ii.get("mime") not in ("image/jpeg", "image/png"): return None, f"not a photo file type ({ii.get('mime')}) for {fname}"
    url = ii.get("thumburl") or ii["url"]
    ext = "png" if ii["mime"] == "image/png" else "jpg"
    (outdir/f"{fid}.{ext}").write_bytes(get(url))
    return {"file": f"data/app/fish/{fid}.{ext}", "label": c["label"], "title": c["title"], "pick": c.get("pick", ""), "source": fname,
            "author": strip(md.get("Artist", {}).get("value", "")) or "Unknown author", "license": lic,
            "licenseUrl": strip(md.get("LicenseUrl", {}).get("value", "")), "page": ii.get("descriptionurl", "")}, "ok"
ok = bad = skip = 0
for fid, c in cfg.items():
    old = man.get(fid)
    if old and old.get("title") == c["title"] and old.get("pick", "") == c.get("pick", "") and (root/old["file"]).exists():
        old["label"] = c["label"]; skip += 1; continue
    try: rec, why = one(fid, c)
    except Exception as e: rec, why = None, f"error: {e}"
    if rec: man[fid] = rec; ok += 1; print("ok  ", fid, "|", rec["license"], "|", rec["source"])
    else: man.pop(fid, None); bad += 1; print("SKIP", fid, "|", why)
    time.sleep(0.5)
manp.write_text(json.dumps(man, separators=(",", ":"), ensure_ascii=False))
print(f"images: {ok} new, {skip} already had, {bad} skipped; manifest has {len(man)}")
