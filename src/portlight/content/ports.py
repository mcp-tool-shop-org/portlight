"""Phase 2 port network - 10 ports with sharper identities.

Each port now has:
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
    # === Mediterranean ===
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
        ],
        port_fee=5,
        provision_cost=1,   # farming port, cheap provisions
        repair_cost=2,      # shipyard, cheap repairs
        crew_cost=4,        # major port, affordable crew
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
        ],
        port_fee=8,
        provision_cost=3,   # luxury hub, expensive provisions
        repair_cost=4,      # no shipyard, pricey
        crew_cost=6,        # expensive city
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
        ],
        port_fee=4,
        provision_cost=2,
        repair_cost=1,      # best shipyard = cheapest repairs
        crew_cost=5,
    ),

    # === West African Coast ===
    Port(
        id="sun_harbor", name="Sun Harbor", region="West Africa",
        description="Golden coast port where cotton bales stack higher than the warehouses. Silk and spice fetch a fortune.",
        market=[
            _slot("cotton", 35, 30, 3.0, affinity=1.4),   # EXPORTS cotton
            _slot("iron",   25, 22, 2.0, affinity=1.3),   # EXPORTS iron
            _slot("silk",   3,  5,  0.5, affinity=0.6),   # WANTS silk
            _slot("spice",  5,  8,  0.8, affinity=0.6),   # WANTS spice
            _slot("rum",    10, 12, 1.0, affinity=0.9),
        ],
        port_fee=5,
        provision_cost=2,
        repair_cost=4,      # no shipyard
        crew_cost=3,        # cheap labor
    ),
    Port(
        id="palm_cove", name="Palm Cove", region="West Africa",
        description="A sheltered cove where rum barrels outnumber the inhabitants. Cheapest provisions on the coast.",
        market=[
            _slot("rum",    40, 35, 3.0, affinity=1.6),   # EXPORTS rum
            _slot("grain",  12, 15, 1.5, affinity=0.8),
            _slot("timber", 8,  10, 1.0, affinity=0.7),   # WANTS timber
            _slot("cotton", 15, 18, 1.5, affinity=1.1),
        ],
        port_fee=3,
        provision_cost=1,   # cheapest provisions in the game
        repair_cost=5,      # remote, expensive repairs
        crew_cost=3,
    ),
    Port(
        id="iron_point", name="Iron Point", region="West Africa",
        description="Mining settlement at the river mouth. Iron flows out, everything else flows in at a premium.",
        market=[
            _slot("iron",   50, 45, 4.0, affinity=1.6),   # EXPORTS iron
            _slot("grain",  8,  12, 1.0, affinity=0.6),   # WANTS grain
            _slot("timber", 12, 15, 1.5, affinity=0.9),
            _slot("porcelain", 2, 4, 0.5, affinity=0.65), # WANTS porcelain
        ],
        port_fee=4,
        provision_cost=3,   # mining town, food is scarce
        repair_cost=3,
        crew_cost=4,
    ),

    # === East Indies ===
    Port(
        id="jade_port", name="Jade Port", region="East Indies",
        description="Porcelain workshops line the waterfront. Iron and grain are worth their weight in gold here.",
        market=[
            _slot("porcelain", 35, 30, 3.0, affinity=1.5),  # EXPORTS porcelain
            _slot("silk",   25, 22, 2.5, affinity=1.3),     # EXPORTS silk
            _slot("spice",  15, 18, 1.5, affinity=1.1),
            _slot("grain",  5,  8,  0.8, affinity=0.6),     # WANTS grain
            _slot("iron",   3,  5,  0.5, affinity=0.6),     # WANTS iron
        ],
        port_fee=10,
        provision_cost=3,
        repair_cost=3,
        crew_cost=7,        # far from home, expensive crew
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
        ],
        port_fee=8,
        provision_cost=2,
        repair_cost=2,      # shipyard port
        crew_cost=6,
    ),
    Port(
        id="silk_haven", name="Silk Haven", region="East Indies",
        description="Premier silk market of the eastern waters. Rum and iron are scarce luxuries here.",
        market=[
            _slot("silk",   40, 35, 3.5, affinity=1.6),   # EXPORTS silk (best source)
            _slot("porcelain", 15, 12, 1.5, affinity=1.2),
            _slot("spice",  10, 12, 1.0, affinity=0.9),
            _slot("rum",    5,  8,  0.8, affinity=0.5),   # WANTS rum badly
        ],
        port_fee=7,
        provision_cost=3,
        repair_cost=5,      # remote, no shipyard
        crew_cost=8,        # most expensive crew
    ),
    Port(
        id="crosswind_isle", name="Crosswind Isle", region="East Indies",
        description="Free port at the junction of all trade winds. Everything passes through, nothing stays cheap for long.",
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
        ],
        port_fee=6,
        provision_cost=2,
        repair_cost=3,
        crew_cost=5,
    ),
]}
