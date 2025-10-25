CONSTRUCTION_SAFETY_PROMPTS = [
    # Scenario 1: Distracted Worker Under Scaffold (EARLY DETECTION)
    (
        "Wide establishing shot from elevated surveillance camera angle showing active construction "
        "site ground level and scaffolding two stories above. Scene begins with normal workflow - "
        "several workers moving materials, one operating equipment. Camera positioned to capture "
        "vertical height and horizontal breadth simultaneously. Focus develops on one worker in orange "
        "safety vest who stops in walking path directly under scaffold structure and pulls out mobile "
        "phone, begins texting with head down. Camera clearly shows DETECTABLE RISK FACTORS: worker "
        "stationary in falling object zone marked by yellow caution striping on ground, worker's "
        "attention completely on phone screen not surroundings, unsecured red tool bag visible on "
        "scaffold platform edge above beginning to slide toward edge, no overhead protection or "
        "catch nets present, other workers in motion but not watching this area. Hold on this moment "
        "of escalating risk - tool bag teetering on edge 20 feet above distracted worker. All warning "
        "signs present and detectable before impact. Wide enough to show spatial relationships, danger "
        "zones, and multiple unsafe conditions. Overcast natural light, industrial construction site, "
        "realistic multi-level workspace with clear sight lines for AI detection training."
    ),
    # Scenario 2: Improper Ladder Safety (EARLY DETECTION)
    (
        "Wide angle shot from across street level showing entire construction building facade from "
        "ground to three stories up, full width to capture context. Camera positioned like fixed "
        "surveillance camera capturing whole work area. Scene opens with metal extension ladder already "
        "leaning against building at visibly incorrect steep angle. Camera clearly shows DETECTABLE "
        "HAZARDS before climbing begins: ladder angle approximately 80 degrees (should be 75 degrees or "
        "less), base of ladder has no visible foot pads stabilizers or ground anchoring, top of ladder "
        "not secured tied-off or braced against structure, ladder extends only 2 feet above landing "
        "(should extend 3+ feet), no second worker spotter present in area, no safety cones or barrier "
        "tape around ladder base, nearby workers walking past unaware. Worker in blue coveralls approaches "
        "ladder carrying power drill in one hand and heavy tool belt. Worker begins climb showing ADDITIONAL "
        "RISK FACTORS: improper three-point contact (using only two limbs), body leaning laterally outside "
        "ladder rails instead of centered, tools unclipped hanging free creating imbalance, each step causes "
        "visible ladder flex and base movement on ground. Pause on worker at mid-height showing all detectable "
        "violations - improper setup, improper technique, multiple intervention opportunities. Wide perspective "
        "shows ground securing issues and height hazard simultaneously. Bright natural daylight, other "
        "construction activity in background, realistic ladder installation showing all setup deficiencies."
    ),
    # Scenario 3: Missing PPE - Power Tool Operation (EARLY DETECTION)
    (
        "Medium-wide shot of workshop workbench area from angle showing worker's full body profile "
        "face and surrounding workspace. Camera positioned at torso height 10 feet away capturing "
        "worker and visible safety equipment storage in background. Scene begins with worker in gray "
        "work shirt and hard hat approaching workbench where angle grinder and metal beam are set up. "
        "Camera emphasizes DETECTABLE PPE VIOLATIONS visible before work begins: worker wearing hard hat "
        "but NO safety goggles or face shield on face, NO goggles hanging around neck or clipped to vest, "
        "NO hearing protection ear muffs or plugs visible, work gloves present but shirt sleeves rolled "
        "up exposing forearms, NO protective apron for metal grinding work. Background shows SAFETY "
        "RESOURCES AVAILABLE: PPE cabinet with safety glasses visible on wall 15 feet away, eye wash "
        "station marked with green sign, safety compliance poster showing proper PPE for grinding operations, "
        "unused face shield hanging on peg. Worker picks up angle grinder checks power cord and positions "
        "tool against metal beam with finger near trigger ready to start. Hold this preparation moment "
        "showing clear PPE deficiency detectable before operation begins - intervention point. Metal shavings "
        "and grinding marks on beam indicate this is repeat work with spark generation potential. Worker's "
        "unprotected face oriented toward grinding point. Shot wide enough to show missing PPE, available "
        "safety equipment, and work about to commence. Indoor workshop, bright fluorescent overhead lighting, "
        "safety compliance materials visible emphasizing preventable violation."
    ),
    # Scenario 4: Unsecured Scaffold Platform (EARLY DETECTION)
    (
        "Wide shot from ground level angled up showing complete multi-level tubular metal scaffolding "
        "structure from ground to third floor - full system visible. Camera positioned to capture "
        "vertical spans, platform levels, and ground clearance simultaneously like job site safety "
        "inspection view. Scene opens on two workers in high-vis vests already present on second-floor "
        "scaffold platform preparing to move materials. Camera emphasizes DETECTABLE STRUCTURAL HAZARDS: "
        "visible 8-inch gap between wooden planks on platform where one end bracket is missing, unsecured "
        "plank end cantilevered beyond support with no tie-down clamp visible, platform lacks perimeter "
        "guardrails or toe boards, vertical lifeline anchor points present on scaffold but workers' safety "
        "harness lanyards visibly dangling unconnected, base plates at ground level show missing mud sills "
        "under some legs, diagonal bracing incomplete on one section, tools and materials stacked near "
        "unsecured plank creating additional edge loading. Workers begin walking across platform toward "
        "the problem plank area - trajectory clear. Hold before worker reaches unstable section showing "
        "multiple detectable fall hazards: unconnected harnesses, gap in decking, inadequate edge protection, "
        "problematic weight distribution. Camera wide enough to show 15-foot fall distance to ground below, "
        "improperly secured components at multiple levels, and worker paths toward danger zone. All structural "
        "deficiencies visible and detectable for intervention before worker reaches hazard. Daytime exterior, "
        "building under construction in background, clear sight lines showing scaffold integrity issues and "
        "PPE non-compliance simultaneously."
    ),
    # Scenario 5: Forklift Blind Spot Collision Path (EARLY DETECTION)
    (
        "Wide aerial overhead shot of warehouse loading dock showing entire operational area like bird's-eye "
        "surveillance camera view. Camera positioned high enough to see forklift, pedestrian walkways, "
        "loading zones, and traffic patterns simultaneously. Scene opens with yellow forklift with stacked "
        "pallets positioned at loading dock, engine running brake lights on, preparing to reverse into "
        "staging area. Camera shows DETECTABLE SAFETY DEFICIENCIES: no ground guide spotter person present "
        "near forklift, no painted pedestrian walkway lanes or vehicle separation barriers, no floor-mounted "
        "convex mirrors at blind spot intersections, backup alarm light flashing on forklift roof but no "
        "visible audible warning system, driver in orange vest visible through forklift cage checking only "
        "right side mirror not full 360-degree scan. Simultaneously show pedestrian worker in blue hard hat "
        "and reflective vest walking across warehouse floor from left side on collision course with forklift's "
        "reverse path - pedestrian wearing headphones visible as white earbuds, looking down at tablet or "
        "clipboard, not watching forklift. Camera emphasizes CONVERGENCE OF RISK FACTORS detectable now: "
        "forklift begins slow reverse motion, pedestrian continues steady walking pace from blind spot "
        "zone, intersection point calculable, no safety barriers or warning systems between them, no other "
        "workers in immediate area noticing the developing situation. Hold this moment showing both parties "
        "on collision trajectory with 15-20 feet separation - detection and intervention window clearly "
        "present. Overhead view shows spatial relationships, movement vectors, blind zones, and lack of "
        "safety controls. Industrial warehouse setting with concrete floor, stacked pallet rows, bright "
        "natural light from large bay doors, wide enough perspective to see entire developing scenario "
        "before critical moment."
    ),
]


def get_all_prompts() -> list[str]:
    return CONSTRUCTION_SAFETY_PROMPTS
