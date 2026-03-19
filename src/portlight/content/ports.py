"""Phase 1 port network — 10 ports across 3 regions.

Each port has a market with specific goods at specific stock levels.
Affinity > 1 = port produces that good (cheaper to buy).
Affinity < 1 = port consumes that good (more expensive, good to sell here).
"""

from portlight.engine.models import MarketSlot, Port, PortFeature


def _slot(good_id: str, stock: int, target: int, restock: float, affinity: float = 1.0, spread: float = 0.15) -> MarketSlot:
    return MarketSlot(good_id=good_id, stock_current=stock, stock_target=target, restock_rate=restock, local_affinity=affinity, spread=spread)


PORTS: dict[str, Port] = {p.id: p for p in [
    # === Mediterranean ===
    Port(
        id="porto_novo", name="Porto Novo", region="Mediterranean",
        description="A bustling harbor city, gateway to inland trade.",
        features=[PortFeature.SHIPYARD],
        market=[
            _slot("grain",  40, 35, 3.0, affinity=1.3),   # grain producer
            _slot("timber", 20, 25, 2.0, affinity=0.8),
            _slot("iron",   15, 15, 1.5, affinity=1.0),
            _slot("cotton", 10, 12, 1.0, affinity=0.7),
            _slot("rum",    18, 20, 1.5, affinity=1.1),
        ],
        port_fee=5,
    ),
    Port(
        id="al_manar", name="Al-Manar", region="Mediterranean",
        description="Ancient port famed for its spice markets.",
        market=[
            _slot("spice",  30, 25, 2.5, affinity=1.5),   # spice producer
            _slot("silk",   8,  10, 1.0, affinity=0.9),
            _slot("grain",  10, 15, 1.5, affinity=0.6),
            _slot("porcelain", 5, 8, 0.8, affinity=0.7),
            _slot("rum",    12, 15, 1.0, affinity=0.8),
        ],
        port_fee=8,
    ),
    Port(
        id="silva_bay", name="Silva Bay", region="Mediterranean",
        description="Timber-rich bay surrounded by dense forests.",
        features=[PortFeature.SHIPYARD],
        market=[
            _slot("timber", 45, 40, 3.5, affinity=1.5),   # timber producer
            _slot("iron",   20, 18, 2.0, affinity=1.2),
            _slot("grain",  15, 18, 1.5, affinity=0.9),
            _slot("cotton", 8,  10, 1.0, affinity=0.7),
        ],
        port_fee=4,
    ),

    # === West African Coast ===
    Port(
        id="sun_harbor", name="Sun Harbor", region="West Africa",
        description="Golden coast port where cotton and iron change hands.",
        market=[
            _slot("cotton", 35, 30, 3.0, affinity=1.4),   # cotton producer
            _slot("iron",   25, 22, 2.0, affinity=1.3),
            _slot("silk",   3,  5,  0.5, affinity=0.5),
            _slot("spice",  5,  8,  0.8, affinity=0.6),
            _slot("rum",    10, 12, 1.0, affinity=0.9),
        ],
        port_fee=5,
    ),
    Port(
        id="palm_cove", name="Palm Cove", region="West Africa",
        description="A sheltered cove known for its rum distilleries.",
        market=[
            _slot("rum",    40, 35, 3.0, affinity=1.6),   # rum producer
            _slot("grain",  12, 15, 1.5, affinity=0.8),
            _slot("timber", 8,  10, 1.0, affinity=0.7),
            _slot("cotton", 15, 18, 1.5, affinity=1.1),
        ],
        port_fee=3,
    ),
    Port(
        id="iron_point", name="Iron Point", region="West Africa",
        description="Mining settlement at the river mouth. Rich in ore.",
        market=[
            _slot("iron",   50, 45, 4.0, affinity=1.6),   # iron producer
            _slot("grain",  8,  12, 1.0, affinity=0.6),
            _slot("timber", 12, 15, 1.5, affinity=0.9),
            _slot("porcelain", 2, 4, 0.5, affinity=0.4),
        ],
        port_fee=4,
    ),

    # === East Indies ===
    Port(
        id="jade_port", name="Jade Port", region="East Indies",
        description="Porcelain workshops line the waterfront.",
        market=[
            _slot("porcelain", 35, 30, 3.0, affinity=1.5),  # porcelain producer
            _slot("silk",   25, 22, 2.5, affinity=1.3),
            _slot("spice",  15, 18, 1.5, affinity=1.1),
            _slot("grain",  5,  8,  0.8, affinity=0.5),
            _slot("iron",   3,  5,  0.5, affinity=0.4),
        ],
        port_fee=10,
    ),
    Port(
        id="monsoon_reach", name="Monsoon Reach", region="East Indies",
        description="Seasonal winds make this a spice trade crossroads.",
        features=[PortFeature.SHIPYARD],
        market=[
            _slot("spice",  25, 22, 2.5, affinity=1.4),
            _slot("silk",   20, 18, 2.0, affinity=1.2),
            _slot("cotton", 5,  8,  0.8, affinity=0.6),
            _slot("timber", 5,  8,  0.8, affinity=0.5),
            _slot("rum",    8,  10, 1.0, affinity=0.7),
        ],
        port_fee=8,
    ),
    Port(
        id="silk_haven", name="Silk Haven", region="East Indies",
        description="Premier silk market of the eastern waters.",
        market=[
            _slot("silk",   40, 35, 3.5, affinity=1.6),   # silk producer
            _slot("porcelain", 15, 12, 1.5, affinity=1.2),
            _slot("spice",  10, 12, 1.0, affinity=0.9),
            _slot("rum",    5,  8,  0.8, affinity=0.5),
        ],
        port_fee=7,
    ),
    Port(
        id="crosswind_isle", name="Crosswind Isle", region="East Indies",
        description="Free port at the junction of all trade winds. Everything passes through.",
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
    ),
]}
