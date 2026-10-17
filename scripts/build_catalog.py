"""Species catalog for the Southwest Florida Gulf coast (Gulf state waters unless noted).
Hand-entered from the saved FWC page text. Each entry lists 'evidence' lines copied from the page.
verify_catalog.py checks that every evidence line still appears in the latest saved page text."""
import json, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
LIC = "Saltwater fishing license (unless exempt)"
SRFS = "State Reef Fish Survey sign-up (required to fish for certain reef fish from a private vessel)"
GEARROW = ["Reef fish gear","Required when fishing for reef fish (FWC Reef Fish Gear Rules page). Gulf state waters: have on board and use non-stainless-steel, non-offset circle hooks when fishing with natural bait, a dehooking device, and a descending device or venting tool rigged and ready for use. Gulf federal waters: the same, except the page says only 'non-stainless steel circle hooks' (offset not mentioned), so use non-offset to be safe. Reef fish in state waters means groupers, snappers, amberjacks, gray triggerfish, red porgy, sea bass, hogfish and tilefish. Full page text is below."]
ALWAYS = {"kind": "always"}
E = []
def add(id, name, group, slug, size, bag, season=ALWAYS, rows=None, lic=None, fed=None, evidence=None, **kw):
    e = dict(id=id, name=name, group=group, slug=slug, size=size, bag=bag, season=season,
             rows=rows or [], lic=lic or [LIC], fed=fed or {"check": True}, evidence=evidence or [])
    e.update(kw); E.append(e)
SAME = lambda note: {"same": True, "note": note}

# ---------- Snook, redfish, seatrout and other inshore ----------
add("snook","Snook","Inshore","snook","28 to 33 inches total length (slot)","1 per person per day",
    {"kind":"md","open":[["03-01","04-30"],["10-01","11-30"]]},
    [["Possession","Whole until landed ashore. Hook and line only. Charter captain and crew may not keep a bag limit."],["Location","Charlotte Harbor snook region"]],
    [LIC,"Snook permit"],SAME("Snook rules also apply in adjacent federal waters."),
    ["Slot Limit: Not less than 28” or more than 33” total length","Bag Limit: One fish per person per day"],
    region={"latMin":26.2538,"latMax":27.0788,"msg":"This pin is outside the Charlotte Harbor snook region (26°15.2'N to 27°04.7'N on the Gulf coast). Snook rules differ by region."})
add("red-drum","Red drum (redfish)","Inshore","red-drum","18 to 27 inches total length (slot)","1 per person per day, 2 per vessel",ALWAYS,
    [["Possession","Whole until landed ashore. Transport limit: 4 per person when traveling by vehicle away from the fishing site."],["Gear","Hook and line and cast net only. No spearing, snatch hooking, or multiple hooks with natural bait."],["Charter","Captain and crew may not keep a bag limit on a for-hire trip."]],
    None,SAME("Regional rules apply in state and adjacent federal waters per page; this region has the same limits."),
    ["Slot Limit: Not less than 18\" and no more than 27\" total length","Daily Bag Limit: 1 fish per person, 2 fish vessel limit"])
add("seatrout","Spotted seatrout (speckled trout)","Inshore","spotted-seatrout","15 to 19 inches total length (slot)","3 per person per day",ALWAYS,
    [["Over-slot","May possess one fish over 19 inches per vessel (or per person if fishing from shore), included in the bag limit."],["Regions","Same limits in the Sarasota Bay, Charlotte Harbor and Southwest regions."],["Possession","Must remain in whole condition until landed ashore."],["Gear","Allowed: hook and line, cast net. Prohibited: any multiple hook used with live or dead natural bait; snatching."],["Charter","For-hire captain and crew may not keep a bag limit on a for-hire trip."]],
    None,SAME("Regulations apply in inland, state and adjacent federal waters."),
    ["Slot limit: Not less than 15” or more than 19” total length","Bag limit: Three fish per person per day"])
add("black-drum","Black drum","Inshore","black-drum","14 to 24 inches (slot); one over 24 inches allowed","5 per harvester per day (may include one over 24 inches)",ALWAYS,
    [["Gear","Hook and line, cast net, seine, spear or gig. No multiple hooks with natural bait; no snatching."]],
    None,{"check":True},["Slot Limit: 14-24\" with one fish over 24\"","Daily Bag Limit: 5 per harvester per day"])
add("sheepshead","Sheepshead","Inshore","sheepshead","12 inches total length minimum","8 per person per day (vessel limit 50 per trip in March and April)",ALWAYS,
    [["Gear","Hook and line, cast net, seine, spear or gig. No multiple hooks with natural bait; no snatching."]],
    None,SAME("State regulations extend into federal waters."),["Minimum Size Limit: 12\" total length","Daily Bag Limit: 8 per person"])
add("flounder","Flounder","Inshore","flounder","14 inches total length minimum","5 per person per day",
    {"kind":"closed_md","closed":[["10-15","11-30"]]},
    [["Species covered","Gulf flounder, southern flounder, summer flounder and fringed flounder. Rules apply in state and federal waters off Florida."],["Closed","Closed every year Oct. 15 through Nov. 30."],["Gear","Spears, gigs, hook and line, seine, cast net. No multiple hooks with natural bait; no snatching."]],
    None,SAME("Flounder regulations are for state and federal waters off Florida."),["Minimum Size Limit: 14\" total length","Daily Bag Limit: 5 per person","Closed annually from Oct. 15 through Nov. 30."])
add("pompano","Florida pompano","Inshore","permit","11 inches fork length minimum","6 per harvester per day",ALWAYS,
    [["Gear","Hook and line, cast net, beach or haul seine only. No multiple hooks with natural bait; no snatching."],["Related","Permit and African pompano have different rules (see separate card)."]],
    None,SAME("Page lists state and federal waters together."),["Minimum Size Limit: 11\" fork length","Daily Bag Limit: 6 per harvester"])
add("mullet","Mullet","Inshore","mullet","None","50 per person per day. Vessel limit 50 (Sept. 1-Jan. 31) or 100 (Feb. 1-Aug. 31)",ALWAYS,
    [["Local","More restrictive seasonal bag limits apply in parts of Pinellas County, and seasonal night closures apply in parts of Charlotte County."],["Gear","Hook and line, spears, gigs, seine, cast net."]],
    None,{"check":True},["Daily Bag Limit: 50 fish per person","Minimum Size Limit: None"],
    forceCheckRegion={"latMin":26.7,"latMax":27.2,"msg":"Parts of Charlotte County have seasonal night closures for mullet. Check the FWC page."})
add("tripletail","Tripletail","Inshore","tripletail","18 inches minimum","2 per person per day",ALWAYS,
    [["Gear","Hook and line only. No nets or spearing. No multiple hooks with natural bait; no snatching."]],
    None,SAME("State regulations apply in federal waters."),["Minimum Size Limit: 18\"","Daily Bag Limit: 2 fish per person"])
add("bluefish","Bluefish","Inshore","bluefish","12 inches fork length minimum","10 per harvester per day",ALWAYS,
    [["Gear","Hook and line, spears, gigs, seine, cast net."]],None,{"same":True,"note":"Page lists Gulf state and federal waters together."},
    ["Minimum Size Limit: 12\" fork length","Daily Bag Limit: 10 per harvester"])
add("spanish-mackerel","Spanish mackerel","Inshore","spanish-mackerel","12 inches fork length minimum","15 per harvester per day",ALWAYS,
    [["Gear","Beach or haul seine, cast net, hook and line, spear."]],None,{"check":True},["Minimum Size Limit: 12\" fork length","Daily Bag Limit: 15 per harvester"])
add("king-mackerel","King mackerel","Inshore","king-mackerel","24 inches fork length minimum","3 per harvester per day",ALWAYS,
    [["Gear","Hook and line and spearing only."]],None,{"check":True},["Minimum Size Limit: 24\" fork length","Daily Bag Limit: 3 per harvester"])
add("cobia","Cobia","Inshore","cobia","36 inches fork length minimum","1 per person or 2 per vessel, whichever is less",ALWAYS,
    [["Gear","Spears, gigs, hook and line, seine, cast net."]],None,SAME("Page lists the same limits for Gulf federal waters."),["Minimum Size Limit: 36” fork length","Daily Bag Limit: 1 per person or 2 per vessel, whichever is less"])
add("barracuda","Barracuda","Inshore","barracuda","None (Lee County and north)","2 fish or 100 pounds per person, whichever is more",ALWAYS,
    [["Collier County","Waters off Collier County and south: slot 15-36 inches fork length with 1 fish over 36 inches per person or vessel; 2 per person, 6 per vessel."]],
    None,{"check":True},["Minimum Size Limit: None","Daily Bag Limit: 2 fish or 100 pounds, whichever is more"],
    forceCheckRegion={"latMin":0,"latMax":26.33,"msg":"Collier County rules differ for barracuda (slot 15-36 inches, 2 per person, 6 per vessel). Shown for Lee County and north."})
add("spot-croaker","Spot and croaker","Inshore","spot-croaker","None","100 pounds per person per day",ALWAYS,[],None,{"check":True},["Daily Bag Limit: 100 pounds per person"])
add("sand-seatrout","Weakfish and sand seatrout","Inshore","weakfish","None (outside the Nassau County weakfish zone)","100 pounds per person per day",ALWAYS,
    [["Gear","Hook and line, cast net."]],None,{"check":True},["Minimum Size Limit: None","Daily Bag Limit: 100 pounds per person"])
add("dolphinfish","Dolphinfish (mahi-mahi)","Offshore","dolphinfish","None (Gulf state waters)","10 per person or 60 per vessel, whichever is less",ALWAYS,
    [["Charter","Captain and crew may not keep a bag limit."],["Gear","Hook and line, spearing."]],None,{"check":True},["Minimum Size Limit: None","Daily Bag Limit: 10 per person or 60 per vessel, whichever is less"])
add("wahoo","Wahoo","Offshore","wahoo","None","2 per person per day",ALWAYS,[],None,{"check":True},["Minimum Size Limit: None","Daily Bag Limit: 2 per person"])

# ---------- Reef fish ----------
LAND = ["Landing","Must be landed with the head and fins intact (FWC grouper page, stated at the end of the Gulf section)."]
CH_GAG = ["Charter","0 fish bag limit for charter captain and crew (FWC grouper page)."]
CH_ST = ["Charter","State waters only: 0 fish bag limit for charter captain and crew (FWC grouper page)."]
FEDG = "Federal waters: several grouper are closed Feb. 1-Mar. 31 seaward of the 20-fathom break and The Edges are closed Jan. 1-Apr. 30. Yellowmouth has no federal size limit."
AGG = ["Aggregate","No more than 4 grouper of all species combined, per person per day."]
add("gag","Gag grouper","Reef fish","groupers","24 inches TL minimum","2 per person (within the 4 grouper aggregate)",
    {"kind":"dates","from":"2026-01-01","to":"2026-12-31","open":[["2026-09-01","2026-09-30"]]},
    [AGG,LAND,GEARROW,CH_GAG],[LIC,SRFS],SAME(FEDG),
    ["Open September 1-30, 2026.","24” TL"])
add("black-grouper","Black grouper","Reef fish","groupers","24 inches TL minimum","Up to 4 per person (within the 4 grouper aggregate)",ALWAYS,
    [AGG,LAND,GEARROW,CH_ST],[LIC,SRFS],SAME(FEDG),["Black\nMin. Size Limit\n24” TL","4 per person within 4 grouper aggregate"] if False else ["4 per person within 4 grouper aggregate"],fedClosed=[["02-01","03-31"]])
add("red-grouper","Red grouper","Reef fish","groupers","20 inches TL minimum","2 per person (within the 4 grouper aggregate)",ALWAYS,
    [AGG,LAND,GEARROW,CH_ST],[LIC,SRFS],SAME(FEDG),["2 per person within the 4 grouper aggregate"],fedClosed=[["02-01","03-31"]])
add("scamp","Scamp, yellowfin, yellowmouth","Reef fish","groupers","Scamp 16 in. TL. Yellowfin 20 in. TL. Yellowmouth 20 in. TL (state)","Up to 4 per person (within the 4 grouper aggregate)",ALWAYS,
    [AGG,LAND,GEARROW],[LIC,SRFS],SAME(FEDG),["Scamp\nMin. Size Limit\n16” TL","Yellowfin"] if False else ["Up to 4 per person within 4 grouper aggregate"],fedClosed=[["02-01","03-31"]])
add("grouper-other","Other groupers (hinds, coney, graysby, misty, snowy, Warsaw, speckled)","Reef fish","groupers","None","Up to 4 per person (within aggregate). Warsaw and speckled hind: 1 of each per vessel",ALWAYS,
    [AGG,LAND,GEARROW],[LIC,SRFS],SAME(FEDG),["1 of each per vessel within 4 grouper aggregate","Snowy"])
add("hogfish","Hogfish","Reef fish","hogfish","14 inches fork length minimum","5 per harvester per day",ALWAYS,
    [GEARROW],[LIC,SRFS],SAME("Gulf federal waters north of Cape Sable: open year-round, 14 inch minimum, 5 per person."),
    ["Minimum Size Limit: 14\" fork length","Daily Bag Limit: 5 per harvester"])
add("triggerfish","Gray triggerfish","Reef fish","triggerfish","15 inches fork length minimum","1 per person per day",
    {"kind":"md","open":[["03-01","05-31"],["08-01","12-31"]]},
    [GEARROW,["Queen triggerfish","Managed as marine life; must be kept alive until landed."]],[LIC,SRFS],
    {"same":True,"note":"Federal waters: same season; 1 fish within the 20 reef fish aggregate; possible early quota closures."},
    ["Minimum Size Limit: 15\" fork length","Open March 1-May 31 And Aug. 1 - Dec. 31."])
add("greater-amberjack","Greater amberjack","Reef fish","amberjack","34 inches fork length minimum","1 per person per day",
    {"kind":"dates","from":"2026-01-01","to":"2026-12-31","open":[["2026-09-01","2026-10-13"]]},
    [GEARROW],[LIC,SRFS],SAME("State and federal Gulf waters share this season."),
    ["Minimum Size Limit: 34” Fork Length","Season: Open September 1 - October 13, 2026"])
add("lesser-amberjack","Lesser amberjack and banded rudderfish","Reef fish","amberjack","14 to 22 inches fork length (slot)","5 per person per day (both species combined)",ALWAYS,
    [["Related","Almaco jack is an unregulated species (default limit)."]],[LIC,SRFS],{"check":True},
    ["Cannot be less than","Daily Recreational Bag Limit:"])
add("black-sea-bass","Black sea bass","Reef fish","black-sea-bass","10 inches total length minimum","100 pounds per person per day",ALWAYS,
    [["Gear","Gulf: non-stainless-steel, non-offset circle hooks and a dehooking device."]],None,SAME("Page lists Gulf state rules only. Federal Gulf rules were not reviewed."),
    ["Minimum Size Limit: 10\" total length","Daily Bag Limit: 100 pounds per person"])
add("red-porgy","Red porgy","Reef fish","red-porgy","None (Gulf state waters)","2 fish or 100 pounds per person, whichever is more",ALWAYS,
    [GEARROW],None,{"check":True},["Minimum Size Limit: None","Daily Bag Limit: 2 fish or 100 lbs. per person, whichever is more."])
add("tilefish","Tilefish (golden, blueline)","Reef fish","tilefish","None (Gulf state waters)","100 pounds or 2 per person, whichever is greater",ALWAYS,
    [GEARROW],None,{"check":True},["Minimum Size Limit: None","Daily Bag Limit: 100 pounds or 2 per person, whichever is greater"])
# Snappers (Gulf state waters)
SNAGG = ["Aggregate","Snapper aggregate: no more than 10 snapper per person per day across listed species (exceptions noted)."]
RS = ["2026-05-22","2026-07-31"],["2026-09-01","2026-10-04"],["2026-10-09","2026-10-22"],["2026-10-23","2026-10-25"],["2026-10-30","2026-11-01"],["2026-11-07","2026-11-08"],["2026-11-14","2026-11-15"],["2026-11-21","2026-11-22"],["2026-11-26","2026-11-29"],["2026-12-05","2026-12-06"],["2026-12-12","2026-12-13"],["2026-12-19","2026-12-20"],["2026-12-25","2026-12-27"],["2027-01-01","2027-01-04"]
add("red-snapper","Red snapper","Reef fish","snappers","16 inches TL minimum","2 per person (within the 10 snapper aggregate)",
    {"kind":"dates","from":"2026-01-01","to":"2027-01-04","open":[list(x) for x in RS]},
    [SNAGG,["Applies to","Private recreational vessels and for-hire vessels without a federal permit. Charter captain and crew: zero."],GEARROW],[LIC,SRFS],
    SAME("Season applies to private vessels in state and federal Gulf waters."),
    ["Oct. 9 - 22 (Daily)","Dec. 25 - 27 (Christmas weekend)","16\" TL"])
add("lane-snapper","Lane snapper","Reef fish","snappers","10 inches TL minimum (state)","20 per person (not in the 10 snapper aggregate)",ALWAYS,
    [["Federal","8 inch minimum; 20 within the 20 reef fish aggregate."]],[LIC,SRFS],{"check":True},["Lane\nMin. Size Limit\nState: 10\" TL\nFederal: 8\" TL"] if False else ["State: 20 per person (not included in the 10-snapper aggregate bag limit)"])
add("vermilion","Vermilion snapper","Reef fish","snappers","10 inches TL minimum","10 per person (not in the snapper aggregate)",ALWAYS,
    [["Federal","10 per person within the 20 reef fish aggregate."]],[LIC,SRFS],{"check":True},["State: 10 per person (not included in the 10 snapper aggregate bag limit)"])
add("gray-snapper","Gray (mangrove) snapper","Reef fish","snappers","10 inches TL minimum (state); 12 inches (federal)","5 per person (within the 10 snapper aggregate)",ALWAYS,
    [SNAGG,["Federal","12 inch minimum; 10 per person within the snapper aggregate."]],[LIC,SRFS],{"check":True},["State: 5 per person within the 10 snapper aggregate bag limit"])
add("mutton-snapper","Mutton snapper","Reef fish","snappers","18 inches TL minimum","5 per person (within the 10 snapper aggregate)",ALWAYS,
    [SNAGG],[LIC,SRFS],{"check":True},["5 per person within the 10 snapper aggregate bag limit"])
add("cubera-snapper","Cubera snapper","Reef fish","snappers","12 inches TL minimum","10 per person (within the snapper aggregate). No more than 2 over 30 inches per harvester or vessel",ALWAYS,
    [SNAGG,["Over 30 inches","30 inch or larger cubera are not counted in the snapper aggregate."]],[LIC,SRFS],{"check":True},["30\" or larger cubera are not included within the 10 snapper aggregate bag limit"])
add("other-snappers","Yellowtail, dog, mahogany, schoolmaster, black, wenchman, queen, blackfin, silk snapper","Reef fish","snappers","Yellowtail, dog, mahogany: 12 in. TL. Schoolmaster: 10 in. TL. Others: none","Up to 10 per person (within the snapper aggregate)",ALWAYS,
    [SNAGG],[LIC,SRFS],{"check":True},["Yellowtail, Dog, and Mahogany","Black Wenchman, Queen, Blackfin, and Silk"])

# ---------- Crustaceans ----------
add("stone-crab","Stone crab (claws)","Crustaceans","stone-crab","2 7/8 inches claw; claws only","1 gallon of claws per person or 2 gallons per vessel, whichever is less",
    {"kind":"md","open":[["10-15","12-31"],["01-01","05-01"]]},
    [["Egg-bearing","Harvest from egg-bearing crabs prohibited."],["Traps","Up to 5 traps per person. Age 16+ must complete the free recreational trap registration at GoOutdoorsFlorida.com. Traps may be set 10 days before the season but not tended until it opens."]],
    [LIC],{"check":True},["Minimum Size Limit: 2 7/8 inches; only claws may be harvested.","State Waters Harvest Seasons: Open Oct. 15 - May 1 (closed on May 2)"])
add("blue-crab","Blue crab","Crustaceans","blue-crab","None","10 gallons whole per harvester per day",ALWAYS,
    [["Egg-bearing","Harvest of egg-bearing crabs prohibited."],["Traps","Up to 5 traps per person. Age 16+ must complete the free recreational trap registration. New throat size rules apply."]],[LIC],{"check":True},
    ["Size Limit: None","Daily Bag Limit: 10 gallons whole per harvester per day"])
add("lobster","Spiny lobster","Crustaceans","lobster","Carapace longer than 3 inches, measured in the water","6 per person per day (regular season)",
    {"kind":"md","open":[["08-06","12-31"],["01-01","03-31"]],"check":[["07-20","07-31"]]},
    [["Mini-season","Last consecutive Wednesday and Thursday of July. The dates printed on the FWC page look inconsistent, so confirm them."],["Gear","Landing or dip nets, bullynets up to 3 ft, hoop nets up to 10 ft. No spears, snares or traps."],["Required","A measuring device must be carried and used."]],
    [LIC+" (check whether a lobster permit is also required)"],{"check":True},
    ["Season: Aug. 6-March 31","Minimum Size Limit: Carapace length must be larger than 3 inches, measured in the water."])
add("shrimp","Shrimp","Crustaceans","shrimp","None","5 gallons heads-on per harvester or per vessel",ALWAYS,
    [["Region","Southwest region: open year-round."],["Gear","Cast net up to 14 ft stretched; dip net up to 96 inches around; no more than two nets per vessel. See page for other gear."]],
    None,{"check":True},["All other regions (Southeast and Southwest) open year-round.","5 gallons (heads on) per harvester"])
# ---------- Special handling ----------
add("sharks","Sharks","Special","sharks","Group 1 (8 species): none. Group 2 (7 species): 54 inches fork length","1 shark per person per day; 2 per vessel",ALWAYS,
    [["Prohibited","About 30 species are prohibited, including great hammerhead, lemon, sandbar, tiger and bull-type look-alikes. Learn them before keeping a shark."],["From shore","Shore-based shark fishing needs the Shark-Smart course and a free permit."]],
    None,{"check":True},["Bag limit","1 shark per person per day."],status="CHECK",why="Many shark species are prohibited. Identify the species and read the FWC shark page before keeping one.")
add("permit-pompano","Permit and African pompano","Special","permit","Varies by species and zone","Varies by species and zone",ALWAYS,[["Note","The FWC page splits permit and African pompano by tabs and zones. I could not extract their limits reliably. Read the page."]],
    None,{"check":True},["Pompano Endorsement Zone"],status="CHECK",why="Limits vary by species and zone. Read the FWC page.")
add("tuna-billfish","Tuna, billfish, swordfish","Special","billfish-tuna","See page","See page",ALWAYS,[["Note","Federal highly migratory species rules and permits apply. Not reviewed."]],None,{"check":True},[],status="CHECK",why="Federal permits and special rules apply. Not reviewed.")
add("lionfish","Lionfish","Special","lionfish","None","Unlimited",ALWAYS,[["Note","Harvest is encouraged. Special gear is allowed; see FWC page."]],None,SAME("Page says regulations apply in state and federal waters."),["Minimum Size Limit: None","Daily Bag Limit: Unlimited"])
add("unregulated","Unregulated species (jack crevalle, ladyfish, pinfish, gafftopsail catfish, whiting, cero mackerel, bonito and others)","Special","unregulated","None","2 fish or 100 pounds per person per day, whichever is more",ALWAYS,
    [["Gear","Hook and line, spears, gigs, haul seines and cast nets (some local limits). No chemicals, explosives, electricity, bang sticks or fish traps."],["Note","This default also applies to any species with no specific rule, but check the species-specific pages first."]],
    None,{"check":True},["Two fish or 100 pounds per person, per day - whichever is more."])
# ---------- Never keep ----------
add("tarpon","Tarpon","Never keep","tarpon","n/a","Catch and release only",{"kind":"never"},
    [["Handling","Fish over 40 inches must stay in the water. One record tag per person per year allows pursuit of a state or world record."],["Boca Grande Pass","Special gear rules: no jigs with the weight hanging below the hook; Apr.-Jun. limits on lines and no breakaway gear."]],
    None,SAME("State and federal Gulf waters."),["Tarpon is a catch-and-release only fishery."],status="CLOSED",why="Catch and release only.")
add("bonefish","Bonefish","Never keep","bonefish","n/a","Catch and release only",{"kind":"never"},[],None,SAME("Applies in Florida waters."),["Bonefish is a Catch-And-Release fishery"],status="CLOSED",why="Catch and release only.")
add("goliath","Goliath grouper","Never keep","goliath","n/a","Harvest prohibited without a Goliath Harvest Program permit",{"kind":"never"},
    [["Handling","Release immediately; do not lift large fish out of the water."]],None,SAME("Applies in Florida waters."),["Harvest is prohibited without a permit."],status="CLOSED",why="Harvest prohibited without a permit.")
add("nassau","Nassau grouper","Never keep","groupers","n/a","Harvest prohibited",{"kind":"never"},[],None,SAME("Gulf and Atlantic."),["Nassau\nHarvest Prohibited"],status="CLOSED",why="Harvest prohibited.")

# ---------- full FWC rule text, copied word for word from the saved pages ----------
STOP = re.compile(r"^(more information|information|related links|management history:?|\U0001F4AC ask buck!|\u2716)$|management$|^regulation(s)? (history|update)$", re.I)
DROP = re.compile(r"^(expand/collapse.*|image credit.*|copyright.*|photo.*|skip to main content|learn more|full text (rule|regulations?)|.* species profile|federal (gulf|atlantic) regulations|saf?mc website)$", re.I)
REGION = re.compile(r"^(Panhandle|Big Bend|Tampa Bay|Sarasota Bay|Charlotte Harbor|Southwest|Southeast|Indian River Lagoon|Northeast) Region$")
def page_lines(text):
    L = [l.strip() for l in text.splitlines()]
    try: i = L.index("Recreational Regulations") + 2
    except ValueError: i = 0
    out = []
    for l in L[i:]:
        if STOP.search(l) and out: break
        if not l or DROP.match(l): continue
        out.append(l)
    return out
def split_regions(lines):
    pre, regs, post, cur = [], {}, [], None
    for l in lines:
        m = REGION.match(l)
        if m: cur = m.group(1); regs[cur] = [l]; continue
        if l == "Other Regulations": cur = None; post.append(l); continue
        if post: post.append(l)
        elif cur: regs[cur].append(l)
        else: pre.append(l)
    return {"pre": pre, "regions": regs, "post": post}
texts = {}
for slug in sorted({e["slug"] for e in E} | {"gear-rules"}):
    p = root/"data"/"raw"/"species"/(slug + ".txt")
    if not p.exists(): continue
    lines = page_lines(p.read_text(encoding="utf8"))
    if any(REGION.match(l) for l in lines):
        t = split_regions(lines)
        t["regions"] = {k: v for k, v in t["regions"].items() if k in ("Sarasota Bay", "Charlotte Harbor", "Southwest")}  # the three regions this page covers
        texts[slug] = t
    else: texts[slug] = {"lines": lines}
fetched = ""
try: fetched = json.loads((root/"data"/"status.json").read_text())["run_utc"][:10]
except Exception: pass
out = {"updated":"2026-10-04","scope":"Gulf state waters, Southwest Florida (Venice to south of Naples)","species":E,"texts":texts,"fetched":fetched}
(root/"data"/"app"/"catalog.json").write_text(json.dumps(out,separators=(",",":")))
print(len(E),"entries,",(root/"data"/"app"/"catalog.json").stat().st_size,"bytes")
