"""Sea culture — route encounters, NPC sightings, lore, weather, crew voice.

The sea between ports should feel as alive as the ports themselves. This module
provides route-specific flavor text, encounters unique to specific trade lanes,
NPC sightings from the 134 port characters, sea superstitions, and crew morale.

Design principle: every voyage should feel like it happens in a SPECIFIC place,
not in "generic ocean." The Grain Road should smell like wheat. The Smuggler's
Run should feel like held breath. Typhoon Alley should terrify.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RouteEncounter:
    """A flavor encounter specific to a named route or region."""
    text: str                        # what happens / what you see
    category: str                    # sighting / lore / weather / crew / encounter
    mechanical_effect: str = ""      # optional: "speed+10%", "morale+1", etc.


@dataclass(frozen=True)
class RouteEncounterTable:
    """Encounter table for a specific route or region."""
    route_key: str                   # lore_name or region name
    encounters: list[RouteEncounter] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Route-Specific Encounters (15 named routes)
# ---------------------------------------------------------------------------

ROUTE_ENCOUNTERS: dict[str, RouteEncounterTable] = {

    "The Grain Road": RouteEncounterTable(
        route_key="The Grain Road",
        encounters=[
            # Sightings
            RouteEncounter("A grain convoy from Porto Novo passes — six barges in formation, hulls riding low. The Exchange Guild flag snaps in the breeze.", "sighting"),
            RouteEncounter("A felucca from Al-Manar crosses your wake, its deck stacked with brass-bound spice chests. The crew waves.", "sighting"),
            RouteEncounter("You pass the marker buoy where the old coast road meets the sea. Grain ships have used this lane since before the Exchange was built.", "sighting"),
            # Lore
            RouteEncounter("Your bosun points at the coastline. 'See that cliff? They say the first Grain Exchange was carved into it — before Porto Novo even had a harbor.'", "lore"),
            RouteEncounter("An old sailor on deck murmurs a prayer as you pass a rocky outcrop. 'Every grain ship salutes the Stone. It's bad luck not to.' You can't see why the rock matters. He won't explain.", "lore"),
            # Weather
            RouteEncounter("The Mediterranean breeze carries the smell of baking bread from the coastal villages. The crew breathes deep.", "weather"),
            RouteEncounter("Calm water, clear sky. The Grain Road earns its reputation as the gentlest route in the Known World.", "weather"),
            # Crew
            RouteEncounter("The crew is relaxed — they know this route. Someone starts humming a Porto Novo dock song. Others join.", "crew"),
            RouteEncounter("Your navigator corrects course by a fraction. 'The current shifts here every spring,' he says. 'Old knowledge.'", "crew"),
        ],
    ),

    "The Timber Run": RouteEncounterTable(
        route_key="The Timber Run",
        encounters=[
            RouteEncounter("A timber barge from Silva Bay passes, logs lashed together and riding the current. The smell of fresh-cut oak carries across the water.", "sighting"),
            RouteEncounter("Sawdust floats on the surface — you're near Silva Bay. The entire harbor sheds wood dust like a forest sheds leaves.", "weather"),
            RouteEncounter("Your ship's carpenter examines the hull planking and nods. 'Silva Bay timber. Best in the Mediterranean. This wood will outlast all of us.'", "crew"),
            RouteEncounter("A fishing boat crosses your path. The fisherman shouts: 'Elena's building something big! Three masts! I saw the keel!'", "sighting"),
        ],
    ),

    "The Shadow Lane": RouteEncounterTable(
        route_key="The Shadow Lane",
        encounters=[
            RouteEncounter("A ship passes with no flag flying. The crew watches you. You watch them. Nobody waves. This is the Shadow Lane.", "sighting"),
            RouteEncounter("Your lookout spots a rowboat tucked into the cliff shadow. Empty. Or is it? On the Shadow Lane, the difference matters.", "encounter"),
            RouteEncounter("The coast here is riddled with coves — each one a potential anchorage, each one a potential ambush. Your helmsman hugs the deeper water.", "weather"),
            RouteEncounter("A crewman mutters: 'My cousin sailed this lane for years. Made a fortune. Then one day he didn't come back. Nobody asked questions. You don't, on the Shadow Lane.'", "lore"),
            RouteEncounter("You catch a whiff of torch smoke from a cliff face. Corsair's Rest is close — you can't see it, but you can smell it.", "sighting"),
        ],
    ),

    "The Iron Strait": RouteEncounterTable(
        route_key="The Iron Strait",
        encounters=[
            RouteEncounter("A Stormwall patrol ship passes — grey hull, no flag of welcome. The crew watches you with professional interest. They're always watching.", "sighting"),
            RouteEncounter("Iron barges from the foundry ride low in the water, sparks still drifting from the cargo. The Great Foundry's chimney glows on the horizon.", "sighting"),
            RouteEncounter("The water here is dark — iron runoff from the foundries. Your navigator says it's deeper than it looks. The iron goes all the way down.", "weather"),
            RouteEncounter("An old hand on deck says: 'I served at Stormwall once. The strait's the only thing between the north and... whatever's out there.' He doesn't finish.", "lore"),
        ],
    ),

    "The Tea and Tobacco Road": RouteEncounterTable(
        route_key="The Tea and Tobacco Road",
        encounters=[
            RouteEncounter("A Thornport whaler — converted to trading — passes with tea crates stacked on deck. The crew smokes pipes and waves cheerfully.", "sighting"),
            RouteEncounter("The Whale Arch is visible from here — a bleached jawbone spanning the harbor entrance. Even at this distance, you can see the names carved in it.", "sighting"),
            RouteEncounter("Your cook brews tea with leaves bought at Thornport. The crew gathers. For a moment, the northern sea feels almost warm.", "crew"),
            RouteEncounter("Fog rolls in. A horn sounds from somewhere ahead — Thornport's harbor signal. The old whalers' way of saying 'you're close.'", "weather"),
        ],
    ),

    "The Cotton Crossing": RouteEncounterTable(
        route_key="The Cotton Crossing",
        encounters=[
            RouteEncounter("The water changes color as you leave the Mediterranean — warmer, greener. The Gold Coast is ahead. The air carries the faintest scent of earth.", "weather"),
            RouteEncounter("A cotton trader's vessel passes, bales stacked so high the deck is barely visible. Women in indigo cloth stand at the rail, singing the count.", "sighting"),
            RouteEncounter("Your crew's mood shifts as the coast changes. The northern rigidity fades. Someone laughs. Someone else starts a story. The Gold Coast does this to people.", "crew"),
            RouteEncounter("A pod of dolphins escorts you for an hour. Your bosun says it's a sign of welcome from the coast. The crew believes him.", "encounter"),
            RouteEncounter("You pass a merchant vessel flying the Exchange Alliance flag, heading north. 'Cotton north, grain south,' your navigator says. 'Been this way for centuries.'", "sighting"),
        ],
    ),

    "The Long Crossing": RouteEncounterTable(
        route_key="The Long Crossing",
        encounters=[
            RouteEncounter("Open water. No land in any direction. The sky meets the sea in a circle that hasn't changed in three days. The crew goes quiet.", "weather"),
            RouteEncounter("Day twelve of the crossing. Your navigator takes star readings twice a night. The slightest error here means weeks of drift.", "crew"),
            RouteEncounter("A piece of driftwood with carved symbols floats past — a prayer marker from an island nobody's charted. Someone was here before you.", "lore"),
            RouteEncounter("The crew's conversation turns to home. Where they came from. Where they'll go when they're done. The Long Crossing forces these thoughts.", "crew"),
            RouteEncounter("Your water casks are half-empty. The navigator says two more days. The cook starts rationing without being asked. Everyone knows what's at stake.", "encounter"),
            RouteEncounter("A flying fish lands on deck. The crew takes it as a sign — land is close. Your navigator confirms: the current has shifted. The East Indies are near.", "weather"),
            RouteEncounter("You spot another ship on the same heading — impossibly far away, a speck of sail. Someone else is making the crossing. You'll never know who.", "sighting"),
        ],
    ),

    "The Porcelain Lane": RouteEncounterTable(
        route_key="The Porcelain Lane",
        encounters=[
            RouteEncounter("A junk with the Kiln Masters' guild mark on its sail passes — its hold padded with straw. Every piece of porcelain in the west passed through this lane.", "sighting"),
            RouteEncounter("Your crew handles the cargo more carefully here. In the East Indies, they've learned that porcelain commands respect — and that broken porcelain means broken trust.", "crew"),
            RouteEncounter("The water turns jade-green. Islands appear like scattered emeralds. You're in the Porcelain Lane — where the oldest trade in the East flows.", "weather"),
            RouteEncounter("A fishing sampan pulls alongside. The fisherman offers you a fresh catch in exchange for news. In the East Indies, information is currency.", "encounter"),
        ],
    ),

    "The Silk Road by Sea": RouteEncounterTable(
        route_key="The Silk Road by Sea",
        encounters=[
            RouteEncounter("A silk convoy glides past — three junks in formation, their sails painted with the Weavers' Guild pattern. The silk inside is worth more than your ship.", "sighting"),
            RouteEncounter("Incense drifts from a passing vessel. In the Silk Waters, even the cargo smells beautiful.", "weather"),
            RouteEncounter("Your crew folds their clothes more carefully after a few days in these waters. The East Indies changes how people treat fabric.", "crew"),
            RouteEncounter("A sampan merchant offers a bolt of silk through your porthole while you're anchored for the night. The price is suspiciously good. Your bosun advises caution.", "encounter"),
        ],
    ),

    "Typhoon Alley": RouteEncounterTable(
        route_key="Typhoon Alley",
        encounters=[
            RouteEncounter("The pressure drops. Your ears pop. The sky turns a color you've never seen — yellow-grey-green. Typhoon Alley earns its name.", "weather"),
            RouteEncounter("A wrecked hull drifts past — no mast, no crew, barnacles already growing. Someone's journey ended here. Your crew says nothing.", "lore"),
            RouteEncounter("A storm rider's outrigger appears from nowhere, surfs the leading wave, and vanishes behind a squall. You're in their territory.", "sighting"),
            RouteEncounter("Your ship groans. The hull flexes in ways the shipwright intended — if she's from Monsoon Reach or Typhoon Anchorage. If she's Mediterranean... you pray.", "crew"),
            RouteEncounter("Lightning illuminates something on the horizon — an island not on your charts. When dawn comes, it's gone. The crew doesn't discuss it.", "lore"),
            RouteEncounter("Rain so heavy it stings the skin. The crew works by touch. The compass spins. Your navigator switches to dead reckoning and doesn't sleep for two days.", "weather"),
        ],
    ),

    "The Volcanic Passage": RouteEncounterTable(
        route_key="The Volcanic Passage",
        encounters=[
            RouteEncounter("The water warms. Not from the sun — from below. Volcanic vents heat the current here. The hull temperature rises. Your crew shifts nervously.", "weather"),
            RouteEncounter("Sulfur. The air thickens with it. Your eyes water. Welcome to the Volcanic Passage — the sea itself is on fire underneath.", "weather"),
            RouteEncounter("A column of steam rises from the water ahead — an underwater vent. Your navigator routes around it. The crew watches the thermometer climb.", "encounter"),
            RouteEncounter("An Ember Isle medicine boat crosses your path, obsidian-hulled and silent. The herbalists wave. Their cargo smells of eucalyptus and volcanic earth.", "sighting"),
            RouteEncounter("Your cook heats water for tea using the sea itself — he drops a bucket into the volcanic current and it comes up warm. 'Free fuel,' he says.", "crew"),
        ],
    ),

    "The Monsoon Shortcut": RouteEncounterTable(
        route_key="The Monsoon Shortcut",
        encounters=[
            RouteEncounter("You catch the monsoon wind and FLY. The ship heels over, sails taut, crew bracing. This is why they call it the Shortcut — if you time it right, nothing's faster.", "weather"),
            RouteEncounter("The wind dies. Completely. You're becalmed in open water between the Mediterranean and the East Indies. The crew stares at limp sails.", "weather"),
            RouteEncounter("A merchant vessel that attempted the Shortcut last season drifts past. Abandoned. The log is gone. Whatever happened, nobody recorded it.", "lore"),
            RouteEncounter("Your navigator pulls out the monsoon charts — handwritten, passed down from Farouk in Al-Manar's tea house. 'He sailed this seven times,' your navigator says. 'Trust the charts.'", "lore"),
            RouteEncounter("Wind shifts. The monsoon is changing direction — a day early. Your navigator adjusts instantly. The margin between 'Shortcut' and 'death sentence' is measured in hours.", "encounter"),
        ],
    ),

    "The Smuggler's Run": RouteEncounterTable(
        route_key="The Smuggler's Run",
        encounters=[
            RouteEncounter("Darkness. You run without lights because on the Smuggler's Run, visibility is the enemy. Your crew communicates in whispers.", "encounter"),
            RouteEncounter("A Crimson Tide ship appears on the horizon — then another. Then a third. They're not pursuing you. They're watching. The Run belongs to them.", "sighting"),
            RouteEncounter("Your lookout spots a trail of floating debris — crates, barrels, a torn sail. Someone dumped cargo in a hurry. Navy patrol, probably. Your crew moves your contraband deeper into the hold.", "encounter"),
            RouteEncounter("Eighty leagues of open water between two black market ports. The longest, most dangerous route in the Known World. Your crew knows the stakes. Nobody complains. Nobody jokes.", "crew"),
            RouteEncounter("An old pirate shanty drifts from below deck — someone's singing about the Run. The lyrics are about a captain who made the crossing so many times, the navy thought he was a ghost. He stopped correcting them.", "lore"),
            RouteEncounter("The Syndicate's signal — a lantern flash from an unseen ship — briefly illuminates the darkness. Three short, one long. It means 'patrol ahead, alter course.' Your navigator adjusts without being told.", "encounter"),
        ],
    ),

    "The Northern Passage": RouteEncounterTable(
        route_key="The Northern Passage",
        encounters=[
            RouteEncounter("The longest profitable route in the world. Iron west, porcelain east. Your hold tells the story of two civilizations that need each other.", "lore"),
            RouteEncounter("Ice. Not dangerous — floating crystals from the northern edge of the passage. Beautiful and foreign. Your crew collects pieces as souvenirs.", "weather"),
            RouteEncounter("A whale surfaces alongside — massive, slow, unconcerned. It travels the same passage, following the same currents, and has done so longer than any ship.", "sighting"),
            RouteEncounter("Week three. The provisions are holding, the crew is tired, and the passage stretches on. Your navigator says halfway. He's been saying halfway for two days.", "crew"),
            RouteEncounter("You spot Ironhaven's foundry glow on the western horizon — or is it Jade Port's kilns on the eastern? On the Northern Passage, both ends look the same from the middle.", "weather"),
        ],
    ),

    "The Deep South Run": RouteEncounterTable(
        route_key="The Deep South Run",
        encounters=[
            RouteEncounter("Pearl to pearl. The divers of the shallows and the divers of the reef — same craft, different kingdoms. Your cargo carries the weight of both traditions.", "lore"),
            RouteEncounter("Turquoise water so clear you can see the reef twenty feet below. Beautiful and deadly. One wrong turn and the coral claims your hull.", "weather"),
            RouteEncounter("A war canoe from Coral Throne appears. Warriors in painted armor watch you pass. One raises a spear — not in threat but in salute. You've been recognized.", "sighting"),
            RouteEncounter("Your crew spots something glinting in the shallows — a pearl, dropped or thrown. Nobody dives for it. On the Deep South Run, taking what the reef didn't offer is bad luck.", "lore"),
            RouteEncounter("Ceremonial drums carry across the water from an island you can't see. The Coral Kingdom is celebrating something. Your crew listens. The rhythm is infectious.", "encounter"),
        ],
    ),
}


# ---------------------------------------------------------------------------
# Region-Default Encounters (for unnamed routes)
# ---------------------------------------------------------------------------

REGION_ENCOUNTERS: dict[str, RouteEncounterTable] = {
    "Mediterranean": RouteEncounterTable(
        route_key="Mediterranean",
        encounters=[
            RouteEncounter("A merchant galley passes flying the Exchange Alliance flag. Orderly, clean, professional. The Mediterranean way.", "sighting"),
            RouteEncounter("Fishing boats dot the horizon — small, colorful, and everywhere. The Mediterranean feeds itself.", "sighting"),
            RouteEncounter("The coast is never far. Villages, harbors, lighthouses — civilization lines every shore.", "weather"),
            RouteEncounter("Your crew discusses grain prices — the universal conversation on Mediterranean routes.", "crew"),
        ],
    ),
    "North Atlantic": RouteEncounterTable(
        route_key="North Atlantic",
        encounters=[
            RouteEncounter("Grey seas, grey sky. The North Atlantic doesn't waste energy on color.", "weather"),
            RouteEncounter("A Stormwall patrol passes without greeting. In the north, silence IS the greeting.", "sighting"),
            RouteEncounter("Your crew pulls collars tight. The Atlantic cold gets into your bones and stays.", "crew"),
            RouteEncounter("Fog banks drift like walls. Your lookout strains forward. In the North Atlantic, what you can't see is what kills you.", "weather"),
        ],
    ),
    "West Africa": RouteEncounterTable(
        route_key="West Africa",
        encounters=[
            RouteEncounter("Warm air carries the scent of earth — red earth, growing things. The Gold Coast is alive.", "weather"),
            RouteEncounter("A fishing fleet returns singing. The rhythm is centuries old and utterly joyful.", "sighting"),
            RouteEncounter("Your crew relaxes. Something about the Gold Coast waters changes the mood. Shoulders drop. Voices soften.", "crew"),
            RouteEncounter("Rain falls warm and brief. The crew stands on deck, faces upturned, laughing. The Gold Coast rains are gifts, not threats.", "weather"),
        ],
    ),
    "East Indies": RouteEncounterTable(
        route_key="East Indies",
        encounters=[
            RouteEncounter("Incense drifts from a passing junk. In the East Indies, even the air is cultivated.", "weather"),
            RouteEncounter("A fleet of sampans crosses your path — fishermen, traders, and families living on the water. The East Indies floats.", "sighting"),
            RouteEncounter("Your crew becomes more formal in Eastern waters. They bow instead of waving. The culture seeps in.", "crew"),
            RouteEncounter("Islands appear and vanish in the morning mist. A thousand islands hide in the haze. Your charts show a fraction of them.", "weather"),
        ],
    ),
    "South Seas": RouteEncounterTable(
        route_key="South Seas",
        encounters=[
            RouteEncounter("The reef glows beneath the surface — alive, colorful, dangerous. The South Seas are beautiful the way a blade is beautiful.", "weather"),
            RouteEncounter("An outrigger canoe appears, its crew watching you with calm interest. They've been watching ships pass for generations.", "sighting"),
            RouteEncounter("Your crew falls silent. The South Seas demand a different kind of attention — not the bustle of the Mediterranean but the focus of a diver reading the reef.", "crew"),
            RouteEncounter("Flying fish skip across the bow. Stars reflected in still water. The South Seas overwhelm through beauty, not force.", "weather"),
        ],
    ),
}


# ---------------------------------------------------------------------------
# Lookup
# ---------------------------------------------------------------------------

def get_route_encounters(lore_name: str) -> RouteEncounterTable | None:
    """Get encounters specific to a named route."""
    return ROUTE_ENCOUNTERS.get(lore_name)


def get_region_encounters(region: str) -> RouteEncounterTable | None:
    """Get default encounters for a region (unnamed routes)."""
    return REGION_ENCOUNTERS.get(region)


# ---------------------------------------------------------------------------
# NPC Sightings at Sea
# ---------------------------------------------------------------------------
# When traveling through a region, you might spot NPCs from nearby ports
# going about their business. Non-interactive — passing ships, not meetings.
# Each sighting is region-locked so you only see local NPCs.

@dataclass(frozen=True)
class NPCSighting:
    """A named NPC spotted at sea — flavor, not interaction."""
    npc_name: str
    port_id: str
    region: str
    text: str


NPC_SIGHTINGS: dict[str, list[NPCSighting]] = {
    "Mediterranean": [
        NPCSighting("Dimitri Andros", "silva_bay", "Mediterranean",
            "A Silva Bay hull — unmistakable lines — cuts across your bow. Dimitri Andros stands at the prow, examining the waterline of a new build. He's testing it himself. He always does."),
        NPCSighting("Marta Soares", "porto_novo", "Mediterranean",
            "A Porto Novo grain barge passes with the Exchange Guild flag. On the quarterdeck, Marta Soares scans the horizon with a spyglass — checking the competition's cargo, no doubt."),
        NPCSighting("Scarlet Ana", "corsairs_rest", "Mediterranean",
            "Crimson pennants on the horizon. Scarlet Ana's flagship passes at distance — she sees you, tips her hat, and sails on. Business elsewhere today."),
        NPCSighting("Inspector Salva", "porto_novo", "Mediterranean",
            "A Porto Novo customs cutter crosses your wake. Inspector Salva stands at the rail with a manifest in hand, heading to intercept someone else. You're glad it's not you."),
        NPCSighting("Ghost", "corsairs_rest", "Mediterranean",
            "A ship passes in the early hours — no lights, no flag, loaded heavy. Ghost's crew, running cargo. By the time you blink, they've vanished into the dark."),
    ],
    "North Atlantic": [
        NPCSighting("The Smith", "ironhaven", "North Atlantic",
            "An Ironhaven supply boat passes carrying a crate marked with the Smith's personal seal. Whatever's inside, it was built by the best hands in the north. Someone ordered something special."),
        NPCSighting("Sergeant Kruze", "ironhaven", "North Atlantic",
            "A grey-hulled ship cuts through the fog — Iron Wolves. Sergeant Kruze stands at the helm, scanning methodically. He spots you, holds your gaze for three seconds, then turns away. Assessment complete."),
        NPCSighting("Siv Lindgren", "stormwall", "North Atlantic",
            "A small trade vessel flying Stormwall colors passes. Siv Lindgren waves energetically from the deck — she's heading to recruit merchants for the garrison's supply contracts. Her enthusiasm is visible from a league away."),
        NPCSighting("Bones Thorsen", "thornport", "North Atlantic",
            "A converted whaler — Bones Thorsen's fishing fleet — trawls the northern waters. The whale skeleton mounted on the bow catches the light. Bones raises a hand in silent greeting."),
    ],
    "West Africa": [
        NPCSighting("Ama Mensah", "sun_harbor", "West Africa",
            "A Gold Coast trading vessel passes with the Compact flag. On deck, Chief Weigher Ama stands with her counting staff, supervising a cotton shipment. Even at sea, her standards travel with her."),
        NPCSighting("Old Cassius", "palm_cove", "West Africa",
            "A Palm Cove rum boat passes close enough that you can smell the cargo. Old Cassius himself sits on a barrel, waving a bottle. 'BEST RUM ON THE COAST!' he shouts. Some things don't need a harbor."),
        NPCSighting("Yaa Acheampong", "iron_point", "West Africa",
            "An Iron Point ore barge passes, Yaa Acheampong standing on a crate of raw iron, negotiating by signal flag with a ship heading east. She's cutting deals even in transit."),
        NPCSighting("Elder Ama Diallo", "pearl_shallows", "West Africa",
            "A canoe of Breath-Holder divers glides past, heading for the outer reef. Elder Ama sits at the stern, eyes closed, breathing slowly. The morning dive is sacred. You pass in silence."),
    ],
    "East Indies": [
        NPCSighting("Factor Wu Jian", "jade_port", "East Indies",
            "A Jade Port silk-and-porcelain convoy passes — three junks in formation. Factor Wu stands on the lead ship, silk robes immaculate even at sea. He bows precisely as you pass. Fifteen degrees."),
        NPCSighting("Brother Anand", "monsoon_reach", "East Indies",
            "A small boat with a saffron sail drifts past the Wind Temple headland. Brother Anand sits cross-legged on the deck, eyes closed, reading the wind by feel. His forecast will be posted at dawn."),
        NPCSighting("Typhoon Mei", "spice_narrows", "East Indies",
            "A ship erupts from behind an island at impossible speed. Typhoon Mei stands on the bowsprit, laughing into the wind. She sees you, waves wildly, and vanishes around the next headland. Chaos in human form."),
        NPCSighting("Master Ink", "silk_haven", "East Indies",
            "A sampan drifts past Silk Haven's harbor. Master Ink sits cross-legged, painting the sea. He doesn't look up. A perfect brushstroke captures a wave that no longer exists. The painting will outlast the ocean."),
        NPCSighting("Apprentice Lin Yue", "jade_port", "East Indies",
            "A small kiln-boat from Jade Port passes — Apprentice Lin testing a new glaze in sea air. She holds a tile up to the light, frowns, adjusts something, holds it up again. Obsession at twenty-two."),
    ],
    "South Seas": [
        NPCSighting("Storm Chief Rangi", "typhoon_anchorage", "South Seas",
            "An outrigger war canoe slices through the swell — Storm Chief Rangi at the helm, reading the weather through the spray. Seven typhoons survived. She's watching the horizon for the eighth."),
        NPCSighting("Dive Boss Moana", "typhoon_anchorage", "South Seas",
            "A diving boat surfaces nearby — Moana's crew returning from the deep reef. Moana herself emerges glistening, a pouch of pearls tied to her wrist. She dives where others won't."),
        NPCSighting("Reef Pilot Iti", "coral_throne", "South Seas",
            "A pilot canoe approaches from the reef. Iti stands at the bow, reading the coral by water color. Twelve generations of reef knowledge in one pair of eyes."),
        NPCSighting("War Chief Tane", "coral_throne", "South Seas",
            "War canoes appear — painted to match the coral, nearly invisible until they're alongside. War Chief Tane's escort. They watch you pass. The spears stay lowered. Today."),
        NPCSighting("Healer Sera", "ember_isle", "South Seas",
            "An Ember Isle medicine boat passes, volcanic-stone hull and eucalyptus smoke trailing behind. Head Herbalist Sera waves from the deck, surrounded by crates of freshly harvested remedies."),
    ],
}


def get_npc_sightings(region: str) -> list[NPCSighting]:
    """Get possible NPC sightings for a region."""
    return NPC_SIGHTINGS.get(region, [])


# ---------------------------------------------------------------------------
# Sea Lore & Superstitions
# ---------------------------------------------------------------------------
# First-time experiences that trigger crew stories and beliefs.
# Each fires once per game — tracked by the narrative system.

@dataclass(frozen=True)
class SeaSuperstition:
    """A crew belief or story triggered by a specific condition."""
    id: str
    trigger: str                     # what triggers it: "first_region_X", "first_storm", etc.
    text: str
    crew_reaction: str               # how the crew responds


SEA_SUPERSTITIONS: list[SeaSuperstition] = [
    # First-time region entries
    SeaSuperstition("first_east_indies", "first_region_East Indies",
        "The old hands gather the new crew at the bow. 'The East Indies,' the bosun says. 'Everything here is older than us. Older than our ships. Older than our countries. Show respect and the waters will let you pass.'",
        "The crew moves more quietly. Voices lower. Something has shifted."),
    SeaSuperstition("first_south_seas", "first_region_South Seas",
        "The lookout calls 'Reef!' and the crew rushes to the rail. Below the hull, the coral glows in colors nobody has words for. Your navigator whispers: 'The charts are wrong here. The reef moves. Trust your eyes, not the paper.'",
        "Wonder. Genuine, wide-eyed wonder. Even the veterans stare."),
    SeaSuperstition("first_north_atlantic", "first_region_North Atlantic",
        "The temperature drops. The Mediterranean warmth fades like a memory. An old sailor wraps himself in a wool coat and says: 'The Atlantic doesn't warn you. It just hits. Keep your head down and your hull tight.'",
        "The crew gets serious. Joking stops. Preparation begins."),
    SeaSuperstition("first_west_africa", "first_region_West Africa",
        "Warm rain — the first the crew has felt. It tastes of earth and growing things. A sailor who's been here before says: 'The Gold Coast gives freely. But it remembers what you give back. Trade honestly here.'",
        "Relaxation. Shoulders drop. Someone laughs. The coast has a way."),

    # Voyage events
    SeaSuperstition("first_storm_survived", "survived_storm",
        "After the storm passes, the crew is silent for a long time. Then someone starts bailing, and everyone follows. The bosun says: 'She held. The ship held.' It sounds like a prayer.",
        "Bond. The crew who survives a storm together is a different crew afterward."),
    SeaSuperstition("first_pirate_encounter", "survived_pirates",
        "The pirate ship fades behind you. Hands are shaking. Someone laughs — the high, thin laugh of relief. 'That was close,' the helmsman says. Nobody disagrees.",
        "Alertness. Every sail on the horizon gets a long look from now on."),
    SeaSuperstition("passing_wreck", "wreck_sighted",
        "A wrecked hull drifts past — no mast, no crew, barnacles thick on the waterline. The crew watches in silence. Someone removes their hat. 'Could've been us,' the bosun says. Nobody argues.",
        "Mortality. The sea reminds you what happens when luck runs out."),
    SeaSuperstition("becalmed_first", "first_calm",
        "No wind. The sails hang like wet laundry. The sea is a mirror. Time stops. After two hours, the crew starts making up games. After six, they start telling truths they'd never say on land.",
        "Honesty. There's nothing to do but wait and talk. The truths come out."),

    # Cargo and trade
    SeaSuperstition("sacred_cargo", "carrying_sacred_good",
        "The old hands treat the cargo differently — more carefully, more quietly. 'This is what they revere,' the bosun explains. 'Handle it with respect and the port will remember. Handle it badly and so will the sea.'",
        "Reverence. The cargo becomes more than weight. It becomes responsibility."),
    SeaSuperstition("contraband_nerves", "carrying_contraband",
        "Nobody says the word. They call it 'the special cargo' or 'the extra provisions' or just nod toward the hold. The crew avoids the inspector's eye even when there isn't one. Contraband changes how people breathe.",
        "Tension. Jokes become quieter. Laughter becomes shorter. Everyone watches the horizon."),

    # Milestones
    SeaSuperstition("hundredth_day", "day_100",
        "Day one hundred. The navigator marks it in the log with a small ceremony — a tradition older than anyone aboard can explain. A cup of the best drink is poured into the sea. 'For the water that carried us,' the navigator says.",
        "Pride. A hundred days of voyaging. Not everyone can say that."),
    SeaSuperstition("fifth_region", "visited_all_regions",
        "The crew realizes, quietly, that they've sailed every water the charts show. Mediterranean, Atlantic, Gold Coast, East Indies, South Seas. The Known World, all of it, beneath their keel. A sailor says: 'What's left?' Nobody answers. Nobody needs to.",
        "Completion. And the strange emptiness that follows. What do you seek when you've seen everything?"),
]


# ---------------------------------------------------------------------------
# Crew Morale & Voice
# ---------------------------------------------------------------------------
# Crew reactions based on game state — the emotional mirror of the voyage.

@dataclass(frozen=True)
class CrewMood:
    """Crew mood triggered by game state conditions."""
    id: str
    condition: str                   # what triggers this mood
    flavor_texts: list[str]          # random selection from these


CREW_MOODS: list[CrewMood] = [
    CrewMood("prosperous", "silver > 2000",
        ["The crew walks taller. When the hold is full and the silver heavy, even the sea looks friendly.",
         "Someone's whistling at the helm. The cook made extra tonight. Prosperity makes generous sailors.",
         "The crew discusses what they'll spend their shares on. Houses, farms, a boat of their own. Silver breeds dreams."]),

    CrewMood("struggling", "silver < 100",
        ["The crew eats quietly. Nobody complains — but nobody laughs either. Thin times make thin smiles.",
         "Whispered conversations below deck. 'How long can we keep sailing?' your bosun hears. He doesn't repeat it.",
         "The cook stretches the provisions. Watered rum, thinner stew. The crew notices but says nothing. Loyalty has limits."]),

    CrewMood("first_voyage", "day < 10",
        ["Everything is new. The crew leans over the rail watching the wake. Even the seagulls are fascinating. This won't last, but right now, the world is enormous.",
         "Your navigator explains the stars to a young sailor. The old hands pretend not to listen. They listen anyway.",
         "The smell of the sea — salt, kelp, distance. For the crew, this is the smell of possibility. For the captain, it's the smell of responsibility."]),

    CrewMood("veteran", "day > 200",
        ["The crew moves like a machine — sails adjusted before you call for it, rigging checked without orders. Two hundred days builds instinct.",
         "Your bosun can read your expression from the helm. You don't need to give orders anymore. A glance at the sails is enough.",
         "The crew has its own language now — gestures, looks, half-sentences that carry complete meanings. They're not a crew. They're a crew."]),

    CrewMood("after_big_trade", "recent_profit > 500",
        ["The hold is lighter and the silver heavier. The crew celebrates with an extra ration. Your bosun says: 'That's a trade they'll talk about at port.'",
         "Word travels fast on a ship. Everyone knows the margin you made. Respect comes in the form of sharper salutes and louder songs."]),

    CrewMood("after_loss", "recent_loss",
        ["Silence on deck. The cargo is gone — seized, sunk, or sold at a loss. The crew doesn't blame you. Not out loud. The sea takes what it takes.",
         "Your bosun finds you at the helm after dark. 'It happens to every captain,' he says. 'The ones who quit are the ones who deserved to.' Then he leaves."]),

    CrewMood("new_ship", "just_upgraded",
        ["The crew explores the new ship like children in a new house — opening every hatch, testing every line, arguing about which berth is best.",
         "The new ship creaks differently. The old hands listen, learning her voice. Every ship has one. This one hasn't told them yet."]),

    CrewMood("carrying_contraband", "has_contraband",
        ["Nobody talks about it. The hold is rearranged so the 'special cargo' is behind the legitimate goods. The crew avoids eye contact when inspectors are mentioned.",
         "Your lookout watches the horizon with unusual intensity. Every sail could be a patrol. Every sail probably isn't. But every sail gets watched.",
         "A nervous joke from the galley: 'What's the difference between a merchant and a smuggler? The smuggler knows when to shut up.' Nobody laughs. Then everyone laughs."]),

    CrewMood("in_storm", "during_storm",
        ["Rain. Wind. The deck tilts at angles that make standing an act of faith. The crew works in silence because the storm takes every word.",
         "The ship groans. The crew listens. You learn to read a hull's voice — complaint vs. warning vs. surrender. This groan is complaint. You hope.",
         "Someone prays. Someone else checks the bilge pump. Both are acts of faith."]),

    CrewMood("calm_seas", "extended_calm",
        ["The sea is glass. The sky is empty. The wind is a memory. Your crew invents entertainment: card games, fishing, arguments about whose home port has better food.",
         "Day three of calm. The cook runs a fishing line. The catch is better than anything in the provisions. 'I should do this for a living,' he says. Nobody points out that he does.",
         "Becalmed. The old hands say it's the sea's way of making you think. What you think about depends on what you carry — in the hold and in the heart."]),
]


def get_crew_moods() -> list[CrewMood]:
    """Get all crew mood definitions."""
    return CREW_MOODS


def get_superstitions() -> list[SeaSuperstition]:
    """Get all sea superstitions."""
    return SEA_SUPERSTITIONS
