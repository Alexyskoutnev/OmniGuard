CONSTRUCTION_SAFETY_PROMPTS = [
    # === EMS SCENARIOS (5 scenarios) ===
    # EMS Scenario 1: Worker Chest Pain Early Warning Signs
    (
        "Wide shot from elevated site office camera showing construction break area capturing 50-foot "
        "radius. Camera positioned like surveillance showing break tables, water stations, and foot "
        "traffic. Scene opens with worker in late 50s wearing orange vest sitting at break table. "
        "Camera shows DETECTABLE MEDICAL DISTRESS: worker's hand repeatedly moving to chest area, "
        "visible facial grimacing, breathing with visible effort, complexion appearing pale, posture "
        "hunched forward. BEFORE EMERGENCY ESCALATION: water bottle untouched despite heat, hard hat "
        "removed with forehead wiping repeatedly, other workers unaware, no first aid station visible, "
        "supervisor 40 feet away with back turned. CRITICAL MOMENT: worker stands unsteadily gripping "
        "table edge, takes two steps and stops placing hand against wall, left arm hanging protectively, "
        "short shallow breaths. Construction site break area, natural daylight, realistic medical "
        "emergency showing detectable pre-event symptoms requiring EMS response."
    ),
    # EMS Scenario 2: Heat Stroke Worker Confusion
    (
        "Wide overhead shot from crane showing ground work area with concrete crew during peak heat. "
        "Camera captures 80-foot radius. Temperature display showing 96°F, worker in blue coveralls "
        "operating finishing equipment showing erratic patterns - starting/stopping, weaving, stumbling "
        "on flat ground. DETECTABLE WARNINGS: worker removes hard hat forgotten on ground, profuse "
        "sweating with saturated clothing, bright red skin, disoriented looking around, coworkers "
        "focused on pour not watching. BEFORE EMERGENCY: cooling station 30 feet away unused, water "
        "bottle on ground, heat prevention chart showing breaks not followed, no buddy system. CRITICAL: "
        "worker attempts continuing but lacks coordination, drops tool showing grip weakness, sits on "
        "ground in full sun not shade, nausea visible. Overhead shot captures environmental heat stress, "
        "symptom progression, available cooling unused, response gaps. Construction site summer heat, "
        "harsh sunlight, realistic heat illness before critical emergency."
    ),
    # EMS Scenario 3: Severe Laceration From Sheet Metal
    (
        "Wide shot from loading dock camera showing material staging area 25 feet away. Worker moving "
        "sheet metal panels wearing gloves but no arm protection. INJURY OCCURRENCE: worker lifting "
        "4x8 aluminum panel, sharp edge catching forearm between glove and sleeve, immediate reaction "
        "pulling arm away grabbing injury, dark stain appearing on sleeve. BEFORE MEDICAL RESPONSE: "
        "worker sets panel with one hand while other maintains pressure, blood seeping through fingers, "
        "no first aid kit visible, no coworker nearby, medical supplies 100 feet away in trailer. "
        "CRITICAL: worker removes hand revealing 6-inch laceration with active bleeding, wraps with "
        "shirt tail showing inadequate materials, early shock signs - pale face, unsteady, trembling, "
        "wound near radial artery. Material staging area, natural lighting, realistic laceration "
        "emergency showing need for EMS and improved first aid positioning."
    ),
    # EMS Scenario 4: Allergic Reaction to Insulation
    (
        "Medium-wide shot from interior camera showing insulation work area 20 feet away. Worker "
        "installing fiberglass batts wearing basic dust mask but minimal skin protection. ALLERGIC "
        "REACTION: exposed neck showing visible red rash spreading, breathing rate increasing, "
        "repeatedly scratching neck and arms. DISTRESS ESCALATION: worker removes mask revealing facial "
        "swelling around eyes and lips, visible hives on forearms, hand to throat indicating tightening, "
        "wheezing audible. CRITICAL: worker sits on floor showing weakness, breathing labored and "
        "audible, skin pale with bluish lips indicating oxygen deficit, no epinephrine auto-injector "
        "visible, no emergency oxygen. Interior construction, dusty atmosphere, realistic allergic "
        "emergency showing need for advanced medical intervention requiring EMS."
    ),
    # EMS Scenario 5: Diabetic Emergency Low Blood Sugar
    (
        "Wide shot from elevated warehouse camera showing material sorting area 60-foot zone. Worker "
        "operating pallet equipment showing progressive distress - movements slower, confusion, leaning "
        "heavily on jack, visible trembling. HYPOGLYCEMIA SIGNS: lunch box with diabetes bracelet "
        "visible, heavy perspiration in cool warehouse, coordination failing with dropped tool, "
        "irritability waving coworker away. BEFORE COLLAPSE: worker attempts walking but veers off "
        "path showing disorientation, legs weak with unsteady gait, grabs shelf but grip fails causing "
        "stumble, confusion unable to recognize danger. Warehouse interior, commercial lighting, "
        "realistic diabetic emergency showing detectable symptoms requiring rapid medical intervention "
        "with glucose or IV."
    ),
    # === FIRE HAZARD SCENARIOS (5 scenarios) ===
    # Fire Scenario 1: Oily Rags Spontaneous Combustion
    (
        "Wide shot from corner camera 30 feet elevated showing workshop finishing area. Wooden bench "
        "with staining project, oil-based polyurethane containers open, cotton rags saturated with "
        "linseed oil in loose pile on bench, no metal safety container, temperature 92°F creating "
        "combustion conditions. IGNITION RISKS: oily rag pile 2 feet diameter with heat shimmer above, "
        "wooden bench with flammable residue, electrical outlet 3 feet away, no smoke detector, paint "
        "thinner fumes visible. BEFORE IGNITION: worker leaves without addressing disposal, waste bin "
        "15 feet away unused, ventilation fan off allowing vapor accumulation, sun beam directly heating "
        "rag pile. CRITICAL: shimmer increasing indicating oxidation and heat generation, small smoke "
        "wisp from pile center, no worker present, no sprinkler visible. Workshop interior, natural "
        "sunlight, realistic spontaneous combustion showing detectable pre-ignition conditions."
    ),
    # Fire Scenario 2: Welding Sparks Near Combustibles
    (
        "Wide angle shot 40 feet away elevated showing steel fabrication outdoors. Welder performing "
        "stick welding creating spark shower falling 10 feet, hot work permit visible but not updated. "
        "IGNITION HAZARDS: wooden pallets 12 feet away with spark travel reaching them, cardboard between "
        "pallets showing charring from sparks, dried grass 8 feet away not cleared, paint booth exhaust "
        "20 feet away. FIRE DEVELOPING: smoke wisp from cardboard edge where spark landed, no fire watch "
        "person, no extinguisher within 50 feet, wind sock showing 15 mph carrying sparks toward storage. "
        "BEFORE FLAME: welder focused on weld not spark pattern, cardboard smoke increasing, pallet wood "
        "showing blackened spots, no detection system. CRITICAL: larger spark shower, wind gust carrying "
        "cluster into pallets, cardboard transitioning to glow. Outdoor fabrication, angled sunlight, "
        "realistic welding fire hazard with clear ignition progression."
    ),
    # Fire Scenario 3: Overloaded Circuit Heating
    (
        "Medium-wide shot from corner camera 15 feet away showing construction trailer electrical setup. "
        "Temporary power panel with six circuits, power strips daisy-chained together, 12 devices "
        "including space heater, microwave, coffee maker. OVERLOAD WARNINGS: outlet discoloration around "
        "face plate, power strip cord browning at plug, breaker showing unusual position, shimmer near "
        "outlet indicating heat, burning smell. BEFORE IGNITION: current meter showing 24 amps on 20-amp "
        "circuit, power strip heating visible by case discoloration, no GFCI, cord bundled retaining "
        "heat, wooden wall behind outlet. CRITICAL: smoke detector not activating, workers leaving with "
        "heater running unattended, smoke wisp from power strip case, outlet scorch marks darkening. "
        "Trailer interior, fluorescent lighting, realistic electrical fire showing progressive failure."
    ),
    # Fire Scenario 4: Fuel Storage Near Heat Source
    (
        "Wide shot from tower crane showing equipment refueling area 100-foot radius. Diesel generator "
        "running at full load with heat shimmer, fuel storage 10 feet away instead of 50-foot requirement. "
        "IGNITION HAZARDS: five 5-gallon gas cans, one with loose cap showing vapor escape, fuel transfer "
        "occurring with spill potential, diesel puddle 6 feet from generator, dry vegetation scattered. "
        "WARNING INDICATORS: fuel vapors visible between storage and generator, wind carrying vapors "
        "toward hot exhaust, no type B extinguisher, no spill containment, worker refueling while "
        "generator runs. BEFORE FIRE: static electricity from metal funnel, fuel spill running toward "
        "heat source, exhaust pipe showing red glow, vapor at ignition temperature. CRITICAL: worker's "
        "boot in fuel puddle, walks to generator placing can on hot housing, visible gap in cap showing "
        "vapor escape. Outdoor equipment yard, natural daylight, realistic fuel fire hazard with "
        "detectable pre-ignition conditions."
    ),
    # Fire Scenario 5: Battery Charging Thermal Runaway
    (
        "Medium shot from wall camera 20 feet away showing equipment charging station in enclosed room. "
        "Forklift battery bank with 12 batteries charging, controller showing red warning light, one "
        "battery showing abnormal bulging. FAILURE INDICATORS: affected battery case discoloration and "
        "melting at terminals indicating 400°F+, acid vapor shimmer, charger ammeter showing 3x normal "
        "current. BEFORE IGNITION: battery against wooden wall with no fire separation, no suppression "
        "system, ventilation fan off allowing hydrogen accumulation, single exit door, no gas detection. "
        "CRITICAL: smoke from battery case as separator pyrolyzes, acid leaking creating vapor, arcing "
        "at terminal as insulation fails. EMERGENCY: no personnel present, door closed preventing smoke "
        "visibility, battery showing glow through case, nearby batteries at cascade failure risk. "
        "Storage room interior, industrial lighting, realistic battery fire showing thermal runaway "
        "before ignition."
    ),
    # === INJURY SCENARIOS (5 scenarios) ===
    # Injury Scenario 1: Hand Caught in Machinery
    (
        "Wide shot from elevated shop camera 25 feet away showing metal fabrication brake machine. "
        "Worker operating sheet bender with hands guiding material, machine guard removed and on floor, "
        "fingers within 3 inches of descending ram. HAZARDS BEFORE INJURY: emergency stop 6 feet away, "
        "two-hand control bypassed with zip-tied button, attention on sheet not hand position, no "
        "barrier guard or light curtain. CRITICAL MOMENT: worker activates foot pedal starting ram "
        "descent, left hand still in contact with sheet within crush point, ram descending with 2-3 "
        "seconds to clear, worker reacts pulling back but sheet shifts requiring re-grip. IMMEDIATE "
        "HAZARD: ram continuing with hand returning to danger zone, pinch point showing 1-inch gap "
        "closing with fingertips present, no safety mat, coworker yells warning insufficient time. "
        "Workshop interior, industrial lighting, realistic machinery hazard showing safety violations "
        "before crush injury."
    ),
    # Injury Scenario 2: Back Strain From Improper Lifting
    (
        "Wide shot from warehouse camera 35 feet away showing material handling area. Worker approaching "
        "concrete mix bags (80 lbs marked weight) stacked three layers requiring below-knee lift, no "
        "mechanical assistance. IMPROPER TECHNIQUE: worker bends at waist with rounded back not "
        "squatting, feet close together not shoulder-width, gripping bag at one end not center, no back "
        "support belt. BEFORE INJURY: worker begins lift with rounded back pulling upward, facial strain "
        "beyond normal, jerking not smooth motion, excessive lumbar curve. CRITICAL INSTANT: mid-lift "
        "6 inches off ground with back maximally flexed, pain reaction as face contorts and motion "
        "freezes, losing grip as spasm starts, lift dolly 15 feet away unused. IMMEDIATE INJURY: worker "
        "drops bag, hand to lower back in pain response, protective stance leaning away, unable to stand "
        "upright. Warehouse interior, fluorescent lighting, realistic lifting injury showing technique "
        "violations before and during injury event."
    ),
    # Injury Scenario 3: Eye Injury From Flying Debris
    (
        "Medium-wide shot from fixed camera 15 feet away showing carpentry work area. Worker operating "
        "circular saw cutting pressure-treated lumber creating sawdust cloud, clearly NOT wearing safety "
        "glasses despite required sign, glasses on rack 8 feet away unused, saw guard damaged. PPE "
        "VIOLATION: face unprotected with eyes exposed, ongoing cutting ejecting particles toward face, "
        "shop fan deflecting dust at worker, no face shield. BEFORE INJURY: saw encountering knot "
        "creating increased debris, large wood chip ejected at high velocity toward face, worker focused "
        "on cut with eyes wide open, typical blink insufficient at current velocity. CRITICAL: fragment "
        "traveling toward right eye on intercept trajectory, head stationary, no protective barrier, "
        "coworker shouts warning but timing insufficient. IMPACT: fragment strikes eye area, immediate "
        "pain reaction dropping saw, hand to injured eye, excessive tearing, other eye squinting. "
        "Workshop interior, mixed lighting, realistic eye injury showing consequences of PPE "
        "non-compliance."
    ),
    # Injury Scenario 4: Finger Laceration From Utility Knife
    (
        "Medium shot from overhead camera showing packaging area. Worker using retractable utility knife "
        "opening boxes, blade extended at maximum length, free hand on box surface directly in cutting "
        "path. UNSAFE TECHNIQUE: pulling knife toward body and toward hand not away using push-cut, "
        "blade angle steep, non-knife hand fingers extended not curled, no cut-resistant glove despite "
        "policy poster requiring it. BEFORE INJURY: knife encountering resistance from double-layer "
        "cardboard requiring increased force, pulling motion increasing, blade breaking through suddenly "
        "with motion continuing toward stabilizing hand. CRITICAL INSTANT: blade tip exiting cardboard "
        "toward index finger 2 inches from emergence, velocity and sharpness creating high laceration "
        "risk, facial expression showing awareness but motion committed. IMPACT: blade contacting finger "
        "at joint creating depression before penetration, worker releases knife, injured hand pulled "
        "back with blood visible. Packaging area, bright overhead lighting, realistic hand tool injury "
        "showing technique violations before laceration."
    ),
    # Injury Scenario 5: Ankle Sprain From Uneven Ground
    (
        "Wide shot from elevated site camera 40 feet elevated showing construction walking paths. "
        "Uneven ground with excavation backfill creating 3-4 inch elevation changes, temporary walkway "
        "boards ending abruptly, debris scattered, mud patches from rain. WORKER AT RISK: carrying large "
        "4x8 plywood blocking forward vision, view over material obscured, hard hat visible but attention "
        "on balancing load not foot placement, worn boot tread, moving at normal pace despite impaired "
        "visibility. BEFORE INJURY: path approaching backfill transition with 4-inch grade change, no "
        "warning cones, foot trajectory landing at edge in unstable position, load creating imbalance. "
        "CRITICAL: right foot contacts ground at edge with ankle inverted, body weight and load driving "
        "force through ankle, ankle rolling lateral as structures overload, losing balance. INJURY: "
        "drops plywood, hands catch fall, face showing pain, falls right side with ankle trapped creating "
        "inversion injury, lands clutching ankle, immediate swelling, unable to bear weight. Construction "
        "site, natural daylight, realistic sprain showing contributing factors and injury sequence."
    ),
    # === COMPLIANCE SAFETY WEAR SCENARIOS (5 scenarios) ===
    # Compliance Scenario 1: Missing Hard Hat in Active Zone
    (
        "Wide angle shot from tower crane showing multi-level site 100-foot radius. Worker in blue "
        "coveralls entering active zone from parking, clearly NOT wearing hard hat despite zone sign, "
        "carrying lunch bag indicating break return. OVERHEAD HAZARDS: scaffolding three stories with "
        "workers moving materials, crane hook with suspended pallet at 40 feet, roofing crew with nail "
        "guns and debris, ductwork being positioned. VIOLATION BEFORE HAZARD: all other personnel "
        "wearing hard hats providing contrast, hard hat dispenser 20 feet behind worker, safety sign "
        "requiring hard hat clearly visible, superintendent with back turned. CONVERGING HAZARDS: path "
        "leads under active overhead zones including suspended load, loose hammer on scaffold edge, wind "
        "gust could dislodge items. CRITICAL: worker passing under scaffolding, overhead worker shifts "
        "bracket causing hardware to fall, non-compliant worker unaware with unprotected head. "
        "Construction site, natural daylight, realistic PPE non-compliance showing enforcement need."
    ),
    # Compliance Scenario 2: Inadequate High-Visibility Clothing
    (
        "Wide shot from entrance camera showing equipment zone 80-foot radius. Worker wearing dark gray "
        "sweatshirt and navy pants without high-vis vest despite policy poster showing requirement. LOW "
        "VISIBILITY: overcast flat lighting, yellow equipment creating clutter, ground matching clothing "
        "colors, dust reducing visibility. HAZARD BEFORE INCIDENT: excavator backing with raised bucket "
        "and restricted operator view, worker in dark clothing walking in reverse path approaching blind "
        "spot, no spotter, worker wearing earbuds blocking alarm. CONVERGING RISK: operator checking "
        "right mirror showing partial view, paths intersecting in 8-10 seconds at 15 feet behind machine, "
        "dark clothing disappearing against background, no physical barriers. CRITICAL: excavator "
        "continuing reverse, worker in blind spot 12 feet and closing, operator's mirror showing no "
        "detection against busy background, worker on phone not watching. Construction site, overcast "
        "conditions, realistic visibility safety showing PPE compliance gap."
    ),
    # Compliance Scenario 3: Missing Safety Harness at Heights
    (
        "Wide shot from aerial lift 30 feet away showing roofing work area. Two workers on flat roof "
        "25 feet above ground installing HVAC, clearly NOT wearing harnesses despite working within 6 "
        "feet of edge, anchor points installed but unused with lanyards hanging, no D-rings on tool "
        "belts. FALL HAZARDS: roof edge completely unguarded, no warning line 6 feet from edge, HVAC "
        "unit 3 feet from edge requiring perimeter approach, bending and reaching creating balance "
        "challenge, no safety monitor. DETECTABLE NON-COMPLIANCE: harnesses on roof 20 feet away showing "
        "deliberate non-use, hard hats and glasses showing partial compliance but fall protection "
        "omitted, incomplete checklist. BEFORE FALL: worker in red carrying ductwork backward toward "
        "edge with attention on partner not edge, path progressing toward edge from 10 feet, no edge "
        "markers, worker two directing not watching proximity. CRITICAL: red shirt taking backward steps "
        "now 4 feet from edge, heel approaching with next step at 2-foot margin, wind gust creating "
        "distraction, no fall protection to arrest fall. Rooftop work area, natural daylight, realistic "
        "height safety showing non-compliance creating life-safety risk."
    ),
    # Compliance Scenario 4: Missing Hearing Protection in Noise Zone
    (
        "Wide shot from observation window 25 feet elevated showing metal fabrication floor. Grinding, "
        "cutting, hammering creating sound waves, noise sign showing '95 dB - HEARING PROTECTION "
        "REQUIRED', worker in orange entering without hearing protection - no earmuffs, no earplugs, "
        "nothing around neck. HIGH NOISE: angle grinder with sparks and high-pitched whine, pneumatic "
        "hammer creating percussive impacts, industrial fan running, multiple workers properly wearing "
        "protection except non-compliant worker. EXPOSURE BEFORE DAMAGE: conversation attempt failing "
        "showing noise level, non-compliant worker showing facial reaction - squinting, head turn away "
        "indicating discomfort, PPE station 15 feet away with accessible protection. CONTINUED EXPOSURE: "
        "remaining in zone approaching grinding operation, dosimeter showing 98 dB sustained exceeding "
        "OSHA limits, face showing discomfort but non-compliance continuing, supervisor in office 40 "
        "feet away with back turned. CRITICAL: worker spending 5+ minutes without protection retrieving "
        "tool, cumulative exposure toward temporary threshold shift, no intervention from nearby workers. "
        "Industrial shop, fluorescent lighting, realistic noise hazard showing hearing conservation "
        "program enforcement gap."
    ),
    # Compliance Scenario 5: Improper Respirator Use in Dust
    (
        "Medium-wide shot from fixed camera 20 feet away showing concrete cutting in enclosed space. "
        "Concrete saw creating visible dust cloud, silica warning posted, worker wearing N95 but "
        "improperly positioned - one strap loose not over head leaving inadequate seal, visible gap at "
        "cheek, beard protruding preventing seal. EXPOSURE HAZARD: substantial dust visible as thick "
        "cloud, silica warning emphasizing lung disease risk, enclosed space with insufficient "
        "ventilation, dust hanging in stagnant air. NON-COMPLIANCE: proper half-face elastomeric "
        "respirator with P100 on wall 10 feet away, fit-testing records showing certification but not "
        "wearing fitted device, facial hair violating clean-shaven requirement, worker periodically "
        "adjusting mask showing awareness of poor fit. CONTINUED EXPOSURE: breathing visible showing "
        "deep respirations inhaling around seal leaks, dust settling on face confirming exposure, "
        "coughing even with mask indicating inadequate protection, 15+ minutes of cutting with sustained "
        "dust. CRITICAL: worker removes ineffective N95 to wipe face showing complete unprotected "
        "breathing during peak dust, replaces without adjusting straps, no real-time monitoring, "
        "supervisor not present. Enclosed workspace, dusty atmosphere with backlighting showing "
        "particles, realistic respiratory hazard showing PPE program gaps."
    ),
    # === HEAT EXHAUSTION SCENARIOS (5 scenarios) ===
    # Heat Exhaustion Scenario 1: Roofer in Peak Afternoon Heat
    (
        "Wide shot from aerial platform 40 feet lateral showing flat roof during summer afternoon. "
        "Black EPDM surface with heat shimmer rising indicating 140°F+ surface temperature, time 2:30 "
        "PM peak heat, ambient 96°F, heat index sign showing 'feels like 108°F', full sun no shade. "
        "HEAT ILLNESS DEVELOPING: worker in gray performing membrane installation showing progressive "
        "distress - pace declining over 10 minutes, heavy sweating with saturated shirt, frequent stops "
        "standing motionless, bright red skin on forearms, removing hard hat wiping forehead every 30 "
        "seconds. WARNING SIGNS: empty water bottle uncapped showing inadequate hydration, cooling tent "
        "50 feet away unused, break schedule clipboard showing 15-minute breaks not followed, no buddy "
        "system. BEFORE EXHAUSTION: coordination decline - fumbling and dropping tools, swaying when "
        "standing, elevated breathing visible, squatting to rest showing fatigue, nausea with hand on "
        "stomach. CRITICAL: standing showing dizziness - hand to head unsteady, skin now pale not red "
        "indicating progression, attempting work but slow and clumsy showing confusion, sits on roof "
        "in sun not shade showing impaired judgment. Rooftop work, intense sunlight, realistic heat "
        "stress showing early warnings requiring intervention before emergency."
    ),
    # Heat Exhaustion Scenario 2: Concrete Worker in Direct Sun
    (
        "Wide shot from elevated position showing concrete flatwork mid-day heat 60-foot zone. Pour "
        "in parking lot with no overhead cover, direct sunlight at zenith, concrete radiating heat "
        "with shimmer, display showing 94°F and 70% humidity creating 110°F+ heat index, long sleeves "
        "and pants per chemical protection adding insulation. HEAT SYMPTOMS: finisher using bull float "
        "showing declining output - slower strokes and longer pauses, profuse perspiration dripping "
        "continuously, saturated clothing, deep red neck skin, breathing heavily mouth open panting. "
        "WARNING INDICATORS: requesting water frequently - fourth break in 30 minutes showing excessive "
        "fluid loss, removing gloves placing hands on knees bent over, face showing distress beyond "
        "normal, coworkers aware but work continues, foreman 40 feet away not monitoring. BEFORE "
        "COLLAPSE: muscle cramps visible - grimacing grabbing calf indicating electrolyte depletion, "
        "attempting float work but uncoordinated and off-balance, nausea bending forward spitting, "
        "slurred speech showing confusion, skin pale replacing red. CRITICAL: abandons float dropping "
        "on wet concrete, stumbles to edge sitting heavily, lies back in sun not shade showing altered "
        "status, crew approaching noting emergency. Concrete pour site, intense midday sun, realistic "
        "heat illness showing escalation requiring urgent intervention."
    ),
    # Heat Exhaustion Scenario 3: Confined Space Elevated Temperature
    (
        "Medium shot from manway opening showing confined space inside 15-foot tank. Worker performing "
        "interior cleaning, metal tank in direct sunlight heating skin to extreme temperature, no active "
        "cooling or ventilation - blower at manway not running, permit showing temperature monitoring "
        "fields blank. HEAT STRESS: worker visible by work lights showing heavy perspiration with sweat "
        "rolling, soaked coveralls, confined humidity visible as moisture on tank walls, breathing with "
        "visible effort showing rapid movements, frequent pausing to lean against wall. WARNING SIGNS: "
        "radio communication showing slowed speech and delayed responses indicating cognitive impairment, "
        "removing hard hat despite policy showing impaired judgment, bright red hands, movements slower "
        "and less coordinated, attendant noting tired appearance not recognizing heat symptoms. BEFORE "
        "EMERGENCY: reporting dizzy via radio but dismissing and continuing, squatting inside tank, "
        "nausea visible as dry heaves, attempting ladder exit showing difficulty coordinating climb - "
        "foot missing rung, breathing gasping quality. CRITICAL: halfway up ladder stopping and clinging "
        "showing weakness, calling for help weak voice, attendant recognizing emergency, grip weakening "
        "showing fall risk. Industrial tank interior, artificial lighting, realistic confined space "
        "heat stress showing amplified risk from limited air exchange."
    ),
    # Heat Exhaustion Scenario 4: Paving Crew Asphalt Exposure
    (
        "Wide shot from elevated lift 30 feet showing asphalt paving operation summer afternoon. Paving "
        "machine laying 300°F+ hot mix creating heat waves, black surface radiating stored heat with "
        "shimmer, ambient 92°F plus radiant heat creating 120°F+ combined exposure, full afternoon sun "
        "at 3:00 PM, crew in direct heat from sun and paved surface. HEAT ILLNESS: screed operator on "
        "platform exposed to hopper and screed heat showing distress, saturated high-vis shirt, hand "
        "trembling adjusting controls indicating motor impairment, removing hard hat pouring water on "
        "head, extreme red face. SYMPTOMS BEFORE COLLAPSE: attention wandering - looking away from grade "
        "indicators repeatedly showing concentration difficulty, leaning heavily on panel for support "
        "not standing, rapid chest heaving showing cardiovascular stress, confused radio responses "
        "requesting repetition, crew lead noticing erratic operation attributing to equipment not "
        "medical. CRITICAL: suddenly stopping machine creating interruption, gripping railing swaying "
        "showing severe dizziness, skin changing red to pale, sitting on edge dangling legs, head "
        "dropping forward toward chest showing altered consciousness. EMERGENCY: driver climbing to "
        "check operator, discovering unresponsive to questions, lying back showing progression to stroke, "
        "crew calling EMS, no cooling equipment immediately available. Asphalt paving site, intense "
        "summer with heat shimmer, realistic severe heat illness showing stroke risk in high-heat "
        "industries."
    ),
    # Heat Exhaustion Scenario 5: Elderly Worker in Hot Warehouse
    (
        "Wide shot from office window showing warehouse interior 80-foot zone. No air conditioning "
        "with temperature display 88°F interior, bay doors open introducing hot outside air, ceiling "
        "fans circulating warm air not cooling, afternoon sun through skylights creating hot spots. "
        "HEAT-SUSCEPTIBLE: worker in 60s visible by gray hair performing order picking with hand cart, "
        "long pants and shirt with no cooling vest, prescription pill bottle visible (many medications "
        "impair heat tolerance), moving slower than younger coworkers showing reduced capacity. HEAT "
        "STRESS: heavy perspiration on forehead and arms, stopping frequently to rest showing unusual "
        "fatigue, using cart for support when standing showing balance difficulty, flushed skin, "
        "drinking water but showing signs despite hydration attempt. BEFORE MEDICAL EVENT: coordination "
        "decline - fumbling scanner and dropping items, walking pattern showing slight weaving indicating "
        "neurological effect, reporting feeling unwell but downplaying, supervisor suggesting break but "
        "worker declining showing poor self-assessment, coworkers noticing red face and heavy breathing. "
        "CRITICAL: attempting continuing but movements showing confusion - wrong aisle/items, suddenly "
        "sitting on floor using shelving, headache holding head in hands, nausea leaning forward, skin "
        "pale change indicating circulatory failure. EMERGENCY: lying on floor in recovery position, "
        "workers surrounding calling help, first aid with cool towels, altered consciousness with "
        "delayed responses, calling 911 due to age and severity. Warehouse interior, warm conditions, "
        "realistic heat illness in older workers showing need for age-appropriate management."
    ),
    # === FALLING HAZARD SCENARIOS (5 scenarios) ===
    # Falling Hazard Scenario 1: Scaffold Missing Guardrails
    (
        "Wide shot from across street 60 feet away showing commercial facade and three-story scaffolding. "
        "Tube and coupler to 30 feet height, top platform completely missing perimeter guardrail on "
        "street side, middle platform with 8-foot gap in rails, bottom with complete rails for "
        "comparison. FALL HAZARDS: two workers on top performing masonry within 4 feet of unprotected "
        "30-foot drop, no fall arrest systems - no harnesses or lanyards, no warning line 6 feet from "
        "edge, no safety netting below, platform planks showing 3-inch gaps creating trip hazard. "
        "VIOLATIONS BEFORE FALL: worker in red moving materials backward toward edge with attention on "
        "coordinating not watching proximity, position 8 feet from edge closing to 5 feet as walking "
        "continues, no edge markers, repeated trips increasing exposure. CRITICAL: backwards trajectory "
        "continuing with heel within 2 feet of unprotected edge, carrying concrete block affecting "
        "balance, wind gust creating challenge, second worker warning but not heard over street noise. "
        "BEFORE FALL: heel reaching edge board, weight shift beginning fall as center of gravity beyond "
        "support, surprise reaction dropping block reaching for non-existent rail, no fall protection "
        "to arrest. Commercial building exterior, natural daylight, realistic scaffold fall showing "
        "critical need for perimeter protection."
    ),
    # Falling Hazard Scenario 2: Skylight Fall Through Fragile Surface
    (
        "Wide shot from adjacent taller building 40 feet elevated showing warehouse roof. Flat roof "
        "with white coating making surface uniform, 12 fiberglass skylights flush with surface painted "
        "over and visually indistinguishable from structural deck, skylights not marked or guarded, "
        "weathering degraded strength creating brittle fragile surface insufficient for worker weight. "
        "WORKERS APPROACHING: two-person HVAC crew carrying ductwork across roof toward unit, path "
        "crosses directly over skylight field with 6 panels, workers unaware due to coating concealment, "
        "no roof plan showing positions, no spotter watching path. HAZARD INDICATORS: slight "
        "discoloration in raking sunlight showing rectangular patterns where skylights located (visible "
        "to camera not workers), nearby skylight showing crack indicating fragile condition, warning "
        "sign faded and illegible, proper covers stored at edge unused. BEFORE FALL THROUGH: lead "
        "worker's foot landing on skylight surface, full weight transferring to fragile panel, skylight "
        "showing deflection and cracking at edges, continuing forward unaware. CRITICAL: panel failing "
        "under load, visible crack propagation, worker dropping through as fragments give way, surprise "
        "with arms flailing, second worker unable to grab, 25-foot fall to floor visible below, no "
        "netting to arrest. Warehouse roof exterior, angled sunlight, realistic skylight fall showing "
        "critical need for protection over fragile surfaces."
    ),
    # Falling Hazard Scenario 3: Ladder Slip on Smooth Surface
    (
        "Wide shot from ground 25 feet away showing building exterior and ladder access. Aluminum "
        "extension ladder extended to 20 feet leaning against facade for window repair, base on smooth "
        "polished concrete sidewalk with no texture, recent rain creating wet sheen and puddles, no "
        "stabilization - no footpads, stakes, or footing person. INSTABILITY INDICATORS: angle too "
        "steep approximately 80 degrees (should be 75 - 4:1 ratio), base showing no slip-resistant "
        "feet - worn pads or missing exposing aluminum contact, top not tied off, slight lateral "
        "movement visible as wind creates oscillation. HAZARDS BEFORE FALL: worker in blue at mid-height "
        "12 feet up carrying paint can and brush, three-point contact compromised - one hand for tool "
        "leaving two points, body leaning left reaching for window creating lateral load, wet concrete "
        "base with water where feet contact creating zero-friction. BEFORE SLIP: reaching further "
        "increasing lateral force, base showing initial movement - slight 1-inch slide on wet concrete "
        "creating sudden shift, reaction gripping tighter and tensing, attempting return to center but "
        "momentum continuing. CRITICAL: base sliding rapidly on frictionless wet surface, angle changing "
        "steep to near-vertical in rapid transition, worker losing all handholds as ladder accelerates, "
        "beginning fall at 12-foot height, hard concrete below with no padding. FALL: ladder sliding "
        "away leaving worker airborne, 12-foot freefall to concrete, landing on side with impact, ladder "
        "clattering down striking worker, paint and tools falling creating secondary impacts. Building "
        "exterior, wet conditions visible, realistic ladder slip fall showing critical need for base "
        "stabilization."
    ),
    # Falling Hazard Scenario 4: Aerial Lift Platform Tip Over
    (
        "Wide shot from elevated building window 30 feet showing outdoor lift operation. Scissor lift "
        "extended to 25-foot working height on outdoor gravel surface, ground showing recent grading "
        "with soft uncompacted soil and loose rock, lift showing visible 3-degree tilt from vertical, "
        "manufacturer placard stating 'LEVEL GROUND ONLY - 1% GRADE MAXIMUM'. DESTABILIZING FACTORS: "
        "two workers on platform at full extension rather than single-person limit per capacity placard, "
        "positioned same side creating eccentric load away from centerline, reaching outside guardrails "
        "with bodies extending beyond zone creating overturning moment, outriggers not deployed despite "
        "elevation exceeding safe height. INSTABILITY BEFORE TIPOVER: platform showing increased tilt "
        "as workers move - visible angle change relative to vertical, audible warning beep from sensing "
        "system indicating over-limit, wheels on low side showing lifting off ground visible as daylight "
        "gap, ground showing subsidence under loaded wheels on high side creating progressive tilt. "
        "CRITICAL: workers simultaneously moving to edge reaching for facade creating maximum offset, "
        "tilt increasing rapidly showing 8-degree lean against building reference, warning escalating "
        "to continuous tone indicating critical stability, wheels fully lifted 6 inches showing supported "
        "by only two wheels. TIPOVER INITIATING: center of gravity passing beyond support base creating "
        "unrecoverable tip, platform tilting rapidly toward low side, workers grabbing rails and each "
        "other as platform accelerates in rotation, reaching 30-degree tilt continuing, unable to exit "
        "during motion. IMPACT: platform impacting ground at 45 degrees, workers thrown against railings "
        "and floor, secondary impact as lift settling, workers trapped in tilted platform with no egress. "
        "Outdoor construction site, natural lighting, realistic lift stability failure showing critical "
        "need for level firm surface and load management."
    ),
    # Falling Hazard Scenario 5: Unprotected Floor Opening Fall
    (
        "Wide shot from mezzanine 20 feet elevated and 30 feet lateral showing warehouse floor with "
        "elevator shaft opening. Rectangular opening 6x8 feet creating 20-foot drop to basement, "
        "completely unguarded with no perimeter railing or toeboard, no hole cover despite available "
        "grating stored against wall 15 feet away, no warning signs or caution tape establishing "
        "barrier, no lighting around opening in dimly lit warehouse creating visibility hazard. "
        "APPROACHING HAZARD: forklift operator driving in reverse carrying pallet load obscuring "
        "rearview, checking side mirrors showing attention away from reverse path directly toward "
        "opening, backing speed steady at 3 mph providing limited reaction time, no ground guide, no "
        "painted floor markings or physical barriers. WARNING FAILURE: floor surface showing uniform "
        "color providing no visual indication of opening to operator, other workers normalizing "
        "unguarded hazard indicating long-standing violation, lighting creating shadows further "
        "obscuring edges, facility manager office with window overlooking floor showing supervisor "
        "absent. BEFORE FALL: forklift rear wheel approaching opening edge with trajectory crossing "
        "void in 3 seconds, operator completely unaware shown by steady speed with no deceleration, "
        "load weight creating momentum difficult to stop, opening edge showing no reflective marking. "
        "CRITICAL: rear wheel reaching opening edge with tire at void threshold, operator suddenly "
        "noticing and slamming brakes but reaction time insufficient, weight and momentum carrying with "
        "rear wheels entering void, operator's panic expression as machine tips. FALL OCCURRING: "
        "forklift rear dropping into opening with front rising as pivot reached, operator restrained by "
        "seatbelt but cab rotating backward at increasing angle, pallet load sliding backward off forks "
        "falling into shaft, forklift reaching vertical and tipping completely into shaft, tremendous "
        "crash as machine impacts basement 20 feet below, operator injured in overturned cab. Warehouse "
        "interior, poor lighting conditions, realistic floor opening fall showing critical need for "
        "physical guarding or covers at all floor penetrations."
    ),
]


def get_all_prompts() -> list[str]:
    return CONSTRUCTION_SAFETY_PROMPTS
