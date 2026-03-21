"""Port institutions — East Indies + South Seas continuation.

Split from port_institutions.py for maintainability (the main file exceeded
4000 lines). Same dataclasses, same patterns, imported by the main module.

Ports in this file:
  East Indies: Silk Haven, Crosswind Isle, Dragon's Gate, Spice Narrows
  South Seas: Ember Isle, Typhoon Anchorage, Coral Throne
"""

from portlight.content.port_institutions import (
    PortInstitution,
    PortInstitutionalProfile,
    PortNPC,
)


# =========================================================================
# SILK HAVEN — The Loom Quarter
# =========================================================================

_SILK_HAVEN_NPCS = [
    PortNPC(
        id="slh_harbor_jun", name="Harbor Keeper Jun", title="Harbor Keeper",
        port_id="silk_haven", institution="harbor_master", personality="graceful",
        description="A man who manages ships the way a weaver manages threads — each vessel placed precisely. Jun runs Silk Haven's small harbor with an aesthete's eye: berths arranged to look beautiful from the Loom Quarter above.",
        agenda="Elegance. Jun wants Silk Haven's harbor to reflect the silk it exports. Every arriving ship is an opportunity for visual composition.",
        greeting_neutral="\"Welcome to Silk Haven. Your berth is port-side, third position. Please keep your rigging tidy.\"",
        greeting_friendly="\"Captain! Inner quay, first position — where the morning light catches your sails. I've been saving it.\"",
        greeting_hostile="\"Outer anchorage. Your vessel's condition does not meet the harbor's aesthetic standards.\"",
        rumor="Jun once rearranged every ship in harbor because a junk's crimson sails clashed with a brig's blue hull. The captains were baffled. The Loom Quarter artists applauded.",
        relationship_notes={"slh_grand_weaver": "He serves her vision. The harbor is the first thread visitors see.", "slh_lady_sato": "Coordinates with the magistrate. Prefers coordinating with the view.", "slh_master_ink": "Ink's studio overlooks the harbor. Jun arranges ships as compositions for Ink to paint.", "slh_silk_merchant_feng": "Feng needs fast loading. Jun needs beauty. They compromise.", "slh_inspector_yuki": "Yuki inspects inside. Jun inspects outside. Non-overlapping aesthetics.", "slh_broker_chang": "Chang brings captains. Jun presents the harbor."},
    ),
    PortNPC(
        id="slh_grand_weaver", name="Grand Weaver Seo-yeon", title="Guild Matriarch",
        port_id="silk_haven", institution="exchange", personality="proud",
        description="Fingers that have woven silk for fifty years without a single broken thread. Seo-yeon is the Silk Weavers' Guild matriarch — her patterns are family secrets passed down for centuries. She presents bolts folded, never rolled, because rolling insults the weaver's art.",
        agenda="Silk's supremacy. Seo-yeon believes silk is the highest art form. Her rivalry with Chen Bai in Jade Port is personal: he called silk 'decorated thread.' She responded with a tapestry depicting the Kiln Masters' ancestors as monkeys. It still hangs in the Loom Quarter.",
        greeting_neutral="\"You wish to see the silk? Come. Touch nothing until I have unfolded the bolt. The weave speaks first.\"",
        greeting_friendly="\"Captain — I have woven something no living eye has seen. For trusted friends only. Come to the inner loom. Bring clean hands.\"",
        greeting_hostile="\"Standard bolts at posted prices. The master weaves are not for your hands. The silk decides its buyer.\"",
        rumor="Seo-yeon's eldest daughter wove a bolt she declared 'adequate.' In the Guild, 'adequate' from the Grand Weaver is the highest praise. The daughter wept with pride.",
        relationship_notes={"slh_harbor_jun": "He arranges ships to complement the Quarter. She approves.", "slh_lady_sato": "Allies. Sato protects the Guild; Seo-yeon provides the art.", "slh_master_ink": "Fellow artists. They disagree about everything and respect each other deeply because of it.", "slh_silk_merchant_feng": "He sells her silk. She tolerates commerce as a necessary evil.", "slh_inspector_yuki": "Sacred work. Yuki protects the Grand Weaver's mark.", "slh_broker_chang": "The only merchant she doesn't despise. He presents silk as art."},
    ),
    PortNPC(
        id="slh_lady_sato", name="Lady Sato Hana", title="Circle Magistrate",
        port_id="silk_haven", institution="governor", personality="subtle",
        description="Silk robes in patterns so complex they appear to move, and a political mind that weaves with equal intricacy. Lady Sato governs Silk Haven as the Circle's magistrate — less imperious than Jade Port's Mei, more culturally engaged.",
        agenda="The Guild's independence within the Circle. Sato wants Silk Haven to remain artistically sovereign — not subordinate to Jade Port. She supports the rivalry with Chen because decentralization protects independence.",
        greeting_neutral="\"Silk Haven welcomes those who appreciate craft. Our silk speaks for itself — as does our hospitality.\"",
        greeting_friendly="\"Captain — you return with appreciation in your eyes. That is the only currency we value above silver.\"",
        greeting_hostile="\"Your visit is noted. Standard trade is available. The inner Quarter is closed to you today.\"",
        rumor="Lady Sato once wore a robe to a meeting with Jade Port that contained a pattern depicting their porcelain as inferior. Chen pretended not to notice. Everyone else did.",
        relationship_notes={"slh_harbor_jun": "He serves the aesthetic; she serves the politics.", "slh_grand_weaver": "Symbiotic. Sato protects; Seo-yeon creates.", "slh_master_ink": "Commissions his calligraphy for diplomacy.", "slh_silk_merchant_feng": "Monitors his trade to protect the Guild.", "slh_inspector_yuki": "Values her quality enforcement.", "slh_broker_chang": "He operates within her parameters."},
    ),
    PortNPC(
        id="slh_master_ink", name="Master Ink", title="Calligrapher",
        port_id="silk_haven", institution="tavern", personality="eccentric",
        description="Nobody uses his real name. He runs the Brush and Bowl — a calligraphy studio that serves rice wine, where sailors watch him paint while they drink. His calligraphy is the most beautiful in the East. His social skills are the worst.",
        agenda="Perfection of line. Ink doesn't care about trade or politics. He paints trade agreements that Sato sends to other ports — his calligraphy turns contracts into art.",
        greeting_neutral="He doesn't look up. After a long pause: \"...Wine is there. Sit quietly or leave. I'm working.\"",
        greeting_friendly="He looks up. A rare event. \"Ah. You. Sit. I painted something yesterday and your face was in it. I don't know why. Look.\"",
        greeting_hostile="Complete silence. He turns his back. The wine is still available.",
        rumor="Master Ink painted a scroll for Scarlet Ana — the only pirate who sat in his studio. She didn't move for four hours. She paid in pearls. The scroll hangs in Corsair's Rest. It's the most valuable object in the cove.",
        relationship_notes={"slh_harbor_jun": "Jun arranges ships for Ink to paint. Neither has discussed this.", "slh_grand_weaver": "Fellow artists who disagree about everything. The disagreement IS the respect.", "slh_lady_sato": "She commissions his calligraphy. He ignores her politics.", "slh_silk_merchant_feng": "Once asked Ink for a logo. Was stared at for 30 seconds. Never asked again.", "slh_inspector_yuki": "She visits on difficult days. He pours wine. Neither speaks.", "slh_broker_chang": "Invisible to each other. By mutual choice."},
    ),
    PortNPC(
        id="slh_silk_merchant_feng", name="Merchant Feng", title="Silk Factor",
        port_id="silk_haven", institution="shipyard", personality="commercial",
        description="The only person in Silk Haven who thinks about silk in terms of bales and margins. Feng manages silk exports — grading, packaging, shipping. The weavers consider him necessary. He considers himself unappreciated.",
        agenda="Volume. Feng wants more silk sold at higher margins. He respects the Guild's quality but wishes they'd produce faster. Art doesn't scale, which is his permanent frustration.",
        greeting_neutral="\"Silk? Guild-marked, Seo-yeon approved. The finest in the Known World. The price reflects that.\"",
        greeting_friendly="\"Captain! A new collection just cleared the Guild. Three bolts of a pattern not seen in fifty years. I held one for you.\"",
        greeting_hostile="\"Standard export bolts. Posted prices. The collector pieces are not available for your standing.\"",
        rumor="Feng once tried to hire weavers from a rival province to increase production. Seo-yeon found out and threatened to rescind his license. He never tried again. He still mutters about 'scalability.'",
        relationship_notes={"slh_harbor_jun": "They compromise between fast loading and beautiful placement.", "slh_grand_weaver": "She tolerates him. He funds the Guild. Necessary, not warm.", "slh_lady_sato": "She monitors his trade. He complies.", "slh_master_ink": "Once asked for a logo. Was stared at. Never again.", "slh_inspector_yuki": "She checks his lots. He keeps them genuine.", "slh_broker_chang": "Commercial allies. Different markets, shared margins."},
    ),
    PortNPC(
        id="slh_inspector_yuki", name="Inspector Yuki", title="Silk Inspector",
        port_id="silk_haven", institution="customs", personality="meticulous",
        description="Can identify counterfeit silk by touch alone — thread count, weave tension, dye saturation, all through trained fingertips. Protects the Guild's marks from forgery the way Zhao in Jade Port protects the Kiln Masters'.",
        agenda="Authenticity. Every bolt must be genuine. Counterfeit silk insults the weaver. Yuki takes both offenses personally.",
        greeting_neutral="\"All silk exports require authentication. I inspect by touch — it takes longer but misses nothing.\"",
        greeting_friendly="\"Captain — your shipments are always genuine. Quick authentication. You respect the Guild's work.\"",
        greeting_hostile="\"Full authentication. Every bolt, every thread. I've found patterns in your route's shipments that concern me.\"",
        rumor="Yuki and Zhao Min in Jade Port trained under the same master. They now respect each other as the two finest inspectors in the East, and exchange notes by letter on new counterfeiting techniques.",
        relationship_notes={"slh_harbor_jun": "Non-overlapping domains.", "slh_grand_weaver": "Sacred work — protects Seo-yeon's mark.", "slh_lady_sato": "Values her quality enforcement.", "slh_master_ink": "Visits his studio on hard days. Wine. Silence.", "slh_silk_merchant_feng": "Checks his lots. Self-interest aligned with quality.", "slh_broker_chang": "Her seal authenticates his exports."},
    ),
    PortNPC(
        id="slh_broker_chang", name="Broker Chang", title="Silk Broker",
        port_id="silk_haven", institution="broker", personality="refined",
        description="A broker who speaks the language of art to sell the products of commerce. Chang presents silk as acquisition — each bolt with provenance, history, and meaning. He prices by story, not weight.",
        agenda="Premium positioning. A bolt with a thousand-year pattern costs more than one with fifty years, regardless of thread count.",
        greeting_neutral="\"Each bolt has a history — the pattern, the weaver, the tradition. Shall I tell it?\"",
        greeting_friendly="\"Captain! Seo-yeon wove this personally — her hands, her pattern, her mark. This hasn't happened in three years.\"",
        greeting_hostile="\"Standard bolts through Merchant Feng. The curated collection requires a different relationship.\"",
        rumor="Chang sold a single bolt for more silver than most captains earn in a season. The collector didn't ask the price — he asked the story. Chang told it for an hour. The collector paid without negotiating.",
        relationship_notes={"slh_harbor_jun": "Aesthetics aligned.", "slh_grand_weaver": "The only merchant she doesn't despise.", "slh_lady_sato": "He operates within her parameters.", "slh_master_ink": "Invisible to each other. By mutual choice.", "slh_silk_merchant_feng": "Different markets, shared margins.", "slh_inspector_yuki": "Her seal authenticates his premium."},
    ),
]

_SILK_HAVEN_INSTITUTIONS = [
    PortInstitution(id="slh_harbor", name="The Arranged Harbor", port_id="silk_haven", institution_type="harbor_master",
        description="A small harbor where berths are assigned for visual composition. Ships are part of the Loom Quarter's view.",
        function="Aesthetic-first berthing. Function serves form.", political_leaning="Silk Circle, artistically.", npc_id="slh_harbor_jun"),
    PortInstitution(id="slh_loom", name="The Loom Quarter", port_id="silk_haven", institution_type="exchange",
        description="A district where a hundred looms never stop. Silk in thousand-year patterns. Green tea steam and the clack of threads.",
        function="Silk production, Guild marking, pattern guardianship.", political_leaning="Guild sovereignty.", npc_id="slh_grand_weaver"),
    PortInstitution(id="slh_court", name="The Silk Court", port_id="silk_haven", institution_type="governor",
        description="A hall draped in silk — walls, ceiling, cushions. Every surface woven. Sato governs from within the art.",
        function="Political governance, Guild protection, Circle diplomacy.", political_leaning="Artistic independence.", npc_id="slh_lady_sato"),
    PortInstitution(id="slh_brush", name="The Brush and Bowl", port_id="silk_haven", institution_type="tavern",
        description="A calligraphy studio that serves rice wine. Sailors watch Ink paint. Beauty changes how they see the world.",
        function="Social hub through art. Ink's calligraphy turns contracts into art.", political_leaning="Above politics.", npc_id="slh_master_ink"),
    PortInstitution(id="slh_warehouse", name="The Silk Warehouse", port_id="silk_haven", institution_type="shipyard",
        description="Climate-controlled silk storage. Humidity, temperature, light managed. Feng runs it with Guild-demanded precision.",
        function="Export packaging. The practical bridge between loom and ship.", political_leaning="Commercial.", npc_id="slh_silk_merchant_feng"),
    PortInstitution(id="slh_touch", name="The Touch Room", port_id="silk_haven", institution_type="customs",
        description="A silent room where Yuki inspects silk by touch. No instruments — trained fingertips only.",
        function="Silk authentication. Thread count, tension, dye saturation by hand.", political_leaning="Quality enforcement.", npc_id="slh_inspector_yuki"),
    PortInstitution(id="slh_story", name="The Story Room", port_id="silk_haven", institution_type="broker",
        description="A curtained alcove where Chang tells each bolt's story. Buyers don't negotiate. They listen.",
        function="Premium brokering by narrative. Story, not weight.", political_leaning="Artistic commerce.", npc_id="slh_broker_chang"),
]

SILK_HAVEN_PROFILE = PortInstitutionalProfile(
    port_id="silk_haven", governor_title="Circle Magistrate",
    power_structure="Silk Haven is governed by art. Seo-yeon's Guild produces the silk. Sato protects independence from Jade Port. Master Ink creates beauty that transcends commerce. Jun arranges the harbor as poetry. Chang sells meaning. Yuki guards authenticity. Feng moves volume and resents the pace of art.",
    internal_tension="Surface: Silk Haven vs. Jade Port — the monkey tapestry vs. 'decorated thread.' Sato encourages the rivalry because decentralization protects independence. Internal: Feng vs. the Guild on scaling production. Deep thread: Yuki and Zhao (Jade Port) trained under the same master — the inspectors are closer to each other than to their own ports. Master Ink painted a scroll for Scarlet Ana that hangs in Corsair's Rest — art connecting the pirate cove to the silk capital.",
    institutions=_SILK_HAVEN_INSTITUTIONS, npcs=_SILK_HAVEN_NPCS,
)


# =========================================================================
# Export all profiles from this file
# =========================================================================


# =========================================================================
# CROSSWIND ISLE — The Free Port
# =========================================================================

_CROSSWIND_ISLE_NPCS = [
    PortNPC(
        id="ci_captain_council", name="The Captain's Table", title="Governing Council",
        port_id="crosswind_isle", institution="governor", personality="democratic",
        description="Not a person — a rotating council of five captains elected monthly by whoever happens to be in harbor. No permanent government, no bureaucracy, no taxes beyond the docking fee. The only rule: no one rules. A bell is rung when votes are needed. Whoever shows up, votes.",
        agenda="Freedom. The Captain's Table exists to prevent governance, not to provide it. They settle disputes, maintain the dock, and ensure no nation ever claims the isle. That's it.",
        greeting_neutral="\"Crosswind Isle welcomes all flags. Dock where you find space. The only rule: no one claims authority here. Understood?\"",
        greeting_friendly="\"Captain — your voice is welcome at the Table this month. Stay for the vote. Your experience matters.\"",
        greeting_hostile="\"You may dock. You may trade. You may NOT attempt to impose order, recruit for factions, or claim territory. We've thrown out better than you.\"",
        rumor="Someone tried to claim the isle for an eastern dynasty last year. By morning, every captain in harbor had their guns trained on his ship. He left before breakfast. The Table didn't even need to vote.",
        relationship_notes={"ci_dock_master_tao": "Tao keeps the dock working. The Table keeps governance from happening.", "ci_every_merchant": "Every Merchant runs the exchange. The Table lets them.", "ci_neutrality_keeper": "Mother Ko enforces the one rule. The Table backs her.", "ci_money_changer_hassan": "Hassan changes currency. The Table doesn't regulate it.", "ci_inspector_nobody": "No customs. The Table considers this a feature.", "ci_broker_various": "Brokers come and go. The Table doesn't license them."},
    ),
    PortNPC(
        id="ci_dock_master_tao", name="Dock Master Tao", title="Dock Master",
        port_id="crosswind_isle", institution="harbor_master", personality="efficient",
        description="The only permanent employee of Crosswind Isle — Tao has maintained the dock for twelve years through elected councils, trade wars, and one attempted invasion. He assigns berths by first-come-first-served and considers this the purest form of justice.",
        agenda="A working dock. Tao doesn't care about politics, factions, or who's fighting whom. He cares about moorings, tides, and keeping the dock from falling into the sea.",
        greeting_neutral="\"Berth's open. Tie up, stay or go. First come, first served. Nobody gets priority here.\"",
        greeting_friendly="\"Captain! Good to see you again. Berth six — the mooring's been fixed since last time. I remembered your complaint.\"",
        greeting_hostile="\"You can dock. But I'm watching your crew. Last time they left a mess. This time, you clean it or you pay.\"",
        rumor="Tao once repaired the entire dock by himself during a typhoon because nobody else would help. It took four days. The dock held. He doesn't talk about it because he considers dock maintenance self-explanatory.",
        relationship_notes={"ci_captain_council": "The Table comes and goes. Tao stays. That's the arrangement.", "ci_every_merchant": "They share dock space. Professional.", "ci_neutrality_keeper": "Mother Ko maintains order. Tao maintains infrastructure. Both essential.", "ci_money_changer_hassan": "Hassan's table is on Tao's dock. They've been neighbors for a decade.", "ci_inspector_nobody": "Nobody inspects. Tao doesn't mind.", "ci_broker_various": "The brokers need dock access. Tao provides it."},
    ),
    PortNPC(
        id="ci_every_merchant", name="Every Merchant", title="Exchange Keeper",
        port_id="crosswind_isle", institution="exchange", personality="chaotic",
        description="Not a single person — a rotating cast of merchants who set up stalls on the dock every morning and take them down every night. No permanent exchange, no posted prices, no Guild marks. Crosswind Isle's 'exchange' is pure chaos: shouted prices, competing offers, and the only quality control is reputation.",
        agenda="Profit through chaos. The merchants like it this way — no regulation means no fees, no inspectors, and no restrictions. The good merchants thrive on reputation. The bad ones get shouted off the dock.",
        greeting_neutral="\"BUYING! SELLING! Everything at once! Name your price, Captain — someone here has what you need!\"",
        greeting_friendly="\"Captain! Good to see an honest face! Come to my stall — I have what you want before you know you want it!\"",
        greeting_hostile="\"...Your silver's good? Then your history doesn't matter here. That's the point of Crosswind Isle.\"",
        rumor="The merchants once collectively boycotted a captain who sold counterfeit spice. No Guild forced it — the merchants just stopped selling to him. He left within the day. Self-regulation by shame.",
        relationship_notes={"ci_captain_council": "The Table lets them trade. They let the Table pretend to govern.", "ci_dock_master_tao": "Professional. They share dock space.", "ci_neutrality_keeper": "Mother Ko keeps fights from escalating. The merchants appreciate this.", "ci_money_changer_hassan": "Essential — Hassan converts the dozen currencies that flow through.", "ci_inspector_nobody": "No inspection is the merchants' favorite policy.", "ci_broker_various": "The brokers formalize what the merchants shout. Different styles, same trades."},
    ),
    PortNPC(
        id="ci_neutrality_keeper", name="Mother Ko", title="Keeper of the Peace",
        port_id="crosswind_isle", institution="tavern", personality="iron",
        description="A massive woman who runs the Bell and Board — Crosswind Isle's only permanent tavern — and who enforces the isle's one rule with a voice that can stop a brawl at forty paces. Mother Ko doesn't care about your faction, your flag, or your grudge. Inside her tavern and within the isle's boundaries, you are NEUTRAL or you are GONE.",
        agenda="The rule. No one claims authority. No one fights about politics. No one recruits for factions on the isle. Mother Ko is the immune system — she identifies threats to neutrality and eliminates them with a word, a look, or if necessary, a thrown stool.",
        greeting_neutral="\"Welcome to the Bell and Board. All flags fly. All tongues speak. One rule: neutrality or the door. Drink?\"",
        greeting_friendly="\"Captain! Your table's empty — that means it's been too long. Sit. Drink. Tell me who's trying to ruin the world today.\"",
        greeting_hostile="\"You're welcome to drink. You're NOT welcome to start trouble. I've thrown out admirals and pirate kings. Don't test me.\"",
        rumor="Mother Ko once threw a Silk Circle official and an Iron Pact officer out of her tavern simultaneously — one through each door — because they were arguing about trade policy at the bar. She said, 'Take your politics to the sea. The isle doesn't serve it.' Neither came back. Both sent flowers.",
        relationship_notes={"ci_captain_council": "The Table enforces the rule politically. Mother Ko enforces it physically.", "ci_dock_master_tao": "Mutual respect. Two permanent fixtures on a transient isle.", "ci_every_merchant": "She stops fights from spilling into the market.", "ci_money_changer_hassan": "Hassan drinks quietly. She appreciates quiet drinkers.", "ci_inspector_nobody": "No customs means no arguments about customs. Mother Ko approves.", "ci_broker_various": "Brokers keep their voices down in her tavern. This is wisdom."},
    ),
    PortNPC(
        id="ci_money_changer_hassan", name="Hassan al-Farsi", title="Money Changer",
        port_id="crosswind_isle", institution="customs", personality="precise",
        description="Crosswind Isle has no customs — but it does have Hassan, who sits at a small table with scales, abacus, and stacks of every currency in the Known World. He converts Mediterranean silver to Eastern brass to Gold Coast cowries without blinking. He IS the customs system: not inspecting cargo but lubricating the twelve currencies that flow through.",
        agenda="Fair rates. Hassan's exchange rates are the most trusted in the East because he's survived fifteen years at Crosswind Isle by never cheating anyone. His table is the only institution on the isle that everyone — pirates, merchants, officials — trusts absolutely.",
        greeting_neutral="\"What currency are you carrying? I exchange all at fair rates. Posted on the board. No negotiation — the rate is the rate.\"",
        greeting_friendly="\"Captain! I've been tracking exchange rates for your route — you'll want to convert now. The eastern brass is strong this week.\"",
        greeting_hostile="\"I exchange currency for all. My rates don't change based on who you are. That's why I'm still alive after fifteen years.\"",
        rumor="Hassan keeps a personal ledger of every transaction he's ever made — fifteen years, twelve currencies, hundreds of thousands of exchanges. He says the ledger tells the story of the Known World's economy better than any market report. Nobody has seen it except him.",
        relationship_notes={"ci_captain_council": "They don't regulate him. He doesn't need regulation.", "ci_dock_master_tao": "Neighbors for a decade. Tao fixed Hassan's table once. Hassan never forgot.", "ci_every_merchant": "Essential — converts the dozen currencies flowing through.", "ci_neutrality_keeper": "Drinks quietly at Mother Ko's. She appreciates quiet.", "ci_inspector_nobody": "No inspection. Hassan's precision IS the quality control.", "ci_broker_various": "Brokers use his rates. He uses their volume. Symbiotic."},
    ),
    PortNPC(
        id="ci_inspector_nobody", name="(Nobody)", title="(No Customs)",
        port_id="crosswind_isle", institution="apothecary", personality="absent",
        description="Crosswind Isle has no customs inspector. This is deliberate. The absence is the policy. Where other ports have an inspector, Crosswind Isle has an empty chair with a sign: 'THIS SEAT INTENTIONALLY LEFT VACANT.' It's the isle's most photographed landmark.",
        agenda="None. The empty chair's agenda is being empty. This is, arguably, the most powerful statement any institution has ever made.",
        greeting_neutral="The chair is empty. A seagull sits on it. The seagull does not check your manifest.",
        greeting_friendly="The chair is empty. The sign has been polished recently. Someone cares.",
        greeting_hostile="The chair is still empty. Whatever you're carrying, nobody is checking it. That's the point.",
        rumor="Three different alliances have offered to station an inspector at Crosswind Isle. Each time, the Captain's Table voted unanimously to decline. The chair remains empty. The seagull remains.",
        relationship_notes={"ci_captain_council": "The Table voted for this vacancy. Three times.", "ci_dock_master_tao": "Tao built the chair. He's proud of it.", "ci_every_merchant": "The merchants' favorite institution is the one that doesn't exist.", "ci_neutrality_keeper": "Mother Ko considers the empty chair her best ally.", "ci_money_changer_hassan": "Hassan's precision is the only quality control needed.", "ci_broker_various": "No inspection means no delays. Brokers approve."},
    ),
    PortNPC(
        id="ci_broker_various", name="The Dock Brokers", title="Freelance Brokers",
        port_id="crosswind_isle", institution="broker", personality="competitive",
        description="Not one broker — a dozen freelancers who compete for contracts on the dock every morning. No licensing, no territory, no regulation. The best broker wins. Today it might be a Silk Circle agent; tomorrow a Gold Coast trader; next week a retired pirate. Crosswind Isle doesn't curate its brokers. It lets them fight.",
        agenda="Each broker has their own agenda. Collectively, they ensure that every cargo finds a buyer and every buyer finds a cargo — pure market efficiency through unregulated competition.",
        greeting_neutral="\"Captain! I have — \" \"No, THIS captain, MY contract is better — \" \"Ignore them both, I know the REAL prices — \" The dock brokers compete for your attention.",
        greeting_friendly="\"Captain! I saved this one for you — don't tell the others. Quick, before they notice.\"",
        greeting_hostile="\"...Even here, reputation matters. The best contracts go to the captains the brokers trust. You'll need to earn that.\"",
        rumor="The dock brokers once held an informal competition: who could broker the most contracts in a single day. The winner brokered seventeen. The runner-up brokered fifteen but argues that three of the winner's were technically the same contract repackaged. The debate continues.",
        relationship_notes={"ci_captain_council": "The Table doesn't license them. They prefer it that way.", "ci_dock_master_tao": "They need dock access. Tao provides it.", "ci_every_merchant": "The merchants shout; the brokers formalize. Different styles.", "ci_neutrality_keeper": "Mother Ko keeps broker arguments from becoming broker fights.", "ci_money_changer_hassan": "Brokers use Hassan's rates. Essential.", "ci_inspector_nobody": "No inspection means no delays. Brokers approve."},
    ),
]

_CROSSWIND_ISLE_INSTITUTIONS = [
    PortInstitution(id="ci_dock", name="The Free Dock", port_id="crosswind_isle", institution_type="harbor_master",
        description="First-come-first-served. No priority, no hierarchy. Tao maintains it. The democracy starts at the mooring.", function="Pure first-come berthing. Nobody gets priority.", political_leaning="Aggressively neutral.", npc_id="ci_dock_master_tao"),
    PortInstitution(id="ci_market", name="The Open Market", port_id="crosswind_isle", institution_type="exchange",
        description="Stalls set up every morning, taken down every night. Shouted prices, competing offers. Pure market chaos.", function="Unregulated exchange. Quality control by reputation only.", political_leaning="Anti-regulation.", npc_id="ci_every_merchant"),
    PortInstitution(id="ci_table", name="The Captain's Table", port_id="crosswind_isle", institution_type="governor",
        description="A round table at the dock where elected captains vote. No building. The government is a piece of furniture.", function="Preventing governance. Settling disputes. Maintaining the dock. That's all.", political_leaning="Anti-authority.", npc_id="ci_captain_council"),
    PortInstitution(id="ci_bell", name="The Bell and Board", port_id="crosswind_isle", institution_type="tavern",
        description="The only permanent building on the isle. Mother Ko's domain. The bell rings for votes and for last call.", function="Neutral ground enforced by Mother Ko. All flags, all tongues, one rule.", political_leaning="Neutrality as religion.", npc_id="ci_neutrality_keeper"),
    PortInstitution(id="ci_empty_chair", name="The Empty Chair", port_id="crosswind_isle", institution_type="apothecary",
        description="An empty chair with a sign: 'THIS SEAT INTENTIONALLY LEFT VACANT.' Where other ports have customs. The most powerful non-institution in the Known World.", function="Nothing. Deliberately. The absence IS the policy.", political_leaning="The absence of politics.", npc_id="ci_inspector_nobody"),
    PortInstitution(id="ci_exchange_table", name="Hassan's Table", port_id="crosswind_isle", institution_type="customs",
        description="A small table with scales, abacus, and every currency. Hassan converts twelve currencies without blinking. The only 'customs' Crosswind Isle needs.", function="Currency exchange. Fair rates, no negotiation. The rate is the rate.", political_leaning="Neutral by profession.", npc_id="ci_money_changer_hassan"),
    PortInstitution(id="ci_brokers", name="The Dock Scrum", port_id="crosswind_isle", institution_type="broker",
        description="A dozen freelance brokers competing on the dock every morning. No licensing, no territory. The best wins.", function="Unregulated brokering. Pure competition. Every cargo finds a buyer.", political_leaning="Market anarchy.", npc_id="ci_broker_various"),
]

CROSSWIND_ISLE_PROFILE = PortInstitutionalProfile(
    port_id="crosswind_isle", governor_title="Captain's Table",
    power_structure="Crosswind Isle has no permanent government — the Captain's Table rotates monthly. Tao maintains the dock. Mother Ko enforces neutrality. Hassan changes money. The merchants shout. The brokers compete. The customs chair is empty. It's the closest thing to anarchy that actually works.",
    internal_tension="The tension IS the system. Crosswind Isle works because everyone agrees on one thing: no one rules. The moment someone tries, the system activates — Mother Ko throws them out, the Table votes them down, and every captain in harbor trains their guns. The real vulnerability: what happens when the trade blocs get desperate enough to claim the isle by force? The Table has no navy. Mother Ko has a stool.",
    institutions=_CROSSWIND_ISLE_INSTITUTIONS, npcs=_CROSSWIND_ISLE_NPCS,
)


# =========================================================================
# DRAGON'S GATE — The Fortress Strait
# =========================================================================

_DRAGONS_GATE_NPCS = [
    PortNPC(
        id="dg_commander_zhang", name="Commander Zhang Wei", title="Gate Commander",
        port_id="dragons_gate", institution="governor", personality="absolute",
        description="A man whose authority is measured in chains — the harbor chains that can close the eastern strait in under a minute. Commander Zhang governs Dragon's Gate as both military commander and civil authority. His word is law, his chains are persuasion, and his fifteen-year record of zero unauthorized passages speaks for itself.",
        agenda="Control. Zhang controls the strait. Ships pass when he permits. Weapons do not pass — ever. His fortress exists to prevent armed escalation in the East Indies, and he considers every weapon that enters the strait a personal failure.",
        greeting_neutral="\"State your cargo. All weapons must be declared. Failure to declare is treated as hostile intent. These are the terms of passage.\"",
        greeting_friendly="\"Captain — your record is clean. Passage is granted. But I will still inspect the weapons hold. Protocol serves everyone.\"",
        greeting_hostile="\"Full inspection. Full chain deployment. Your ship will not leave this harbor until I am satisfied that no weapons pass through my strait.\"",
        rumor="The last captain who tried to run Zhang's chains is still chained to the seabed as a warning. Zhang considers this proportionate. The strait has been quiet ever since.",
        relationship_notes={"dg_harbor_captain_li": "His harbor officer. Runs the dock under Zhang's absolute authority.", "dg_tea_merchant_liu": "The tea trade funds the fortress. Zhang tolerates commerce because he must.", "dg_weapons_inspector_sun": "His most trusted officer. Sun finds the weapons Zhang can't allow.", "dg_healer_chen_ling": "The fortress healer. Zhang respects medicine — soldiers need it.", "dg_inn_keeper_wu": "Wu's inn is where soldiers decompress. Zhang allows it because the alternative is desertion.", "dg_broker_ming": "Ming brokers what Zhang permits. The boundary is absolute."},
    ),
    PortNPC(
        id="dg_harbor_captain_li", name="Harbor Captain Li Jun", title="Harbor Captain",
        port_id="dragons_gate", institution="harbor_master", personality="precise",
        description="A military officer who runs the harbor like a military operation — because it is one. Li Jun coordinates inspections, manages the chain deployment mechanism, and ensures that no ship docks, departs, or moves within the strait without Zhang's approval.",
        agenda="The chain. Li Jun's job is ensuring the chains work — that they can close the strait in under sixty seconds. Everything else is secondary to this capability.",
        greeting_neutral="\"Berth assignment pending inspection. Anchor in the holding area. Inspector Sun will board within the hour.\"",
        greeting_friendly="\"Captain — clean record, priority passage. Inspector Sun will do an abbreviated check. You'll be through within two hours.\"",
        greeting_hostile="\"Holding area. Indefinite. Commander Zhang has flagged your vessel. Cooperation will determine how long this takes.\"",
        rumor="Li Jun can deploy the harbor chains from memory — he's memorized every winch, every link, every anchor point. In a drill last year, he closed the strait in forty-three seconds. Zhang said 'acceptable.' Li Jun is trying for thirty-five.",
        relationship_notes={"dg_commander_zhang": "His commander. Absolute loyalty.", "dg_tea_merchant_liu": "Tea ships get efficient processing. The fortress needs revenue.", "dg_weapons_inspector_sun": "Sun inspects; Li Jun manages the dock flow around inspections.", "dg_healer_chen_ling": "No strong connection. Different jurisdictions.", "dg_inn_keeper_wu": "Li Jun drinks there. Quietly. Officers' corner.", "dg_broker_ming": "Ming's contracts must be approved by Li Jun before loading begins."},
    ),
    PortNPC(
        id="dg_tea_merchant_liu", name="Tea Merchant Liu", title="Tea Factor",
        port_id="dragons_gate", institution="exchange", personality="patient",
        description="A woman who has learned to trade tea within the framework of a military fortress — which means patience, paperwork, and the understanding that Commander Zhang's approval is required for everything, including breathing. Liu manages Dragon's Gate's tea trade, which is the fortress's economic lifeline.",
        agenda="Tea. Liu wants to export the finest tea in the East Indies — and Dragon's Gate's volcanic soil produces extraordinary leaves. She's patient because she has to be, and shrewd because patience alone doesn't pay the fortress's bills.",
        greeting_neutral="\"Tea? Dragon's Gate produces the finest in the East. I have varieties you won't find elsewhere. The inspection will take time — shall I brew a sample while you wait?\"",
        greeting_friendly="\"Captain! I've been aging a special batch — eighteen months in volcanic clay jars. The flavor is... remarkable. Worth waiting for the inspection.\"",
        greeting_hostile="\"Standard tea at posted prices. The premium lots require Commander Zhang's approval. Which requires your record to improve.\"",
        rumor="Liu's volcanic-aged tea was served at a Silk Circle diplomatic banquet. The Circle's magistrates called it the finest they'd ever tasted. Liu didn't mention she ages it in old weapons crates — the iron residue gives it a mineral finish Zhang would definitely not approve of.",
        relationship_notes={"dg_commander_zhang": "The tea funds the fortress. He tolerates her commerce.", "dg_harbor_captain_li": "Tea ships get efficient processing.", "dg_weapons_inspector_sun": "Sun once accidentally detained a tea shipment for three days. Liu hasn't forgiven him.", "dg_healer_chen_ling": "They exchange ingredients. Tea and medicine share more than people think.", "dg_inn_keeper_wu": "Wu serves Liu's tea. The soldiers drink it. The cycle funds everything.", "dg_broker_ming": "Ming brokers Liu's export contracts. A necessary partnership."},
    ),
    PortNPC(
        id="dg_weapons_inspector_sun", name="Inspector Sun", title="Weapons Inspector",
        port_id="dragons_gate", institution="customs", personality="relentless",
        description="The man who finds weapons. Inspector Sun has a reputation that extends across the entire East Indies — if you're smuggling weapons through the Gate, Sun will find them. He's found weapons hidden in grain barrels, sewn into sail canvas, disguised as ship's hardware, and once, memorably, dissolved in acid and stored as liquid iron. He found that too.",
        agenda="Zero tolerance. Sun doesn't inspect for tariffs or quality. He inspects for weapons. Every blade, every barrel, every ingot of iron that could be reforged. His fifteen-year record of zero unauthorized passages is Commander Zhang's greatest pride and Sun's only motivation.",
        greeting_neutral="\"Weapons declaration. Full manifest. I will inspect the hold personally. Cooperation determines speed.\"",
        greeting_friendly="\"Captain — your record is clean. Abbreviated inspection. But I will still check the forward hold. Protocol respects no friendship.\"",
        greeting_hostile="\"Full strip inspection. Every hold, every compartment, every barrel. I've found weapons in places you can't imagine. Don't test me.\"",
        rumor="Sun found weapons dissolved in acid and stored as liquid iron. The smuggler was a chemist. Sun is not a chemist — but he noticed the acid smell was wrong for the declared cargo of vinegar. He tested one drop. The smuggler is in chains. Sun considers this a normal Tuesday.",
        relationship_notes={"dg_commander_zhang": "His commander and the man whose record he protects with every inspection.", "dg_harbor_captain_li": "They coordinate: Sun inspects, Li Jun manages the queue.", "dg_tea_merchant_liu": "He once detained her tea for three days. She hasn't forgiven him. He doesn't care.", "dg_healer_chen_ling": "Medicine shipments pass quickly — Sun has no quarrel with healing.", "dg_inn_keeper_wu": "Sun doesn't drink. He watches the inn for weapons deals. Wu knows. It keeps both honest.", "dg_broker_ming": "Every contract Ming brokers must pass Sun's review. No exceptions."},
    ),
    PortNPC(
        id="dg_healer_chen_ling", name="Healer Chen Ling", title="Fortress Healer",
        port_id="dragons_gate", institution="apothecary", personality="dedicated",
        description="A woman whose gentle hands have tended fortress soldiers and civilian sailors alike for twenty years. Chen Ling runs Dragon's Gate's infirmary — a small but well-equipped facility that serves as the eastern strait's only reliable medical care. She buys medicines desperately — Dragon's Gate's remoteness makes supplies scarce.",
        agenda="Medicine for the fortress. Chen Ling needs medicines more than any other port in the East Indies. She'll pay above market for anything — herbs, compounds, surgical supplies. Her infirmary keeps the garrison functional and visiting captains alive.",
        greeting_neutral="\"Are you carrying medicines? I will pay premium — Dragon's Gate is always in need. And if you need healing yourself, my infirmary is open to all.\"",
        greeting_friendly="\"Captain! You brought medicines! You may have saved lives today — I mean that literally. Come, let me show you what I need most.\"",
        greeting_hostile="\"I heal all who ask. My oath outranks the Commander's displeasure. If you're wounded or sick, come to the infirmary. Politics stops at my door.\"",
        rumor="Chen Ling once treated an Iron Wolf sailor who washed up near the fortress. Zhang ordered her to interrogate the prisoner. She treated him and refused to interrogate. Zhang backed down. The Wolves returned the favor by not raiding the strait for six months.",
        relationship_notes={"dg_commander_zhang": "Respects her dedication. Knows better than to override her medical judgment.", "dg_harbor_captain_li": "No strong connection.", "dg_tea_merchant_liu": "They exchange ingredients — tea and medicine share secrets.", "dg_weapons_inspector_sun": "Medicine passes quickly. Sun has no quarrel with healing.", "dg_inn_keeper_wu": "Sends her the soldiers who've drunk too much. A familiar cycle.", "dg_broker_ming": "Ming sources rare medicines through his contracts. Chen Ling is grateful."},
    ),
    PortNPC(
        id="dg_inn_keeper_wu", name="Inn Keeper Wu", title="Inn Keeper",
        port_id="dragons_gate", institution="tavern", personality="discreet",
        description="A quiet man who runs the Gate's only inn — a stone building inside the fortress walls where soldiers, sailors, and merchants drink jasmine tea and, after dark, something stronger. Wu has mastered the art of being invisible: he sees everything, hears everything, and says nothing. The fortress runs on his discretion.",
        agenda="A functioning inn within a military fortress. Wu provides the social lubrication that keeps the garrison from cracking under Zhang's rigid discipline. He also provides information — to Zhang, to Liu, to anyone who asks the right question in the right way.",
        greeting_neutral="\"Tea? Or the evening menu? Rooms are available — the fortress isn't comfortable, but it's safe. Isn't that enough?\"",
        greeting_friendly="\"Captain — your usual room. I've prepared the jasmine blend you liked. Also... I may have heard something about the inspection schedule. If you're interested.\"",
        greeting_hostile="\"Tea is available. Rooms are available. Information is not. Not today.\"",
        rumor="Wu was a Monsoon Syndicate informant before he came to Dragon's Gate. Or he still is. Nobody knows for certain, including Zhang. The Commander keeps him because a known intelligence risk is more useful than an unknown one.",
        relationship_notes={"dg_commander_zhang": "Zhang knows Wu has connections. Wu knows Zhang knows. The equilibrium works.", "dg_harbor_captain_li": "Officers' corner. Li Jun drinks quietly.", "dg_tea_merchant_liu": "Wu serves her tea. Soldiers drink it. Revenue cycle.", "dg_weapons_inspector_sun": "Sun watches the inn for deals. Wu keeps it honest — mostly.", "dg_healer_chen_ling": "Sends her the drunk soldiers.", "dg_broker_ming": "Ming negotiates deals at Wu's tables. Wu overhears. Sometimes helpfully."},
    ),
    PortNPC(
        id="dg_broker_ming", name="Broker Ming", title="Gate Broker",
        port_id="dragons_gate", institution="broker", personality="cautious",
        description="The most restricted broker in the East Indies — Ming can only broker what Zhang permits, which excludes weapons, explosives, and anything Inspector Sun considers suspicious. Within those boundaries, Ming is excellent: tea contracts, porcelain orders, medicine sourcing. He's learned to thrive in a cage.",
        agenda="Maximum commerce within minimum permissions. Ming wants Dragon's Gate to be a trade port, not just a military chokepoint. He dreams of the day Zhang loosens the restrictions. That day has never come in nine years. Ming keeps dreaming.",
        greeting_neutral="\"Contracts available: tea export, porcelain transit, medicine supply. No weapons, no explosives, no exceptions. What are you looking for?\"",
        greeting_friendly="\"Captain! Tea contract — premium volcanic-aged, Liu's best. Commander Zhang approved it this morning. The margin is excellent.\"",
        greeting_hostile="\"I have nothing for flagged vessels. Come back when your record clears the Commander's review.\"",
        rumor="Ming once submitted a contract proposal to Zhang that would have allowed limited iron transit through the strait — for agricultural tools only. Zhang read it, wrote 'NO' in brush strokes three inches tall, and returned it. Ming framed it. It hangs behind his desk as a reminder of the boundaries he works within.",
        relationship_notes={"dg_commander_zhang": "Every contract requires Zhang's approval. Ming has learned the boundaries.", "dg_harbor_captain_li": "Contracts must be approved before loading. Li Jun enforces the sequence.", "dg_tea_merchant_liu": "Necessary partnership. She produces; he sells.", "dg_weapons_inspector_sun": "Every contract reviewed by Sun. No exceptions.", "dg_healer_chen_ling": "Sources medicines for her. One of his proudest contract lines.", "dg_inn_keeper_wu": "Negotiations happen at Wu's tables. Wu overhears. Useful."},
    ),
]

_DRAGONS_GATE_INSTITUTIONS = [
    PortInstitution(id="dg_strait", name="The Chain Harbor", port_id="dragons_gate", institution_type="harbor_master",
        description="Twin stone towers flanking the strait. Chains ready to close in sixty seconds. Li Jun's domain.", function="Military harbor with chain deployment. No unauthorized passage in 15 years.", political_leaning="Absolute military control.", npc_id="dg_harbor_captain_li"),
    PortInstitution(id="dg_tea_hall", name="The Tea Terraces", port_id="dragons_gate", institution_type="exchange",
        description="Terraced gardens on the fortress's south wall where volcanic soil produces extraordinary tea.", function="Tea trade — the fortress's economic lifeline. Liu manages production and export.", political_leaning="Commerce within military constraints.", npc_id="dg_tea_merchant_liu"),
    PortInstitution(id="dg_command", name="The Gate Command", port_id="dragons_gate", institution_type="governor",
        description="The fortress's highest tower. Maps of the strait, chain deployment controls, and Zhang's desk — military-neat, one personal item: nothing. He has no personal items.", function="Absolute military governance. Zhang's word is law.", political_leaning="Silk Circle military enforcement.", npc_id="dg_commander_zhang"),
    PortInstitution(id="dg_inn", name="The Gate Inn", port_id="dragons_gate", institution_type="tavern",
        description="Stone building inside fortress walls. Jasmine tea by day, something stronger at night. Wu sees everything and says nothing.", function="Social pressure valve + intelligence nexus. Wu provides both.", political_leaning="Discreet. Wu's loyalties are ambiguous by design.", npc_id="dg_inn_keeper_wu"),
    PortInstitution(id="dg_inspection", name="The Strip Room", port_id="dragons_gate", institution_type="customs",
        description="A brightly lit room where every cargo is examined. Sun's tools: acid tests, magnifying lenses, and an encyclopedic memory for every smuggling technique ever attempted.", function="Weapons inspection. Zero tolerance. Sun finds everything.", political_leaning="Fortress security.", npc_id="dg_weapons_inspector_sun"),
    PortInstitution(id="dg_infirmary", name="The Strait Infirmary", port_id="dragons_gate", institution_type="apothecary",
        description="Small but well-equipped. Chen Ling's domain. The eastern strait's only reliable medical care.", function="Medical care + desperate medicine purchasing. Chen Ling will pay premium for any medical supply.", political_leaning="Humanitarian within military structure.", npc_id="dg_healer_chen_ling"),
    PortInstitution(id="dg_broker", name="The Permitted Desk", port_id="dragons_gate", institution_type="broker",
        description="Ming's desk with Zhang's framed 'NO' hanging behind it. The most restricted brokerage in the East.", function="Brokering within Zhang's permissions. Tea, porcelain, medicine. No weapons. No exceptions.", political_leaning="Commerce in a cage.", npc_id="dg_broker_ming"),
]

DRAGONS_GATE_PROFILE = PortInstitutionalProfile(
    port_id="dragons_gate", governor_title="Gate Commander",
    power_structure="Dragon's Gate is Zhang's fortress. His word is absolute. Li Jun runs the harbor chains. Sun finds the weapons. Liu produces the tea that funds everything. Chen Ling heals. Wu watches and says nothing. Ming brokers what's permitted. Every institution exists within Zhang's boundaries — and those boundaries have not moved in fifteen years.",
    internal_tension="The tension is between security and commerce. Zhang wants zero weapons through the strait — absolute control. Liu needs trade to fund the fortress. Ming needs contracts to exist. The equilibrium works because Zhang's strictness makes the strait safe, which makes it valuable, which brings trade. Break any link and it collapses. Wu is the wildcard: his possible Syndicate connections are the one variable Zhang can't fully control, and he keeps Wu precisely because a known risk is better than an unknown one.",
    institutions=_DRAGONS_GATE_INSTITUTIONS, npcs=_DRAGONS_GATE_NPCS,
)


# =========================================================================
# SPICE NARROWS — The Hidden Market
# =========================================================================

_SPICE_NARROWS_NPCS = [
    PortNPC(
        id="sn_the_mouth", name="The Mouth", title="Anchorage Keeper",
        port_id="spice_narrows", institution="harbor_master", personality="invisible",
        description="You never see The Mouth. You hear a voice from the cliff face directing you through the volcanic channel to the hidden anchorage. The voice knows your ship's name, your cargo, and whether you're welcome. How it knows is the Narrows' first mystery.",
        agenda="Access control. The Mouth decides who enters the Narrows. Unlike One-Eye at Corsair's Rest who checks if you're followed, The Mouth checks if you're WORTHY. Unwelcome ships are directed into dead-end channels where they ground on volcanic rock.",
        greeting_neutral="A voice from the cliff: \"Follow the left channel. Anchor at the third cave. Touch nothing until you hear the second voice.\"",
        greeting_friendly="\"Captain! The Narrows expected you. Center channel — the deep berth. The Spice Lords have prepared your welcome.\"",
        greeting_hostile="\"Right channel. Shallow anchorage. Do not proceed further. Your reputation precedes you, Captain. It is not welcome here.\"",
        rumor="Nobody has ever seen The Mouth. Some say it's a person in a cave with speaking tubes. Others say it's three people working in shifts. One captain claims the voice came from the rock itself. The Narrows does not clarify.",
        relationship_notes={"sn_spice_lord_kiran": "The Mouth serves the Spice Lords. Access is their decision.", "sn_the_weigher": "The Weigher prices what The Mouth admits. Sequential trust.", "sn_raj_shadow": "Raj uses different channels. The Mouth knows which ones.", "sn_mama_smoke": "The Mouth has never been to Mama Smoke's kitchen. Nobody's sure if The Mouth eats.", "sn_poison_doctor": "Medicine enters freely. The Mouth never delays medical cargo.", "sn_ghost_broker": "The Ghost Broker moves what The Mouth admits. Clean chain."},
    ),
    PortNPC(
        id="sn_spice_lord_kiran", name="Spice Lord Kiran", title="Lord of the Narrows",
        port_id="spice_narrows", institution="governor", personality="dangerous",
        description="The Monsoon Syndicate's governor at Spice Narrows. Kiran sits cross-legged on silk cushions in the deepest cave, surrounded by the most concentrated spice wealth in the world. He speaks softly because he never needs to shout. His authority is the Syndicate's authority, and the Syndicate controls the opium trade, the spice lanes, and the informant network that spans every port east of Crosswind Isle.",
        agenda="Control of information and spice. Kiran doesn't just sell spice — he sells KNOWLEDGE. Which ships carry what cargo on which route at which time. The Syndicate's informants are everywhere, and Kiran is their handler. His real product isn't opium or spice — it's intelligence.",
        greeting_neutral="\"You've found the Narrows. That alone suggests someone trusts you. Sit. Tell me what you need, and I will tell you what it costs. The prices here are not in silver alone.\"",
        greeting_friendly="\"Ah, Captain — a valued friend of the Syndicate. Please, sit. I have information as valuable as any cargo. And some cargo, too. Shall we discuss both?\"",
        greeting_hostile="\"You are here because The Mouth permitted it. I am less generous than The Mouth. State your business quickly.\"",
        rumor="Kiran predicted a navy raid on the Narrows three days before it happened — because the raid commander's servant was a Syndicate informant. The Narrows was empty when the navy arrived. They found nothing but spice dust and the smell of incense.",
        relationship_notes={"sn_the_mouth": "The Mouth guards access. Kiran controls everything inside.", "sn_the_weigher": "His commercial arm. The Weigher prices the product. Kiran sets the strategy.", "sn_raj_shadow": "Raj the Quiet is his intelligence chief. They communicate in notes, never voice.", "sn_mama_smoke": "Even Kiran eats at Mama Smoke's. Even Kiran pays. Some rituals transcend authority.", "sn_poison_doctor": "The Poison Doctor serves the Syndicate's medical needs — and occasionally its darker needs.", "sn_ghost_broker": "The Ghost Broker handles the contracts Kiran approves. The approval is non-negotiable."},
    ),
    PortNPC(
        id="sn_the_weigher", name="The Weigher", title="Price Master",
        port_id="spice_narrows", institution="exchange", personality="mathematical",
        description="A figure in a dark room lit by a single lamp, surrounded by scales of extraordinary precision. The Weigher prices everything at the Narrows: spice by the grain, opium by the pipe, stolen cargo by the crate, and information by the word. Prices are whispered. Always.",
        agenda="Perfect pricing. The Weigher's job is ensuring the black market stays liquid — prices that are too high drive buyers away; too low and sellers stop coming. Like Whisper at Corsair's Rest but more calculating — The Weigher uses mathematics, not intuition.",
        greeting_neutral="A whisper from the dark: \"Place your goods on the scale. I will name the price once. You accept or you leave.\"",
        greeting_friendly="\"Ah, a trusted buyer. For you, the second scale.\" A different set of weights appears. Better prices. The lamp flickers.",
        greeting_hostile="\"The first scale only. Posted rates. Do not ask for the second.\"",
        rumor="The Weigher's scales are rumored to be a thousand years old — from a dynasty that measured spice in gold equivalents. Whether this is true or marketing is the Narrows' second mystery.",
        relationship_notes={"sn_the_mouth": "Sequential trust. The Mouth admits; The Weigher prices.", "sn_spice_lord_kiran": "Commercial arm of the Syndicate. Kiran sets strategy; The Weigher executes.", "sn_raj_shadow": "Raj provides intelligence that affects pricing. The Weigher incorporates it silently.", "sn_mama_smoke": "The Weigher sends food orders through notes. Nobody's seen The Weigher eat in person.", "sn_poison_doctor": "Medicine is priced separately. The Weigher considers healing exempt from market forces.", "sn_ghost_broker": "The Ghost Broker sells what The Weigher prices. Clean chain."},
    ),
    PortNPC(
        id="sn_raj_shadow", name="Raj the Quiet's Shadow", title="Intelligence Officer",
        port_id="spice_narrows", institution="customs", personality="phantom",
        description="Not Raj the Quiet himself — Raj operates from the sea. This is his representative at the Narrows: a figure known only as Raj's Shadow, who receives intelligence reports, dispatches informants, and ensures the Syndicate knows everything happening east of the Gate. The Shadow sits in a cave with a dozen message tubes and a map marked with pins.",
        agenda="Information. Every ship, every cargo, every captain's route and schedule — the Shadow collects it all and sends it to Raj. The Narrows' 'customs' isn't inspection — it's intelligence gathering. Every captain who docks is observed, catalogued, and filed.",
        greeting_neutral="You don't see anyone. But you have the distinct feeling you've been observed, assessed, and catalogued. A note appears: \"Your arrival has been recorded.\"",
        greeting_friendly="A note in familiar handwriting: \"Raj sends regards. Your route has been noted as friendly. The Syndicate will not interfere with your next three voyages.\"",
        greeting_hostile="No note. No contact. But your cargo manifest appears, accurately detailed, on a wall in the intelligence cave. You were never told about the intelligence cave.",
        rumor="Raj's Shadow is rumored to be three people working in shifts — or one person who never sleeps. The Shadow has never been seen entering or leaving the intelligence cave. Food appears inside. Reports appear outside. The mechanism is unknown.",
        relationship_notes={"sn_the_mouth": "Raj uses different channels. The Mouth knows which.", "sn_spice_lord_kiran": "Intelligence chief. They communicate in notes, never voice.", "sn_the_weigher": "Intelligence affects pricing. The Shadow provides; The Weigher incorporates.", "sn_mama_smoke": "Food appears in the intelligence cave. Mama Smoke denies delivering it.", "sn_poison_doctor": "The Shadow occasionally requests specific compounds. Nobody asks why.", "sn_ghost_broker": "The Ghost Broker's contracts are informed by the Shadow's intelligence."},
    ),
    PortNPC(
        id="sn_mama_smoke", name="Mama Smoke", title="Cave Cook",
        port_id="spice_narrows", institution="tavern", personality="motherly",
        description="A stout woman who cooks in a cave filled with spice smoke so thick it stings the eyes. Mama Smoke feeds the Narrows — smugglers, Syndicate agents, visiting captains, and whoever else finds their way to her fire. Her spice-smoked fish is legendary. Her neutrality is absolute. Even Kiran pays.",
        agenda="Feeding people in a place that tries to forget they need feeding. Mama Smoke provides the only human warmth in the Narrows — a cave full of spice smoke where people can sit, eat, and for a moment, be something other than smugglers.",
        greeting_neutral="\"Sit. The smoke clears your lungs — don't fight it. Fish is on the fire. Tea is in the pot. You look like you need both.\"",
        greeting_friendly="\"My captain! You came back to the deep! Sit, sit — I've been smoking a special batch. The spice in this one will make you see colors you didn't know existed.\"",
        greeting_hostile="\"Everyone eats. Even those the Lords distrust. Sit. The smoke doesn't judge, and neither does my fish.\"",
        rumor="Mama Smoke's cave has a back exit that nobody maps. Twice, when raids threatened the Narrows, captains escaped through her kitchen. She claims she doesn't know about any back exit. The rescued captains send her gifts annually.",
        relationship_notes={"sn_the_mouth": "The Mouth has never visited. Mama Smoke finds this suspicious.", "sn_spice_lord_kiran": "Even Kiran pays. Even Kiran sits quietly. Some things are sacred.", "sn_the_weigher": "Sends food through notes. Nobody's seen The Weigher eat.", "sn_raj_shadow": "Food appears in the intelligence cave. She denies delivering it. Denial is a form of kindness.", "sn_poison_doctor": "Friends. Two people who keep others alive in a place that values other things.", "sn_ghost_broker": "She feeds the Ghost Broker's crews after midnight runs. Hot spice tea and smoked fish."},
    ),
    PortNPC(
        id="sn_poison_doctor", name="The Poison Doctor", title="Apothecary",
        port_id="spice_narrows", institution="apothecary", personality="ambiguous",
        description="A figure whose title is deliberately unsettling — 'Poison Doctor' could mean healer or assassin, and at the Narrows, the answer is yes. The Doctor compounds medicines from the archipelago's rare spice-based pharmacopoeia, treats wounds and fevers, and occasionally prepares things that nobody asks about for clients nobody names.",
        agenda="Survival. The Poison Doctor provides medical care to a community that has no other access to it — and provides other services to clients who can afford them. The morality is as ambiguous as the title. The Doctor sleeps fine.",
        greeting_neutral="\"Sick? Wounded? I can help. If you need something else... describe the symptoms. I'll decide what you need.\"",
        greeting_friendly="\"Captain — your health is good. I can see it. But I've prepared a preventive compound for the southern waters. Take it daily. You'll thank me.\"",
        greeting_hostile="\"I treat all. Even those I'm told not to. The oath doesn't come with conditions. Sit down or don't.\"",
        rumor="The Poison Doctor once cured a plague in the Narrows using a spice compound that also happens to be mildly hallucinogenic. The patients recovered and reported vivid dreams for a week. The Doctor said this was a side effect. Some patients came back for refills. The Doctor didn't ask why.",
        relationship_notes={"sn_the_mouth": "Medicine enters freely. The Mouth never delays medical cargo.", "sn_spice_lord_kiran": "Serves the Syndicate's medical needs — and darker needs.", "sn_the_weigher": "Medicine priced separately. Healing is exempt from market forces.", "sn_raj_shadow": "Occasionally requests specific compounds. Nobody asks why.", "sn_mama_smoke": "Friends. Two people keeping others alive in a place that values other things.", "sn_ghost_broker": "Provides medical supplies for the broker's crews."},
    ),
    PortNPC(
        id="sn_ghost_broker", name="The Ghost Broker", title="Contract Handler",
        port_id="spice_narrows", institution="broker", personality="anonymous",
        description="Nobody's sure if the Ghost Broker is one person or a service. Contracts appear on a cave wall — pinned to the rock, detailed in precise handwriting, with pickup and delivery instructions that account for navy patrols, monsoon timing, and faction territory. The contracts are always profitable. The source is always unknown.",
        agenda="Moving product. The Ghost Broker matches Syndicate cargo to willing captains. Opium runs, spice contracts, stolen goods fencing — all appear on the wall with terms that are fair enough to attract takers and profitable enough to sustain the operation.",
        greeting_neutral="A contract appears on the wall near you. It matches your ship's capacity, your route, and your risk tolerance. There is no signature. Just terms.",
        greeting_friendly="Three contracts appear. The best one has a note: 'For trusted captains only. Higher margin. Raj's guarantee.' You've never met Raj.",
        greeting_hostile="The wall is blank where you stand. Contracts appear elsewhere. You are not being offered work today.",
        rumor="The Ghost Broker once posted a contract that was completed before anyone in the Narrows saw it. The cargo moved, the payment cleared, and nobody knows who took the job. Either the Ghost Broker has captains nobody else knows about, or the Ghost Broker IS one of the captains.",
        relationship_notes={"sn_the_mouth": "The Mouth admits; the Ghost Broker contracts. Clean chain.", "sn_spice_lord_kiran": "Contracts approved by Kiran. The approval is non-negotiable.", "sn_the_weigher": "The Ghost Broker sells what The Weigher prices.", "sn_raj_shadow": "Contracts informed by the Shadow's intelligence.", "sn_mama_smoke": "Crews fed after midnight runs.", "sn_poison_doctor": "Medical supplies provided for crews."},
    ),
]

_SPICE_NARROWS_INSTITUTIONS = [
    PortInstitution(id="sn_channel", name="The Volcanic Channel", port_id="spice_narrows", institution_type="harbor_master",
        description="A narrow volcanic channel with The Mouth's voice echoing from cliff faces. Left for welcome. Right for unwelcome. Center for trusted.", function="Voice-guided access. The Mouth directs. Unwelcome ships ground on volcanic rock.", political_leaning="Monsoon Syndicate.", npc_id="sn_the_mouth"),
    PortInstitution(id="sn_dark_room", name="The Dark Room", port_id="spice_narrows", institution_type="exchange",
        description="A cave lit by a single lamp. Scales of extraordinary precision. Prices whispered, never spoken aloud.", function="Black market pricing. Spice by the grain, opium by the pipe, information by the word.", political_leaning="Pure black market.", npc_id="sn_the_weigher"),
    PortInstitution(id="sn_deep_cave", name="The Deep Throne", port_id="spice_narrows", institution_type="governor",
        description="The deepest cave. Silk cushions. The most concentrated spice wealth in the world. Kiran sits. The world comes to him.", function="Syndicate governance + intelligence nexus. Kiran's real product is information.", political_leaning="Monsoon Syndicate headquarters.", npc_id="sn_spice_lord_kiran"),
    PortInstitution(id="sn_smoke_kitchen", name="Mama Smoke's Cave", port_id="spice_narrows", institution_type="tavern",
        description="A cave of spice smoke so thick it stings the eyes. The fish is legendary. The back exit is officially nonexistent.", function="The only human warmth in the Narrows. Neutrality absolute. Even Kiran pays.", political_leaning="Neutral by fire.", npc_id="sn_mama_smoke"),
    PortInstitution(id="sn_intel_cave", name="The Intelligence Cave", port_id="spice_narrows", institution_type="customs",
        description="A cave with message tubes, a pin-marked map, and food that appears from nowhere. Raj's Shadow operates here.", function="Not customs — intelligence. Every captain observed, catalogued, filed.", political_leaning="Syndicate intelligence operations.", npc_id="sn_raj_shadow"),
    PortInstitution(id="sn_lab", name="The Poison Lab", port_id="spice_narrows", institution_type="apothecary",
        description="A cave of rare compounds, spice-based pharmacopoeia, and ambiguous morality. The Doctor heals. The Doctor also prepares other things.", function="Medicine + ambiguous services. The title is deliberately unsettling.", political_leaning="Above faction. The oath doesn't come with conditions.", npc_id="sn_poison_doctor"),
    PortInstitution(id="sn_wall", name="The Contract Wall", port_id="spice_narrows", institution_type="broker",
        description="A cave wall where contracts appear — pinned to rock in precise handwriting, no signature, terms that account for patrols and monsoons.", function="Anonymous contract posting. Profitable terms, unknown source. The Ghost Broker may be one person or a service.", political_leaning="Syndicate operations.", npc_id="sn_ghost_broker"),
]

SPICE_NARROWS_PROFILE = PortInstitutionalProfile(
    port_id="spice_narrows", governor_title="Spice Lord",
    power_structure="Spice Narrows is the Monsoon Syndicate's heart — Kiran controls everything from the deepest cave. The Mouth guards access. The Weigher prices in darkness. Raj's Shadow collects intelligence on every captain who enters. The Ghost Broker posts contracts on cave walls. Mama Smoke feeds people in spice smoke. The Poison Doctor heals and occasionally does other things. Every person here is partially invisible, partially anonymous, and entirely controlled by Kiran's intelligence network.",
    internal_tension="The Narrows has no internal tension — because Kiran's information control eliminates the possibility of opposition. He knows everything before it happens. The EXTERNAL tension is the navy: Dragon's Gate's Commander Zhang and Inspector Sun are systematically mapping the Narrows' supply lines. Every raid Kiran predicts and escapes makes him more confident, which makes him less careful. Mama Smoke's back exit — the one she denies exists — is the Narrows' secret survival insurance. If Kiran ever fails to predict a raid, that exit becomes the most important tunnel in the East Indies.",
    institutions=_SPICE_NARROWS_INSTITUTIONS, npcs=_SPICE_NARROWS_NPCS,
)


# =========================================================================
# Export all profiles from this file
# =========================================================================

EAST_PROFILES = {
    "silk_haven": SILK_HAVEN_PROFILE,
    "crosswind_isle": CROSSWIND_ISLE_PROFILE,
    "dragons_gate": DRAGONS_GATE_PROFILE,
    "spice_narrows": SPICE_NARROWS_PROFILE,
}
