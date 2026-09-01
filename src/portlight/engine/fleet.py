"""Fleet management engine — multi-ship operations.

The player's flagship is captain.ship. Docked ships are in captain.fleet.
Captain.cargo is always the flagship's cargo. When switching ships,
cargos swap between the flagship and the OwnedShip entry.

Pure functions — callers decide what to mutate.
"""

from __future__ import annotations

from portlight.engine.models import (
    Captain,
    CargoItem,
    OwnedShip,
    Ship,
)


def dock_ship(
    captain: Captain,
    port_id: str,
) -> str | None:
    """Move the flagship to the fleet as a docked ship at the given port.

    Requires another ship docked at the same port to switch to.
    Returns error string or None on success.
    """
    if not captain.ship:
        return "No ship to dock"

    # Find a ship docked at this port to switch to
    candidates = [
        (i, owned) for i, owned in enumerate(captain.fleet)
        if owned.docked_port_id == port_id
    ]
    if not candidates:
        return "No other ship at this port to switch to"

    # Switch: move flagship to fleet, promote first candidate to flagship
    idx, new_flagship = candidates[0]

    # Create OwnedShip from current flagship
    docked_entry = OwnedShip(
        ship=captain.ship,
        docked_port_id=port_id,
        cargo=list(captain.cargo),
    )

    # Promote the docked ship to flagship
    captain.ship = new_flagship.ship
    captain.cargo = list(new_flagship.cargo)

    # Replace the promoted ship with the docked flagship
    captain.fleet[idx] = docked_entry

    return None


def board_ship(
    captain: Captain,
    ship_name: str,
    port_id: str,
) -> str | None:
    """Switch flagship to a named docked ship at the same port.

    Returns error string or None on success.
    """
    if not captain.ship:
        return "No active ship"

    for i, owned in enumerate(captain.fleet):
        if owned.docked_port_id == port_id and (
            owned.ship.name.lower() == ship_name.lower()
            or owned.ship.template_id.lower() == ship_name.lower()
        ):
            # Swap flagship and docked ship
            docked_entry = OwnedShip(
                ship=captain.ship,
                docked_port_id=port_id,
                cargo=list(captain.cargo),
            )
            captain.ship = owned.ship
            captain.cargo = list(owned.cargo)
            captain.fleet[i] = docked_entry
            return None

    return f"No ship named '{ship_name}' docked at this port"


def transfer_cargo(
    captain: Captain,
    good_id: str,
    qty: int,
    from_ship_name: str,
    to_ship_name: str,
    port_id: str,
) -> str | None:
    """Move cargo between two ships at the same port.

    Ship names match against flagship name/template_id and fleet entries.
    Returns error string or None on success.
    """
    from portlight.content.upgrades import UPGRADES
    from portlight.engine.ship_stats import resolve_cargo_capacity

    # Resolve source and destination (flagship or fleet entry)
    def _find_ship(name: str) -> tuple[Ship, list[CargoItem], str] | None:
        """Returns (ship, cargo_list, location) or None."""
        if captain.ship and (
            captain.ship.name.lower() == name.lower()
            or captain.ship.template_id.lower() == name.lower()
        ):
            return captain.ship, captain.cargo, "flagship"
        for owned in captain.fleet:
            if owned.docked_port_id == port_id and (
                owned.ship.name.lower() == name.lower()
                or owned.ship.template_id.lower() == name.lower()
            ):
                return owned.ship, owned.cargo, "fleet"
        return None

    src = _find_ship(from_ship_name)
    if src is None:
        return f"Ship '{from_ship_name}' not found at this port"
    dst = _find_ship(to_ship_name)
    if dst is None:
        return f"Ship '{to_ship_name}' not found at this port"

    _src_ship, src_cargo, _ = src
    dst_ship, dst_cargo, _ = dst

    from portlight.engine.economy import cargo_quantity, cargo_weight, consume_cargo_fifo, item_weight

    avail = cargo_quantity(src_cargo, good_id)
    if avail < qty:
        return f"Only {avail} units of {good_id} on {from_ship_name}"

    dst_weight = cargo_weight(dst_cargo)
    dst_cap = resolve_cargo_capacity(dst_ship, UPGRADES)
    added = item_weight(good_id, qty)
    if dst_weight + added > dst_cap:
        space = dst_cap - dst_weight
        return f"Only {space} cargo space on {to_ship_name}"

    slices = consume_cargo_fifo(src_cargo, good_id, qty)
    for sl in slices:
        dst_item = next(
            (item for item in dst_cargo
             if item.good_id == good_id and item.acquired_port == sl.acquired_port),
            None,
        )
        if dst_item:
            dst_item.quantity += sl.quantity
            dst_item.cost_basis += sl.cost_basis
            dst_item.acquired_day = max(dst_item.acquired_day, sl.acquired_day)
        else:
            dst_cargo.append(CargoItem(
                good_id=good_id,
                quantity=sl.quantity,
                cost_basis=sl.cost_basis,
                acquired_port=sl.acquired_port,
                acquired_region=sl.acquired_region,
                acquired_day=sl.acquired_day,
            ))

    return None


def sell_docked_ship(
    captain: Captain,
    ship_name: str,
    port_id: str,
) -> tuple[int, str] | str:
    """Sell a docked ship at a shipyard. Returns (silver_gained, ship_name) or error."""
    from portlight.content.ships import SHIPS

    for i, owned in enumerate(captain.fleet):
        if owned.docked_port_id == port_id and (
            owned.ship.name.lower() == ship_name.lower()
            or owned.ship.template_id.lower() == ship_name.lower()
        ):
            if owned.cargo:
                return "Ship has cargo — transfer it first"
            template = SHIPS.get(owned.ship.template_id)
            hull_ratio = owned.ship.hull / max(1, owned.ship.hull_max)
            base_value = template.price if template else 0
            sale_value = int(base_value * 0.3 * hull_ratio)
            sold_name = owned.ship.name
            captain.silver += sale_value
            captain.fleet.pop(i)
            return sale_value, sold_name

    return f"No ship named '{ship_name}' docked at this port"


def fleet_daily_wages(captain: Captain) -> int:
    """Total daily wage bill across all fleet ships (docked crews too).

    Does not include the flagship — that's handled by voyage.py.
    """
    from portlight.content.ships import SHIPS
    total = 0
    for owned in captain.fleet:
        template = SHIPS.get(owned.ship.template_id)
        daily_wage = template.daily_wage if template else 1
        total += daily_wage * owned.ship.crew
    return total
