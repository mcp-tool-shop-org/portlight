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

from portlight.engine.models import CargoItem, GoodCategory, MarketSlot, Port
from portlight.receipts.models import TradeAction, TradeReceipt

if TYPE_CHECKING:
    from portlight.engine.captain_identity import PricingModifiers
    from portlight.engine.models import Captain, WorldState


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


def tick_markets(ports: dict[str, Port], days: int = 1, rng: random.Random | None = None) -> list[str]:
    """Advance all port markets by `days`. Returns list of shock messages (if any)."""
    rng = rng or random.Random()
    messages: list[str] = []
    for port in ports.values():
        for slot in port.market:
            for _ in range(days):
                # Drift toward target (stronger pull when far from target)
                diff = slot.stock_target - slot.stock_current
                if abs(diff) <= 0:
                    pass
                elif abs(diff) > slot.restock_rate:
                    # Proportional restock: faster recovery when further from target
                    pull = slot.restock_rate * (1 + abs(diff) / slot.stock_target * 0.5)
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


def _cargo_slot(captain: Captain, good_id: str) -> CargoItem | None:
    for item in captain.cargo:
        if item.good_id == good_id:
            return item
    return None


def _cargo_weight(captain: Captain) -> float:
    return sum(item.quantity for item in captain.cargo)


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
        return f"{good_id} not available at {port.name}"
    if qty <= 0:
        return "Quantity must be positive"
    if qty > slot.stock_current:
        return f"Only {slot.stock_current} units available"

    total = slot.buy_price * qty
    if total > captain.silver:
        return f"Need {total} silver, have {captain.silver}"

    # Check cargo capacity
    ship = captain.ship
    if ship is None:
        return "No ship"
    current_weight = _cargo_weight(captain)
    good = goods_table.get(good_id)
    weight_per = good.weight_per_unit if good else 1.0  # type: ignore[union-attr]
    if current_weight + qty * weight_per > ship.cargo_capacity:
        return "Not enough cargo space"

    # Execute
    stock_before = slot.stock_current
    captain.silver -= total
    slot.stock_current -= qty

    existing = _cargo_slot(captain, good_id)
    if existing:
        existing.cost_basis += total
        existing.quantity += qty
    else:
        captain.cargo.append(CargoItem(good_id=good_id, quantity=qty, cost_basis=total))

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
    seq: int = 0,
) -> TradeReceipt | str:
    """Sell goods to port. Returns TradeReceipt on success, error string on failure."""
    slot = next((s for s in port.market if s.good_id == good_id), None)
    if slot is None:
        return f"{port.name} doesn't trade {good_id}"
    if qty <= 0:
        return "Quantity must be positive"

    existing = _cargo_slot(captain, good_id)
    if existing is None or existing.quantity < qty:
        have = existing.quantity if existing else 0
        return f"Only have {have} units of {good_id}"

    # Execute
    stock_before = slot.stock_current
    total = slot.sell_price * qty
    captain.silver += total
    slot.stock_current += qty

    # Increase flood penalty proportional to dump size vs target
    flood_increase = qty / max(slot.stock_target, 1) * 0.3
    slot.flood_penalty = min(1.0, slot.flood_penalty + flood_increase)

    # Update cargo
    existing.quantity -= qty
    if existing.quantity == 0:
        captain.cargo.remove(existing)

    return TradeReceipt(
        receipt_id=_make_receipt_id(captain.name, port.id, good_id, captain.day, seq),
        captain_name=captain.name,
        port_id=port.id,
        good_id=good_id,
        action=TradeAction.SELL,
        quantity=qty,
        unit_price=slot.sell_price,
        total_price=total,
        day=captain.day,
        stock_before=stock_before,
        stock_after=slot.stock_current,
    )
