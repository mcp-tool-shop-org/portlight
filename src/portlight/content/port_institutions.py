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



# =========================================================================
# AL-MANAR — The Exchange Alliance's Soul
# =========================================================================

_AL_MANAR_NPCS = [
    PortNPC(
        id="am_khalil",
        name="Khalil al-Rashid",
        title="Harbor Master",
        port_id="al_manar",
        institution="harbor_master",
        personality="ceremonial",
        description=(
            "A tall man in white robes with a gold chain of office that he wears "
            "even in the sweltering heat. Khalil treats every arriving ship as a "
            "diplomatic event. He greets captains personally, offers dates and water, "
            "and only then asks for paperwork. The ceremony is the paperwork."
        ),
        agenda=(
            "Dignity. Khalil believes Al-Manar's harbor should reflect the city's "
            "ancient prestige. He wants captains to feel honored to dock here — and "
            "to pay accordingly. He quietly resents Porto Novo's larger harbor and "
            "compensates with superior hospitality."
        ),
        greeting_neutral="\"Welcome to Al-Manar, Captain. Please — dates, water. We discuss your berth after you have rested from the sea.\"",
        greeting_friendly="\"Captain! The harbor sings your name. Your berth awaits, and I have taken the liberty of arranging fresh provisions. We are honored.\"",
        greeting_hostile="\"...Captain. You may dock at the outer quay. The inner harbor is reserved for merchants of established reputation.\"",
        rumor="Khalil once refused docking to a Porto Novo flagship because the captain didn't observe the greeting ritual. The diplomatic incident lasted a month. Khalil didn't apologize.",
        relationship_notes={
            "am_yasmin": "Deep respect. The Spice Mother is the heart of the city. He serves her vision.",
            "am_old_farouk": "Fond. Farouk's tea house is where Khalil relaxes — the only place he drops the ceremony.",
            "am_senhora_nadia": "Loyal. She appointed him. He repays that trust with flawless protocol.",
            "am_inspector_zara": "Uneasy. Zara's inspections sometimes lack the grace Khalil expects. Efficiency without elegance offends him.",
            "am_hakim": "Respectful. The Apothecary Master's medicines are part of Al-Manar's prestige.",
            "am_broker_tariq": "Cordial. Tariq brings quality captains. Quality captains deserve quality arrivals.",
        },
    ),
    PortNPC(
        id="am_yasmin",
        name="Yasmin al-Nadir",
        title="The Spice Mother",
        port_id="al_manar",
        institution="exchange",
        personality="imperious",
        description=(
            "Silver rings on every finger, robes that smell of cardamom and saffron, "
            "and eyes that have judged the quality of spice for fifty years. Yasmin "
            "is the Spice Merchants' Circle's eldest — they call her the Spice Mother. "
            "She doesn't negotiate. She declares the price, and the market adjusts."
        ),
        agenda=(
            "Al-Manar's supremacy. Yasmin believes Al-Manar — not Porto Novo — is "
            "the true heart of Mediterranean trade. Grain is survival; spice is "
            "civilization. She wants the Spice Circle to lead the Exchange Alliance, "
            "and she'll use every trade relationship, every favor owed, and every "
            "ounce of her considerable influence to make it happen."
        ),
        greeting_neutral="\"You come to the Bazaar? Good. Tell me what you carry, and I will tell you what it is worth. In Al-Manar, the price is the truth.\"",
        greeting_friendly="\"Ah, a captain who understands quality. Come — I have set aside a blend that even my daughters haven't tasted. For trusted friends only.\"",
        greeting_hostile="\"I know what you've been trading. And where. The Bazaar has long memories, Captain. Your prices here will reflect that.\"",
        rumor="Yasmin once tasted a spice blend and named the island it came from, the year of harvest, and the family who grew it. She was right on all three counts. Nobody tests her anymore.",
        relationship_notes={
            "am_khalil": "Appreciates his ceremony. It reflects Al-Manar's dignity — which is her life's work.",
            "am_old_farouk": "Her oldest friend. They've argued about spice and tea for forty years. Neither has conceded a single point.",
            "am_senhora_nadia": "Political ally, personal rival. Both want Al-Manar to lead. They disagree on how.",
            "am_inspector_zara": "Useful. Zara catches the counterfeit spice that Yasmin's reputation can't afford.",
            "am_hakim": "Family. Hakim is her nephew. She appointed him. His success is her legacy.",
            "am_broker_tariq": "Watches him carefully. Tariq is ambitious. Ambition is useful — until it isn't.",
        },
    ),
    PortNPC(
        id="am_senhora_nadia",
        name="Senhora Nadia Khoury",
        title="Merchant Princess",
        port_id="al_manar",
        institution="governor",
        personality="regal",
        description=(
            "Dark eyes, impeccable posture, and the quiet authority of someone who "
            "has never had to raise her voice to be obeyed. Nadia's family has governed "
            "Al-Manar for six generations — she inherited the title 'Merchant Princess' "
            "along with the port's debts and ambitions. She governs from a tiled palace "
            "above the harbor, where every surface reflects light."
        ),
        agenda=(
            "Legacy. Nadia wants Al-Manar to outlast her — to be the port her "
            "great-grandchildren govern. She's more patient than Costa, more political "
            "than Marta, and more dangerous than either because she thinks in "
            "generations, not quarters. She's been quietly building trade relationships "
            "with the Silk Circle — something the Alliance would consider dangerously "
            "close to disloyalty."
        ),
        greeting_neutral="\"Al-Manar welcomes all who trade with honor. My house is open, Captain. What brings you to our harbor?\"",
        greeting_friendly="\"Captain — you honor my house with your return. I have been thinking about our last conversation. There is an opportunity I wish to discuss.\"",
        greeting_hostile="\"My harbor master informs me of your... recent activities. I will be plain: Al-Manar remembers everything. Consider your next trade carefully.\"",
        rumor="Nadia has been exchanging private letters with a Silk Circle official. The Alliance doesn't know — or pretends not to. If it's a trade deal, it could reshape Mediterranean commerce. If it's betrayal, it could shatter the Alliance.",
        relationship_notes={
            "am_khalil": "Her appointee. His ceremony reflects her standards.",
            "am_yasmin": "Political ally, personal rival. Yasmin wants the Circle to lead; Nadia wants the Khoury family to lead. Both want Al-Manar on top.",
            "am_old_farouk": "Amused by him. His tea house is where she goes to think without being watched — or so she believes.",
            "am_inspector_zara": "Respects her competence. Zara is the best inspector in the Mediterranean. Nadia poached her from Porto Novo.",
            "am_hakim": "Patron. She funds his apothecary research from the port treasury. His medicines are Al-Manar's quiet advantage.",
            "am_broker_tariq": "Grooming him. Tariq is young, sharp, and loyal — for now. She's testing whether he stays loyal when the stakes rise.",
        },
    ),
    PortNPC(
        id="am_old_farouk",
        name="Old Farouk",
        title="Tea Master",
        port_id="al_manar",
        institution="tavern",
        personality="philosophical",
        description=(
            "Weathered face, calm hands, and the patience of a man who has brewed "
            "ten thousand pots of tea and plans to brew ten thousand more. Old Farouk "
            "runs the Amber Glass — not a tavern but a tea house, because in Al-Manar, "
            "information flows over tea, not rum. He listens more than he speaks, "
            "and what he speaks is worth the silence."
        ),
        agenda=(
            "Understanding. Farouk doesn't want power or silver — he wants to "
            "understand why people trade, why they sail, why they risk everything "
            "for cargo that could sink in a storm. He collects stories the way "
            "Yasmin collects spices. His tea house is where captains come to think, "
            "and where deals are conceived before anyone signs anything."
        ),
        greeting_neutral="\"Sit. Tea first. Business is for those who have already tasted patience.\"",
        greeting_friendly="\"My friend — the good leaves today. I saved them when I heard your ship on the horizon. Tell me: what did the sea teach you this time?\"",
        greeting_hostile="\"...Tea is served to all. Even those the harbor distrusts. Sit, if you wish. But the good leaves are not for everyone.\"",
        rumor="Farouk was a navigator once — sailed the Monsoon Shortcut seven times. He retired after the seventh, saying he'd learned everything the sea had to teach. Nobody knows if he meant the route or something else entirely.",
        relationship_notes={
            "am_khalil": "The only person who sees Khalil without the ceremony. They play chess in the evenings.",
            "am_yasmin": "Forty years of argument about whether spice or tea is the higher art. The argument IS the friendship.",
            "am_senhora_nadia": "She comes to his tea house to think. He lets her believe she's not being observed.",
            "am_inspector_zara": "Sympathetic. Zara carries a weight Farouk recognizes. He serves her a special blend — calming, no charge.",
            "am_hakim": "Mentored him as a boy. Taught Hakim that medicine is patience, not ingredients.",
            "am_broker_tariq": "Wary. Tariq moves too fast. Farouk has seen what happens to men who outrun their wisdom.",
        },
    ),
    PortNPC(
        id="am_inspector_zara",
        name="Inspector Zara Osman",
        title="Chief Customs Inspector",
        port_id="al_manar",
        institution="customs",
        personality="precise",
        description=(
            "Short hair, sharp uniform, and the focused intensity of a surgeon. "
            "Zara was Porto Novo's best inspector before Nadia poached her with a "
            "better title and a harder challenge: Al-Manar's spice market attracts "
            "the most sophisticated counterfeiters in the Mediterranean. Zara can "
            "identify fake saffron by smell alone."
        ),
        agenda=(
            "Authenticity. Zara's mission is protecting Al-Manar's reputation for "
            "quality. Counterfeit spice dilutes the market and destroys trust. She "
            "cares less about smuggling than about fraud — a captain carrying real "
            "goods gets a nod; a captain carrying adulterated spice gets a cell. "
            "She misses Porto Novo sometimes. Salva was a good partner."
        ),
        greeting_neutral="\"Cargo for inspection. I'm particularly interested in your spice lots — origin documentation, please.\"",
        greeting_friendly="\"Captain — your goods are always genuine. Quick inspection, and you're through. I wish every captain traded as cleanly.\"",
        greeting_hostile="\"Open everything. I've seen cargo from your route before, Captain, and I've found problems. Let's see if today is different.\"",
        rumor="Zara left Porto Novo after a disagreement with Inspector Salva about methods. Salva hunts smugglers; Zara hunts frauds. They respect each other but couldn't work together. Different obsessions.",
        relationship_notes={
            "am_khalil": "Tolerates his ceremony. She'd prefer efficiency, but his greeting ritual gives her time to observe the crew.",
            "am_yasmin": "Allies. Yasmin's reputation depends on quality. Zara guarantees it.",
            "am_senhora_nadia": "Loyal. Nadia gave her the freedom Salva wouldn't. In return, Zara protects Al-Manar's market integrity.",
            "am_old_farouk": "Grateful. Farouk's tea is the only thing that helps her sleep. The job wears on her.",
            "am_hakim": "Professional respect. His medicines are always pure. She never needs to inspect twice.",
            "am_broker_tariq": "Watching him. Some of Tariq's contracts originate from sources she hasn't verified. That bothers her.",
        },
    ),
    PortNPC(
        id="am_hakim",
        name="Hakim al-Nadir",
        title="Apothecary Master",
        port_id="al_manar",
        institution="apothecary",
        personality="gentle",
        description=(
            "Soft-spoken, always smelling faintly of eucalyptus, with ink-stained "
            "fingers from recording recipes. Hakim is Yasmin's nephew — he inherited "
            "her nose for quality but not her ruthlessness. He runs Al-Manar's "
            "Apothecary Guild, blending medicines from spice-market ingredients that "
            "no other port can replicate."
        ),
        agenda=(
            "Healing. Hakim genuinely wants to cure sickness, not profit from it. "
            "He sells medicines at fair prices — which infuriates merchants who want "
            "to mark them up. He's building a collection of medicinal recipes from "
            "every region, and he'll trade generously with any captain who brings him "
            "ingredients from the East Indies or South Seas."
        ),
        greeting_neutral="\"Captain — do you carry medicines or ingredients? I'm always interested in what the sea brings. And if you need healing, my rates are fair.\"",
        greeting_friendly="\"My friend! Did you find the root I asked about? No? No matter — come, see what I've been working on. I think I've cracked the Ember Isle formula.\"",
        greeting_hostile="\"I heal all who ask. That is my oath. But I will not supply medicines for... questionable purposes. If your intentions are honest, I am here.\"",
        rumor="Hakim turned down a fortune from the Iron Pact for exclusive medicine rights. He said healing belongs to everyone, not to the highest bidder. Yasmin was furious. Then she was proud.",
        relationship_notes={
            "am_khalil": "Grateful. Khalil ensures medicine shipments get priority berthing.",
            "am_yasmin": "His aunt, his patron, his harshest critic. She expects perfection. He tries to give her compassion instead.",
            "am_senhora_nadia": "His patron from the treasury. She funds his research. He's not sure why — political advantage or genuine interest. Both, probably.",
            "am_old_farouk": "His mentor. Farouk taught him patience. Every recipe begins with patience.",
            "am_inspector_zara": "Grateful she's here. Counterfeit medicines kill people. Zara stops counterfeits.",
            "am_broker_tariq": "Uneasy. Tariq keeps suggesting he should raise his prices. Hakim keeps refusing.",
        },
    ),
    PortNPC(
        id="am_broker_tariq",
        name="Tariq Sayed",
        title="Senior Broker",
        port_id="al_manar",
        institution="broker",
        personality="ambitious",
        description=(
            "Young, sharp-dressed, and always moving. Tariq is the youngest senior "
            "broker in Al-Manar's history — appointed by Nadia over the objections "
            "of older candidates. He has excellent instincts for matching captains "
            "to contracts, but his ambition makes the establishment nervous. He wants "
            "Al-Manar's broker desk to rival Porto Novo's, and he's not patient about it."
        ),
        agenda=(
            "Prominence. Tariq wants to make Al-Manar the contract capital of the "
            "Mediterranean — not just the spice capital. He's been quietly courting "
            "Silk Circle traders for exclusive luxury contracts that bypass Porto Novo "
            "entirely. If he succeeds, it shifts the balance of power within the "
            "Alliance. If he fails, Nadia will deny she ever supported him."
        ),
        greeting_neutral="\"Captain. I have contracts — good ones. Al-Manar doesn't waste time with small work. Tell me your capacity and I'll match you.\"",
        greeting_friendly="\"Captain! I've been waiting for you. I have something — a contract that Fernanda in Porto Novo would kill for. But it came to MY desk first.\"",
        greeting_hostile="\"I... don't have anything suitable for your profile at this time. Perhaps try Porto Novo? I hear their standards are more... flexible.\"",
        rumor="Tariq was seen dining with a Silk Circle merchant from Jade Port. If he's brokering a direct Al-Manar-to-Jade-Port luxury contract, it would be the biggest deal in a decade — and Porto Novo's Fernanda Reis would be furious.",
        relationship_notes={
            "am_khalil": "Impatient with the ceremony but respects its purpose. First impressions matter for contract negotiations.",
            "am_yasmin": "She watches him. He knows she watches him. He performs for her judgment while trying to exceed it.",
            "am_senhora_nadia": "His patron. She appointed him. He suspects she's testing him. He's right.",
            "am_old_farouk": "Avoids the tea house. Farouk sees through him, and Tariq isn't ready to be seen through yet.",
            "am_inspector_zara": "Careful. Some of his contracts push boundaries. Zara hasn't said anything — yet.",
            "am_hakim": "Frustrated. Hakim's medicines could be worth a fortune if he'd just raise his prices. Hakim won't. Tariq finds this baffling.",
        },
    ),
]

_AL_MANAR_INSTITUTIONS = [
    PortInstitution(
        id="am_harbor",
        name="The Harbor of Arrivals",
        port_id="al_manar",
        institution_type="harbor_master",
        description=(
            "A curved stone quay lined with date palms, with a reception pavilion "
            "where arriving captains are offered dates and water before any business "
            "is discussed. The harbor is smaller than Porto Novo's but immaculately "
            "maintained. Every bollard is polished bronze."
        ),
        function="Controls docking, assigns berths, collects port fees. Arrival is a ceremony here, not a transaction.",
        political_leaning="Alliance loyalist with Al-Manar pride. Khalil serves the city's dignity before the Alliance's efficiency.",
        npc_id="am_khalil",
    ),
    PortInstitution(
        id="am_bazaar",
        name="The Spice Bazaar",
        port_id="al_manar",
        institution_type="exchange",
        description=(
            "A covered market stretching three city blocks, its ceiling hung with "
            "brass lamps and dried herb bundles. A hundred stalls compete for the "
            "nose — cinnamon, cardamom, saffron, clove. The auction floor is at the "
            "center, where the Spice Mother holds court every morning."
        ),
        function="Sets spice prices, auctions rare lots, arbitrates quality disputes. The Mediterranean's premier spice market.",
        political_leaning="Al-Manar supremacist. The Bazaar believes it IS Mediterranean trade, and Porto Novo is just a granary.",
        npc_id="am_yasmin",
    ),
    PortInstitution(
        id="am_palace",
        name="The Khoury Palace",
        port_id="al_manar",
        institution_type="governor",
        description=(
            "A tiled palace above the harbor where every surface catches light — "
            "mosaics of trade ships, courtyards with fountains, and a receiving room "
            "where the Merchant Princess conducts business from a divan instead of "
            "a desk. Six generations of Khourys watch from portraits on the walls."
        ),
        function="Sets port policy, manages diplomatic relations, controls the port treasury. Hereditary governance — not elected.",
        political_leaning="Alliance member with independent ambitions. Nadia is loyal to the Alliance when it serves Al-Manar, and creative when it doesn't.",
        npc_id="am_senhora_nadia",
    ),
    PortInstitution(
        id="am_tea_house",
        name="The Amber Glass",
        port_id="al_manar",
        institution_type="tavern",
        description=(
            "Not a tavern — a tea house. Low tables, silk cushions, and the quiet "
            "murmur of conversation conducted in a language that rum drinkers wouldn't "
            "understand. The amber glass windows filter the harbor light into gold. "
            "Everything here moves at the speed of tea."
        ),
        function="Social hub, intelligence exchange, crew recruitment. Information flows over tea, not rum. Deals are conceived here before they're signed anywhere else.",
        political_leaning="Neutral, but Farouk's neutrality is informed. He knows everything and judges nothing — which makes him invaluable to everyone.",
        npc_id="am_old_farouk",
    ),
    PortInstitution(
        id="am_customs",
        name="The Scales of Truth",
        port_id="al_manar",
        institution_type="customs",
        description=(
            "A marble building with the inscription 'WEIGHT AND TRUTH' carved above "
            "the door. Inside, brass scales of extraordinary precision line the walls. "
            "Zara's office is spare — a desk, a lamp, and a collection of confiscated "
            "counterfeit spices mounted in glass cases like specimens."
        ),
        function="Cargo inspection focused on QUALITY and AUTHENTICITY, not just legality. Fake saffron is a worse crime than smuggling here.",
        political_leaning="Quality enforcement. Zara serves Al-Manar's reputation, which happens to align with Alliance standards.",
        npc_id="am_inspector_zara",
    ),
    PortInstitution(
        id="am_apothecary",
        name="The Apothecary House",
        port_id="al_manar",
        institution_type="apothecary",
        description=(
            "A whitewashed building with a garden of medicinal herbs on the roof. "
            "Inside, the air is thick with eucalyptus and camphor. Shelves of labeled "
            "jars line every wall — roots, dried flowers, mineral powders, pressed "
            "oils. Hakim's workbench is at the center, surrounded by mortars and "
            "handwritten recipe books."
        ),
        function="Medicine production, quality certification, medicinal ingredient trading. Unique to Al-Manar — no other port has a dedicated apothecary institution.",
        political_leaning="Humanitarian. Hakim serves health, not politics. But his medicines give Al-Manar a trade advantage nobody talks about openly.",
        npc_id="am_hakim",
    ),
    PortInstitution(
        id="am_broker",
        name="The Broker's Alcove",
        port_id="al_manar",
        institution_type="broker",
        description=(
            "An arched alcove off the Bazaar's main hall, curtained with silk — "
            "because in Al-Manar, even contract negotiations happen behind beautiful "
            "fabric. Tariq's desk is polished rosewood. The contracts on it are "
            "handwritten on parchment, not printed on paper like Porto Novo's."
        ),
        function="Contract matching with an emphasis on prestige and exclusivity. Better contracts than Porto Novo — but fewer of them, and you have to earn access.",
        political_leaning="Ambitious Al-Manar loyalist. Tariq wants the Alcove to replace Porto Novo's desk as the Alliance's contract center.",
        npc_id="am_broker_tariq",
    ),
]

AL_MANAR_PROFILE = PortInstitutionalProfile(
    port_id="al_manar",
    governor_title="Merchant Princess",
    power_structure=(
        "Al-Manar is governed by hereditary merchant aristocracy — the Khoury family "
        "has held the title 'Merchant Princess' for six generations. But real power "
        "is shared: Nadia sets policy, Yasmin controls the spice market through the "
        "Circle, and Hakim's apothecary gives Al-Manar a unique trade advantage. "
        "Old Farouk's tea house is where all three go to think — separately, each "
        "believing they're unobserved. Zara, poached from Porto Novo, protects the "
        "market's integrity. Tariq pushes for expansion at the broker's desk, "
        "supported by Nadia but watched by everyone."
    ),
    internal_tension=(
        "The core tension is between tradition and ambition. Yasmin wants to preserve "
        "Al-Manar's ancient way — the Bazaar's authority, the Circle's traditions, "
        "the slow pace of tea-and-negotiation commerce. Tariq wants to modernize — "
        "faster contracts, direct Silk Circle partnerships, bypassing Porto Novo "
        "entirely. Nadia is playing both sides: she funds Tariq's ambitions while "
        "publicly deferring to Yasmin's traditions. Meanwhile, Nadia's private "
        "correspondence with the Silk Circle could reshape the entire Alliance — "
        "or destroy it. Only Farouk suspects the full picture, and he's not talking."
    ),
    institutions=_AL_MANAR_INSTITUTIONS,
    npcs=_AL_MANAR_NPCS,
)



# =========================================================================
# SILVA BAY — The Shipwrights' Republic
# =========================================================================

_SILVA_BAY_NPCS = [
    PortNPC(
        id="sb_elena",
        name="Elena Madeira",
        title="Master Shipwright",
        port_id="silva_bay",
        institution="shipyard",
        personality="exacting",
        description=(
            "Broad hands scarred by adze and chisel, hair tied back with a leather "
            "thong, and sawdust permanently ground into the creases of her knuckles. "
            "Elena is the Brotherhood's elected Master — the finest shipwright in the "
            "Mediterranean and possibly the world. She can look at a hull and tell you "
            "where it was built, when, and whether the builder rushed the keel."
        ),
        agenda=(
            "The craft and the Brotherhood's independence. Elena will build for "
            "anyone who respects ships — pirate, merchant, navy, she doesn't care. "
            "But she will NEVER build warships. The Brotherhood builds vessels to "
            "carry cargo and people, not weapons of war. She turned down the Iron "
            "Pact's contract personally, and she'd do it again. Her loyalty is to "
            "wood, not politics."
        ),
        greeting_neutral="\"Show me your ship. I'll tell you what she needs and what it'll cost. I don't need your name — I need to see your keel.\"",
        greeting_friendly="\"Captain! Brought her back in one piece, I see. Good sailor. Come — I've been experimenting with a new hull design. I want your opinion.\"",
        greeting_hostile="\"I'll repair your ship because the sea doesn't care about grudges. But I'm charging double, and I'm not smiling about it.\"",
        rumor="Elena once rebuilt a ship that had been cracked in half by a storm. The owner said it was impossible. Elena said it was Tuesday. The ship sailed for another twelve years.",
        relationship_notes={
            "sb_nuno": "Her harbor master, her old apprentice. She trained him. He still defers to her on everything that matters.",
            "sb_tomás": "Her timber buyer. She's the only person who can overrule his assessments. He respects that.",
            "sb_council": "She IS the council. The Brotherhood elects a Master; the Master governs. She governs lightly.",
            "sb_rosa": "Drinks at Rosa's tavern every night. The only person who can make Elena laugh.",
            "sb_customs_pires": "Ignores him. Ships are her jurisdiction; cargo is his. Clean boundaries.",
            "sb_broker_ana": "Appreciates her. Ana brings captains who need good ships. Good ships are Elena's purpose.",
        },
    ),
    PortNPC(
        id="sb_nuno",
        name="Nuno Ferreira",
        title="Harbor Master",
        port_id="silva_bay",
        institution="harbor_master",
        personality="practical",
        description=(
            "A former shipwright who lost three fingers to a bandsaw and moved to "
            "harbor management — 'same work, fewer blades,' he says. Nuno runs the "
            "harbor with a shipwright's eye: he cares about how ships dock, not "
            "about paperwork. Vasco in Porto Novo would have a seizure watching "
            "Nuno's filing system, which consists of a nail on the wall and a "
            "good memory."
        ),
        agenda=(
            "Keep the harbor moving. Ships in, ships out, timber in, timber out. "
            "Nuno has no political ambitions — he wants berths filled, slipways busy, "
            "and the tide tables accurate. He learned harbor craft from Elena and "
            "still checks with her before making big decisions."
        ),
        greeting_neutral="\"Berth's over there. Tie up properly — I don't want you drifting into the slipways. Timber loading happens at dawn, so don't sleep late.\"",
        greeting_friendly="\"Captain! Good to see her still floating. Take berth three — it's closest to the yard if you need Elena's people. Rough voyage?\"",
        greeting_hostile="\"You can dock, but stay out of the yard. Elena's orders. And if your ship leaks on my harbor floor, you're cleaning it up.\"",
        rumor="Nuno can predict the weather better than any barometer. He says it's the missing fingers — they ache before a storm. Nobody laughs anymore, because he's never been wrong.",
        relationship_notes={
            "sb_elena": "His mentor. He defers to her on anything important and isn't embarrassed about it.",
            "sb_tomás": "Good friends. They coordinate timber deliveries — Tomás grades it, Nuno stores it.",
            "sb_council": "Sits on the council but rarely speaks. 'I run the harbor, not the town.'",
            "sb_rosa": "Regular at her tavern. Brings her harbor news; she gives him the first pour of the evening.",
            "sb_customs_pires": "Works alongside him. Clean relationship — they share the dock without competing.",
            "sb_broker_ana": "Helpful. Tips her off when interesting captains arrive.",
        },
    ),
    PortNPC(
        id="sb_tomás",
        name="Tomás Verdelho",
        title="Timber Factor",
        port_id="silva_bay",
        institution="exchange",
        personality="patient",
        description=(
            "Quiet, deliberate, with the slow-moving confidence of a man who has "
            "handled every kind of wood that grows. Tomás runs the Timber Exchange — "
            "not an auction house like Porto Novo's grain operation, but a grading "
            "yard where every log is assessed by hand. He can tell oak from elm by "
            "the sound it makes when he taps it with his knuckle."
        ),
        agenda=(
            "Quality timber at honest prices. Tomás has no interest in cornering "
            "markets or playing politics. He grades wood, sets fair prices, and "
            "goes home. His one passion outside timber is protecting the forests — "
            "he's pushed the Brotherhood to limit harvests, arguing that a forest "
            "cut too fast won't grow back. This makes him unpopular with merchants "
            "who want volume."
        ),
        greeting_neutral="\"Looking for timber? Let me show you what's in the yard. I'll grade it while you watch — no surprises.\"",
        greeting_friendly="\"Captain — I've been setting aside a batch of coastal oak. Perfect for hull planking. Thought of you when it came in.\"",
        greeting_hostile="\"Timber's timber. I'll sell it to you at posted prices. But don't expect me to hold stock for someone who doesn't respect the wood.\"",
        rumor="Tomás once refused to sell a batch of mahogany because he said the trees were too young. The buyer offered triple. Tomás said the trees would be worth ten times that in twenty years. He was right.",
        relationship_notes={
            "sb_elena": "She's the only person who can overrule his grades. He respects that — she knows wood as well as he does.",
            "sb_nuno": "Good friends. They coordinate timber logistics — a clean partnership.",
            "sb_council": "Active council member. He's the environmental voice — limit harvests, replant, think long-term.",
            "sb_rosa": "Quiet regular. He drinks slowly and says little. Rosa respects the silence.",
            "sb_customs_pires": "No strong feelings. Timber doesn't need inspecting — it is what it is.",
            "sb_broker_ana": "She brings buyers; he grades the wood. Simple relationship.",
        },
    ),
    PortNPC(
        id="sb_council",
        name="The Brotherhood Council",
        title="Governing Council",
        port_id="silva_bay",
        institution="governor",
        personality="collective",
        description=(
            "Not a single ruler — a council of seven shipwrights who govern Silva "
            "Bay by consensus. The Master Shipwright (currently Elena) chairs it, "
            "but every member has equal voice. They meet in the Brotherhood Hall, "
            "a timber longhouse where the walls are carved with the names of every "
            "ship built in Silva Bay for the last two centuries."
        ),
        agenda=(
            "Independence. The Council's primary concern is keeping Silva Bay free "
            "from outside control. They're in the Exchange Alliance because it's "
            "convenient, not because they're loyal. If the Alliance ever demands "
            "something that conflicts with the Brotherhood's principles — like "
            "building warships — they'll leave. Everyone knows this. It's why "
            "nobody pushes."
        ),
        greeting_neutral="\"The Brotherhood welcomes all captains who come in peace. If you need ships built or repaired, we are at your service.\"",
        greeting_friendly="\"Captain — the Council recognizes your contribution to Silva Bay's prosperity. Your voice is welcome in our hall.\"",
        greeting_hostile="\"The Council has discussed your recent conduct. You may dock and repair, but you are not welcome in the Brotherhood Hall until trust is rebuilt.\"",
        rumor="The Council once voted on whether to leave the Exchange Alliance entirely. The vote was 4-3 to stay. Nobody knows which way Elena voted. She says it doesn't matter — the Brotherhood decided.",
        relationship_notes={
            "sb_elena": "She chairs the council. Her word carries weight, but she lets others speak first.",
            "sb_nuno": "Sits on the council, rarely speaks. His harbor expertise is valued when it's needed.",
            "sb_tomás": "The environmental conscience. His harvest limits are controversial but respected.",
            "sb_rosa": "Not on the council, but Rosa's tavern is where council members discuss things they won't say in the Hall.",
            "sb_customs_pires": "Not on the council. Customs is an Alliance function, not a Brotherhood one. The distinction matters.",
            "sb_broker_ana": "Not on the council, but her contract income funds Brotherhood operations.",
        },
    ),
    PortNPC(
        id="sb_rosa",
        name="Rosa Carvalho",
        title="Tavern Keeper",
        port_id="silva_bay",
        institution="tavern",
        personality="warm",
        description=(
            "Strong arms from hauling kegs, a voice that carries over any crowd, "
            "and a laugh that makes everyone within earshot feel like the world is "
            "simpler than they thought. Rosa runs the Dry Dock — the only tavern "
            "in Silva Bay, built from the timbers of a decommissioned brigantine. "
            "The bar is the ship's original helm. She steers conversations the way "
            "the old captain steered the ship."
        ),
        agenda=(
            "Community. Rosa's tavern is where Silva Bay actually works — where "
            "apprentices celebrate finishing their first hull, where the Council "
            "argues after meetings, where captains hear which shipwright to request. "
            "She has no political agenda, but her tavern IS the town square, which "
            "gives her more influence than she'd ever admit."
        ),
        greeting_neutral="\"Welcome to the Dry Dock! Sit anywhere — if you can find a seat. The special tonight is fish stew, and yes, there's sawdust in it. There's sawdust in everything here.\"",
        greeting_friendly="\"Captain! Your stool's been empty too long. Sit, sit — Elena was just telling a story about your ship. Something about the rudder? You should hear this.\"",
        greeting_hostile="\"...You can drink. But I'd keep my voice down if I were you. The Brotherhood has long memories and short tempers when the ale flows.\"",
        rumor="Rosa was married to a captain who sailed the Smuggler's Run and never came back. She built the Dry Dock with the insurance payout. She never remarried, and she never talks about it, and nobody asks.",
        relationship_notes={
            "sb_elena": "Best friends. Elena drinks here every night. Rosa is the only person who can make her laugh — or slow down.",
            "sb_nuno": "Fond. He brings her harbor news; she pours first. A good trade.",
            "sb_tomás": "Respects his quiet. She gives him the corner table and doesn't interrupt.",
            "sb_council": "Her tavern is the unofficial second meeting hall. She pretends not to listen. She always listens.",
            "sb_customs_pires": "Cautious. Pires is the only outsider in Silva Bay — Alliance-appointed. Rosa is polite but hasn't fully accepted him.",
            "sb_broker_ana": "Like a daughter. Ana grew up in the Dry Dock while her mother worked the yard.",
        },
    ),
    PortNPC(
        id="sb_customs_pires",
        name="Customs Officer Pires",
        title="Customs Officer",
        port_id="silva_bay",
        institution="customs",
        personality="awkward",
        description=(
            "A young man from Porto Novo who drew the short straw — assigned to "
            "Silva Bay by the Alliance, where nobody asked for a customs officer "
            "and nobody particularly wants one. Pires is competent but uncomfortable. "
            "He knows he's an outsider in a town that governs itself, and he tries "
            "too hard to fit in. The Brotherhood tolerates him because the Alliance "
            "requires it."
        ),
        agenda=(
            "Doing his job without making enemies. Pires inspects cargo because "
            "the Alliance says he must, but he keeps it light — quick checks, no "
            "drama. He dreams of a transfer back to Porto Novo where Inspector "
            "Salva's methods are appreciated. In Silva Bay, thoroughness is seen "
            "as interference."
        ),
        greeting_neutral="\"Quick inspection — routine, I promise. I know you're here for the yard, not for paperwork. I'll be fast.\"",
        greeting_friendly="\"Captain — everything looks good. I've already signed off on your manifest. Go see Elena before the queue gets long.\"",
        greeting_hostile="\"I... need to do a full inspection. Alliance regulations. I'm sorry — I know it's inconvenient. Please don't tell Elena.\"",
        rumor="Pires applied for a transfer back to Porto Novo three times. Each time, Salva sent back the same response: 'Learn to inspect without a manual first.' Pires isn't sure if it's an insult or a lesson.",
        relationship_notes={
            "sb_elena": "Terrified of her. She treats him like furniture. He inspects what he can and stays out of her yard.",
            "sb_nuno": "Workable. Nuno doesn't mind him — they share dock space without trouble.",
            "sb_tomás": "Irrelevant to each other. Timber doesn't need customs clearance.",
            "sb_council": "Not invited. Not Brotherhood. The distinction stings, but he understands it.",
            "sb_rosa": "Trying. He drinks at the Dry Dock and tips well. Rosa is polite. He can't tell if she likes him or tolerates him.",
            "sb_broker_ana": "She's kind to him. The only person in Silva Bay who treats him as a colleague, not a visitor.",
        },
    ),
    PortNPC(
        id="sb_broker_ana",
        name="Ana Sousa",
        title="Broker",
        port_id="silva_bay",
        institution="broker",
        personality="earnest",
        description=(
            "Grew up in the Dry Dock tavern while her mother worked the yard. Ana "
            "became a broker instead of a shipwright — the first in her family to "
            "choose paper over wood. She runs contracts from a bench outside the "
            "Brotherhood Hall, rain or shine, because Silva Bay doesn't believe in "
            "offices. She knows every ship that's been built here and which captains "
            "treat them well."
        ),
        agenda=(
            "Proving herself. Ana is young and working in a town that values decades "
            "of experience. She brings contract work that funds the Brotherhood, "
            "which earns her a seat at the edge of respect. She wants to prove that "
            "commerce and craft can coexist — that a good broker helps good shipwrights "
            "stay independent."
        ),
        greeting_neutral="\"Captain? I have contracts — mostly timber runs and ship delivery commissions. Nothing fancy, but the work is honest and it pays.\"",
        greeting_friendly="\"Captain! Elena mentioned your ship needs attention — while she's working on it, I have a timber contract that would pay for the repairs. Interested?\"",
        greeting_hostile="\"I... don't have anything for you right now. Try Porto Novo — Fernanda has more to work with than I do. No hard feelings.\"",
        rumor="Ana turned down an offer from Fernanda Reis to join Porto Novo's broker desk. She said Silva Bay needed her more. Rosa cried when she heard. Elena pretended not to notice, which is Elena's way of being proud.",
        relationship_notes={
            "sb_elena": "Admires her fiercely. Elena is everything Ana wants to be — independent, skilled, uncompromising.",
            "sb_nuno": "Helpful. He tips her off when captains arrive who might need contracts.",
            "sb_tomás": "She finds buyers for his timber. A clean business relationship that both appreciate.",
            "sb_council": "Wants to be invited someday. Knows she has to earn it. Isn't sure how.",
            "sb_rosa": "Like a mother. Ana grew up in the Dry Dock. Rosa still saves her a plate of fish stew.",
            "sb_customs_pires": "Kind to him. She knows what it's like to be the outsider trying to earn respect.",
        },
    ),
]

_SILVA_BAY_INSTITUTIONS = [
    PortInstitution(
        id="sb_shipyard",
        name="The Master Shipyard",
        port_id="silva_bay",
        institution_type="shipyard",
        description=(
            "The largest shipyard in the Mediterranean — three slipways, two dry "
            "docks, a steam box for bending timber, and a mast pond where logs "
            "season for years before they're touched. The sign over the gate reads "
            "'BUILT TO SAIL, NOT TO SINK.' It's not a motto. It's a threat."
        ),
        function="Ship repairs, upgrades, and purchases. The best work in the game — cheapest repairs (1 silver/hull point). Elena's standards are the price of admission.",
        political_leaning="Apolitical. The yard builds for anyone. ANYONE. Except warmongers.",
        npc_id="sb_elena",
    ),
    PortInstitution(
        id="sb_harbor",
        name="The Working Harbor",
        port_id="silva_bay",
        institution_type="harbor_master",
        description=(
            "No ceremony, no pavilion — just a clipboard, a tide table nailed to "
            "a post, and Nuno squinting at your approach. Timber barges have priority; "
            "everyone else fits where they fit. The harbor smells of fresh-cut wood "
            "and pitch."
        ),
        function="Berth assignment, timber logistics. No ceremony — function over form. Nuno runs it like a shipwright runs a project.",
        political_leaning="Brotherhood-aligned. The harbor serves the yard first, everything else second.",
        npc_id="sb_nuno",
    ),
    PortInstitution(
        id="sb_timber_exchange",
        name="The Timber Yard",
        port_id="silva_bay",
        institution_type="exchange",
        description=(
            "An open-air grading yard where logs are stacked by species, quality, "
            "and seasoning time. No building — just canopies for rain and Tomás "
            "with his grading chalk. Every log gets a mark: A for hull-grade, B "
            "for general, C for firewood. There is no D. If it's worse than C, "
            "it goes back."
        ),
        function="Timber grading, pricing, and sales. Not an auction — prices are set by quality grade. Fair, transparent, no haggling.",
        political_leaning="Conservation-minded. Tomás limits harvests to protect forests. Unpopular with volume buyers.",
        npc_id="sb_tomás",
    ),
    PortInstitution(
        id="sb_brotherhood_hall",
        name="The Brotherhood Hall",
        port_id="silva_bay",
        institution_type="governor",
        description=(
            "A timber longhouse with walls carved with the names of every ship "
            "built in Silva Bay for two hundred years. Seven chairs around a round "
            "table — no head seat, because the Brotherhood governs as equals. A "
            "ship's bell hangs from the ceiling, rung to open and close each session."
        ),
        function="Self-governance by council of seven shipwrights. No external authority. Alliance membership is by choice, not obligation.",
        political_leaning="Fiercely independent. Alliance membership is conditional — cross the Brotherhood's principles and they leave.",
        npc_id="sb_council",
    ),
    PortInstitution(
        id="sb_tavern",
        name="The Dry Dock",
        port_id="silva_bay",
        institution_type="tavern",
        description=(
            "Built from the timbers of a decommissioned brigantine — the bar is "
            "the original helm, and the booths are made from hull sections. Sawdust "
            "on the floor, ship models on every shelf, and the sound of the yard "
            "leaking in through walls that were never meant to be walls. The fish "
            "stew is legendary. The sawdust content is debatable."
        ),
        function="Social hub, crew recruitment, unofficial council annex. Where Silva Bay actually makes decisions.",
        political_leaning="Community heart. Rosa doesn't take sides — but her tavern is where sides are chosen.",
        npc_id="sb_rosa",
    ),
    PortInstitution(
        id="sb_customs",
        name="The Customs Shed",
        port_id="silva_bay",
        institution_type="customs",
        description=(
            "A wooden shed at the edge of the dock — the most modest customs office "
            "in the Mediterranean. A desk, a chair, a stamp, and a young man who "
            "wishes he were somewhere else. The shed leaks when it rains. Nobody "
            "has offered to fix it."
        ),
        function="Minimal cargo inspection. Alliance requirement, not Brotherhood priority. Quick and apologetic.",
        political_leaning="Alliance outsider. Pires represents Porto Novo's rules in a town that makes its own.",
        npc_id="sb_customs_pires",
    ),
    PortInstitution(
        id="sb_broker",
        name="The Broker's Bench",
        port_id="silva_bay",
        institution_type="broker",
        description=(
            "A wooden bench outside the Brotherhood Hall with a canvas awning for "
            "rain. No office — Ana works in the open because Silva Bay doesn't "
            "believe in walls for work that can be done under sky. A corkboard "
            "behind her displays active contracts. A tin cup holds her pencils."
        ),
        function="Contract matching, timber commissions, ship delivery work. Informal, honest, no prestige games. The income funds the Brotherhood.",
        political_leaning="Brotherhood supporter. Ana's contract income keeps the yard independent from Alliance subsidies.",
        npc_id="sb_broker_ana",
    ),
]

SILVA_BAY_PROFILE = PortInstitutionalProfile(
    port_id="silva_bay",
    governor_title="Brotherhood Council",
    power_structure=(
        "Silva Bay is a shipwrights' republic — no single ruler, no hereditary "
        "title. The Brotherhood Council of seven governs by consensus, chaired by "
        "the elected Master Shipwright (Elena). The yard IS the town: Elena builds "
        "the ships, Tomás grades the timber, Nuno runs the harbor, and everything "
        "else exists to support that work. Rosa's tavern is the unofficial second "
        "chamber where real opinions emerge. Ana's broker bench funds it all. "
        "Pires, the Alliance customs officer, is tolerated but never included."
    ),
    internal_tension=(
        "The core tension is independence vs. relevance. The Brotherhood governs "
        "itself and answers to no one — but the Alliance provides trade protection "
        "and market access that Silva Bay needs. Elena wants to stay free; the "
        "Alliance wants Silva Bay's ships. The leverage is mutual, which creates a "
        "fragile equilibrium. Tomás adds a second tension: his harvest limits "
        "protect the forests but frustrate merchants who want more timber faster. "
        "The quiet tension is Pires — an outsider who represents everything the "
        "Brotherhood distrusts (external authority), yet who genuinely tries to "
        "belong. Ana is his only ally, and she's still earning her own place."
    ),
    institutions=_SILVA_BAY_INSTITUTIONS,
    npcs=_SILVA_BAY_NPCS,
)



# =========================================================================
# CORSAIR'S REST — The Silence
# =========================================================================

_CORSAIRS_REST_NPCS = [
    PortNPC(
        id="cr_one_eye",
        name="One-Eye Basso",
        title="Dockmaster",
        port_id="corsairs_rest",
        institution="harbor_master",
        personality="watchful",
        description=(
            "A man who lost his left eye to a boarding hook and replaced it with a "
            "polished black stone. One-Eye doesn't check manifests — he checks the "
            "horizon behind you. His job isn't paperwork; it's making sure you weren't "
            "followed. He stands at the cove's narrow entrance with a spyglass that "
            "never leaves his hand, and if he doesn't wave you in, you don't enter."
        ),
        agenda=(
            "Security. Basso's only concern is the cove's secrecy. He doesn't care "
            "what you carry, who you are, or what you've done — he cares whether a "
            "navy patrol is behind you. Betray the cove's location and Basso will "
            "find you. He always finds them."
        ),
        greeting_neutral="\"...Clear behind you. Come in. Kill your running lights before the bend.\"",
        greeting_friendly="\"Clean approach. Good. Take the inner berth — I'll watch your stern tonight. No charge.\"",
        greeting_hostile="\"You brought heat. I can smell it. Outer anchorage, away from everyone else. And if a patrol appears, you never saw this cove.\"",
        rumor="One-Eye was a navy lookout before he lost the eye — ironic, and nobody laughs about it. Some say he can see further with one eye than most men can with two. Others say the black stone eye sees something else entirely.",
        relationship_notes={
            "cr_whisper": "Trusts completely. Whisper runs the inside; Basso runs the perimeter. They've never had a disagreement that mattered.",
            "cr_mama_lucia": "Protective. He makes sure her kitchen is never raided by navy patrols. She makes sure he eats.",
            "cr_no_one": "Respectful distance. No One runs the Tide's business. Basso runs the cove's safety. Different jurisdictions.",
            "cr_the_physician": "Grateful. The Physician patched his eye socket for free. Basso repays it by ensuring medicine shipments arrive undisturbed.",
            "cr_ghost": "Professional trust. Ghost moves cargo; Basso makes sure nobody sees it arrive.",
            "cr_little_fish": "Watches over her. She's young. The cove isn't kind to the young.",
        },
    ),
    PortNPC(
        id="cr_whisper",
        name="Whisper",
        title="Price Keeper",
        port_id="corsairs_rest",
        institution="exchange",
        personality="secretive",
        description=(
            "Nobody knows Whisper's real name, age, or where they came from. They "
            "appear between the market stalls like smoke, murmur a price, and vanish. "
            "Whisper is the black market's price-setter — the person who knows what "
            "everything is worth when it can't be sold in daylight. They communicate "
            "in hand signals, written notes, and single whispered words."
        ),
        agenda=(
            "The market's survival. Whisper keeps Corsair's Rest functioning by "
            "maintaining fair black market prices. If prices get too high, buyers "
            "go elsewhere. Too low, and sellers stop coming. Whisper finds the line "
            "every day, wordlessly, and the market obeys because Whisper has never "
            "been wrong. Nobody understands how. Nobody asks."
        ),
        greeting_neutral="A folded note appears in your hand. It reads: \"Buying or selling?\" with two prices written below in small, precise handwriting.",
        greeting_friendly="A note: \"Good to see you. Special prices today — for friends.\" A third column of numbers appears, lower than the posted rate.",
        greeting_hostile="No note. No prices. Whisper passes you without stopping. The market stalls seem to close as you approach. Nobody is selling today.",
        rumor="Three different people claim to have seen Whisper's face. They describe three completely different people. Either Whisper changes faces, or there's more than one of them. Both explanations are unsettling.",
        relationship_notes={
            "cr_one_eye": "The only person Whisper communicates with directly. They've worked together longer than anyone at the Rest.",
            "cr_mama_lucia": "Leaves payment for meals under the plate. Always exact. Mama Lucia has never seen Whisper eat.",
            "cr_no_one": "Whisper sets the prices; No One enforces the deals. Neither interferes with the other's work.",
            "cr_the_physician": "Ensures medicine prices stay accessible. Whether this is compassion or economics, nobody knows.",
            "cr_ghost": "Ghost moves the cargo that Whisper prices. A chain with no weak links.",
            "cr_little_fish": "Sends her notes with market intelligence. Teaching her, maybe. Or recruiting.",
        },
    ),
    PortNPC(
        id="cr_no_one",
        name="No One",
        title="The Tide's Voice",
        port_id="corsairs_rest",
        institution="governor",
        personality="cold",
        description=(
            "The Crimson Tide's representative at Corsair's Rest. No One is not a "
            "governor — the Rest has no government. No One is the person who makes "
            "sure the Crimson Tide's interests are respected, tribute is collected, "
            "and disputes are settled before they become violence. Tall, gaunt, "
            "dressed in a faded crimson coat that was once military issue. Speaks "
            "rarely. When No One speaks, the cove goes quiet."
        ),
        agenda=(
            "The Crimson Tide's authority. Corsair's Rest exists because the Tide "
            "protects it. In return, the Tide takes a cut of every transaction, "
            "gets first pick of contraband shipments, and uses the cove as a staging "
            "area. No One ensures this arrangement continues. Captains who forget "
            "that the Rest belongs to the Tide are reminded — once."
        ),
        greeting_neutral="A long look. Then: \"The Tide permits your stay. Trade as you wish. The tribute is ten percent.\"",
        greeting_friendly="\"The Tide remembers its friends. Your tribute is waived this visit. Scarlet Ana sends regards.\"",
        greeting_hostile="\"You owe the Tide. Pay what you owe, or leave the cove. You will not be asked a second time.\"",
        rumor="No One was a garrison officer who deserted — like the Iron Wolves, but earlier. The Wolves hate No One for not joining them. No One hates the Wolves for the same reason they hate everyone: on principle.",
        relationship_notes={
            "cr_one_eye": "Mutual respect. Basso protects the cove; No One protects the Tide's interests. They never conflict because their territories don't overlap.",
            "cr_whisper": "Depends on Whisper for market stability. Doesn't understand them. Doesn't need to.",
            "cr_mama_lucia": "Even No One eats at Mama Lucia's. Even No One pays. Some things are sacred even in a lawless port.",
            "cr_the_physician": "Complicated. The Physician heals everyone — even the Tide's enemies. No One tolerates this because even pirates get sick.",
            "cr_ghost": "Direct reports. Ghost handles the Tide's smuggling logistics. No One handles the politics.",
            "cr_little_fish": "Ignores her. She's beneath the Tide's notice. That's probably the safest place to be.",
        },
    ),
    PortNPC(
        id="cr_mama_lucia",
        name="Mama Lucia",
        title="Cook and Keeper",
        port_id="corsairs_rest",
        institution="tavern",
        personality="fierce",
        description=(
            "A stout woman with iron-grey hair, forearms like ham hocks, and a "
            "ladle she wields like a weapon — because it is one. Mama Lucia runs "
            "the only kitchen at Corsair's Rest: a cave carved into the cliff face "
            "with a smoke hole above and benches below. She feeds everyone. Pirates, "
            "smugglers, fugitives, the lost, the desperate. She feeds them all, and "
            "violence in her kitchen means you never eat again."
        ),
        agenda=(
            "Feeding people and keeping the peace — inside her kitchen, which she "
            "considers the only civilized square meter in Corsair's Rest. Mama Lucia "
            "fled a bad marriage in Porto Novo twenty years ago. The Rest took her in. "
            "She repays it by making sure nobody starves and nobody kills each other "
            "over stew. Her kitchen is neutral ground. Everyone respects this — even "
            "No One, even the Butcher, even captains with blood feuds."
        ),
        greeting_neutral="\"Sit. Eat. Whatever you are, you're hungry — I can see it. We'll talk about what you need after your belly's full.\"",
        greeting_friendly="\"My favorite captain! I saved you the good fish — not the stuff I serve the pirates. Sit, sit. Tell Mama what happened.\"",
        greeting_hostile="\"You can eat. EVERYONE can eat. But you keep your trouble outside my kitchen, understand? My ladle has settled bigger disputes than yours.\"",
        rumor="Mama Lucia's fish stew cured a plague that swept through the cove six years ago. Nobody knows the recipe. She says the secret ingredient is 'minding your own business.' The Physician suspects it's actually turmeric.",
        relationship_notes={
            "cr_one_eye": "He protects the cove; she feeds it. They're the two pillars the Rest stands on. They don't say this. They don't need to.",
            "cr_whisper": "Has never seen Whisper eat, but the payment is always under the plate. She saves a bowl anyway. Someone has to worry.",
            "cr_no_one": "Even the Tide's enforcer respects her kitchen. No One pays. No One sits quietly. No One eats everything on the plate.",
            "cr_the_physician": "Friends. The two people at the Rest who care about keeping others alive. They share ingredients and worries.",
            "cr_ghost": "Feeds his crew when they come in cold and wet from midnight runs. Doesn't ask where they've been.",
            "cr_little_fish": "Took her in when she arrived with nothing. Gave her the dish-washing job. Watches over her like a hawk. Will hurt anyone who hurts her.",
        },
    ),
    PortNPC(
        id="cr_the_physician",
        name="The Physician",
        title="Doctor",
        port_id="corsairs_rest",
        institution="apothecary",
        personality="weary",
        description=(
            "A former navy surgeon who saw too much and drank too much and washed "
            "up at Corsair's Rest with nothing but a medical bag and steady hands. "
            "The Physician (no one uses a name, and the title is as close to respect "
            "as the Rest gets) treats everyone — pirate wounds, smuggler fevers, "
            "the injuries nobody talks about. Charges what you can pay. Sometimes "
            "charges nothing."
        ),
        agenda=(
            "Doing what he was trained for, in the only place that would have him. "
            "The Physician doesn't care about sides, factions, or morality. He stitches "
            "wounds. He sets bones. He brews medicine from whatever Mama Lucia's "
            "kitchen doesn't need. He drinks too much at night and wakes with steady "
            "hands at dawn, which is the only miracle anyone at the Rest believes in."
        ),
        greeting_neutral="\"Hurt? Sick? Sit on the table. If you're neither, buy medicine or leave — I'm busy. I'm always busy.\"",
        greeting_friendly="\"Captain. Intact, I see. Good. I worry about the ones I've patched — professional investment. What can I do for you?\"",
        greeting_hostile="\"I treat everyone. That's the oath. Sit down or don't, but if you bleed in here, I'm stitching you whether you want it or not.\"",
        rumor="The Physician was a brilliant navy surgeon — could have run any hospital in the Mediterranean. Then something happened on a ship. He won't say what. The navy won't say either. He drinks to forget it, and every morning his hands are steady anyway.",
        relationship_notes={
            "cr_one_eye": "Patched his eye socket for free. Basso has been silently grateful ever since — the quietest debt in the cove.",
            "cr_whisper": "Whisper ensures medicine stays affordable on the black market. The Physician suspects compassion. He hopes he's right.",
            "cr_no_one": "Treats the Tide's wounded. No One tolerates his neutrality because the alternative is no doctor.",
            "cr_mama_lucia": "His closest friend. They share ingredients, share worries, and share the belief that keeping people alive matters more than taking sides.",
            "cr_ghost": "Patches Ghost's crew after rough runs. Doesn't ask questions. Receives extra medical supplies in return.",
            "cr_little_fish": "Taught her basic wound care. She's a quick study. He hopes she'll leave before the cove takes away the light in her eyes.",
        },
    ),
    PortNPC(
        id="cr_ghost",
        name="Ghost",
        title="Cargo Master",
        port_id="corsairs_rest",
        institution="broker",
        personality="efficient",
        description=(
            "You hear Ghost before you see him — the creak of rope, the thud of "
            "crates being moved in the dark. Ghost runs the Tide's smuggling logistics "
            "at the Rest: what comes in, what goes out, what gets hidden in the cliff "
            "caves when a patrol passes. He's thin, pale, and moves through the cove "
            "like he was born in shadow. His crew can unload a full ship in two hours "
            "by moonlight."
        ),
        agenda=(
            "Moving cargo. Ghost doesn't care about politics or factions — he cares "
            "about logistics. What needs to go where, by when, without being seen. "
            "He's the best smuggling coordinator in the Mediterranean, and he knows it. "
            "Captains who need contraband moved come to Ghost. He quotes a price, a "
            "time, and a route. He has never missed a deadline."
        ),
        greeting_neutral="\"What are you moving? Where does it need to go? When? ...I can do that. Here's the price.\"",
        greeting_friendly="\"Captain. I have a run for you — clean route, good margin, and I've already scouted the patrol schedule. Interested?\"",
        greeting_hostile="\"I don't move cargo for people I can't trust. Find another broker. Or better yet — leave the cove before morning.\"",
        rumor="Ghost once moved a full cargo of opium through a navy blockade using fishing boats, decoy ships, and a route through underwater caves that only he knew existed. The navy still doesn't know how it happened.",
        relationship_notes={
            "cr_one_eye": "Basso watches the entrance; Ghost watches the cargo. Two halves of the same operation.",
            "cr_whisper": "Whisper prices it; Ghost moves it. The most efficient supply chain in the underworld.",
            "cr_no_one": "Direct superior in the Tide hierarchy. Ghost reports to No One on logistics. Professional, clean, no friction.",
            "cr_mama_lucia": "His crews eat at Mama's after midnight runs. She doesn't ask. He doesn't tell. The stew is always hot.",
            "cr_the_physician": "Sends medical supplies as payment for patching his crew. The Physician never asks where the supplies come from.",
            "cr_little_fish": "Using her as a runner. She's fast, small, and invisible — perfect for messages. Whether this is exploitation or mentorship depends on who you ask.",
        },
    ),
    PortNPC(
        id="cr_little_fish",
        name="Little Fish",
        title="Runner",
        port_id="corsairs_rest",
        institution="customs",
        personality="sharp",
        description=(
            "A girl of maybe fourteen — nobody knows exactly, including her. "
            "She arrived at the Rest on a cargo ship two years ago, hidden in a "
            "barrel. Mama Lucia took her in. Now she runs messages, watches the "
            "cliff paths for approaching ships, and knows every crack and tunnel "
            "in the cove. The Rest's unofficial lookout and messenger — the 'customs "
            "officer' in a port that has no customs."
        ),
        agenda=(
            "Survival and belonging. Little Fish has no family, no past she'll "
            "discuss, and no plan beyond tomorrow. She's sharp, fast, and learning "
            "the cove's ways with the intensity of someone who knows that usefulness "
            "is the only protection she has. Ghost uses her as a runner. Whisper "
            "sends her notes. The Physician teaches her wound care. She's absorbing "
            "everything, and someday the cove will realize she's the most dangerous "
            "person in it."
        ),
        greeting_neutral="She appears beside you without a sound. \"Message for you. Or from you. Which?\" She holds out her hand — for a coin or a note, either works.",
        greeting_friendly="She drops from a rock ledge and lands silently. \"Captain! I saw you coming around the point. Mama says your table is ready. Also, Whisper left you something.\"",
        greeting_hostile="You don't see her. But you have the distinct feeling you're being watched from the cliff above. A pebble clatters down near your feet. A warning, maybe.",
        rumor="Little Fish can navigate the cliff tunnels in complete darkness. She claims to have found a tunnel that leads to a second harbor — the one the old pirates talk about. She won't say whether she's telling the truth. She's learning from the best.",
        relationship_notes={
            "cr_one_eye": "He watches over her. She doesn't know he's the reason the rough sailors leave her alone. She thinks she handles it herself.",
            "cr_whisper": "Receives notes from Whisper with market intelligence. Whether Whisper is teaching her or recruiting her is the cove's favorite debate.",
            "cr_no_one": "Invisible to the Tide's notice. That's the safest place to be, and Little Fish is smart enough to stay there.",
            "cr_mama_lucia": "The closest thing to a mother she has. Mama gave her a job, a bed, and a reason to stay. Little Fish would fight anyone who threatened Mama's kitchen.",
            "cr_the_physician": "Teaching her wound care. She's a quick study. He hopes she'll use the skills somewhere better than the cove.",
            "cr_ghost": "Her employer for running jobs. Ghost pays fairly and doesn't put her in danger — usually. She's learning logistics from the best, which is either a gift or a curse.",
        },
    ),
]

_CORSAIRS_REST_INSTITUTIONS = [
    PortInstitution(
        id="cr_entrance",
        name="The Cove Mouth",
        port_id="corsairs_rest",
        institution_type="harbor_master",
        description=(
            "Not an office — a rock ledge at the narrow entrance to the cove "
            "where One-Eye Basso stands with his spyglass. A signal lantern hangs "
            "from a hook: green for enter, dark for stay away. No dock, no paperwork, "
            "no ceremony. Just one man deciding whether you get in."
        ),
        function="Access control. Not manifest review — threat assessment. Basso decides who enters. His spyglass is the only checkpoint.",
        political_leaning="Brotherhood of the Cove. The cove's security is its own politics.",
        npc_id="cr_one_eye",
    ),
    PortInstitution(
        id="cr_market",
        name="The Whisper Market",
        port_id="corsairs_rest",
        institution_type="exchange",
        description=(
            "Not a building — a series of canvas-covered stalls in the cliff shadow "
            "where goods change hands without receipts. Prices are written in chalk "
            "on slate boards that can be wiped clean in seconds if a patrol appears. "
            "The market has no opening hours. It's always open and never officially there."
        ),
        function="Black market pricing and contraband trade. No receipts, no records, no evidence. Prices set by Whisper.",
        political_leaning="Outside all systems. The Whisper Market acknowledges no authority except supply and demand.",
        npc_id="cr_whisper",
    ),
    PortInstitution(
        id="cr_tide_seat",
        name="The Crimson Chair",
        port_id="corsairs_rest",
        institution_type="governor",
        description=(
            "A carved stone chair at the back of the deepest cave — the Crimson Tide's "
            "seat of authority at the Rest. Nobody sits in it except when No One holds "
            "court. The rest of the time it's empty, which is its own kind of threat. "
            "A faded crimson banner hangs behind it, salt-stained and torn."
        ),
        function="Crimson Tide authority. Tribute collection, dispute resolution, faction governance. Not a government — a protection arrangement.",
        political_leaning="Crimson Tide. The Rest exists because the Tide permits it. The Chair is the proof.",
        npc_id="cr_no_one",
    ),
    PortInstitution(
        id="cr_kitchen",
        name="Mama Lucia's Kitchen",
        port_id="corsairs_rest",
        institution_type="tavern",
        description=(
            "A cave carved into the cliff face with a smoke hole above and timber "
            "benches below. A fire pit, three iron pots, and the smell of fish stew "
            "that seeps into the rock itself. It's always too hot, always crowded, "
            "and the only place in Corsair's Rest where violence is absolutely "
            "forbidden. Mama's ladle enforces the peace."
        ),
        function="Neutral ground. Food, crew recruitment, information exchange. The only safe space in the cove. Violence here means you never eat again.",
        political_leaning="Aggressively neutral. Mama feeds everyone. EVERYONE. Politics stops at her threshold.",
        npc_id="cr_mama_lucia",
    ),
    PortInstitution(
        id="cr_surgery",
        name="The Surgery",
        port_id="corsairs_rest",
        institution_type="apothecary",
        description=(
            "A cave with better lighting than most — the Physician rigged a system "
            "of mirrors to reflect sunlight inside during the day. A wooden table "
            "stained with things nobody asks about, shelves of salvaged medical "
            "supplies, and a bottle of rum that serves double duty as antiseptic "
            "and anesthetic."
        ),
        function="Medical care, medicine trading. Treats everyone regardless of faction or crime. Charges what you can pay.",
        political_leaning="Neutral by oath. The Physician's loyalty is to the practice of medicine, not to any flag.",
        npc_id="cr_the_physician",
    ),
    PortInstitution(
        id="cr_caves",
        name="The Cliff Caves",
        port_id="corsairs_rest",
        institution_type="broker",
        description=(
            "A network of sea caves accessible only by rope or at low tide. Ghost's "
            "crews use them to store, move, and hide cargo. Some caves are mapped; "
            "others aren't. Somewhere in the network is the 'second harbor' that the "
            "old pirates whisper about — or don't."
        ),
        function="Smuggling logistics, contraband storage, contract coordination. Ghost matches cargo to routes and captains to runs.",
        political_leaning="Crimson Tide operations. Ghost works for the Tide. The caves are the Tide's infrastructure.",
        npc_id="cr_ghost",
    ),
    PortInstitution(
        id="cr_cliffs",
        name="The Cliff Watch",
        port_id="corsairs_rest",
        institution_type="customs",
        description=(
            "The cliff paths above the cove where Little Fish watches for approaching "
            "ships, carries messages, and knows every tunnel and crack. Not a customs "
            "house — the inverse: a lookout system designed to ensure customs never "
            "arrives. The paths are invisible from the sea."
        ),
        function="Counter-customs. Patrol detection, message running, early warning. The cove's immune system against official interference.",
        political_leaning="Survival. The Cliff Watch exists to keep the Rest hidden. That's everyone's politics here.",
        npc_id="cr_little_fish",
    ),
]

CORSAIRS_REST_PROFILE = PortInstitutionalProfile(
    port_id="corsairs_rest",
    governor_title="The Tide's Voice",
    power_structure=(
        "Corsair's Rest has no government — it has an arrangement. The Crimson Tide "
        "protects the cove through No One's authority, collecting tribute and settling "
        "disputes. One-Eye Basso controls physical access — if he doesn't wave you in, "
        "you don't enter. Whisper sets prices in the shadow market. Ghost moves the "
        "cargo. Mama Lucia feeds everyone and enforces the only law that holds: no "
        "violence in her kitchen. The Physician keeps people alive. Little Fish watches "
        "everything from the cliffs, learning, and growing into something the cove "
        "hasn't figured out yet."
    ),
    internal_tension=(
        "The surface tension is between the Crimson Tide's authority (No One) and "
        "the cove's organic independence (everyone else). The Tide protects the Rest "
        "but takes a cut. If the cut gets too big, the cove dies. If the protection "
        "falters, the navy finds them. It's a balance maintained by mutual need. "
        "The deeper tension is generational: One-Eye, Mama Lucia, and the Physician "
        "are aging. Ghost and Little Fish are the future. Ghost is Tide-loyal — "
        "whatever the Tide becomes, Ghost follows. Little Fish is loyal to Mama and "
        "the cove itself. When the old guard is gone, the question is whether the "
        "cove serves the Tide or the Tide serves the cove. No One watches this "
        "tension carefully and says nothing, which is the most unsettling thing of all."
    ),
    institutions=_CORSAIRS_REST_INSTITUTIONS,
    npcs=_CORSAIRS_REST_NPCS,
)


# ---------------------------------------------------------------------------
# Master registry — will grow as we build each port
# ---------------------------------------------------------------------------

PORT_INSTITUTIONAL_PROFILES: dict[str, PortInstitutionalProfile] = {
    "porto_novo": PORTO_NOVO_PROFILE,
    "al_manar": AL_MANAR_PROFILE,
    "silva_bay": SILVA_BAY_PROFILE,
    "corsairs_rest": CORSAIRS_REST_PROFILE,
}

ALL_NPCS: dict[str, PortNPC] = {npc.id: npc for profile in PORT_INSTITUTIONAL_PROFILES.values() for npc in profile.npcs}

ALL_INSTITUTIONS: dict[str, PortInstitution] = {inst.id: inst for profile in PORT_INSTITUTIONAL_PROFILES.values() for inst in profile.institutions}
