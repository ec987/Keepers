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

# ---------- rule text from the saved FWC pages, trimmed to what matters for keeping a fish ----------
# Lines are copied word for word. We drop only: news banners, links, other coasts (Atlantic), Biscayne National Park,
# other regions' text, region boundary descriptions, and the other species on shared pages.
# Federal-only lines are kept but tagged "f" so the page shows them only when the pin is in or near federal waters.
STOP = re.compile(r"^(more information|information|related links|management history:?|\U0001F4AC ask buck!|✖)$|management$|^regulation(s)? history$|^federal code of regulations$", re.I)
NOISE = re.compile(r"port meeting|SAFMC|Fishery Management Council is hosting|^learn more|^why:|^effective\b.*\d{4}:?$|^regulation update|image (credit|courtesy)|^copyright|^photo|^publications$|maps are not to scale|species profile|^full (text )?rule|^full rule|ask buck|^description$|return .em right|a resource for anglers|20-fathom map|view larger|^have you signed up|state reef fish angler designation|^participation mandatory|^annual renewal|now in effect|skip to main content|^expand/collapse aggregate|^trap diagrams$|^report .* sightings|^federal (gulf|atlantic) regulations$|^gulf federal waters rules$|^atlantic federal waters rules$|^regulations by coast$|^tilefish inhabit|^although (the crab|it is currently)|^the quicker the crab|^if a juvenile female|^releasing female|^blue crap trap|^previous$|^next$|^links for more information|^can i feed sharks|^additional grouper resources|^snapper research|^gulf red snapper$|^state reef fish survey$|^additional information$|^for more, see noaa|^florida regulations:?$|^(shore-based shark fishing|federal permit holders|shark-smart fishing|tagged sharks|shore-based shark fishing course|take the course)$", re.I)
LABELS = {"min. size limit","daily bag limit","season","slot limit","minimum size limit","size limit","bag limit","vessel limit","daily vessel limit"}
REGION = re.compile(r"^(Panhandle|Big Bend|Tampa Bay|Sarasota Bay|Charlotte Harbor|Southwest|Southeast|Indian River Lagoon|Northeast) Region$")
KEEP_REGIONS = ("Sarasota Bay", "Charlotte Harbor", "Southwest")
REGION_KEEP = re.compile(r"^(season|open season|closed season|slot|slot limit|minimum|bag|daily bag|vessel|may possess|may not possess|catch|special|\*|note)", re.I)
# which accordion blocks on a shared page belong to which catalog entry
PARTS = {"gag":["Gag"],"black-grouper":["Black"],"red-grouper":["Red"],"scamp":["Scamp","Yellowfin","Yellowmouth"],
 "grouper-other":["Rock Hind/Red Hind","Coney/Graysby","Yellowedge/Misty","Warsaw/Speckled Hind","Snowy"],"nassau":["Nassau"],
 "red-snapper":["Red"],"vermilion":["Vermilion"],"gray-snapper":["Gray (Mangrove)"],"mutton-snapper":["Mutton"],"cubera-snapper":["Cubera"],
 "lane-snapper":["Lane"],"other-snappers":["Schoolmaster","Black Wenchman, Queen, Blackfin, and Silk","Black, Wenchman, Queen, Blackfin, and Silk","Yellowtail, Dog, and Mahogany"]}
AGG_BLOCK = {"gag","black-grouper","red-grouper","scamp","grouper-other","nassau"}
KW = {"gag":["gag"],"lane-snapper":["lane"],"red-snapper":["red snapper"],"greater-amberjack":["greater amberjack"],"lesser-amberjack":["lesser amberjack"]}
def raw_lines(text):
    L = [l.strip() for l in text.splitlines()]
    try: i = L.index("Recreational Regulations") + 2
    except ValueError: i = 0
    out = []
    for l in L[i:]:
        if STOP.search(l) and out: break
        if l: out.append(l)
    return out
def merge_labels(lines):
    out, i = [], 0
    while i < len(lines):
        l = lines[i]
        if l.rstrip(":").lower() in LABELS and i + 1 < len(lines) and lines[i+1].rstrip(":").lower() not in LABELS:
            out.append(l.rstrip(":") + ": " + lines[i+1]); i += 2
        else: out.append(l); i += 1
    return out
FEDHDR = re.compile(r"^(federal( waters)?( regulations| rules)?|federal - gulf and atlantic|gulf and atlantic federal waters regulations|gulf federal waters( rules| regulations)?|federal regulations):?$", re.I)
def hdr_kind(l):
    """return (coast, fed) if the line is a section header, else None. coast: 'gulf','atlantic','all'"""
    if len(l) > 190 or re.search(r"\d", l.split("(")[0]) or re.search(r"season open", l, re.I): return None
    low = l.lower().rstrip(":")
    if low in ("other regulations", "regulations", "gear requirements", "gear requirements:"): return ("all", False) if low == "other regulations" else None
    if re.match(r"^(gulf|atlantic)$", low): return ("gulf" if low == "gulf" else "atlantic", False)
    if FEDHDR.match(l): return ("all", True)
    m = re.match(r"^(gulf|atlantic)\b.*(waters|regulations|state)", low)
    if m and ":" not in l.split("(")[0][:40] or (m and low.startswith(("gulf state","gulf of america regulations","atlantic state","atlantic regulations","atlantic federal"))):
        if low.startswith("atlantic") and "gulf" not in low: return ("atlantic", "federal" in low and "state" not in low)
        if "federal" in low and "state" not in low and "regulations (" not in low: return ("all", True)
        return ("gulf", False)
    return None
def parse(lines):
    """-> list of dict(t, coast, fed, block)"""
    items, coast, fed, block = [], "all", False, None
    for l in merge_labels(lines):
        if l.startswith("##"):
            coast, fed, block = "all", False, None
            items.append(dict(t=l[2:], coast="all", fed=False, block=None, h=True)); continue
        m = re.match(r"^Expand/Collapse (.+)$", l)
        if m:
            name = m.group(1).strip()
            if items and items[-1]["t"] == name: items.pop()
            block = name; items.append(dict(t=name, coast=coast, fed=fed, block=block, head=True)); continue
        k = hdr_kind(l)
        if k:
            coast, fed = k[0], k[1]
            if k[0] != "all" or k[1] or l.lower().startswith("other regulations"): block = None
            items.append(dict(t=l, coast=coast, fed=fed, block=block, head=True)); continue
        it = dict(t=l, coast=coast, fed=fed, block=block)
        if re.match(r"^(gulf )?federal\b", l, re.I): it["fed"] = True
        if re.match(r"^reef fish gear requirements apply|^note: reef fish gear requirements apply", l, re.I): it["block"] = None
        items.append(it)
    return items
def clean_banner(lines):
    """leading news banners are short groups of lines that end with 'Learn More'; return (banner_groups, rest)"""
    groups, cur, start = [], [], 0
    for i, l in enumerate(lines[:80]):
        if l.lower() == "learn more":
            if len(cur) > 6: break
            groups.append(cur); cur = []; start = i + 1
        else:
            if l.startswith("NEW ") and cur: groups.append(cur); cur = []
            cur.append(l)
            if len(cur) > 6: break
    return groups, lines[start:]
EXTRA = {  # extra lines to drop for one page (other regions, promotions)
 "lionfish": r"^interested in selling|^the fwc only issues permits|monroe county|^habitat and fishing tips",
 "unregulated": r"^for more information",
 "tarpon": r"jig prohibited example|^\(note: this video|^map of boca grande",
 "goliath": r"^catch and release$|^goliath harvest program$|^life history$|^population assessment$|^catching and releasing goliath",

 "lobster": r"monroe|florida keys|marathon|^florida.s spiny lobster season$",
 "blue-crab": r"st\. johns|georgia/florida|brevard|franklin county|hernando through wakulla|regional blue crab trap closures|^in an effort|^these six",
 "shrimp": r"^northeast region|^northwest region|^any tributary|^inland waters|^all waters of (sheepshead|big bayou|indian lagoon|ochlockonee)|big bend shrimp closed area|miami-dade|^\*view the full|^within the big bend closed area",
}
def select(items, eid, kws, slug=""):
    parts = PARTS.get(eid); has_blocks = any(i["block"] for i in items)
    out = []
    for it in items:
        t = it["t"]
        if it["coast"] == "atlantic": continue
        if re.search(r"atlantic", t, re.I) and not re.search(r"gulf", t, re.I): continue
        if re.search(r"biscayne", t, re.I) or NOISE.search(t): continue
        if EXTRA.get(slug) and re.search(EXTRA[slug], t, re.I): continue
        if has_blocks and it["block"]:
            if parts is not None and it["block"] not in parts: continue
        out.append(["h" if it.get("h") else ("f" if it["fed"] else "s"), t])
    # drop section headers that ended up with nothing under them
    res = []
    for i, (k, t) in enumerate(out):
        isH = bool(hdr_kind(t)) and len(t) < 200
        nxt = out[i+1] if i + 1 < len(out) else None
        if isH and (nxt is None or (nxt[0] != k and False)): continue
        res.append([k, t])
    ded = []
    for r in res:
        if not ded or ded[-1] != r: ded.append(r)
    return ded
SLICES = {  # (heading, start regex, start occurrence, end regex or None, end occurrence) on the page's lines; heading is ours, not FWC's
 "pompano": [("Florida pompano", r'^Minimum Size Limit: 11"', 0, r"^Pompano Endorsement Zone", 0)],
 "permit-pompano": [("African pompano", r'^Minimum Size Limit: 24"', 0, r"^Special Permit Zone", 0), ("Permit (outside the Special Permit Zone, which is south of 25\u00b009'N, well south of this page's area)", r'^Slot Limit: Not less than 11"', 0, None, 0)],
 "greater-amberjack": [(None, r"^Gulf$", 0, r"^Atlantic$", 0), (None, r"^Legal Gear", 0, r"^Have you signed", 0)],
 "lesser-amberjack": [(None, r"^State waters regulations", 0, r"^Have you signed", 0)],
 "tilefish": [("Golden tilefish", r"^Gulf State$", 0, r"^Gulf State$", 1), ("Blueline tilefish", r"^Gulf State$", 1, r"^Gear Requirements$", 0), (None, r"^Gear Requirements$", 0, r"^Description$", 0)],
 "sand-seatrout": [(None, r"^State Waters Outside Weakfish Management Zone$", 0, r"^Weakfish Management Zone$", 1)],
 "lionfish": [(None, r"^Minimum Size Limit: None", 0, r"^Habitat and Fishing Tips", 0)],
 "tarpon": [(None, r"^Regulations$", 0, r"^Tarpon Best Fishing Practices$", 0)],
 "sharks": [(None, r"^Harvestable Sharks$", 0, r"^Help released sharks survive", 0), (None, r"^Prohibited species: Know before you go", 0, r"^Negative Shark Encounters", 0), (None, r"^Sawfish$", 0, r"^Is that shark tagged", 0)],
 "gear-rules": [(None, r"^State and federal regulations require", 0, r"^Gulf of America$", 0), (None, r"^State Waters$", 0, r"^State Waters$", 1), ("What the terms mean", r"^Circle hooks are made", 0, None, 0)],
 "bonefish": [(None, r"^Bonefish is a Catch", 0, r"^June 2013", 0)],
 "goliath": [(None, r"^Harvest is prohibited without a permit", 0, r"^Catch and Release$", 0), (None, r"^If you capture a goliath", 0, r"^Can I feed", 0)],
}
def apply_slices(eid, lines):
    spec = SLICES.get(eid)
    if not spec: return lines
    def find(rx, nth, frm=0):
        n = 0
        for i in range(frm, len(lines)):
            if re.search(rx, lines[i]):
                if n == nth: return i
                n += 1
        return None
    out = []
    for head, a, an, b, bn in spec:
        i = find(a, an)
        if i is None: continue
        j = find(b, bn) if b else len(lines)
        if j is None or j <= i: j = len(lines)
        if head: out.append("##" + head)
        out += lines[i:j]
    return out
def build_texts(E, root):
    texts, pages = {}, {}
    def page(slug):
        if slug not in pages:
            p = root/"data"/"raw"/"species"/(slug + ".txt")
            pages[slug] = raw_lines(p.read_text(encoding="utf8")) if p.exists() else None
        return pages[slug]
    for e in E + [dict(id="gear-rules", slug="gear-rules", name="gear")]:
        L = page(e["slug"])
        if L is None: continue
        groups, rest = clean_banner(L)
        rest = apply_slices(e["id"], rest)
        kws = KW.get(e["id"], [e["name"].split()[0].lower()])
        banner = []
        for g in groups:
            txt = " ".join(g).lower()
            if any(k in txt for k in kws) and not (re.search(r"atlantic", txt) and "gulf" not in txt): banner += g
        if e["id"] == "barracuda":
            k = rest.index("Rest of state")
            keepre = lambda xs: [x for x in select(parse(merge_labels(xs[1:])), e["id"], kws, e["slug"]) if not x[1].startswith("Includes all waters off") and x[1] not in ("Collier through Martin counties", "Rest of state")]
            texts[e["id"]] = {"by": "collier", "regions": {"Collier through Martin counties": keepre(rest[:k]), "Rest of state": keepre(rest[k:])}, "common": []}
        elif any(REGION.match(l) for l in rest):
            pre, regs, post, cur = [], {}, [], None
            for l in rest:
                m = REGION.match(l)
                if m: cur = m.group(1); regs[cur] = []; continue
                if l == "Other Regulations": cur = None; post.append(l); continue
                if post: post.append(l)
                elif cur: regs[cur].append(l)
                else: pre.append(l)
            R = {}
            for name in KEEP_REGIONS:
                keep = [x for x in regs.get(name, []) if REGION_KEEP.match(x) and not NOISE.search(x) and not re.search(r"biscayne", x, re.I)]
                R[name] = [["s", x] for x in merge_labels(keep)]
            common = [["f", x] for x in pre if x.startswith("*")] + [x for x in select(parse(post), e["id"], kws, e["slug"])]
            texts[e["id"]] = {"regions": R, "common": common}
        else:
            texts[e["id"]] = {"lines": [["s", b] for b in banner if not NOISE.search(b)] + select(parse(rest), e["id"], kws, e["slug"])}
    return texts
texts = build_texts(E, root)
fetched = ""
try: fetched = json.loads((root/"data"/"status.json").read_text())["run_utc"][:10]
except Exception: pass
out = {"updated":"2026-10-04","scope":"Gulf state waters, Southwest Florida (Venice to south of Naples)","species":E,"texts":texts,"fetched":fetched}
(root/"data"/"app"/"catalog.json").write_text(json.dumps(out,separators=(",",":")))
print(len(E),"entries,",(root/"data"/"app"/"catalog.json").stat().st_size,"bytes")
