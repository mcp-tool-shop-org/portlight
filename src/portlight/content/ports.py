"""Expanded port network — 20 ports across 5 regions.

Phase 1: 10 ports, 3 regions (Mediterranean, West Africa, East Indies)
Phase 2: +10 ports, +2 regions (North Atlantic, South Seas)

Each port has:
  - Clear export/import identity (affinity-driven)
  - Variable provisioning cost (cheap at farming ports, expensive at luxury hubs)
  - Variable repair cost (cheap at shipyard ports, expensive elsewhere)
  - Variable crew cost (cheap at large ports, expensive at remote ones)

Port identity should be readable in one glance from the market screen.
"""

from portlight.engine.models import MarketSlot, Port, PortFeature


def _slot(good_id: str, stock: int, target: int, restock: float, affinity: float = 1.0, spread: float = 0.15) -> MarketSlot:
    return MarketSlot(good_id=good_id, stock_current=stock, stock_target=target, restock_rate=restock, local_affinity=affinity, spread=spread)


PORTS: dict[str, Port] = {p.id: p for p in [
    # =========================================================================
    # MEDITERRANEAN (4 ports)
    # =========================================================================
    Port(
        id="porto_novo", name="Porto Novo", region="Mediterranean",
        description="A bustling harbor city, gateway to inland trade. Grain ships fill the docks.",
        features=[PortFeature.SHIPYARD],
        market=[
            _slot("grain",  40, 35, 3.0, affinity=1.3),   # EXPORTS grain
            _slot("timber", 20, 25, 2.0, affinity=0.8),
            _slot("iron",   15, 15, 1.5, affinity=1.0),
            _slot("cotton", 10, 12, 1.0, affinity=0.7),   # WANTS cotton
            _slot("rum",    18, 20, 1.5, affinity=1.1),
            _slot("dyes",   8,  10, 1.0, affinity=0.7),   # WANTS dyes for textiles
        ],
        port_fee=5,
        provision_cost=1,   # farming port, cheap provisions
        repair_cost=2,      # shipyard, cheap repairs
        crew_cost=4,        # major port, affordable crew
        map_x=18, map_y=8,
    ),
    Port(
        id="al_manar", name="Al-Manar", region="Mediterranean",
        description="Ancient port famed for its spice markets. Merchants bid fiercely for grain and iron.",
        market=[
            _slot("spice",  30, 25, 2.5, affinity=1.5),   # EXPORTS spice
            _slot("silk",   8,  10, 1.0, affinity=0.9),
            _slot("grain",  10, 15, 1.5, affinity=0.6),   # WANTS grain badly
            _slot("porcelain", 5, 8, 0.8, affinity=0.7),  # WANTS porcelain
            _slot("rum",    12, 15, 1.0, affinity=0.8),
            _slot("tea",    6,  8,  0.8, affinity=0.7),    # WANTS tea
            _slot("medicines", 10, 12, 1.0, affinity=1.1),
        ],
        port_fee=8,
        provision_cost=3,   # luxury hub, expensive provisions
        repair_cost=4,      # no shipyard, pricey
        crew_cost=6,        # expensive city
        map_x=24, map_y=6,
    ),
    Port(
        id="silva_bay", name="Silva Bay", region="Mediterranean",
        description="Timber-rich bay surrounded by dense forests. The shipwrights here are the best in the region.",
        features=[PortFeature.SHIPYARD],
        market=[
            _slot("timber", 45, 40, 3.5, affinity=1.5),   # EXPORTS timber
            _slot("iron",   20, 18, 2.0, affinity=1.2),   # EXPORTS iron
            _slot("grain",  15, 18, 1.5, affinity=0.9),
            _slot("cotton", 8,  10, 1.0, affinity=0.7),   # WANTS cotton
            _slot("weapons", 5, 8,  0.8, affinity=0.6),   # WANTS weapons (shipyard needs)
        ],
        port_fee=4,
        provision_cost=2,
        repair_cost=1,      # best shipyard = cheapest repairs
        crew_cost=5,
        map_x=14, map_y=10,
    ),
    Port(
        id="corsairs_rest", name="Corsair's Rest", region="Mediterranean",
        description="A lawless harbor tucked between cliffs. Smugglers, pirates, and those who trade with them.",
        features=[PortFeature.BLACK_MARKET],
        market=[
            _slot("weapons", 25, 20, 2.5, affinity=1.5),  # EXPORTS weapons
            _slot("rum",     30, 25, 3.0, affinity=1.4),   # EXPORTS rum
            _slot("tobacco", 20, 18, 2.0, affinity=1.3),   # EXPORTS tobacco
            _slot("silk",    3,  5,  0.5, affinity=0.5),   # WANTS silk
            _slot("medicines", 4, 6, 0.5, affinity=0.5),   # WANTS medicines
        ],
        port_fee=3,         # pirate haven, cheap docking
        provision_cost=2,
        repair_cost=3,      # decent repair, pirate shipwrights
        crew_cost=2,        # cheap crew (desperate sailors)
        map_x=21, map_y=13,
    ),

    # =========================================================================
    # NORTH ATLANTIC (3 ports — new region)
    # =========================================================================
    Port(
        id="ironhaven", name="Ironhaven", region="North Atlantic",
        description="Industrial port city wreathed in forge smoke. Weapons and iron flow out, everything else flows in.",
        features=[PortFeature.SHIPYARD],
        market=[
            _slot("iron",    50, 45, 4.0, affinity=1.6),   # EXPORTS iron (best source)
            _slot("weapons", 35, 30, 3.0, affinity=1.5),   # EXPORTS weapons
            _slot("timber",  15, 18, 1.5, affinity=0.8),
            _slot("grain",   10, 15, 1.0, affinity=0.6),   # WANTS grain
            _slot("cotton",  8,  12, 1.0, affinity=0.6),   # WANTS cotton
            _slot("tobacco", 12, 15, 1.0, affinity=0.9),
        ],
        port_fee=6,
        provision_cost=2,
        repair_cost=1,      # industrial shipyard
        crew_cost=4,
        map_x=8, map_y=4,
    ),
    Port(
        id="stormwall", name="Stormwall", region="North Atlantic",
        description="Fortress port guarding the northern straits. Military outpost with strict inspections.",
        market=[
            _slot("weapons", 15, 18, 1.5, affinity=1.0),
            _slot("grain",   20, 22, 2.0, affinity=1.1),
            _slot("timber",  18, 20, 1.5, affinity=1.0),
            _slot("medicines", 15, 12, 1.5, affinity=1.3), # EXPORTS medicines
            _slot("rum",     10, 12, 1.0, affinity=0.7),   # WANTS rum (soldiers love it)
            _slot("tobacco", 8,  10, 0.8, affinity=0.7),   # WANTS tobacco
        ],
        port_fee=10,        # military port, highest fees
        provision_cost=2,
        repair_cost=2,
        crew_cost=3,        # cheap crew (military surplus)
        map_x=4, map_y=8,
    ),
    Port(
        id="thornport", name="Thornport", region="North Atlantic",
        description="Whaling town turned trading post. Tea and tobacco are the local currency. Medicines fetch gold.",
        market=[
            _slot("tea",      25, 22, 2.5, affinity=1.4),  # EXPORTS tea
            _slot("tobacco",  30, 25, 3.0, affinity=1.5),  # EXPORTS tobacco
            _slot("timber",   20, 18, 2.0, affinity=1.2),
            _slot("medicines", 5, 8,  0.8, affinity=0.5),  # WANTS medicines badly
            _slot("silk",     3,  5,  0.5, affinity=0.5),   # WANTS silk
            _slot("spice",    4,  6,  0.6, affinity=0.5),   # WANTS spice
        ],
        port_fee=5,
        provision_cost=1,   # whaling town, cheap food
        repair_cost=3,
        crew_cost=3,        # hardy northern sailors
        map_x=11, map_y=10,
    ),

    # =========================================================================
    # WEST AFRICA (4 ports)
    # =========================================================================
    Port(
        id="sun_harbor", name="Sun Harbor", region="West Africa",
        description="Golden coast port where cotton bales stack higher than the warehouses.",
        market=[
            _slot("cotton", 35, 30, 3.0, affinity=1.4),   # EXPORTS cotton
            _slot("iron",   25, 22, 2.0, affinity=1.3),   # EXPORTS iron
            _slot("dyes",   20, 18, 2.0, affinity=1.3),   # EXPORTS dyes
            _slot("silk",   3,  5,  0.5, affinity=0.6),   # WANTS silk
            _slot("spice",  5,  8,  0.8, affinity=0.6),   # WANTS spice
            _slot("rum",    10, 12, 1.0, affinity=0.9),
        ],
        port_fee=5,
        provision_cost=2,
        repair_cost=4,      # no shipyard
        crew_cost=3,        # cheap labor
        map_x=14, map_y=22,
    ),
    Port(
        id="palm_cove", name="Palm Cove", region="West Africa",
        description="A sheltered cove where rum barrels outnumber the inhabitants. Cheapest provisions on the coast.",
        market=[
            _slot("rum",     40, 35, 3.0, affinity=1.6),  # EXPORTS rum
            _slot("grain",   12, 15, 1.5, affinity=0.8),
            _slot("timber",  8,  10, 1.0, affinity=0.7),  # WANTS timber
            _slot("cotton",  15, 18, 1.5, affinity=1.1),
            _slot("tobacco", 18, 15, 2.0, affinity=1.2),  # EXPORTS tobacco
        ],
        port_fee=3,
        provision_cost=1,   # cheapest provisions in the game
        repair_cost=5,      # remote, expensive repairs
        crew_cost=3,
        map_x=10, map_y=26,
    ),
    Port(
        id="iron_point", name="Iron Point", region="West Africa",
        description="Mining settlement at the river mouth. Iron flows out, everything else flows in at a premium.",
        market=[
            _slot("iron",   50, 45, 4.0, affinity=1.6),   # EXPORTS iron
            _slot("grain",  8,  12, 1.0, affinity=0.6),   # WANTS grain
            _slot("timber", 12, 15, 1.5, affinity=0.9),
            _slot("porcelain", 2, 4, 0.5, affinity=0.65), # WANTS porcelain
            _slot("weapons", 8, 10, 1.0, affinity=0.7),   # WANTS weapons (mining tools)
        ],
        port_fee=4,
        provision_cost=3,   # mining town, food is scarce
        repair_cost=3,
        crew_cost=4,
        map_x=18, map_y=24,
    ),
    Port(
        id="pearl_shallows", name="Pearl Shallows", region="West Africa",
        description="Divers bring up pearls from the warm shallows. A quiet port where fortunes are made by the patient.",
        market=[
            _slot("pearls",  15, 12, 1.5, affinity=1.6),  # EXPORTS pearls (rare)
            _slot("cotton",  20, 18, 2.0, affinity=1.2),
            _slot("dyes",    15, 12, 1.5, affinity=1.3),   # EXPORTS dyes
            _slot("medicines", 3, 5, 0.5, affinity=0.5),   # WANTS medicines
            _slot("grain",   10, 12, 1.0, affinity=0.8),
        ],
        port_fee=4,
        provision_cost=2,
        repair_cost=4,
        crew_cost=4,
        map_x=12, map_y=30,
    ),

    # =========================================================================
    # EAST INDIES (6 ports)
    # =========================================================================
    Port(
        id="jade_port", name="Jade Port", region="East Indies",
        description="Porcelain workshops line the waterfront. Iron and grain are worth their weight in gold here.",
        market=[
            _slot("porcelain", 35, 30, 3.0, affinity=1.5),  # EXPORTS porcelain
            _slot("silk",   25, 22, 2.5, affinity=1.3),     # EXPORTS silk
            _slot("spice",  15, 18, 1.5, affinity=1.1),
            _slot("grain",  5,  8,  0.8, affinity=0.6),     # WANTS grain
            _slot("iron",   3,  5,  0.5, affinity=0.6),     # WANTS iron
            _slot("tea",    20, 18, 2.0, affinity=1.2),     # EXPORTS tea
        ],
        port_fee=10,
        provision_cost=3,
        repair_cost=3,
        crew_cost=7,        # far from home, expensive crew
        map_x=34, map_y=10,
    ),
    Port(
        id="monsoon_reach", name="Monsoon Reach", region="East Indies",
        description="Seasonal winds funnel the spice trade through this crossroads. The shipyard builds for endurance.",
        features=[PortFeature.SHIPYARD],
        market=[
            _slot("spice",  25, 22, 2.5, affinity=1.4),   # EXPORTS spice
            _slot("silk",   20, 18, 2.0, affinity=1.2),   # EXPORTS silk
            _slot("cotton", 5,  8,  0.8, affinity=0.6),   # WANTS cotton
            _slot("timber", 5,  8,  0.8, affinity=0.5),   # WANTS timber
            _slot("rum",    8,  10, 1.0, affinity=0.7),
            _slot("medicines", 8, 10, 1.0, affinity=0.9),
        ],
        port_fee=8,
        provision_cost=2,
        repair_cost=2,      # shipyard port
        crew_cost=6,
        map_x=38, map_y=14,
    ),
    Port(
        id="silk_haven", name="Silk Haven", region="East Indies",
        description="Premier silk market of the eastern waters. Rum and iron are scarce luxuries here.",
        market=[
            _slot("silk",   40, 35, 3.5, affinity=1.6),   # EXPORTS silk (best source)
            _slot("porcelain", 15, 12, 1.5, affinity=1.2),
            _slot("spice",  10, 12, 1.0, affinity=0.9),
            _slot("rum",    5,  8,  0.8, affinity=0.5),   # WANTS rum badly
            _slot("dyes",   3,  5,  0.5, affinity=0.5),   # WANTS dyes
        ],
        port_fee=7,
        provision_cost=3,
        repair_cost=5,      # remote, no shipyard
        crew_cost=8,        # most expensive crew
        map_x=42, map_y=8,
    ),
    Port(
        id="crosswind_isle", name="Crosswind Isle", region="East Indies",
        description="Free port at the junction of all trade winds. Everything passes through, nothing stays cheap.",
        features=[PortFeature.SAFE_HARBOR],
        market=[
            _slot("grain",  15, 15, 1.5, affinity=1.0),
            _slot("timber", 12, 12, 1.2, affinity=1.0),
            _slot("iron",   10, 10, 1.0, affinity=1.0),
            _slot("cotton", 10, 10, 1.0, affinity=1.0),
            _slot("spice",  10, 10, 1.0, affinity=1.0),
            _slot("silk",   8,  8,  0.8, affinity=1.0),
            _slot("rum",    10, 10, 1.0, affinity=1.0),
            _slot("porcelain", 6, 6, 0.6, affinity=1.0),
            _slot("tea",    8,  8,  0.8, affinity=1.0),
        ],
        port_fee=6,
        provision_cost=2,
        repair_cost=3,
        crew_cost=5,
        map_x=32, map_y=16,
    ),
    Port(
        id="dragons_gate", name="Dragon's Gate", region="East Indies",
        description="Fortress harbor controlling the eastern straits. Weapons are contraband here, but medicines are gold.",
        market=[
            _slot("tea",       30, 25, 3.0, affinity=1.5),  # EXPORTS tea
            _slot("porcelain", 20, 18, 2.0, affinity=1.3),
            _slot("medicines", 3,  5,  0.5, affinity=0.4),  # WANTS medicines desperately
            _slot("iron",      5,  8,  0.8, affinity=0.6),  # WANTS iron
            _slot("tobacco",   4,  6,  0.5, affinity=0.5),  # WANTS tobacco
        ],
        port_fee=9,
        provision_cost=2,
        repair_cost=3,
        crew_cost=7,
        map_x=44, map_y=12,
    ),
    Port(
        id="spice_narrows", name="Spice Narrows", region="East Indies",
        description="Hidden anchorage in the spice archipelago. The most concentrated spice market in the world.",
        features=[PortFeature.BLACK_MARKET],
        market=[
            _slot("spice",    45, 40, 4.0, affinity=1.7),  # EXPORTS spice (best source)
            _slot("pearls",   8,  6,  1.0, affinity=1.3),  # Pearls from local divers
            _slot("silk",     10, 12, 1.0, affinity=0.9),
            _slot("weapons",  3,  5,  0.5, affinity=0.5),  # WANTS weapons
            _slot("grain",    5,  8,  0.5, affinity=0.5),  # WANTS grain
        ],
        port_fee=5,
        provision_cost=3,
        repair_cost=5,      # remote
        crew_cost=6,
        map_x=38, map_y=20,
    ),

    # =========================================================================
    # SOUTH SEAS (3 ports — new region)
    # =========================================================================
    Port(
        id="ember_isle", name="Ember Isle", region="South Seas",
        description="Volcanic island with obsidian beaches. Rich in rare minerals and medicinal plants.",
        market=[
            _slot("medicines", 25, 20, 2.5, affinity=1.5),  # EXPORTS medicines
            _slot("dyes",      20, 18, 2.0, affinity=1.4),  # EXPORTS dyes (volcanic pigments)
            _slot("iron",      15, 12, 1.5, affinity=1.2),
            _slot("grain",     5,  8,  0.5, affinity=0.5),  # WANTS grain
            _slot("timber",    5,  8,  0.5, affinity=0.5),  # WANTS timber
            _slot("weapons",   3,  5,  0.5, affinity=0.5),  # WANTS weapons
        ],
        port_fee=6,
        provision_cost=2,
        repair_cost=4,
        crew_cost=5,
        map_x=34, map_y=28,
    ),
    Port(
        id="typhoon_anchorage", name="Typhoon Anchorage", region="South Seas",
        description="Storm-battered harbor that only the boldest captains visit. Pearls and rare goods reward the brave.",
        features=[PortFeature.SHIPYARD],
        market=[
            _slot("pearls",    20, 15, 2.0, affinity=1.6),  # EXPORTS pearls (best source)
            _slot("timber",    25, 22, 2.5, affinity=1.3),  # EXPORTS timber (tropical hardwood)
            _slot("spice",     12, 10, 1.5, affinity=1.2),
            _slot("silk",      3,  5,  0.5, affinity=0.5),  # WANTS silk
            _slot("porcelain", 2,  4,  0.5, affinity=0.5),  # WANTS porcelain
            _slot("medicines", 8,  10, 1.0, affinity=0.8),
        ],
        port_fee=4,
        provision_cost=1,   # tropical, cheap food
        repair_cost=2,      # shipyard port
        crew_cost=4,
        map_x=40, map_y=30,
    ),
    Port(
        id="coral_throne", name="Coral Throne", region="South Seas",
        description="Island kingdom built on coral reefs. The king trades pearls for weapons and demands tribute in silk.",
        market=[
            _slot("pearls",    12, 10, 1.5, affinity=1.4),  # EXPORTS pearls
            _slot("tobacco",   20, 18, 2.0, affinity=1.3),  # EXPORTS tobacco
            _slot("rum",       18, 15, 2.0, affinity=1.3),
            _slot("weapons",   2,  4,  0.3, affinity=0.4),  # WANTS weapons desperately
            _slot("silk",      2,  4,  0.3, affinity=0.4),  # WANTS silk
            _slot("tea",       3,  5,  0.5, affinity=0.5),  # WANTS tea
        ],
        port_fee=7,         # tribute to the king
        provision_cost=1,
        repair_cost=4,
        crew_cost=5,
        map_x=44, map_y=26,
    ),
]}
