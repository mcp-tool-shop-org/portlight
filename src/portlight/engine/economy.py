"""Economy engine — price computation, stock mutation, trade execution.

Contract:
  - recalculate_prices(port) → updates all MarketSlot buy/sell prices in place
  - tick_markets(ports, days=1) → drift all stocks toward target, apply shocks
  - execute_buy(captain, port, good_id, qty) → TradeReceipt | error string
  - execute_sell(captain, port, good_id, qty) → TradeReceipt | error string

Price formula (Option 1.5 — lightweight scarcity):
  scarcity_ratio = stock_target / max(stock_current, 1)
  raw_price = base_price * scarcity_ratio / local_affinity
  buy_price  = round(raw_price * (1 + spread / 2))
  sell_price = round(raw_price * (1 - spread / 2))

  - When stock_current < stock_target → scarcity → prices rise
  - When stock_current > stock_target → abundance → prices fall
  - spread prevents trivial buy-then-sell-same-port exploits
  - local_affinity > 1 means port produces (cheaper), < 1 means port consumes (pricier)
"""

from __future__ import annotations

import hashlib
import random
from typing import TYPE_CHECKING

from portlight.engine.models import CargoItem, MarketSlot, Port
from portlight.receipts.models import TradeAction, TradeReceipt

if TYPE_CHECKING:
    from portlight.engine.models import Captain, WorldState


def recalculate_prices(port: Port, goods_table: dict[str, object]) -> None:
    """Recompute buy/sell prices for every market slot in a port."""
    for slot in port.market:
        good = goods_table.get(slot.good_id)
        if good is None:
            continue
        base = good.base_price  # type: ignore[union-attr]
        scarcity = slot.stock_target / max(slot.stock_current, 1)
        raw = base * scarcity / max(slot.local_affinity, 0.1)
        slot.buy_price = max(1, round(raw * (1 + slot.spread / 2)))
        slot.sell_price = max(1, round(raw * (1 - slot.spread / 2)))


def tick_markets(ports: dict[str, Port], days: int = 1, rng: random.Random | None = None) -> None:
    """Advance all port markets by `days`. Stocks drift toward target; random shocks."""
    rng = rng or random.Random()
    for port in ports.values():
        for slot in port.market:
            for _ in range(days):
                # Drift toward target
                diff = slot.stock_target - slot.stock_current
                restock = slot.restock_rate * (1 if diff > 0 else -0.5)
                slot.stock_current += int(round(restock)) if abs(diff) > restock else diff

                # Random shock (10% chance per day)
                if rng.random() < 0.10:
                    shock = rng.randint(-3, 3)
                    slot.stock_current = max(0, slot.stock_current + shock)


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
