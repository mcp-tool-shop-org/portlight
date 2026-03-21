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
