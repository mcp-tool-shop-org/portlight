"""Economy engine - price computation, stock mutation, trade execution.

Contract:
  - recalculate_prices(port) -> updates all MarketSlot buy/sell prices in place
  - tick_markets(ports, days=1) -> drift all stocks toward target, apply shocks
  - execute_buy(captain, port, good_id, qty) -> TradeReceipt | error string
  - execute_sell(captain, port, good_id, qty) -> TradeReceipt | error string

Price formula (Option 1.5 - lightweight scarcity):
  scarcity_ratio = stock_target / max(stock_current, 1)
  raw_price = base_price * scarcity_ratio / local_affinity
  buy_price  = round(raw_price * (1 + spread / 2))
  sell_price = round(raw_price * (1 - spread / 2) * (1 - flood_penalty))

Anti-dominance:
  - flood_penalty rises when player sells large quantities (diminishing margins)
  - flood_penalty decays over time (market absorbs goods)
  - Stronger restock pulls stock toward target faster
  - Regional shocks occasionally disrupt supply chains
"""

from __future__ import annotations

import hashlib
import random
from typing import TYPE_CHECKING

from portlight.engine.models import CargoItem, GoodCategory, Port, PortFeature
from portlight.receipts.models import TradeAction, TradeReceipt

if TYPE_CHECKING:
    from portlight.engine.captain_identity import PricingModifiers
    from portlight.engine.models import Captain


def recalculate_prices(
    port: Port,
    goods_table: dict[str, object],
    pricing: "PricingModifiers | None" = None,
) -> None:
    """Recompute buy/sell prices for every market slot in a port.

    If pricing modifiers are provided (from captain identity), they affect
    the final buy/sell prices the player sees.
    """
    for slot in port.market:
        good = goods_table.get(slot.good_id)
        if good is None:
            continue
        base = good.base_price  # type: ignore[union-attr]
        scarcity = slot.stock_target / max(slot.stock_current, 1)
        raw = base * scarcity / max(slot.local_affinity, 0.1)

        buy_mult = 1.0
        sell_mult_cap = 1.0
        if pricing:
            buy_mult = pricing.buy_price_mult
            sell_mult_cap = pricing.sell_price_mult
            # Luxury sell bonus for luxury goods
            if pricing.luxury_sell_bonus > 0:
                category = good.category if hasattr(good, "category") else None  # type: ignore[union-attr]
                if category == GoodCategory.LUXURY:
                    sell_mult_cap += pricing.luxury_sell_bonus

        slot.buy_price = max(1, round(raw * (1 + slot.spread / 2) * buy_mult))
        # Flood penalty reduces sell price - dumping the same port tanks your margins
        flood_mult = 1 - slot.flood_penalty * 0.5  # up to 50% sell price reduction
        slot.sell_price = max(1, round(raw * (1 - slot.spread / 2) * flood_mult * sell_mult_cap))


def tick_markets(
    ports: dict[str, Port], days: int = 1, rng: random.Random | None = None,
    current_day: int = 0,
) -> list[str]:
    """Advance all port markets by `days`. Returns list of shock messages (if any).

    If current_day is provided, seasonal demand modifiers are applied.
    """
    rng = rng or random.Random()
    messages: list[str] = []
    for port in ports.values():
        # Get seasonal profile for this port's region
        _seasonal = None
        if current_day > 0:
            from portlight.content.seasons import get_seasonal_profile
            _seasonal = get_seasonal_profile(port.region, current_day)

        for slot in port.market:
            for _ in range(days):
                # Drift toward target (stronger pull when far from target)
                diff = slot.stock_target - slot.stock_current
                if abs(diff) <= 0:
                    pass
                elif abs(diff) > slot.restock_rate:
                    # Proportional restock: faster recovery when further from target
                    pull = slot.restock_rate * (1 + abs(diff) / max(slot.stock_target, 1) * 0.5)
                    pull = pull if diff > 0 else -pull * 0.5
                    slot.stock_current += int(round(pull))
                else:
                    slot.stock_current += diff

                # Flood penalty decay (markets absorb goods over time)
                if slot.flood_penalty > 0:
                    slot.flood_penalty = max(0.0, slot.flood_penalty - 0.05)

                # Random shock (8% chance per day)
                if rng.random() < 0.08:
                    shock = rng.randint(-4, 4)
                    slot.stock_current = max(0, slot.stock_current + shock)

                # Seasonal demand pull (shifts stock target temporarily)
                if _seasonal and slot.good_id in _seasonal.market_effects:
                    demand_mult = _seasonal.market_effects[slot.good_id]
                    if demand_mult > 1.0:
                        # High demand: drain stock faster (consumers buy more)
                        drain = int((demand_mult - 1.0) * slot.restock_rate * 0.5)
                        slot.stock_current = max(0, slot.stock_current - drain)
                    elif demand_mult < 1.0:
                        # Low demand / abundance: stock accumulates
                        surplus = int((1.0 - demand_mult) * slot.restock_rate * 0.5)
                        slot.stock_current += surplus

        # Regional supply shock (3% chance per port per day tick)
        if rng.random() < 0.03 * days:
            shock_slot = rng.choice(port.market) if port.market else None
            if shock_slot:
                direction = rng.choice([-1, 1])
                magnitude = rng.randint(5, 12)
                shock_slot.stock_current = max(0, shock_slot.stock_current + direction * magnitude)
                good_name = shock_slot.good_id
                if direction > 0:
                    messages.append(f"Supply glut: {good_name} floods {port.name}")
                else:
                    messages.append(f"Shortage: {good_name} scarce at {port.name}")

    return messages


def _goods_table(goods_table: dict[str, object] | None = None) -> dict[str, object]:
    if goods_table is not None:
        return goods_table
    from portlight.content.goods import GOODS
    return GOODS


def item_weight(
    good_id: str,
    quantity: int,
    goods_table: dict[str, object] | None = None,
) -> float:
    """Hold/warehouse weight for a quantity of one good."""
    good = _goods_table(goods_table).get(good_id)
    weight_per = getattr(good, "weight_per_unit", 1.0) if good else 1.0
    return quantity * float(weight_per)


def cargo_weight(
    items,
    goods_table: dict[str, object] | None = None,
) -> float:
    """Hold weight: sum(quantity * goods[id].weight_per_unit)."""
    return sum(item_weight(item.good_id, item.quantity, goods_table) for item in items)


def cargo_quantity(items, good_id: str) -> int:
    """Total quantity of good_id across every matching lot."""
    return sum(item.quantity for item in items if item.good_id == good_id)


def consume_cargo_fifo(items: list, good_id: str, qty: int) -> list[CargoItem]:
    """Remove qty of good_id FIFO across lots. Mutates items; drops empty lots.

    Returns consumed slices with proportional cost_basis and original provenance.
    """
    remaining = qty
    consumed: list[CargoItem] = []
    i = 0
    while remaining > 0 and i < len(items):
        item = items[i]
        if item.good_id != good_id:
            i += 1
            continue
        take = min(item.quantity, remaining)
        item_cost = getattr(item, "cost_basis", 0) or 0
        cost_per = item_cost / item.quantity if item.quantity else 0
        leftover_qty = item.quantity - take
        leftover_cost = round(cost_per * leftover_qty) if leftover_qty else 0
        take_cost = item_cost - leftover_cost
        consumed.append(CargoItem(
            good_id=item.good_id,
            quantity=take,
            cost_basis=take_cost,
            acquired_port=getattr(item, "acquired_port", "") or "",
            acquired_region=getattr(item, "acquired_region", "") or "",
            acquired_day=getattr(item, "acquired_day", 0) or 0,
        ))
        if hasattr(item, "cost_basis"):
            item.cost_basis = leftover_cost
        item.quantity = leftover_qty
        remaining -= take
        if item.quantity <= 0:
            items.pop(i)
        else:
            i += 1
    return consumed


def _cargo_slot(captain: Captain, good_id: str) -> CargoItem | None:
    for item in captain.cargo:
        if item.good_id == good_id:
            return item
    return None


def _cargo_weight(captain: Captain, goods_table: dict[str, object] | None = None) -> float:
    return cargo_weight(captain.cargo, goods_table)


def _make_receipt_id(captain_name: str, port_id: str, good_id: str, day: int, seq: int) -> str:
    raw = f"{captain_name}:{port_id}:{good_id}:{day}:{seq}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def execute_buy(
    captain: Captain, port: Port, good_id: str, qty: int,
    goods_table: dict[str, object], seq: int = 0,
) -> TradeReceipt | str:
    """Buy goods from port. Returns TradeReceipt on success, error string on failure."""
    slot = next((s for s in port.market if s.good_id == good_id), None)
    if slot is None:
        # Try matching by display name (case-insensitive) and suggest the correct ID
        for s in port.market:
            g = goods_table.get(s.good_id)
            if g and getattr(g, "name", "").lower().replace(" ", "_") == good_id.lower():
                return f"{good_id} not available at {port.name} -- did you mean: {s.good_id}"
        return f"{good_id} not available at {port.name}"
    if qty <= 0:
        return "Quantity must be positive"
    if qty > slot.stock_current:
        return f"Only {slot.stock_current} units available -- try: buy {good_id} {slot.stock_current}"

    total = slot.buy_price * qty
    if total > captain.silver:
        return f"Need {total} silver, have {captain.silver}"

    # Check cargo capacity (with upgrade bonuses)
    ship = captain.ship
    if ship is None:
        return "No ship"
    from portlight.content.upgrades import UPGRADES
    from portlight.engine.ship_stats import resolve_cargo_capacity
    effective_capacity = resolve_cargo_capacity(ship, UPGRADES)
    current_weight = _cargo_weight(captain, goods_table)
    good = goods_table.get(good_id)
    weight_per = good.weight_per_unit if good else 1.0  # type: ignore[union-attr]
    if current_weight + qty * weight_per > effective_capacity:
        return "Not enough cargo space"

    # Execute
    stock_before = slot.stock_current
    captain.silver -= total
    slot.stock_current -= qty

    existing = next(
        (c for c in captain.cargo
         if c.good_id == good_id and c.acquired_port == port.id),
        None,
    )
    if existing:
        # Same good from same port — merge; refresh acquired_day so a later
        # buy into an aged lot cannot skip the same-port sellback window.
        existing.cost_basis += total
        existing.quantity += qty
        existing.acquired_day = max(existing.acquired_day, captain.day)
    else:
        # New provenance lot (different port or first purchase)
        captain.cargo.append(CargoItem(
            good_id=good_id, quantity=qty, cost_basis=total,
            acquired_port=port.id, acquired_region=port.region,
            acquired_day=captain.day,
        ))

    return TradeReceipt(
        receipt_id=_make_receipt_id(captain.name, port.id, good_id, captain.day, seq),
        captain_name=captain.name,
        port_id=port.id,
        good_id=good_id,
        action=TradeAction.BUY,
        quantity=qty,
        unit_price=slot.buy_price,
        total_price=total,
        day=captain.day,
        stock_before=stock_before,
        stock_after=slot.stock_current,
    )


def execute_sell(
    captain: Captain, port: Port, good_id: str, qty: int,
    goods_table: dict[str, object] | None = None,
    *,
    seq: int = 0,
) -> TradeReceipt | str:
    """Sell goods to port. Returns TradeReceipt on success, error string on failure.

    `seq` is keyword-only so a positional 5th argument is the goods table
    (or a legacy integer sequence number from older callers).
    """
    # Live session used to pass seq positionally as the 5th argument.
    if isinstance(goods_table, int):
        seq = goods_table
        goods_table = None

    table = _goods_table(goods_table)
    good = table.get(good_id)
    if good and getattr(good, "category", None) == GoodCategory.CONTRABAND:
        if PortFeature.BLACK_MARKET not in port.features:
            return f"The harbormaster won't touch {good_id}. Try somewhere less official."

    slot = next((s for s in port.market if s.good_id == good_id), None)
    if slot is None:
        return f"{port.name} doesn't trade {good_id}"
    if qty <= 0:
        return "Quantity must be positive"

    have = cargo_quantity(captain.cargo, good_id)
    if have < qty:
        return f"Only have {have} units of {good_id}"

    # Anti-exploit: cap same-port sellback per lot (not just the first stack)
    # when that lot was acquired at this port within 3 days.
    slices = consume_cargo_fifo(captain.cargo, good_id, qty)
    stock_before = slot.stock_current
    total = 0
    for sl in slices:
        unit_price = slot.sell_price
        same_port_sellback = (
            sl.acquired_port == port.id
            and (captain.day - sl.acquired_day) <= 3
        )
        if same_port_sellback and sl.quantity > 0:
            cost_per_unit = sl.cost_basis / sl.quantity
            if unit_price > cost_per_unit:
                unit_price = max(1, round(cost_per_unit))
        total += unit_price * sl.quantity

    captain.silver += total
    slot.stock_current += qty

    flood_increase = qty / max(slot.stock_target, 1) * 0.3
    slot.flood_penalty = min(1.0, slot.flood_penalty + flood_increase)

    unit_price = round(total / qty) if qty else 0
    return TradeReceipt(
        receipt_id=_make_receipt_id(captain.name, port.id, good_id, captain.day, seq),
        captain_name=captain.name,
        port_id=port.id,
        good_id=good_id,
        action=TradeAction.SELL,
        quantity=qty,
        unit_price=unit_price,
        total_price=total,
        day=captain.day,
        stock_before=stock_before,
        stock_after=slot.stock_current,
    )


# ---------------------------------------------------------------------------
# Anti-soft-lock: dock work and gear sell-back
# ---------------------------------------------------------------------------

def work_docks(captain: "Captain", rng: random.Random) -> int:
    """Work the docks for a day. Returns silver earned (3-5).

    This is a safety valve for players stranded with no silver and no
    tradeable cargo at the current port.
    """
    earned = rng.randint(3, 5)
    captain.silver += earned
    captain.day += 1
    return earned


def sell_gear_value(item_id: str, weapon_tables: dict[str, object]) -> int | None:
    """Get sell-back price for a weapon/armor item (50% of buy price).

    Returns None if item not found in tables.
    """
    weapon = weapon_tables.get(item_id)
    if weapon is None:
        return None
    price = getattr(weapon, "silver_cost", None) or getattr(weapon, "cost", 0)
    return max(1, price // 2)
