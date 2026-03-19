"""Infrastructure content — warehouse tiers and port availability.

Design rules:
  - Depots are cheap enough to be a real early investment (day 10-20 range).
  - Regional warehouses are mid-game commitments (post first contract completion).
  - Commercial warehouses are late-game power (galleon-era capital).
  - Not every port gets every tier. Shipyard ports get commercial.
  - Upkeep is real — a forgotten warehouse drains capital.
  - Capacity is large enough to enable staging, not so large it bypasses timing.
"""

from portlight.engine.infrastructure import WarehouseTier, WarehouseTierSpec

WAREHOUSE_TIERS: dict[WarehouseTier, WarehouseTierSpec] = {
    WarehouseTier.DEPOT: WarehouseTierSpec(
        tier=WarehouseTier.DEPOT,
        name="Small Depot",
        capacity=20,
        lease_cost=50,
        upkeep_per_day=1,
        description="A rented corner of a dockside warehouse. Enough to stage a few crates.",
    ),
    WarehouseTier.REGIONAL: WarehouseTierSpec(
        tier=WarehouseTier.REGIONAL,
        name="Regional Warehouse",
        capacity=50,
        lease_cost=200,
        upkeep_per_day=3,
        description="A proper warehouse with your name on the door. Real staging capacity.",
    ),
    WarehouseTier.COMMERCIAL: WarehouseTierSpec(
        tier=WarehouseTier.COMMERCIAL,
        name="Commercial Warehouse",
        capacity=100,
        lease_cost=500,
        upkeep_per_day=6,
        description="A merchant house warehouse. Full commercial staging operation.",
    ),
}


# Which ports allow which warehouse tiers
# Shipyard ports and major trade hubs get all tiers.
# Smaller ports cap at regional.
# Remote ports cap at depot.
PORT_WAREHOUSE_TIERS: dict[str, list[WarehouseTier]] = {
    # Mediterranean
    "porto_novo":    [WarehouseTier.DEPOT, WarehouseTier.REGIONAL, WarehouseTier.COMMERCIAL],
    "al_manar":      [WarehouseTier.DEPOT, WarehouseTier.REGIONAL, WarehouseTier.COMMERCIAL],
    "silva_bay":     [WarehouseTier.DEPOT, WarehouseTier.REGIONAL, WarehouseTier.COMMERCIAL],
    # West Africa
    "sun_harbor":    [WarehouseTier.DEPOT, WarehouseTier.REGIONAL],
    "palm_cove":     [WarehouseTier.DEPOT],
    "iron_point":    [WarehouseTier.DEPOT, WarehouseTier.REGIONAL],
    # East Indies
    "jade_port":     [WarehouseTier.DEPOT, WarehouseTier.REGIONAL, WarehouseTier.COMMERCIAL],
    "monsoon_reach": [WarehouseTier.DEPOT, WarehouseTier.REGIONAL, WarehouseTier.COMMERCIAL],
    "silk_haven":    [WarehouseTier.DEPOT, WarehouseTier.REGIONAL],
    "crosswind_isle": [WarehouseTier.DEPOT, WarehouseTier.REGIONAL],
}


def available_tiers(port_id: str) -> list[WarehouseTierSpec]:
    """Get warehouse tiers available at a port."""
    tiers = PORT_WAREHOUSE_TIERS.get(port_id, [])
    return [WAREHOUSE_TIERS[t] for t in tiers]


def get_tier_spec(tier: WarehouseTier) -> WarehouseTierSpec:
    """Get the spec for a warehouse tier."""
    return WAREHOUSE_TIERS[tier]
