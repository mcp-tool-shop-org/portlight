"""Infrastructure engine — commercial assets that change how trade is executed.

Warehouses, broker offices, licenses, insurance, credit all live here.
3D-1 ships warehouses. Later sub-packets add the rest.

Design law:
  - Every asset must change trade timing, scale, or access — not just buff a number.
  - Provenance is preserved through all storage operations.
  - Upkeep is real. Assets that aren't maintained decay or close.
  - Physical presence required: deposit/withdraw only when docked at the port.

Warehouse lifecycle:
  - lease_warehouse(state, port_id, tier) → opens a lease
  - deposit_cargo(state, port_id, captain, good_id, qty) → ship → warehouse
  - withdraw_cargo(state, port_id, captain, good_id, qty) → warehouse → ship
  - tick_infrastructure(state, day) → deducts upkeep, closes defaulted leases
  - warehouse_inventory(state, port_id) → read-only view of stored lots
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from portlight.engine.models import Captain, ReputationState


# ---------------------------------------------------------------------------
# Warehouse tier
# ---------------------------------------------------------------------------

class WarehouseTier(str, Enum):
    DEPOT = "depot"                    # small, cheap, starter
    REGIONAL = "regional"              # mid-tier, real staging
    COMMERCIAL = "commercial"          # large, expensive, full power


@dataclass
class WarehouseTierSpec:
    """Static definition of a warehouse tier."""
    tier: WarehouseTier
    name: str
    capacity: int                      # max cargo weight units
    lease_cost: int                    # one-time silver to open
    upkeep_per_day: int                # daily silver cost
    description: str


# ---------------------------------------------------------------------------
# Stored lot (cargo in warehouse, provenance preserved)
# ---------------------------------------------------------------------------

@dataclass
class StoredLot:
    """A single lot of goods in warehouse storage."""
    good_id: str
    quantity: int
    acquired_port: str
    acquired_region: str
    acquired_day: int
    deposited_day: int = 0


# ---------------------------------------------------------------------------
# Warehouse lease (live state)
# ---------------------------------------------------------------------------

@dataclass
class WarehouseLease:
    """An active warehouse at a specific port."""
    id: str
    port_id: str
    tier: WarehouseTier
    capacity: int
    lease_cost: int
    upkeep_per_day: int
    inventory: list[StoredLot] = field(default_factory=list)
    opened_day: int = 0
    upkeep_paid_through: int = 0       # last day upkeep was covered
    active: bool = True

    @property
    def used_capacity(self) -> int:
        return sum(lot.quantity for lot in self.inventory)

    @property
    def free_capacity(self) -> int:
        return max(0, self.capacity - self.used_capacity)


# ---------------------------------------------------------------------------
# Broker office
# ---------------------------------------------------------------------------

class BrokerTier(str, Enum):
    NONE = "none"
    LOCAL = "local"                    # broker contact — foothold
    ESTABLISHED = "established"        # broker house — serious presence


@dataclass
class BrokerOfficeSpec:
    """Static definition of a broker office tier."""
    tier: BrokerTier
    name: str
    purchase_cost: int
    upkeep_per_day: int
    board_quality_bonus: float         # multiplier on premium offer weight (1.5 = 50% more)
    market_signal_bonus: float         # improves shortage/opportunity visibility
    trade_term_modifier: float         # mild spread improvement (0.95 = 5% tighter)
    description: str


@dataclass
class BrokerOffice:
    """A regional broker office — intelligence and commercial quality."""
    region: str
    tier: BrokerTier = BrokerTier.NONE
    opened_day: int = 0
    upkeep_paid_through: int = 0
    active: bool = True


# ---------------------------------------------------------------------------
# License / charter
# ---------------------------------------------------------------------------

@dataclass
class LicenseSpec:
    """Static definition of a purchasable license."""
    id: str
    name: str
    description: str
    region_scope: str | None           # None = global
    purchase_cost: int
    upkeep_per_day: int
    required_trust_tier: str           # min trust to purchase
    required_standing: int             # min regional standing (in scope region)
    required_heat_max: int | None      # max heat allowed (None = no ceiling)
    required_broker_tier: BrokerTier | None  # must have this broker tier in scope region
    effects: dict[str, float] = field(default_factory=dict)
    # Effect keys: "contract_family_unlock", "customs_mult", "premium_offer_mult",
    #              "lawful_board_mult", "luxury_access"


@dataclass
class OwnedLicense:
    """A license the player has purchased."""
    license_id: str
    purchased_day: int
    upkeep_paid_through: int = 0
    active: bool = True


# ---------------------------------------------------------------------------
# Infrastructure state (session-level)
# ---------------------------------------------------------------------------

@dataclass
class InfrastructureState:
    """All commercial infrastructure owned by the player."""
    warehouses: list[WarehouseLease] = field(default_factory=list)
    brokers: list[BrokerOffice] = field(default_factory=list)
    licenses: list[OwnedLicense] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Warehouse ID
# ---------------------------------------------------------------------------

def _warehouse_id(port_id: str, tier: str, day: int) -> str:
    raw = f"wh:{port_id}:{tier}:{day}"
    return hashlib.sha256(raw.encode()).hexdigest()[:12]


# ---------------------------------------------------------------------------
# Lease
# ---------------------------------------------------------------------------

def lease_warehouse(
    state: InfrastructureState,
    captain: "Captain",
    port_id: str,
    tier_spec: WarehouseTierSpec,
    day: int,
) -> WarehouseLease | str:
    """Open a warehouse lease at a port. Returns lease or error string."""
    # Check for existing active warehouse at this port
    existing = next(
        (w for w in state.warehouses if w.port_id == port_id and w.active),
        None,
    )
    if existing:
        if existing.tier == tier_spec.tier:
            return f"Already have a {tier_spec.name} at this port"
        # Upgrading: close old, open new (keep inventory if it fits)
        old_inventory = list(existing.inventory)
        existing.active = False
    else:
        old_inventory = []

    # Cost check
    if tier_spec.lease_cost > captain.silver:
        return f"Need {tier_spec.lease_cost} silver to lease {tier_spec.name}, have {captain.silver}"

    captain.silver -= tier_spec.lease_cost

    lease = WarehouseLease(
        id=_warehouse_id(port_id, tier_spec.tier.value, day),
        port_id=port_id,
        tier=tier_spec.tier,
        capacity=tier_spec.capacity,
        lease_cost=tier_spec.lease_cost,
        upkeep_per_day=tier_spec.upkeep_per_day,
        opened_day=day,
        upkeep_paid_through=day,
        active=True,
    )

    # Transfer old inventory (drop excess if downgrading, which shouldn't happen but be safe)
    transferred = 0
    for lot in old_inventory:
        if transferred + lot.quantity <= lease.capacity:
            lease.inventory.append(lot)
            transferred += lot.quantity
        else:
            # Partial transfer
            remaining = lease.capacity - transferred
            if remaining > 0:
                lot.quantity = remaining
                lease.inventory.append(lot)
            break

    state.warehouses.append(lease)
    return lease


# ---------------------------------------------------------------------------
# Deposit
# ---------------------------------------------------------------------------

def deposit_cargo(
    state: InfrastructureState,
    port_id: str,
    captain: "Captain",
    good_id: str,
    quantity: int,
    day: int,
) -> int | str:
    """Move cargo from ship to warehouse. Returns quantity deposited or error."""
    warehouse = next(
        (w for w in state.warehouses if w.port_id == port_id and w.active),
        None,
    )
    if warehouse is None:
        return "No warehouse at this port"
    if quantity <= 0:
        return "Quantity must be positive"

    # Find cargo in ship hold
    cargo_item = next(
        (c for c in captain.cargo if c.good_id == good_id),
        None,
    )
    if cargo_item is None or cargo_item.quantity < quantity:
        have = cargo_item.quantity if cargo_item else 0
        return f"Only have {have} units of {good_id} in hold"

    # Check warehouse capacity
    if quantity > warehouse.free_capacity:
        return f"Warehouse only has {warehouse.free_capacity} units of space"

    # Execute transfer: ship → warehouse (preserve provenance)
    deposit_qty = quantity
    cargo_item.quantity -= deposit_qty
    if cargo_item.quantity == 0:
        captain.cargo.remove(cargo_item)

    # Merge into existing lot with same provenance, or create new
    merged = False
    for lot in warehouse.inventory:
        if (lot.good_id == good_id and
            lot.acquired_port == cargo_item.acquired_port and
            lot.acquired_region == cargo_item.acquired_region):
            lot.quantity += deposit_qty
            merged = True
            break

    if not merged:
        warehouse.inventory.append(StoredLot(
            good_id=good_id,
            quantity=deposit_qty,
            acquired_port=cargo_item.acquired_port,
            acquired_region=cargo_item.acquired_region,
            acquired_day=cargo_item.acquired_day,
            deposited_day=day,
        ))

    return deposit_qty


# ---------------------------------------------------------------------------
# Withdraw
# ---------------------------------------------------------------------------

def withdraw_cargo(
    state: InfrastructureState,
    port_id: str,
    captain: "Captain",
    good_id: str,
    quantity: int,
    source_port: str | None = None,
) -> int | str:
    """Move cargo from warehouse to ship. Returns quantity withdrawn or error.

    If source_port is specified, only withdraw from lots with that provenance.
    """
    from portlight.engine.models import CargoItem

    warehouse = next(
        (w for w in state.warehouses if w.port_id == port_id and w.active),
        None,
    )
    if warehouse is None:
        return "No warehouse at this port"
    if quantity <= 0:
        return "Quantity must be positive"

    # Check ship capacity
    ship = captain.ship
    if ship is None:
        return "No ship"
    cargo_weight = sum(c.quantity for c in captain.cargo)
    free_space = ship.cargo_capacity - cargo_weight
    if quantity > free_space:
        return f"Ship only has {free_space} units of cargo space"

    # Find matching lots in warehouse
    matching = [
        lot for lot in warehouse.inventory
        if lot.good_id == good_id and (source_port is None or lot.acquired_port == source_port)
    ]
    available = sum(lot.quantity for lot in matching)
    if available < quantity:
        return f"Only {available} units of {good_id} in warehouse" + (
            f" from {source_port}" if source_port else ""
        )

    # Execute transfer: warehouse → ship (preserve provenance per lot)
    remaining = quantity
    for lot in matching:
        if remaining <= 0:
            break
        take = min(lot.quantity, remaining)
        lot.quantity -= take
        remaining -= take

        # Add to ship cargo with original provenance
        existing = next(
            (c for c in captain.cargo
             if c.good_id == good_id and c.acquired_port == lot.acquired_port),
            None,
        )
        if existing:
            existing.quantity += take
        else:
            captain.cargo.append(CargoItem(
                good_id=good_id,
                quantity=take,
                cost_basis=0,  # cost basis lost on warehouse transfer (trade P&L tracked separately)
                acquired_port=lot.acquired_port,
                acquired_region=lot.acquired_region,
                acquired_day=lot.acquired_day,
            ))

    # Clean up empty lots
    warehouse.inventory = [lot for lot in warehouse.inventory if lot.quantity > 0]

    return quantity


# ---------------------------------------------------------------------------
# Upkeep tick
# ---------------------------------------------------------------------------

def tick_infrastructure(
    state: InfrastructureState,
    captain: "Captain",
    day: int,
) -> list[str]:
    """Daily infrastructure upkeep. Deducts costs, closes defaulted assets.

    Returns list of status messages.
    """
    messages: list[str] = []

    # --- Warehouse upkeep ---
    for warehouse in state.warehouses:
        if not warehouse.active:
            continue

        days_owed = day - warehouse.upkeep_paid_through
        if days_owed <= 0:
            continue

        cost = days_owed * warehouse.upkeep_per_day
        if captain.silver >= cost:
            captain.silver -= cost
            warehouse.upkeep_paid_through = day
        else:
            affordable_days = captain.silver // warehouse.upkeep_per_day if warehouse.upkeep_per_day > 0 else 0
            if affordable_days > 0:
                captain.silver -= affordable_days * warehouse.upkeep_per_day
                warehouse.upkeep_paid_through += affordable_days

            unpaid_days = day - warehouse.upkeep_paid_through
            if unpaid_days >= 3:
                warehouse.active = False
                lost_goods = [(lot.good_id, lot.quantity) for lot in warehouse.inventory]
                warehouse.inventory.clear()
                if lost_goods:
                    goods_str = ", ".join(f"{q}x {g}" for g, q in lost_goods)
                    messages.append(
                        f"Warehouse at {warehouse.port_id} closed for non-payment. "
                        f"Goods seized: {goods_str}"
                    )
                else:
                    messages.append(
                        f"Warehouse at {warehouse.port_id} closed for non-payment."
                    )

    # --- Broker office upkeep ---
    from portlight.content.infrastructure import get_broker_spec
    for broker in state.brokers:
        if not broker.active or broker.tier == BrokerTier.NONE:
            continue

        spec = get_broker_spec(broker.region, broker.tier)
        if not spec:
            continue
        upkeep = spec.upkeep_per_day

        days_owed = day - broker.upkeep_paid_through
        if days_owed <= 0:
            continue

        cost = days_owed * upkeep
        if captain.silver >= cost:
            captain.silver -= cost
            broker.upkeep_paid_through = day
        else:
            affordable_days = captain.silver // upkeep if upkeep > 0 else 0
            if affordable_days > 0:
                captain.silver -= affordable_days * upkeep
                broker.upkeep_paid_through += affordable_days

            unpaid_days = day - broker.upkeep_paid_through
            if unpaid_days >= 5:  # brokers are more forgiving than warehouses
                broker.active = False
                messages.append(
                    f"Broker office in {broker.region} closed for non-payment."
                )

    # --- License upkeep ---
    from portlight.content.infrastructure import get_license_spec
    for lic in state.licenses:
        if not lic.active:
            continue

        spec = get_license_spec(lic.license_id)
        if not spec:
            continue
        upkeep = spec.upkeep_per_day

        days_owed = day - lic.upkeep_paid_through
        if days_owed <= 0:
            continue

        cost = days_owed * upkeep
        if captain.silver >= cost:
            captain.silver -= cost
            lic.upkeep_paid_through = day
        else:
            affordable_days = captain.silver // upkeep if upkeep > 0 else 0
            if affordable_days > 0:
                captain.silver -= affordable_days * upkeep
                lic.upkeep_paid_through += affordable_days

            unpaid_days = day - lic.upkeep_paid_through
            if unpaid_days >= 5:  # licenses revoked after 5 days unpaid
                lic.active = False
                messages.append(
                    f"License '{lic.license_id}' revoked for non-payment."
                )

    return messages


# ---------------------------------------------------------------------------
# Queries
# ---------------------------------------------------------------------------

def get_warehouse(state: InfrastructureState, port_id: str) -> WarehouseLease | None:
    """Get the active warehouse at a port, if any."""
    return next(
        (w for w in state.warehouses if w.port_id == port_id and w.active),
        None,
    )


def warehouse_summary(state: InfrastructureState) -> list[WarehouseLease]:
    """Get all active warehouses."""
    return [w for w in state.warehouses if w.active]


# ---------------------------------------------------------------------------
# Broker office operations
# ---------------------------------------------------------------------------

def get_broker(state: InfrastructureState, region: str) -> BrokerOffice | None:
    """Get the active broker office in a region, if any."""
    return next(
        (b for b in state.brokers if b.region == region and b.active and b.tier != BrokerTier.NONE),
        None,
    )


def get_broker_tier(state: InfrastructureState, region: str) -> BrokerTier:
    """Get the broker tier in a region (NONE if no office)."""
    b = get_broker(state, region)
    return b.tier if b else BrokerTier.NONE


def open_broker_office(
    state: InfrastructureState,
    captain: "Captain",
    region: str,
    spec: BrokerOfficeSpec,
    day: int,
) -> BrokerOffice | str:
    """Open or upgrade a broker office in a region."""
    existing = get_broker(state, region)

    if existing:
        if existing.tier == spec.tier:
            return f"Already have a {spec.name} in {region}"
        if existing.tier == BrokerTier.ESTABLISHED and spec.tier == BrokerTier.LOCAL:
            return "Cannot downgrade a broker office"

    if spec.purchase_cost > captain.silver:
        return f"Need {spec.purchase_cost} silver to open {spec.name}, have {captain.silver}"

    captain.silver -= spec.purchase_cost

    if existing:
        # Upgrade in place
        existing.tier = spec.tier
        existing.opened_day = day
        existing.upkeep_paid_through = day
        return existing
    else:
        office = BrokerOffice(
            region=region,
            tier=spec.tier,
            opened_day=day,
            upkeep_paid_through=day,
            active=True,
        )
        state.brokers.append(office)
        return office


# ---------------------------------------------------------------------------
# License operations
# ---------------------------------------------------------------------------

def get_license(state: InfrastructureState, license_id: str) -> OwnedLicense | None:
    """Get an active owned license by ID."""
    return next(
        (lic for lic in state.licenses if lic.license_id == license_id and lic.active),
        None,
    )


def has_license(state: InfrastructureState, license_id: str) -> bool:
    """Check if the player has an active license."""
    return get_license(state, license_id) is not None


def check_license_eligibility(
    state: InfrastructureState,
    spec: LicenseSpec,
    rep: "ReputationState",
) -> str | None:
    """Check if the player meets requirements. Returns error string or None."""
    from portlight.engine.reputation import get_trust_tier

    # Already owned?
    if has_license(state, spec.id):
        return "Already own this license"

    # Trust check
    trust_tier = get_trust_tier(rep)
    trust_rank = {"unproven": 0, "new": 1, "credible": 2, "reliable": 3, "trusted": 4}
    player_trust = trust_rank.get(trust_tier, 0)
    required_trust = trust_rank.get(spec.required_trust_tier, 0)
    if player_trust < required_trust:
        return f"Requires {spec.required_trust_tier} trust (currently {trust_tier})"

    # Standing check (region-scoped)
    if spec.region_scope and spec.required_standing > 0:
        standing = rep.regional_standing.get(spec.region_scope, 0)
        if standing < spec.required_standing:
            return f"Requires {spec.required_standing} standing in {spec.region_scope} (currently {standing})"

    # Heat check
    if spec.required_heat_max is not None and spec.region_scope:
        heat = rep.customs_heat.get(spec.region_scope, 0)
        if heat > spec.required_heat_max:
            return f"Heat too high in {spec.region_scope}: {heat} (max {spec.required_heat_max})"

    # Broker prerequisite
    if spec.required_broker_tier is not None:
        tier_rank = {BrokerTier.NONE: 0, BrokerTier.LOCAL: 1, BrokerTier.ESTABLISHED: 2}
        required_rank = tier_rank.get(spec.required_broker_tier, 0)
        if spec.region_scope:
            # Region-scoped: check specific region
            broker_tier = get_broker_tier(state, spec.region_scope)
            if tier_rank.get(broker_tier, 0) < required_rank:
                return f"Requires {spec.required_broker_tier.value} broker office in {spec.region_scope}"
        else:
            # Global: require the tier in at least one region
            has_any = any(
                tier_rank.get(b.tier, 0) >= required_rank
                for b in state.brokers if b.active
            )
            if not has_any:
                return f"Requires {spec.required_broker_tier.value} broker office in at least one region"

    return None


def purchase_license(
    state: InfrastructureState,
    captain: "Captain",
    spec: LicenseSpec,
    rep: "ReputationState",
    day: int,
) -> OwnedLicense | str:
    """Purchase a license. Returns OwnedLicense or error string."""
    # Eligibility
    err = check_license_eligibility(state, spec, rep)
    if err:
        return err

    # Cost
    if spec.purchase_cost > captain.silver:
        return f"Need {spec.purchase_cost} silver, have {captain.silver}"

    captain.silver -= spec.purchase_cost

    owned = OwnedLicense(
        license_id=spec.id,
        purchased_day=day,
        upkeep_paid_through=day,
        active=True,
    )
    state.licenses.append(owned)
    return owned


# ---------------------------------------------------------------------------
# Board effect computation
# ---------------------------------------------------------------------------

def compute_board_effects(
    state: InfrastructureState,
    region: str,
    license_specs: dict[str, LicenseSpec] | None = None,
) -> dict[str, float]:
    """Compute aggregate board generation effects for a region.

    Returns dict with keys:
      - board_quality_bonus: multiplier on premium offer weight
      - premium_offer_mult: from licenses
      - customs_mult: from licenses
      - lawful_board_mult: from licenses
      - luxury_access: from licenses (0 or 1)
    """
    effects: dict[str, float] = {
        "board_quality_bonus": 1.0,
        "market_signal_bonus": 0.0,
        "trade_term_modifier": 1.0,
        "premium_offer_mult": 1.0,
        "customs_mult": 1.0,
        "lawful_board_mult": 1.0,
        "luxury_access": 0.0,
    }

    # Broker effects
    broker = get_broker(state, region)
    if broker:
        from portlight.content.infrastructure import get_broker_spec
        spec = get_broker_spec(region, broker.tier)
        if spec:
            effects["board_quality_bonus"] = spec.board_quality_bonus
            effects["market_signal_bonus"] = spec.market_signal_bonus
            effects["trade_term_modifier"] = spec.trade_term_modifier

    # License effects (aggregate all active licenses that apply to this region)
    if license_specs:
        for owned in state.licenses:
            if not owned.active:
                continue
            spec = license_specs.get(owned.license_id)
            if spec is None:
                continue
            # Check scope
            if spec.region_scope is not None and spec.region_scope != region:
                continue
            # Apply effects
            for key, value in spec.effects.items():
                if key in effects:
                    if key in ("customs_mult",):
                        effects[key] *= value  # multiplicative
                    elif key in ("luxury_access",):
                        effects[key] = max(effects[key], value)  # flag
                    else:
                        effects[key] *= value  # multiplicative

    return effects
