"""Fish photos from Wikimedia Commons. Two modes:
  python scripts/fetch_images.py              downloads ONLY the photos hand-picked in fish_images.json ("pick"); a fish with no pick shows no photo.
  python scripts/fetch_images.py --candidates saves a numbered contact sheet of candidate photos per fish to data/candidates/ so a person can look and choose.
Old description: Download one freely licensed photo per fish from Wikimedia Commons: the fish alone, out of the water, no people,
shown side-on so it can be compared with a fish that was just caught. Pictures that mention people, hands, anglers,
underwater scenes, aquariums, drawings, cooked fish and similar are scored down or skipped.
Reads scripts/fish_images.json. Writes data/app/fish/<id>.<ext>, data/app/fish.json (credits) and data/app/fish-review.html
(every pick with alternates, so a wrong or poor picture is easy to replace).
Only CC0, public domain, CC BY and CC BY-SA images are kept. Already-downloaded fish are skipped unless their entry changed.
To force a picture, add "pick": "File:Name.jpg" to that fish in fish_images.json. One failure never stops the rest."""
import json, pathlib, re, sys, io, time, html, urllib.request, urllib.parse
root = pathlib.Path(__file__).resolve().parent.parent
cfg = json.loads((root/"scripts"/"fish_images.json").read_text())
outdir = root/"data"/"app"/"fish"; outdir.mkdir(parents=True, exist_ok=True)
manp = root/"data"/"app"/"fish.json"
man = json.loads(manp.read_text()) if manp.exists() else {}
VERSION = 4
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
PLUS = {"lateral view": 4, "side view": 4, "white background": 4, "on ice": 3, "on deck": 3, "on a dock": 3, "on the dock": 3, "freshly caught": 2,
        "fresh": 1, "dead": 1, "lying": 2, "whole fish": 2, "specimen": 1, "noaa": 1, "fwc": 1, "usfws": 1, "fish and wildlife": 1, "caught": 1}
# people, hands and other scenes we do not want (each hit is a heavy penalty)
PEOPLE_RE = re.compile(r"\b(angler|anglers|fisherman|fishermen|fisherwoman|holding|holds|held|hand|hands|man|men|woman|women|boy|girl|child|children|kid|kids|person|people|posing|poses|his|her|family|guide|captain|crew|tournament|proud|smiling|wearing|angling|couple|friends)\b")
MINUS = {"underwater": -8, "aquarium": -8, "diving": -6, "diver": -6, "snorkel": -6, "museum": -4, "preserved": -5, "drawing": -8, "illustration": -8,
         "painting": -8, "plate": -4, "fillet": -6, "cooked": -8, "fried": -8, "grilled": -8, "restaurant": -8, "sushi": -8, "market": -3, "stamp": -8,
         "map": -8, "skeleton": -8, "fossil": -8, "larva": -8, "egg": -5, "swimming": -4, "reef": -4, "school of": -6, "tank": -6, "diagram": -8,
         "sketch": -8, "scale bar": -4, "mount": -5, "taxiderm": -8, "trophy": -3, "cartoon": -8, "logo": -8, "lure": -4, "spear": -4}
def strip(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s or ""))).strip()
def candidates(c):
    sci = c["sci"]; seen = {}
    qs = ['"%s" ("lateral view" OR "side view" OR "white background" OR "on ice" OR "on deck" OR "on a dock" OR "freshly caught" OR dead OR specimen) filetype:bitmap' % sci,
          '"%s" (NOAA OR FWC OR USFWS OR "Fish and Wildlife") filetype:bitmap' % sci,
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
    hit = lambda k: re.search(r"\b" + re.escape(k), text)
    sc = sum(v for k, v in PLUS.items() if hit(k)) + sum(v for k, v in MINUS.items() if hit(k))
    sc -= 10 * len(set(PEOPLE_RE.findall(text)))
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
CAND_MODE = '--candidates' in sys.argv
def one(fid, c):
    if c.get("pick"):
        d = api(action="query", titles=c["pick"], prop="imageinfo", iiprop="url|mime|size|extmetadata", iiurlwidth="400")
        pg = d["query"]["pages"][0]
        if "imageinfo" not in pg: return None, "picked file not found: " + c["pick"]
        ii = pg["imageinfo"][0]; lic = strip(ii.get("extmetadata", {}).get("LicenseShortName", {}).get("value", ""))
        if not lic or BAD_LIC.search(lic) or not GOOD.search(lic): return None, f"picked file license not accepted ({lic})"
        return record(fid, c, c["pick"], ii, lic, "picked by hand"), "ok"
    if not CAND_MODE: return None, "no hand-checked photo yet"
    cand = candidates(c); ranked = []
    avoid = {a.replace("_", " ").lower() for a in c.get("avoid", [])}
    for t, ii in cand.items():
        if t.replace("_", " ").lower() in avoid: continue
        r = score(t, ii, c["sci"])
        if r: ranked.append((r[0], t, ii, r[1]))
    ranked.sort(key=lambda x: -x[0])
    review[fid] = [(sc, t, ii.get("thumburl", ""), lic) for sc, t, ii, lic in ranked[:8]]
    if not ranked: return None, "no suitable freely licensed photo found"
    sc, t, ii, lic = ranked[0]
    if sc < -2: return None, "only underwater, drawn or similar pictures found (best score %d); see fish-review.html" % sc
    how = "out of water (scored %d)" % sc if sc >= 3 else "best available, may be underwater or not a catch photo (scored %d)" % sc
    return record(fid, c, t, ii, lic, how), "ok"

if CAND_MODE:
    from PIL import Image, ImageDraw
    cdir = root/"data"/"candidates"; cdir.mkdir(parents=True, exist_ok=True)
    idxp = cdir/"index.json"; idx = json.loads(idxp.read_text()) if idxp.exists() else {}
    for fid, c in cfg.items():
        if c.get("pick") or fid in idx: continue
        try:
            cand = candidates(c); ranked = []
            for t, ii in cand.items():
                r = score(t, ii, c["sci"])
                if r and r[0] > -8 and ii.get("thumburl"): ranked.append((r[0], t, ii))
            ranked.sort(key=lambda x: -x[0]); ranked = ranked[:12]
            if not ranked: print("none", fid); continue
            W, H = 320, 220; cols = 4; rows_n = (len(ranked) + cols - 1) // cols
            sheet = Image.new("RGB", (W*cols, H*rows_n), "white"); names = []
            for i, (sc, t, ii) in enumerate(ranked):
                try:
                    im = Image.open(io.BytesIO(get(ii["thumburl"]))).convert("RGB"); im.thumbnail((W-4, H-4))
                    sheet.paste(im, ((i % cols)*W + 2, (i // cols)*H + 2))
                except Exception as e: print("  thumb fail", t, e)
                d = ImageDraw.Draw(sheet); x, y = (i % cols)*W, (i // cols)*H
                d.rectangle([x, y, x+34, y+26], fill="red"); d.text((x+8, y+7), str(i+1), fill="white")
                names.append(t)
            sheet.save(cdir/f"{fid}.jpg", quality=80); idx[fid] = names; print("sheet", fid, len(names))
        except Exception as e: print("error", fid, e)
        time.sleep(0.5)
    idxp.write_text(json.dumps(idx, indent=1)); sys.exit(0)
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
