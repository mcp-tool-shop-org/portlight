"""Session manager — load/save active run, command context.

The session is the bridge between CLI commands and engine state.
Every command goes through the session to ensure state is consistent
and saved after mutations.
"""

from __future__ import annotations

import random
from pathlib import Path

from portlight.content.goods import GOODS
from portlight.content.ships import SHIPS, create_ship_from_template
from portlight.content.world import new_game
from portlight.engine.economy import execute_buy, execute_sell, recalculate_prices, tick_markets
from portlight.engine.models import VoyageStatus, WorldState
from portlight.engine.save import load_game, save_game
from portlight.engine.voyage import advance_day, arrive, depart
from portlight.receipts.models import ReceiptLedger, TradeReceipt


class GameSession:
    """Holds active game state and mediates all player actions."""

    def __init__(self, base_path: Path | None = None) -> None:
        self.base_path = base_path or Path(".")
        self.world: WorldState | None = None
        self.ledger: ReceiptLedger = ReceiptLedger()
        self._trade_seq: int = 0
        self._rng: random.Random = random.Random()

    @property
    def active(self) -> bool:
        return self.world is not None

    @property
    def captain(self):
        return self.world.captain if self.world else None

    @property
    def current_port_id(self) -> str | None:
        if not self.world or not self.world.voyage:
            return None
        if self.world.voyage.status == VoyageStatus.IN_PORT:
            return self.world.voyage.destination_id
        return None

    @property
    def current_port(self):
        pid = self.current_port_id
        if pid and self.world:
            return self.world.ports.get(pid)
        return None

    @property
    def at_sea(self) -> bool:
        return (self.world is not None and
                self.world.voyage is not None and
                self.world.voyage.status == VoyageStatus.AT_SEA)

    def new(self, captain_name: str = "Captain", starting_port: str = "porto_novo") -> None:
        """Start a fresh game."""
        self.world = new_game(captain_name, starting_port)
        self._rng = random.Random(self.world.seed)
        self.ledger = ReceiptLedger(run_id=f"run-{self.world.seed}")
        self._trade_seq = 0
        self._save()

    def load(self) -> bool:
        """Load saved game. Returns True if loaded."""
        result = load_game(self.base_path)
        if result is None:
            return False
        self.world, self.ledger = result
        self._rng = random.Random(self.world.seed + self.world.day)
        self._trade_seq = len(self.ledger.receipts)
        return True

    def _save(self) -> None:
        """Auto-save after every mutation."""
        if self.world:
            save_game(self.world, self.ledger, self.base_path)

    # --- Trading ---

    def buy(self, good_id: str, qty: int) -> TradeReceipt | str:
        """Buy goods at current port."""
        port = self.current_port
        if not port:
            return "Not docked at a port"
        result = execute_buy(self.world.captain, port, good_id, qty, GOODS, self._trade_seq)
        if isinstance(result, TradeReceipt):
            self.ledger.append(result)
            self._trade_seq += 1
            recalculate_prices(port, GOODS)
            self._save()
        return result

    def sell(self, good_id: str, qty: int) -> TradeReceipt | str:
        """Sell goods at current port."""
        port = self.current_port
        if not port:
            return "Not docked at a port"
        result = execute_sell(self.world.captain, port, good_id, qty, self._trade_seq)
        if isinstance(result, TradeReceipt):
            self.ledger.append(result)
            self._trade_seq += 1
            recalculate_prices(port, GOODS)
            self._save()
        return result

    # --- Voyage ---

    def sail(self, destination_id: str) -> str | None:
        """Depart for destination. Returns error string or None on success."""
        if not self.world:
            return "No active game"
        result = depart(self.world, destination_id)
        if isinstance(result, str):
            return result
        self._save()
        return None

    def advance(self) -> list:
        """Advance one day. Returns voyage events."""
        if not self.world:
            return []
        if not self.at_sea:
            # In port: tick markets forward
            tick_markets(self.world.ports, days=1, rng=self._rng)
            self.world.day += 1
            self.world.captain.day += 1
            for port in self.world.ports.values():
                recalculate_prices(port, GOODS)
            self._save()
            return []

        events = advance_day(self.world, self._rng)

        # Check arrival
        if self.world.voyage and self.world.voyage.status == VoyageStatus.ARRIVED:
            arrive(self.world)
            # Recalculate prices at new port
            port = self.current_port
            if port:
                recalculate_prices(port, GOODS)

        # Recalculate all markets (time passes)
        for port in self.world.ports.values():
            recalculate_prices(port, GOODS)

        self._save()
        return events

    # --- Provisioning & Repair ---

    def provision(self, days: int) -> str | None:
        """Buy provisions at port-specific cost. Returns error or None."""
        if not self.world:
            return "No active game"
        port = self.current_port
        if not port:
            return "Must be docked to provision"
        cost_per_day = port.provision_cost
        cost = days * cost_per_day
        if cost > self.world.captain.silver:
            return f"Need {cost} silver for {days} days of provisions ({cost_per_day}/day here), have {self.world.captain.silver}"
        self.world.captain.silver -= cost
        self.world.captain.provisions += days
        self._save()
        return None

    def repair(self, amount: int | None = None) -> tuple[int, int] | str:
        """Repair hull at port-specific cost. Returns (repaired, cost) or error."""
        if not self.world:
            return "No active game"
        port = self.current_port
        if not port:
            return "Must be docked to repair"
        ship = self.world.captain.ship
        if not ship:
            return "No ship"
        damage = ship.hull_max - ship.hull
        if damage == 0:
            return "Ship is already in perfect condition"
        if amount is None:
            amount = damage
        amount = min(amount, damage)
        cost_per_hp = port.repair_cost
        cost = amount * cost_per_hp
        if cost > self.world.captain.silver:
            affordable = self.world.captain.silver // cost_per_hp if cost_per_hp > 0 else 0
            if affordable == 0:
                return "Can't afford any repairs"
            amount = affordable
            cost = amount * cost_per_hp
        self.world.captain.silver -= cost
        ship.hull += amount
        self._save()
        return (amount, cost)

    # --- Shipyard ---

    def buy_ship(self, ship_id: str) -> str | None:
        """Buy a new ship at a shipyard port. Returns error or None."""
        if not self.world:
            return "No active game"
        port = self.current_port
        if not port:
            return "Must be docked"
        from portlight.engine.models import PortFeature
        if PortFeature.SHIPYARD not in port.features:
            return f"{port.name} has no shipyard"
        template = SHIPS.get(ship_id)
        if not template:
            return f"Unknown ship: {ship_id}"
        if template.id == self.world.captain.ship.template_id:
            return "You already have this ship"
        if template.price > self.world.captain.silver:
            return f"Need {template.price} silver, have {self.world.captain.silver}"

        # Sell old ship for 40% of its template price
        old_template = SHIPS.get(self.world.captain.ship.template_id)
        if old_template:
            self.world.captain.silver += int(old_template.price * 0.4)

        self.world.captain.silver -= template.price
        self.world.captain.ship = create_ship_from_template(template)

        # Transfer cargo (drop excess if new ship is smaller)
        cargo_used = sum(c.quantity for c in self.world.captain.cargo)
        if cargo_used > template.cargo_capacity:
            # Drop from the end until it fits
            while sum(c.quantity for c in self.world.captain.cargo) > template.cargo_capacity:
                self.world.captain.cargo.pop()

        self._save()
        return None

    # --- Hire crew ---

    def hire_crew(self, count: int) -> str | None:
        """Hire crew at port-specific cost. Returns error or None."""
        if not self.world:
            return "No active game"
        port = self.current_port
        if not port:
            return "Must be docked to hire crew"
        ship = self.world.captain.ship
        if not ship:
            return "No ship"
        space = ship.crew_max - ship.crew
        if space == 0:
            return "Crew is already full"
        count = min(count, space)
        cost_per = port.crew_cost
        cost = count * cost_per
        if cost > self.world.captain.silver:
            return f"Need {cost} silver for {count} crew ({cost_per}/each here), have {self.world.captain.silver}"
        self.world.captain.silver -= cost
        ship.crew += count
        self._save()
        return None
