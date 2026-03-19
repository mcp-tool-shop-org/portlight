"""Tests for the session manager — the full gameplay loop.

Proves: new → buy → sail → events → arrive → sell → ledger → upgrade.
"""

from pathlib import Path

from portlight.app.session import GameSession
from portlight.engine.models import VoyageStatus
from portlight.receipts.models import TradeAction, TradeReceipt


class TestSessionNew:
    def test_new_game_creates_world(self, tmp_path: Path):
        s = GameSession(tmp_path)
        s.new("Hawk")
        assert s.active
        assert s.captain.name == "Hawk"
        assert s.captain.silver == 500
        assert s.current_port_id == "porto_novo"

    def test_new_game_auto_saves(self, tmp_path: Path):
        s = GameSession(tmp_path)
        s.new()
        # Loading a fresh session should find the save
        s2 = GameSession(tmp_path)
        assert s2.load()
        assert s2.captain.name == "Captain"


class TestSessionTrading:
    def test_buy_succeeds(self, tmp_path: Path):
        s = GameSession(tmp_path)
        s.new()
        result = s.buy("grain", 5)
        assert isinstance(result, TradeReceipt)
        assert result.action == TradeAction.BUY
        assert s.captain.silver < 500

    def test_buy_error_at_sea(self, tmp_path: Path):
        s = GameSession(tmp_path)
        s.new()
        s.sail("al_manar")
        result = s.buy("grain", 5)
        assert isinstance(result, str)
        assert "port" in result.lower()

    def test_sell_succeeds(self, tmp_path: Path):
        s = GameSession(tmp_path)
        s.new()
        s.buy("grain", 5)
        silver_after_buy = s.captain.silver
        result = s.sell("grain", 3)
        assert isinstance(result, TradeReceipt)
        assert s.captain.silver > silver_after_buy

    def test_ledger_tracks_trades(self, tmp_path: Path):
        s = GameSession(tmp_path)
        s.new()
        s.buy("grain", 5)
        s.sell("grain", 5)
        assert len(s.ledger.receipts) == 2
        assert s.ledger.total_buys > 0
        assert s.ledger.total_sells > 0


class TestSessionVoyage:
    def test_sail_starts_voyage(self, tmp_path: Path):
        s = GameSession(tmp_path)
        s.new()
        err = s.sail("al_manar")
        assert err is None
        assert s.at_sea

    def test_sail_error_no_route(self, tmp_path: Path):
        s = GameSession(tmp_path)
        s.new()
        err = s.sail("jade_port")
        assert err is not None
        assert "No route" in err

    def test_advance_makes_progress(self, tmp_path: Path):
        s = GameSession(tmp_path)
        s.new()
        s.sail("silva_bay")  # short route
        events = s.advance()
        assert len(events) > 0
        assert s.world.voyage.progress > 0

    def test_full_voyage_completes(self, tmp_path: Path):
        s = GameSession(tmp_path)
        s.new()
        s.sail("silva_bay")  # distance=16, speed=8, ~2 days
        for _ in range(10):
            s.advance()
            if s.current_port_id is not None:
                break
        assert s.current_port_id == "silva_bay"

    def test_advance_in_port_ticks_markets(self, tmp_path: Path):
        s = GameSession(tmp_path)
        s.new()
        day_before = s.world.day
        s.advance()  # in port, should tick
        assert s.world.day == day_before + 1


class TestSessionProvisionRepair:
    def test_provision_costs_silver(self, tmp_path: Path):
        s = GameSession(tmp_path)
        s.new()
        silver_before = s.captain.silver
        # Porto Novo provision cost is 1/day
        err = s.provision(10)
        assert err is None
        assert s.captain.silver == silver_before - 10  # 1 silver/day at Porto Novo
        assert s.captain.provisions == 40  # started with 30

    def test_repair_costs_silver(self, tmp_path: Path):
        s = GameSession(tmp_path)
        s.new()
        s.captain.ship.hull = 40  # damage 20 HP
        silver_before = s.captain.silver
        result = s.repair()
        assert not isinstance(result, str)
        repaired, cost = result
        assert repaired == 20
        # Porto Novo repair cost is 2/hp
        assert cost == 40  # 2 per HP at Porto Novo
        assert s.captain.ship.hull == 60

    def test_provision_error_no_silver(self, tmp_path: Path):
        s = GameSession(tmp_path)
        s.new()
        s.captain.silver = 0
        err = s.provision(10)
        assert err is not None

    def test_hire_crew(self, tmp_path: Path):
        s = GameSession(tmp_path)
        s.new()
        initial_crew = s.captain.ship.crew
        err = s.hire_crew(2)
        assert err is None
        assert s.captain.ship.crew == initial_crew + 2


class TestSessionShipyard:
    def test_buy_ship_at_shipyard(self, tmp_path: Path):
        s = GameSession(tmp_path)
        s.new()  # starts at porto_novo (has shipyard)
        s.captain.silver = 2000
        err = s.buy_ship("trade_brigantine")
        assert err is None
        assert s.captain.ship.template_id == "trade_brigantine"

    def test_buy_ship_no_shipyard(self, tmp_path: Path):
        s = GameSession(tmp_path)
        s.new(starting_port="al_manar")  # no shipyard
        s.captain.silver = 2000
        err = s.buy_ship("trade_brigantine")
        assert err is not None
        assert "shipyard" in err.lower()

    def test_buy_ship_insufficient_silver(self, tmp_path: Path):
        s = GameSession(tmp_path)
        s.new()
        s.captain.silver = 10
        err = s.buy_ship("trade_brigantine")
        assert err is not None

    def test_old_ship_trade_in_value(self, tmp_path: Path):
        s = GameSession(tmp_path)
        s.new()
        s.captain.silver = 800
        # Sloop is free (price=0), so no trade-in value
        s.buy_ship("trade_brigantine")
        assert s.captain.silver == 0  # 800 - 800 + 0 trade-in


class TestFullVoyageLoop:
    """The acceptance test: buy → sail → events → arrive → sell → profit."""

    def test_profitable_grain_run(self, tmp_path: Path):
        """Buy grain at Porto Novo (producer), sell at Al-Manar (consumer)."""
        s = GameSession(tmp_path)
        s.new("Hawk")

        # 1. Buy grain at Porto Novo (cheap here, affinity 1.3)
        buy_result = s.buy("grain", 10)
        assert isinstance(buy_result, TradeReceipt)
        buy_price_per = buy_result.unit_price

        # 2. Sail to Al-Manar
        err = s.sail("al_manar")
        assert err is None

        # 3. Sail through events (cargo may be damaged)
        for _ in range(20):
            events = s.advance()
            if s.current_port_id is not None:
                break
        assert s.current_port_id == "al_manar"

        # 4. Sell whatever grain survived the voyage
        grain_held = sum(c.quantity for c in s.captain.cargo if c.good_id == "grain")
        assert grain_held > 0, "All grain was lost during voyage"
        sell_result = s.sell("grain", grain_held)
        assert isinstance(sell_result, TradeReceipt)

        # 5. Sell price at consumer should be higher than buy price at producer
        assert sell_result.unit_price > buy_price_per, (
            f"Grain not profitable: bought at {buy_price_per}, sold at {sell_result.unit_price}"
        )

        # 6. Ledger reflects the trades
        assert len(s.ledger.receipts) == 2
        assert s.ledger.net_profit > 0

    def test_save_load_mid_voyage(self, tmp_path: Path):
        """Save at sea, reload, and complete the voyage."""
        s = GameSession(tmp_path)
        s.new()
        s.sail("al_manar")
        s.advance()  # one day at sea

        # Reload
        s2 = GameSession(tmp_path)
        assert s2.load()
        assert s2.at_sea
        assert s2.world.voyage.progress > 0

        # Complete
        for _ in range(20):
            s2.advance()
            if s2.current_port_id is not None:
                break
        assert s2.current_port_id == "al_manar"
