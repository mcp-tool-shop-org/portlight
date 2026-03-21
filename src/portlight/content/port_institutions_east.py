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

EAST_PROFILES = {
    "silk_haven": SILK_HAVEN_PROFILE,
}
