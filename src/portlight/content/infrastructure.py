"""Infrastructure content — warehouse tiers, broker offices, and licenses.

Design rules:
  - Depots are cheap enough to be a real early investment (day 10-20 range).
  - Regional warehouses are mid-game commitments (post first contract completion).
  - Commercial warehouses are late-game power (galleon-era capital).
  - Not every port gets every tier. Shipyard ports get commercial.
  - Upkeep is real — a forgotten warehouse drains capital.
  - Capacity is large enough to enable staging, not so large it bypasses timing.

Broker offices (3D-2A):
  - Region-level, 2 tiers each (local → established).
  - Each region has a personality: Mediterranean=lawful, West Africa=staples,
    East Indies=long-haul premium.
  - Offices improve board quality, market legibility, and trade terms.

Licenses (3D-2B):
  - 5 licenses gated by standing, trust, heat, and broker prerequisites.
  - Each unlocks premium contract families or formal access in a region.
"""

from portlight.engine.infrastructure import (
    BrokerOfficeSpec,
    BrokerTier,
    LicenseSpec,
    WarehouseTier,
    WarehouseTierSpec,
)

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


# ---------------------------------------------------------------------------
# Broker office specs — region × tier
# ---------------------------------------------------------------------------

# Key: (region, tier) → BrokerOfficeSpec
BROKER_SPECS: dict[tuple[str, BrokerTier], BrokerOfficeSpec] = {
    # --- Mediterranean: lawful procurement, charter work, stable commerce ---
    ("Mediterranean", BrokerTier.LOCAL): BrokerOfficeSpec(
        tier=BrokerTier.LOCAL,
        name="Mediterranean Local Broker",
        purchase_cost=150,
        upkeep_per_day=2,
        board_quality_bonus=1.3,      # 30% more premium offers
        market_signal_bonus=0.15,     # mild shortage visibility
        trade_term_modifier=0.97,     # 3% tighter spreads
        description="A clerk in the harbor exchange. Knows who's buying what.",
    ),
    ("Mediterranean", BrokerTier.ESTABLISHED): BrokerOfficeSpec(
        tier=BrokerTier.ESTABLISHED,
        name="Mediterranean Broker House",
        purchase_cost=400,
        upkeep_per_day=5,
        board_quality_bonus=1.6,      # 60% more premium offers
        market_signal_bonus=0.30,     # strong shortage visibility
        trade_term_modifier=0.94,     # 6% tighter spreads
        description="A proper merchant's office overlooking the quay. Charter work flows through here.",
    ),

    # --- West Africa: staples, return cargo, efficient regional loops ---
    ("West Africa", BrokerTier.LOCAL): BrokerOfficeSpec(
        tier=BrokerTier.LOCAL,
        name="West Africa Local Broker",
        purchase_cost=120,
        upkeep_per_day=2,
        board_quality_bonus=1.25,
        market_signal_bonus=0.20,     # strong on staple shortages
        trade_term_modifier=0.97,
        description="A trader's agent at the coast. Knows the staple routes cold.",
    ),
    ("West Africa", BrokerTier.ESTABLISHED): BrokerOfficeSpec(
        tier=BrokerTier.ESTABLISHED,
        name="West Africa Trade Office",
        purchase_cost=350,
        upkeep_per_day=4,
        board_quality_bonus=1.5,
        market_signal_bonus=0.35,     # excellent staple intelligence
        trade_term_modifier=0.95,
        description="A permanent office with warehousing contacts. Return freight is the specialty.",
    ),

    # --- East Indies: long-haul, premium cargo, high-upside circuits ---
    ("East Indies", BrokerTier.LOCAL): BrokerOfficeSpec(
        tier=BrokerTier.LOCAL,
        name="East Indies Local Broker",
        purchase_cost=200,
        upkeep_per_day=3,
        board_quality_bonus=1.35,     # premium-heavy region
        market_signal_bonus=0.15,
        trade_term_modifier=0.96,     # 4% tighter (luxury margins are already high)
        description="A factor's contact in the spice quarter. Luxury connections.",
    ),
    ("East Indies", BrokerTier.ESTABLISHED): BrokerOfficeSpec(
        tier=BrokerTier.ESTABLISHED,
        name="East Indies Trading House",
        purchase_cost=500,
        upkeep_per_day=6,
        board_quality_bonus=1.7,      # strongest premium board
        market_signal_bonus=0.30,
        trade_term_modifier=0.93,     # 7% tighter (full house advantage)
        description="A merchant house with direct connections to silk and spice guilds. The serious money flows here.",
    ),
}


def get_broker_spec(region: str, tier: BrokerTier) -> BrokerOfficeSpec | None:
    """Get the broker office spec for a region and tier."""
    return BROKER_SPECS.get((region, tier))


def available_broker_tiers(region: str) -> list[BrokerOfficeSpec]:
    """Get all broker tiers available in a region, ordered local → established."""
    result = []
    for t in (BrokerTier.LOCAL, BrokerTier.ESTABLISHED):
        spec = BROKER_SPECS.get((region, t))
        if spec:
            result.append(spec)
    return result


# ---------------------------------------------------------------------------
# License catalog
# ---------------------------------------------------------------------------

LICENSE_CATALOG: dict[str, LicenseSpec] = {
    "med_trade_charter": LicenseSpec(
        id="med_trade_charter",
        name="Mediterranean Trade Charter",
        description="Formal authorization for commercial shipping in Mediterranean waters. "
                    "Opens lawful procurement contracts and reduces customs friction.",
        region_scope="Mediterranean",
        purchase_cost=300,
        upkeep_per_day=3,
        required_trust_tier="credible",
        required_standing=10,
        required_heat_max=5,
        required_broker_tier=BrokerTier.LOCAL,
        effects={"lawful_board_mult": 1.4, "customs_mult": 0.85},
    ),
    "wa_commerce_permit": LicenseSpec(
        id="wa_commerce_permit",
        name="West Africa Commerce Permit",
        description="Trading permit recognized along the West African coast. "
                    "Unlocks staple procurement contracts and return freight priority.",
        region_scope="West Africa",
        purchase_cost=250,
        upkeep_per_day=2,
        required_trust_tier="credible",
        required_standing=8,
        required_heat_max=6,
        required_broker_tier=BrokerTier.LOCAL,
        effects={"lawful_board_mult": 1.3, "customs_mult": 0.90},
    ),
    "ei_access_charter": LicenseSpec(
        id="ei_access_charter",
        name="East Indies Access Charter",
        description="Permission to trade freely in East Indies ports. "
                    "Opens long-haul circuit contracts and premium cargo access.",
        region_scope="East Indies",
        purchase_cost=400,
        upkeep_per_day=4,
        required_trust_tier="reliable",
        required_standing=15,
        required_heat_max=4,
        required_broker_tier=BrokerTier.LOCAL,
        effects={"premium_offer_mult": 1.5, "customs_mult": 0.80},
    ),
    "luxury_goods_permit": LicenseSpec(
        id="luxury_goods_permit",
        name="Luxury Goods Permit",
        description="Cross-regional authorization for luxury commodity trading. "
                    "Grants access to discreet luxury contracts everywhere.",
        region_scope=None,  # global
        purchase_cost=500,
        upkeep_per_day=5,
        required_trust_tier="reliable",
        required_standing=0,  # global, no regional requirement
        required_heat_max=3,
        required_broker_tier=None,  # no broker needed, but trust and heat are steep
        effects={"luxury_access": 1.0, "premium_offer_mult": 1.3},
    ),
    "high_rep_charter": LicenseSpec(
        id="high_rep_charter",
        name="High Reputation Commercial Charter",
        description="Elite commercial authorization recognized in all regions. "
                    "Highest-tier contract board quality and customs privilege.",
        region_scope=None,  # global
        purchase_cost=800,
        upkeep_per_day=7,
        required_trust_tier="trusted",
        required_standing=0,
        required_heat_max=2,
        required_broker_tier=BrokerTier.ESTABLISHED,  # needs established in at least one region (checked at purchase)
        effects={"lawful_board_mult": 1.5, "premium_offer_mult": 1.4, "customs_mult": 0.75},
    ),
}


def get_license_spec(license_id: str) -> LicenseSpec | None:
    """Get a license spec by ID."""
    return LICENSE_CATALOG.get(license_id)


def available_licenses() -> list[LicenseSpec]:
    """Get all license specs, ordered by purchase cost."""
    return sorted(LICENSE_CATALOG.values(), key=lambda s: s.purchase_cost)
