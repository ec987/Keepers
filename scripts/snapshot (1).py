"""Download each source in sources.json to data/raw/ and record results in data/status.json.
Also saves the text of every FWC saltwater recreational species page to data/raw/species/.
A source is saved only if its content looks right. Otherwise the last good copy is kept."""
import json, hashlib, time, datetime, urllib.request, pathlib, os, re
from html.parser import HTMLParser

root = pathlib.Path(__file__).resolve().parent.parent
raw = root / "data" / "raw"; raw.mkdir(parents=True, exist_ok=True)
UA = "fishing-rules-snapshot/0.3 (personal project)"
status = {"run_utc": datetime.datetime.utcnow().isoformat() + "Z", "sources": {}, "species": {}}
manual = os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch"
sunday = datetime.datetime.utcnow().weekday() == 6

def fetch(url):
    last = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            return urllib.request.urlopen(req, timeout=60).read()
        except Exception as e:
            last = e; time.sleep(5)
    raise last

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

class T(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "nav", "header", "footer", "form", "iframe"}
    BLOCK = {"p", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "br", "section", "table", "dt", "dd"}
    def __init__(s): super().__init__(); s.out = []; s.skip = 0
    def handle_starttag(s, t, a):
        if t in s.SKIP: s.skip += 1
        if t in s.BLOCK: s.out.append("\n")
    def handle_endtag(s, t):
        if t in s.SKIP and s.skip: s.skip -= 1
        if t in s.BLOCK: s.out.append("\n")
    def handle_data(s, d):
        if not s.skip: s.out.append(d)

def page_text(html):
    p = T(); p.feed(html)
    lines = [re.sub(r"[ \t\xa0]+", " ", l).strip() for l in "".join(p.out).split("\n")]
    out = []
    for l in lines:
        if l and (not out or out[-1] != l): out.append(l)
    return "\n".join(out)

for s in json.load(open(root / "sources.json")):
    sid = s["id"]
    if s.get("weekly") and not (manual or sunday):
        continue
    try:
        body = fetch(s["url"])
        problem = check(s["ext"], body)
        entry = {"ok": problem is None, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()[:16]}
        if problem: entry["problem"] = problem
        else: (raw / f"{sid}.{s['ext']}").write_bytes(body)
        status["sources"][sid] = entry
    except Exception as e:
        status["sources"][sid] = {"ok": False, "problem": str(e)[:200]}
    time.sleep(2)

# Species pages: found from the FWC index page, saved as plain text so real rule changes show up in git history.
idx = raw / "fwc-index.html"
if idx.exists() and (manual or sunday):
    html = idx.read_text(errors="ignore")
    slugs = sorted(set(re.findall(r'href="/fishing/saltwater/recreational/([a-z0-9\-]+)/?"', html)))
    sp = raw / "species"; sp.mkdir(exist_ok=True)
    for slug in slugs:
        try:
            body = fetch(f"https://myfwc.com/fishing/saltwater/recreational/{slug}/")
            problem = check("html", body)
            if problem:
                status["species"][slug] = {"ok": False, "problem": problem}
            else:
                txt = page_text(body.decode("utf-8", errors="ignore"))
                (sp / f"{slug}.txt").write_text(txt)
                status["species"][slug] = {"ok": True, "chars": len(txt)}
        except Exception as e:
            status["species"][slug] = {"ok": False, "problem": str(e)[:200]}
        time.sleep(2)

(root / "data" / "status.json").write_text(json.dumps(status, indent=1))
print(json.dumps(status, indent=1))
