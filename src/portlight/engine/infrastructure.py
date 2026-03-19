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
    from portlight.engine.models import Captain, CargoItem


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
# Broker office (stub for 3D-2)
# ---------------------------------------------------------------------------

class BrokerTier(str, Enum):
    NONE = "none"
    LOCAL = "local"
    ESTABLISHED = "established"


@dataclass
class BrokerOffice:
    """A regional broker office. Stub — full implementation in 3D-2."""
    region: str
    tier: BrokerTier = BrokerTier.NONE
    opened_day: int = 0


# ---------------------------------------------------------------------------
# Infrastructure state (session-level)
# ---------------------------------------------------------------------------

@dataclass
class InfrastructureState:
    """All commercial infrastructure owned by the player."""
    warehouses: list[WarehouseLease] = field(default_factory=list)
    brokers: list[BrokerOffice] = field(default_factory=list)
    # licenses, insurance, credit added in 3D-2/3D-3


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
    """Daily infrastructure upkeep. Deducts costs, closes defaulted leases.

    Returns list of status messages.
    """
    messages: list[str] = []

    for warehouse in state.warehouses:
        if not warehouse.active:
            continue

        # Calculate days of upkeep owed
        days_owed = day - warehouse.upkeep_paid_through
        if days_owed <= 0:
            continue

        cost = days_owed * warehouse.upkeep_per_day
        if captain.silver >= cost:
            captain.silver -= cost
            warehouse.upkeep_paid_through = day
        else:
            # Partial payment
            affordable_days = captain.silver // warehouse.upkeep_per_day if warehouse.upkeep_per_day > 0 else 0
            if affordable_days > 0:
                captain.silver -= affordable_days * warehouse.upkeep_per_day
                warehouse.upkeep_paid_through += affordable_days

            # Check if too far behind (3+ days unpaid = closure)
            unpaid_days = day - warehouse.upkeep_paid_through
            if unpaid_days >= 3:
                warehouse.active = False
                # Goods are lost (or could be reclaimed for a fee later — keep simple for now)
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
