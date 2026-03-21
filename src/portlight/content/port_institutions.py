"""Port institutions and NPCs — the people who make ports alive.

Every port has institutions: the harbor master's office, the market exchange,
the shipyard (if any), the broker's desk, the tavern, and the customs house.
Each institution is run by a named NPC with personality, agenda, and
relationships with other NPCs in the same port.

These are the faces of the game. When a player docks at Porto Novo, they
don't interact with "a port" — they interact with Harbor Master Vasco,
who remembers their last visit and has opinions about their cargo.

Design principle: every NPC should have:
  1. A name the player remembers
  2. An agenda that creates tension with at least one other NPC
  3. A relationship with the player that changes based on behavior
  4. A line of dialogue that reveals personality in one breath
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PortNPC:
    """A named character who runs an institution at a port."""
    id: str
    name: str
    title: str                       # "Harbor Master", "Guild Factor", etc.
    port_id: str
    institution: str                 # which institution they run
    personality: str                 # one word: stern, jovial, shrewd, paranoid, etc.
    description: str                 # physical/personality sketch (2-3 sentences)
    agenda: str                      # what they want, what drives them
    greeting_neutral: str            # what they say to a stranger
    greeting_friendly: str           # what they say to a friend (high standing)
    greeting_hostile: str            # what they say to someone they distrust
    rumor: str                       # gossip about them you'd hear at the tavern
    relationship_notes: dict[str, str] = field(default_factory=dict)  # npc_id → how they feel


@dataclass(frozen=True)
class PortInstitution:
    """An institution within a port — a place with purpose and politics."""
    id: str
    name: str
    port_id: str
    institution_type: str            # harbor_master, exchange, shipyard, broker, tavern, customs, governor
    description: str                 # what the building/place looks like
    function: str                    # what it does mechanically (flavor-wrapped)
    political_leaning: str           # how this institution relates to the port's bloc politics
    npc_id: str                      # who runs it


@dataclass(frozen=True)
class PortInstitutionalProfile:
    """Complete institutional profile for a port — all institutions and NPCs."""
    port_id: str
    governor_title: str              # what the local ruler is called
    power_structure: str             # one-paragraph description of who holds power
    internal_tension: str            # the core political conflict within this port
    institutions: list[PortInstitution] = field(default_factory=list)
    npcs: list[PortNPC] = field(default_factory=list)


# =========================================================================
# PORTO NOVO — The Exchange Alliance's Heart
# =========================================================================

_PORTO_NOVO_NPCS = [
    PortNPC(
        id="pn_vasco",
        name="Vasco da Reira",
        title="Harbor Master",
        port_id="porto_novo",
        institution="harbor_master",
        personality="meticulous",
        description=(
            "A lean man with ink-stained fingers and spectacles perched on a sharp nose. "
            "Vasco has logged every ship that entered Porto Novo for thirty-one years. "
            "He knows your tonnage before you drop anchor."
        ),
        agenda=(
            "Order. Vasco wants every manifest filed, every fee collected, and every "
            "berth assigned by dawn. He despises smugglers, tolerates merchants, and "
            "respects captains who arrive with clean paperwork."
        ),
        greeting_neutral="\"Manifest and tonnage, Captain. I'll assign your berth once I've reviewed them.\"",
        greeting_friendly="\"Ah, Captain — berth seven is clear. I saved it when I saw your sails. Your paperwork is always in order.\"",
        greeting_hostile="\"Papers. Now. And if I find a single discrepancy, you'll wait in the outer harbor until I'm satisfied.\"",
        rumor="They say Vasco once held a merchant ship at anchor for three days because the manifest listed 'grain' instead of 'winter wheat.' The merchant never made the mistake again.",
        relationship_notes={
            "pn_marta": "Respects her. She keeps the Exchange running and that keeps his harbor orderly.",
            "pn_old_enzo": "Wary. Enzo's tavern is where rules get bent. Vasco pretends not to notice.",
            "pn_senhora_costa": "Defers to her completely. She appointed him. He serves her vision.",
            "pn_dimitri": "Professional admiration. The shipyard runs clean — Vasco appreciates that.",
            "pn_inspector_salva": "Allies. Salva enforces the law; Vasco enforces the paperwork. Two sides of the same coin.",
            "pn_broker_reis": "Cordial. She needs his arrival logs; he appreciates her orderly contract paperwork.",
        },
    ),
    PortNPC(
        id="pn_marta",
        name="Marta Soares",
        title="Guild Factor",
        port_id="porto_novo",
        institution="exchange",
        personality="shrewd",
        description=(
            "Broad-shouldered, sharp-eyed, and always surrounded by three junior "
            "clerks trailing behind her with wax tablets. Marta is the Exchange Guild's "
            "chief factor — the woman who reads the dawn rates aloud from the Exchange "
            "steps every morning. She's never wrong about grain prices."
        ),
        agenda=(
            "The Exchange Guild's dominance. Marta wants Porto Novo to remain the "
            "Mediterranean's price-setting authority. She views Al-Manar's Spice Circle "
            "as arrogant upstarts and Corsair's Rest as a stain on the region. She'll "
            "offer better rates to captains who bring grain and worse rates to anyone "
            "she suspects of dealing with the black market."
        ),
        greeting_neutral="\"You're here for the rates? They were posted at dawn. Grain is steady, spice is climbing. What are you buying?\"",
        greeting_friendly="\"Captain! Good timing — I have a surplus I need moved before the prices drop. Interested in a private arrangement?\"",
        greeting_hostile="\"I know where your last cargo came from. The Exchange remembers. Your rates will reflect that.\"",
        rumor="Marta once cornered the entire Mediterranean cotton market for three weeks. She bought everything, waited for the price to double, then sold. The Alliance pretended to disapprove. Secretly, they were impressed.",
        relationship_notes={
            "pn_vasco": "Uses him. Vasco's obsession with order serves the Guild perfectly.",
            "pn_old_enzo": "Distrusts him deeply. Enzo's tavern is where black market contacts meet. She's sure of it but can't prove it.",
            "pn_senhora_costa": "Rivals. Costa wants political stability; Marta wants market dominance. They clash on tariff policy monthly.",
            "pn_dimitri": "Cordial. She needs his ships; he needs her contracts. Business.",
            "pn_inspector_salva": "Values him. Salva catches the cheats she can't.",
        },
    ),
    PortNPC(
        id="pn_dimitri",
        name="Dimitri Andros",
        title="Master Shipwright",
        port_id="porto_novo",
        institution="shipyard",
        personality="gruff",
        description=(
            "Hands like ship timbers, salt-white beard, and a voice that carries "
            "across the entire yard. Dimitri has built more hulls than most captains "
            "have sailed. He judges a captain by the condition of their ship, not their "
            "silver. Bring him a well-maintained vessel and he'll work miracles. Bring "
            "him a wreck and he'll tell you what you did wrong — loudly."
        ),
        agenda=(
            "The craft. Dimitri cares about ships, not politics. But he refuses to "
            "build warships for anyone — a principle that cost him the Iron Pact contract "
            "and earned him the Shipwrights' Brotherhood's eternal loyalty. He wants "
            "captains who respect their vessels."
        ),
        greeting_neutral="\"Let me see your hull before we talk price. I don't repair what I wouldn't sail.\"",
        greeting_friendly="\"Captain! She's holding up well — you've been treating her right. Come, I have a new keel design to show you.\"",
        greeting_hostile="\"What did you DO to this ship? This hull has been through a storm and a boarding and you didn't patch either. Get out of my yard until you learn to sail.\"",
        rumor="Dimitri was offered a fortune to build a flagship for the Crimson Tide. He told Scarlet Ana to build it herself. She laughed and left. They've been on oddly respectful terms ever since.",
        relationship_notes={
            "pn_vasco": "Gets along. Two professionals who understand duty.",
            "pn_marta": "Tolerates. She's all about money; he's all about craft. Different species.",
            "pn_old_enzo": "Drinking partners. Enzo's rum is the only thing that gets Dimitri off the yard after dark.",
            "pn_senhora_costa": "Quiet loyalty. She protected the Brotherhood when the Iron Pact pressured them. He hasn't forgotten.",
            "pn_inspector_salva": "Indifferent. Salva inspects cargo, not ships. Different jurisdictions.",
        },
    ),
    PortNPC(
        id="pn_senhora_costa",
        name="Senhora Isabela Costa",
        title="Port Governor",
        port_id="porto_novo",
        institution="governor",
        personality="diplomatic",
        description=(
            "Silver hair pulled back, always in a dark blue coat with the Exchange "
            "seal embroidered on the cuff. Senhora Costa has governed Porto Novo for "
            "twelve years — longer than any predecessor. She rules through consensus, "
            "which means she's always listening and never fully agreeing."
        ),
        agenda=(
            "Stability and the Alliance. Costa wants Porto Novo prosperous, orderly, "
            "and at the center of Mediterranean trade. She views the Silk Circle's "
            "growing influence with concern and the Shadow Ports with outright hostility. "
            "She's the one who proposed the Alliance-wide weapons embargo against "
            "pirate-linked captains."
        ),
        greeting_neutral="\"Welcome to Porto Novo, Captain. I trust you'll find our markets fair and our laws clear.\"",
        greeting_friendly="\"Captain — a pleasure. The Alliance benefits from captains of your standing. Will you join me for dinner? There are matters to discuss.\"",
        greeting_hostile="\"Your reputation precedes you, Captain. I'll be candid: Porto Novo has standards. I suggest you meet them, or seek harbor elsewhere.\"",
        rumor="Costa was once a trader herself — ran the Al-Manar to Sun Harbor route for fifteen years before she entered politics. Some say she still keeps a ship hidden in Silva Bay, just in case.",
        relationship_notes={
            "pn_vasco": "Appointed him. He's her eyes on the harbor.",
            "pn_marta": "Political rivals who need each other. Costa sets policy; Marta controls prices. Neither can rule alone.",
            "pn_old_enzo": "Tolerates him. Enzo's tavern is useful — she gets intelligence from his rumors. He gets immunity from her inspectors.",
            "pn_dimitri": "Protected his Brotherhood from the Iron Pact. He's quietly devoted.",
            "pn_inspector_salva": "Her enforcer. Salva reports directly to her, not the Guild.",
        },
    ),
    PortNPC(
        id="pn_old_enzo",
        name="Old Enzo",
        title="Tavern Keeper",
        port_id="porto_novo",
        institution="tavern",
        personality="jovial",
        description=(
            "Round, red-faced, and always laughing at a joke only he heard. Old Enzo "
            "has run the Harbor Bell tavern since before Vasco started keeping records. "
            "He knows everyone's secrets and tells none of them — unless the rum is "
            "good enough and the listener is interesting enough."
        ),
        agenda=(
            "Survival and stories. Enzo is the unofficial bridge between Porto Novo's "
            "legitimate world and its shadow. He doesn't smuggle — but he knows who "
            "does. He doesn't break laws — but he bends them into pretzels. His tavern "
            "is where contracts are whispered before they're signed, where crew is "
            "recruited, and where captains learn which routes are safe this season."
        ),
        greeting_neutral="\"Sit! Drink! You look like a captain who's been at sea too long. First one's on the house — I'll put it on your next cargo.\"",
        greeting_friendly="\"My favorite captain! Your usual table is waiting. I may have heard something that interests you — but first, how was the voyage?\"",
        greeting_hostile="\"...Ah. You. The rum is full-price tonight, and I haven't heard any rumors. Strange, isn't it? Usually I hear everything.\"",
        rumor="Old Enzo was a pirate once — or so the story goes. He never confirms and never denies. His left hand is missing two fingers, and he changes the subject if you ask about them.",
        relationship_notes={
            "pn_vasco": "Amused by him. Vasco pretends the tavern doesn't exist. Enzo finds this hilarious.",
            "pn_marta": "Wary. Marta suspects him of facilitating black market deals. She's not entirely wrong.",
            "pn_dimitri": "Best friends. They drink together every night and argue about ships vs. rum. Neither wins.",
            "pn_senhora_costa": "Useful to each other. She gets intelligence; he gets protection. An unspoken deal that works.",
            "pn_inspector_salva": "Keeps his distance. Salva is the one person in Porto Novo that Enzo genuinely fears.",
        },
    ),
    PortNPC(
        id="pn_inspector_salva",
        name="Inspector Salva",
        title="Chief Customs Inspector",
        port_id="porto_novo",
        institution="customs",
        personality="relentless",
        description=(
            "Thin as a blade, with eyes that miss nothing and a memory for cargo "
            "that borders on supernatural. Inspector Salva has never accepted a bribe — "
            "not because he's incorruptible, but because the satisfaction of catching "
            "a smuggler is worth more to him than silver."
        ),
        agenda=(
            "The law. Salva is Senhora Costa's instrument, but his motivation is personal. "
            "His brother was killed by black powder smuggled through a legitimate port. "
            "Every contraband seizure is a small act of justice. He is thorough, fair, "
            "and absolutely merciless with anyone carrying undeclared goods."
        ),
        greeting_neutral="\"Cargo manifest. All of it. I'll inspect the hold at my discretion.\"",
        greeting_friendly="\"Captain. Your record is clean — I appreciate that more than you know. Standard inspection, quick and painless.\"",
        greeting_hostile="\"Open every hold. Every crate. Every barrel. I have all day, Captain. Do you?\"",
        rumor="Salva once inspected a ship for nine hours straight. Found three false panels, a hidden compartment, and enough opium to fill a rowboat. The captain is still in prison.",
        relationship_notes={
            "pn_vasco": "Allies. Vasco's paperwork makes Salva's job easier.",
            "pn_marta": "Professional respect. She wants cheats caught; he catches them.",
            "pn_dimitri": "No strong feelings. Different worlds.",
            "pn_senhora_costa": "Reports to her. Loyal, but his real loyalty is to the law itself.",
            "pn_old_enzo": "The one Enzo fears. Salva suspects the tavern is a contact point. He hasn't proven it yet. Yet.",
        },
    ),
    PortNPC(
        id="pn_broker_reis",
        name="Fernanda Reis",
        title="Senior Broker",
        port_id="porto_novo",
        institution="broker",
        personality="calculating",
        description=(
            "Dark eyes, quick hands, and a mind that tracks six contracts simultaneously "
            "without writing anything down. Fernanda runs the broker's desk at the "
            "Exchange — the place where contracts are matched to captains and opportunities "
            "become obligations."
        ),
        agenda=(
            "Commission and connections. Fernanda takes a cut of every contract she "
            "brokers. She wants high-value captains who complete deliveries on time, "
            "because their success is her reputation. She'll steer good contracts toward "
            "reliable captains and leave the scraps for unknowns."
        ),
        greeting_neutral="\"New captain? I have contracts. Small ones, for now. Complete them on time and we'll talk about the real work.\"",
        greeting_friendly="\"Captain! I've been holding something for you — a charter that requires someone I trust. Interested?\"",
        greeting_hostile="\"I have nothing for you today. Or tomorrow. Come back when your reputation improves — if it can.\"",
        rumor="Fernanda once brokered a grain contract worth more than the entire port's weekly revenue. The captain delivered early. Fernanda bought a house. They're still partners.",
        relationship_notes={
            "pn_vasco": "Cordial. She needs his arrival logs to time her offers.",
            "pn_marta": "Complex. The Guild sets the rates; Fernanda sets the contracts. They compete for influence over trade flow.",
            "pn_senhora_costa": "Costa approves her contracts. Fernanda makes sure the right ones cross Costa's desk.",
            "pn_old_enzo": "Useful. Enzo's tavern rumors tell her which captains are desperate — desperation makes captains take risky contracts.",
            "pn_inspector_salva": "Careful around him. Some of her contracts brush close to grey areas. Salva doesn't need to know.",
        },
    ),
]

_PORTO_NOVO_INSTITUTIONS = [
    PortInstitution(
        id="pn_harbor",
        name="The Harbor Master's Tower",
        port_id="porto_novo",
        institution_type="harbor_master",
        description=(
            "A stone tower at the harbor mouth with a brass telescope on the roof "
            "and a ledger room that smells of ink and sealing wax. Every ship is "
            "logged, every berth assigned, every fee collected here."
        ),
        function="Controls docking, assigns berths, collects port fees. Clean records earn faster processing.",
        political_leaning="Alliance loyalist. Vasco runs a tight harbor that reflects Alliance standards.",
        npc_id="pn_vasco",
    ),
    PortInstitution(
        id="pn_exchange",
        name="The Grain Exchange",
        port_id="porto_novo",
        institution_type="exchange",
        description=(
            "A columned hall on the waterfront — the largest building in Porto Novo. "
            "Dawn rates are read from the steps every morning. Inside, the trading "
            "floor hums with negotiation, and the air smells of grain dust and ambition."
        ),
        function="Sets daily prices, arbitrates trade disputes, manages market slots. The Alliance's economic heart.",
        political_leaning="The Exchange IS the Alliance. Marta's policies are Alliance policies.",
        npc_id="pn_marta",
    ),
    PortInstitution(
        id="pn_shipyard",
        name="Andros & Sons Shipyard",
        port_id="porto_novo",
        institution_type="shipyard",
        description=(
            "A sprawling yard of slipways, sawpits, and dry docks. The sound of "
            "adzes and hammers never stops. Three hulls are always under construction. "
            "The sign reads 'Andros & Sons' but the sons are long grown and it's just "
            "Dimitri now, with his apprentices."
        ),
        function="Ship repairs, upgrades, and purchases. Quality work at fair prices — but Dimitri judges your seamanship.",
        political_leaning="Apolitical. Dimitri builds for anyone who respects ships. Except warmongers.",
        npc_id="pn_dimitri",
    ),
    PortInstitution(
        id="pn_governor",
        name="The Governor's Residence",
        port_id="porto_novo",
        institution_type="governor",
        description=(
            "A modest stone house overlooking the harbor, distinguished only by the "
            "Exchange Alliance banner hanging from the balcony. Costa governs from a "
            "desk covered in charts and correspondence. No throne, no court — just "
            "a woman who works."
        ),
        function="Sets port policy, approves trade agreements, manages Alliance relations. The political center.",
        political_leaning="Alliance core. Costa's policies shape the entire Mediterranean legitimate trade.",
        npc_id="pn_senhora_costa",
    ),
    PortInstitution(
        id="pn_tavern",
        name="The Harbor Bell",
        port_id="porto_novo",
        institution_type="tavern",
        description=(
            "A low-ceilinged tavern built from ship timbers, with a salvaged bell "
            "hanging over the door. It's always too warm, too loud, and too crowded. "
            "The food is terrible. The rum is excellent. Everyone comes here."
        ),
        function="Crew recruitment, rumors, underworld contacts. The social hub where deals begin before they're official.",
        political_leaning="Neutral — Enzo serves all sides, which makes him useful to everyone and trusted by no one.",
        npc_id="pn_old_enzo",
    ),
    PortInstitution(
        id="pn_customs",
        name="The Customs House",
        port_id="porto_novo",
        institution_type="customs",
        description=(
            "A clean, whitewashed building near the docks with iron bars on every "
            "window and a locked evidence room in the basement. The waiting bench "
            "outside is the most feared seat in Porto Novo."
        ),
        function="Cargo inspection, tariff collection, contraband seizure. Clean captains pass quickly. Others don't.",
        political_leaning="Alliance enforcer. Salva enforces Alliance trade law with personal intensity.",
        npc_id="pn_inspector_salva",
    ),
    PortInstitution(
        id="pn_broker",
        name="The Broker's Desk",
        port_id="porto_novo",
        institution_type="broker",
        description=(
            "A cramped office at the back of the Exchange, walls covered in pinned "
            "contracts and route maps. Fernanda's desk is the cleanest surface — "
            "everything important is in her head."
        ),
        function="Contract matching, market intelligence, trade opportunities. Better standing unlocks better contracts.",
        political_leaning="Pragmatic Alliance. Fernanda follows the rules — mostly — when it's profitable.",
        npc_id="pn_broker_reis",
    ),
]

PORTO_NOVO_PROFILE = PortInstitutionalProfile(
    port_id="porto_novo",
    governor_title="Port Governor",
    power_structure=(
        "Porto Novo is governed by Senhora Costa, but real power is triangulated: "
        "Costa sets policy, Marta controls prices through the Exchange Guild, and "
        "Salva enforces the law. Dimitri's shipyard is independent — the Brotherhood "
        "answers to craft, not politics. Old Enzo's tavern is the shadow channel "
        "where information flows that the official institutions pretend doesn't exist. "
        "Fernanda's broker desk is where policy meets practice — she decides which "
        "contracts reach which captains."
    ),
    internal_tension=(
        "The core tension is between Marta and Costa. Marta wants market dominance — "
        "she'd squeeze every margin to make the Exchange richer. Costa wants political "
        "stability — she'd sacrifice some profit for Alliance cohesion. They need each "
        "other: Costa can't govern without the Guild's revenue, and Marta can't trade "
        "without Costa's political protection. The tension keeps Porto Novo honest. "
        "Meanwhile, Old Enzo quietly facilitates the grey economy that neither woman "
        "acknowledges exists, and Inspector Salva watches everything with the patience "
        "of a man who knows that sooner or later, everyone makes a mistake."
    ),
    institutions=_PORTO_NOVO_INSTITUTIONS,
    npcs=_PORTO_NOVO_NPCS,
)


# ---------------------------------------------------------------------------
# Master registry — will grow as we build each port
# ---------------------------------------------------------------------------

PORT_INSTITUTIONAL_PROFILES: dict[str, PortInstitutionalProfile] = {
    "porto_novo": PORTO_NOVO_PROFILE,
}

ALL_NPCS: dict[str, PortNPC] = {npc.id: npc for profile in PORT_INSTITUTIONAL_PROFILES.values() for npc in profile.npcs}

ALL_INSTITUTIONS: dict[str, PortInstitution] = {inst.id: inst for profile in PORT_INSTITUTIONAL_PROFILES.values() for inst in profile.institutions}
