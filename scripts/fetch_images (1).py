"""Download one freely licensed photo per fish from Wikimedia Commons, preferring photos of a fish out of the water
(caught, held by an angler, on a dock or boat) over underwater, museum, drawn or cooked pictures.
Reads scripts/fish_images.json. Writes data/app/fish/<id>.<ext>, data/app/fish.json (credits) and data/app/fish-review.html
(every pick with alternates, so a wrong or poor picture is easy to replace).
Only CC0, public domain, CC BY and CC BY-SA images are kept. Already-downloaded fish are skipped unless their entry changed.
To force a picture, add "pick": "File:Name.jpg" to that fish in fish_images.json. One failure never stops the rest."""
import json, pathlib, re, time, html, urllib.request, urllib.parse
root = pathlib.Path(__file__).resolve().parent.parent
cfg = json.loads((root/"scripts"/"fish_images.json").read_text())
outdir = root/"data"/"app"/"fish"; outdir.mkdir(parents=True, exist_ok=True)
manp = root/"data"/"app"/"fish.json"
man = json.loads(manp.read_text()) if manp.exists() else {}
VERSION = 2
UA = "KeepersFishingApp/1.0 (https://github.com/ec987/Keepers; personal fishing-rules page)"
def get(url):
    err = None
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30) as r: return r.read()
        except Exception as e:
            err = e; time.sleep(2 + 3*i)
    raise err
def api(**p):
    p.update(format="json", formatversion="2")
    return json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p)))
GOOD = re.compile(r"^(cc0|public domain|pd\b|pdm|cc[ -]by(-sa)?\b)", re.I)
BAD_LIC = re.compile(r"(^|[\s-])(nc|nd)([\s-]|$)|fair use|non-?commercial|no deriv", re.I)
PLUS = {"caught": 4, "angler": 4, "fisherman": 4, "fishermen": 3, "hooked": 3, "held": 3, "holding": 3, "landed": 3, "catch": 2, "fishing": 2,
        "in hand": 3, "dock": 1, "pier": 1, "boat": 1, "kayak": 1, "cooler": 1, "on ice": 1, "fresh": 1, "angling": 3, "rod": 1}
MINUS = {"underwater": -6, "aquarium": -5, "diving": -4, "diver": -4, "snorkel": -4, "museum": -5, "specimen": -3, "preserved": -4,
         "drawing": -6, "illustration": -6, "painting": -6, "plate": -3, "fillet": -4, "cooked": -5, "fried": -5, "grilled": -5,
         "restaurant": -5, "sushi": -5, "market": -3, "stamp": -6, "map": -6, "skeleton": -5, "fossil": -6, "larva": -6, "egg": -4,
         "swimming": -3, "reef": -3, "school of": -4, "tank": -4, "dead": -2, "diagram": -6, "plate ": -3, "scale bar": -3, "fish tank": -4, "sketch": -6}
def strip(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s or ""))).strip()
def candidates(c):
    sci = c["sci"]; seen = {}
    qs = ['"%s" (caught OR angler OR fisherman OR fishing OR held OR holding OR hooked OR landed OR catch) filetype:bitmap' % sci,
          '"%s" filetype:bitmap' % sci]
    for q in qs:
        try:
            d = api(action="query", generator="search", gsrsearch=q, gsrnamespace="6", gsrlimit="30", prop="imageinfo",
                    iiprop="url|mime|size|extmetadata", iiurlwidth="400")
        except Exception as e:
            print("   search error:", e); continue
        for pg in d.get("query", {}).get("pages", []):
            ii = (pg.get("imageinfo") or [None])[0]
            if ii: seen.setdefault(pg["title"], ii)
    return seen
def score(title, ii, sci):
    md = ii.get("extmetadata", {})
    lic = strip(md.get("LicenseShortName", {}).get("value", ""))
    if not lic or BAD_LIC.search(lic) or not GOOD.search(lic): return None
    if ii.get("mime") not in ("image/jpeg", "image/png"): return None
    if ii.get("width", 0) < 600 or ii.get("height", 0) < 300: return None
    text = " ".join([title, strip(md.get("ImageDescription", {}).get("value", "")), strip(md.get("ObjectName", {}).get("value", "")),
                     strip(md.get("Categories", {}).get("value", "")).replace("|", " ")]).lower()
    parts = sci.lower().split()
    if sci.lower() not in text and not (parts[0] in text and parts[1] in text): return None   # must name this species
    sc = sum(v for k, v in PLUS.items() if k in text) + sum(v for k, v in MINUS.items() if k in text)
    ar = ii["width"] / max(1, ii["height"])
    if ar > 2.6 or ar < 0.5: sc -= 3
    return sc, lic
def record(fid, c, fname, ii, lic, how):
    md = ii.get("extmetadata", {}); ext = "png" if ii["mime"] == "image/png" else "jpg"
    (outdir/f"{fid}.{ext}").write_bytes(get(ii.get("thumburl") or ii["url"]))
    return {"v": VERSION, "file": f"data/app/fish/{fid}.{ext}", "label": c["label"], "title": c["title"], "pick": c.get("pick", ""),
            "source": fname, "how": how, "author": strip(md.get("Artist", {}).get("value", "")) or "Unknown author", "license": lic,
            "licenseUrl": strip(md.get("LicenseUrl", {}).get("value", "")), "page": ii.get("descriptionurl", "")}
review = {}
def one(fid, c):
    if c.get("pick"):
        d = api(action="query", titles=c["pick"], prop="imageinfo", iiprop="url|mime|size|extmetadata", iiurlwidth="400")
        pg = d["query"]["pages"][0]
        if "imageinfo" not in pg: return None, "picked file not found: " + c["pick"]
        ii = pg["imageinfo"][0]; lic = strip(ii.get("extmetadata", {}).get("LicenseShortName", {}).get("value", ""))
        if not lic or BAD_LIC.search(lic) or not GOOD.search(lic): return None, f"picked file license not accepted ({lic})"
        return record(fid, c, c["pick"], ii, lic, "picked by hand"), "ok"
    cand = candidates(c); ranked = []
    for t, ii in cand.items():
        r = score(t, ii, c["sci"])
        if r: ranked.append((r[0], t, ii, r[1]))
    ranked.sort(key=lambda x: -x[0])
    review[fid] = [(sc, t, ii.get("thumburl", ""), lic) for sc, t, ii, lic in ranked[:4]]
    if not ranked: return None, "no suitable freely licensed photo found"
    sc, t, ii, lic = ranked[0]
    if sc < 0: return None, "only underwater, drawn or similar pictures found (best score %d); see fish-review.html" % sc
    how = "out of water (scored %d)" % sc if sc >= 3 else "best available, may be underwater or not a catch photo (scored %d)" % sc
    return record(fid, c, t, ii, lic, how), "ok"
ok = bad = skip = 0
for fid, c in cfg.items():
    old = man.get(fid)
    if old and old.get("v") == VERSION and old.get("title") == c["title"] and old.get("pick", "") == c.get("pick", "") and (root/old["file"]).exists():
        old["label"] = c["label"]; skip += 1; continue
    try: rec, why = one(fid, c)
    except Exception as e: rec, why = None, f"error: {e}"
    if rec: man[fid] = rec; ok += 1; print("ok  ", fid, "|", rec["license"], "|", rec["source"], "|", rec["how"])
    else: man.pop(fid, None); bad += 1; print("SKIP", fid, "|", why)
    time.sleep(0.5)
manp.write_text(json.dumps(man, separators=(",", ":"), ensure_ascii=False))
rows = []
for fid, c in cfg.items():
    m = man.get(fid)
    cell = ('<img src="../../%s" width="260"><br><b>%s</b><br><small>%s<br>%s</small>' % (m["file"], html.escape(m["source"]), html.escape(m["how"]), html.escape(m["license"]))) if m else "<i>no photo</i>"
    alts = "".join('<div style="display:inline-block;width:150px;margin:4px;vertical-align:top;font-size:11px"><img src="%s" width="150"><br>%s<br>score %s</div>' % (th, html.escape(t), sc) for sc, t, th, lic in review.get(fid, [])[1:])
    rows.append("<tr><td style='vertical-align:top;padding:8px'><b>%s</b><br><small>%s</small></td><td style='vertical-align:top;padding:8px'>%s</td><td style='padding:8px'>%s</td></tr>" % (html.escape(c["label"]), fid, cell, alts))
(root/"data"/"app"/"fish-review.html").write_text("<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width'><title>Fish photo review</title><body style='font-family:sans-serif'><h2>Fish photo review</h2><p>To replace a photo, tell Claude the fish and the alternate file name, or add \"pick\": \"File:Name.jpg\" for that fish in scripts/fish_images.json.</p><table>" + "".join(rows) + "</table>", encoding="utf8")
print(f"images: {ok} new, {skip} already had, {bad} skipped; manifest has {len(man)}")
