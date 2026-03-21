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


# ---------------------------------------------------------------------------
# Master registry — will grow as we build each port
# ---------------------------------------------------------------------------

PORT_INSTITUTIONAL_PROFILES: dict[str, PortInstitutionalProfile] = {
    "porto_novo": PORTO_NOVO_PROFILE,
    "al_manar": AL_MANAR_PROFILE,
}

ALL_NPCS: dict[str, PortNPC] = {npc.id: npc for profile in PORT_INSTITUTIONAL_PROFILES.values() for npc in profile.npcs}

ALL_INSTITUTIONS: dict[str, PortInstitution] = {inst.id: inst for profile in PORT_INSTITUTIONAL_PROFILES.values() for inst in profile.institutions}
