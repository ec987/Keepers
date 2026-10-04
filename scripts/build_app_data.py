"""Trim the big raw boundary files down to a small file the phone page can load.
Covers the Southwest Florida Gulf coast only. Output: data/app/boundaries.json"""
import json, pathlib
from shapely.geometry import shape, box
root = pathlib.Path(__file__).resolve().parent.parent
BBOX = (-83.2, 25.9, -81.3, 27.2)   # lon_min, lat_min, lon_max, lat_max
TOL = 0.0005                         # simplification, about 55 m
clip = box(*BBOX)

def load(name):
    return json.load(open(root / "data" / "raw" / f"{name}.json"))["features"]

def polys(geom):
    return list(geom.geoms) if geom.geom_type in ("MultiPolygon", "GeometryCollection") else [geom]

def to_rings(geom):
    out = []
    for p in polys(geom):
        if p.geom_type != "Polygon" or p.is_empty:
            continue
        out.append([[[round(x, 5), round(y, 5)] for x, y in p.exterior.coords]] +
                   [[[round(x, 5), round(y, 5)] for x, y in h.coords] for h in p.interiors])
    return out

result = {"bbox": BBOX, "federal_waters": [], "shellfish": [], "notes": "Reference data only. Not a legal boundary."}
for f in load("gulfcouncil-fedwaters-58"):
    g = shape(f["geometry"]).buffer(0).intersection(clip).simplify(TOL, preserve_topology=True)
    result["federal_waters"] += to_rings(g)
for f in load("fdacs-sha-allyear"):
    p = f["properties"]
    g = shape(f["geometry"]).buffer(0).intersection(clip)
    if g.is_empty:
        continue
    g = g.simplify(TOL, preserve_topology=True)
    rings = to_rings(g)
    if rings:
        result["shellfish"].append({"id": p.get("SH_ID"), "name": p.get("SH_NAME"), "class": p.get("CLASS"), "rings": rings})
out = root / "data" / "app"; out.mkdir(parents=True, exist_ok=True)
(out / "boundaries.json").write_text(json.dumps(result, separators=(",", ":")))
print("federal polygons:", len(result["federal_waters"]), "| shellfish shapes:", len(result["shellfish"]),
      "| bytes:", (out / "boundaries.json").stat().st_size)
