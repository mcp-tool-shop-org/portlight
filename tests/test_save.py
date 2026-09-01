"""Tests for save/load round-trip and migration."""

import json
from pathlib import Path

import pytest

from portlight.content.world import new_game
from portlight.engine.economy import execute_buy, recalculate_prices
from portlight.engine.save import (
    CURRENT_SAVE_VERSION,
    DEFAULT_SLOT,
    SAVE_DIR,
    SaveVersionError,
    load_game,
    migrate_save,
    save_filename,
    save_game,
    world_to_dict,
)
from portlight.content.goods import GOODS
from portlight.receipts.models import ReceiptLedger, TradeReceipt, TradeAction


class TestSaveLoad:
    def test_round_trip_fresh_game(self, tmp_path: Path):
        world = new_game("Hawk")
        save_game(world, base_path=tmp_path)
        result = load_game(base_path=tmp_path)
        assert result is not None
        loaded, ledger, _board, _infra, _campaign, _narrative = result
        assert loaded.captain.name == "Hawk"
        assert loaded.captain.silver == 550  # Merchant starting silver
        assert loaded.day == 1
        assert len(loaded.ports) == 20

    def test_round_trip_with_cargo(self, tmp_path: Path):
        world = new_game()
        port = world.ports["porto_novo"]
        recalculate_prices(port, GOODS)
        execute_buy(world.captain, port, "grain", 5, GOODS)
        save_game(world, base_path=tmp_path)
        loaded, _, _board, _infra, _campaign, _narrative = load_game(base_path=tmp_path)
        assert len(loaded.captain.cargo) == 1
        assert loaded.captain.cargo[0].good_id == "grain"
        assert loaded.captain.cargo[0].quantity == 5

    def test_round_trip_with_ledger(self, tmp_path: Path):
        world = new_game()
        ledger = ReceiptLedger(run_id="test-run")
        ledger.append(TradeReceipt(
            receipt_id="abc",
            captain_name="Hawk",
            port_id="porto_novo",
            good_id="grain",
            action=TradeAction.BUY,
            quantity=10,
            unit_price=12,
            total_price=120,
            day=1,
        ))
        save_game(world, ledger, base_path=tmp_path)
        _, loaded_ledger, _board, _infra, _campaign, _narrative = load_game(base_path=tmp_path)
        assert loaded_ledger.run_id == "test-run"
        assert len(loaded_ledger.receipts) == 1
        assert loaded_ledger.total_buys == 120

    def test_no_save_returns_none(self, tmp_path: Path):
        assert load_game(base_path=tmp_path) is None

    def test_corrupt_save_returns_none(self, tmp_path: Path):
        save_dir = tmp_path / "saves"
        save_dir.mkdir()
        (save_dir / "portlight_save.json").write_text("{{broken", encoding="utf-8")
        assert load_game(base_path=tmp_path) is None

    def test_market_prices_preserved(self, tmp_path: Path):
        world = new_game()
        porto = world.ports["porto_novo"]
        grain = next(s for s in porto.market if s.good_id == "grain")
        original_buy = grain.buy_price
        save_game(world, base_path=tmp_path)
        loaded, _, _board, _infra, _campaign, _narrative = load_game(base_path=tmp_path)
        loaded_grain = next(s for s in loaded.ports["porto_novo"].market if s.good_id == "grain")
        assert loaded_grain.buy_price == original_buy

    def test_voyage_state_preserved(self, tmp_path: Path):
        from portlight.engine.voyage import depart
        world = new_game()
        depart(world, "al_manar")
        save_game(world, base_path=tmp_path)
        loaded, _, _board, _infra, _campaign, _narrative = load_game(base_path=tmp_path)
        assert loaded.voyage.destination_id == "al_manar"
        assert loaded.voyage.status.value == "at_sea"

    def test_ship_state_preserved(self, tmp_path: Path):
        world = new_game()
        world.captain.ship.hull = 42
        world.captain.ship.crew = 5
        save_game(world, base_path=tmp_path)
        loaded, _, _board, _infra, _campaign, _narrative = load_game(base_path=tmp_path)
        assert loaded.captain.ship.hull == 42
        assert loaded.captain.ship.crew == 5

    def test_truncated_current_slot_returns_none(self, tmp_path: Path):
        """Partial JSON on the live slot file (save_filename) must not load."""
        world = new_game("Hawk")
        save_game(world, base_path=tmp_path)
        slot = tmp_path / SAVE_DIR / save_filename(DEFAULT_SLOT)
        full = slot.read_text(encoding="utf-8")
        cut = full.index('"captain"') + len('"captain": {')
        truncated = full[:cut]
        slot.write_text(truncated, encoding="utf-8")
        assert load_game(base_path=tmp_path) is None

    def test_valid_json_missing_required_keys_returns_none(self, tmp_path: Path):
        """Parseable JSON missing captain/ports/routes must return None, not raise."""
        save_dir = tmp_path / SAVE_DIR
        save_dir.mkdir()
        slot = save_dir / save_filename(DEFAULT_SLOT)
        slot.write_text(
            json.dumps({"version": CURRENT_SAVE_VERSION, "day": 1, "seed": 0}),
            encoding="utf-8",
        )
        assert load_game(base_path=tmp_path) is None

    def test_round_trip_fleet_officers_morale_bounties(self, tmp_path: Path):
        """v8–v12 captain fields must survive save_game/load_game."""
        from portlight.content.ships import SHIPS, create_ship_from_template
        from portlight.engine.models import CrewRole, Officer, OwnedShip

        world = new_game("Admiral")
        world.captain.ship.morale = 73
        world.captain.ship.officers = [
            Officer(
                name="Mira Vale",
                role=CrewRole.NAVIGATOR,
                experience=12,
                origin_port="porto_novo",
                trait="loyal",
            ),
        ]
        reserve = create_ship_from_template(SHIPS["trade_brigantine"])
        reserve.name = "Second Wind"
        reserve.morale = 41
        reserve.officers = [
            Officer(
                name="Tom Reed",
                role=CrewRole.GUNNER,
                experience=4,
                origin_port="al_manar",
                trait="greedy",
            ),
        ]
        world.captain.fleet = [OwnedShip(ship=reserve, docked_port_id="porto_novo")]
        world.captain.wanted_level = 2
        world.captain.breach_records = [
            {"contract_id": "silk_01", "family": "silk", "day": 9},
        ]
        world.captain.active_bounties = ["gnaw"]

        save_game(world, base_path=tmp_path)
        loaded, *_ = load_game(base_path=tmp_path)

        assert loaded.captain.ship.morale == 73
        assert len(loaded.captain.ship.officers) == 1
        officer = loaded.captain.ship.officers[0]
        assert officer.name == "Mira Vale"
        assert officer.role == CrewRole.NAVIGATOR
        assert officer.experience == 12
        assert officer.origin_port == "porto_novo"
        assert officer.trait == "loyal"
        assert len(loaded.captain.fleet) == 1
        owned = loaded.captain.fleet[0]
        assert owned.ship.name == "Second Wind"
        assert owned.docked_port_id == "porto_novo"
        assert owned.ship.morale == 41
        assert owned.ship.officers[0].name == "Tom Reed"
        assert owned.ship.officers[0].role == CrewRole.GUNNER
        assert loaded.captain.wanted_level == 2
        assert loaded.captain.breach_records == [
            {"contract_id": "silk_01", "family": "silk", "day": 9},
        ]
        assert loaded.captain.active_bounties == ["gnaw"]


class TestSaveMigration:
    def test_current_version_no_migration(self):
        world = new_game("Hawk")
        data = world_to_dict(world)
        assert data["version"] == CURRENT_SAVE_VERSION
        migrated = migrate_save(data)
        assert migrated["version"] == CURRENT_SAVE_VERSION

    def test_v1_migrates_to_current(self):
        """A v1 save (minimal fields) migrates to current version."""
        world = new_game("Hawk")
        from portlight.engine.campaign import CampaignState
        from portlight.engine.infrastructure import InfrastructureState
        from portlight.engine.contracts import ContractBoard
        data = world_to_dict(world, ReceiptLedger(), ContractBoard(), InfrastructureState(), CampaignState())
        # Simulate v1: strip optional sections and set version=1
        data["version"] = 1
        del data["campaign"]
        del data["infrastructure"]
        del data["contract_board"]
        del data["ledger"]
        migrated = migrate_save(data)
        assert migrated["version"] == CURRENT_SAVE_VERSION
        assert "campaign" in migrated
        assert "infrastructure" in migrated
        assert "contract_board" in migrated
        assert "ledger" in migrated

    def test_v1_save_loads_successfully(self, tmp_path: Path):
        """A v1 save file on disk loads through the migration chain."""
        world = new_game("Hawk")
        from portlight.engine.campaign import CampaignState
        from portlight.engine.infrastructure import InfrastructureState
        from portlight.engine.contracts import ContractBoard
        data = world_to_dict(world, ReceiptLedger(), ContractBoard(), InfrastructureState(), CampaignState())
        data["version"] = 1
        del data["campaign"]
        save_dir = tmp_path / "saves"
        save_dir.mkdir()
        (save_dir / "portlight_save.json").write_text(
            json.dumps(data, indent=2), encoding="utf-8",
        )
        result = load_game(base_path=tmp_path)
        assert result is not None
        loaded, _ledger, _board, _infra, _campaign, _narrative = result
        assert loaded.captain.name == "Hawk"

    def test_future_version_raises_version_error(self, tmp_path: Path):
        """A save from a newer version raises SaveVersionError with descriptive message."""
        world = new_game("Hawk")
        data = world_to_dict(world)
        data["version"] = 999
        save_dir = tmp_path / "saves"
        save_dir.mkdir()
        (save_dir / "portlight_save.json").write_text(
            json.dumps(data, indent=2), encoding="utf-8",
        )
        with pytest.raises(SaveVersionError, match="version 999 is newer"):
            load_game(base_path=tmp_path)

    def test_v1_migration_populates_v8_to_v12_keys(self):
        """v1→current must fill fleet/morale/officers/breach/wanted/bounties, not just version."""
        world = new_game("Hawk")
        from portlight.engine.campaign import CampaignState
        from portlight.engine.infrastructure import InfrastructureState
        from portlight.engine.contracts import ContractBoard
        data = world_to_dict(
            world, ReceiptLedger(), ContractBoard(), InfrastructureState(), CampaignState(),
        )
        data["version"] = 1
        captain = data["captain"]
        flag_crew = captain["ship"]["crew"]
        del captain["fleet"]
        del captain["breach_records"]
        del captain["wanted_level"]
        del captain["active_bounties"]
        del captain["deferred_fees"]
        del captain["ship"]["morale"]
        del captain["ship"]["officers"]
        del captain["ship"]["roster"]
        captain["fleet"] = [{
            "ship": {
                "template_id": "trade_brigantine",
                "name": "Docked", "hull": 100, "hull_max": 100,
                "cargo_capacity": 80, "speed": 6,
                "crew": 10, "crew_max": 20,
                "cannons": 6, "maneuver": 0.5,
                "upgrades": [], "upgrade_slots": 4,
            },
            "docked_port_id": "porto_novo",
            "cargo": [],
        }]
        migrated = migrate_save(data)
        assert migrated["version"] == CURRENT_SAVE_VERSION
        assert migrated["captain"]["ship"]["morale"] == 50
        assert migrated["captain"]["ship"]["officers"] == []
        assert migrated["captain"]["ship"]["roster"]["sailors"] == flag_crew
        fleet_ship = migrated["captain"]["fleet"][0]["ship"]
        assert fleet_ship["morale"] == 50
        assert fleet_ship["officers"] == []
        assert fleet_ship["roster"]["sailors"] == 10
        assert migrated["captain"]["breach_records"] == []
        assert migrated["captain"]["wanted_level"] == 0
        assert migrated["captain"]["active_bounties"] == []
        assert migrated["captain"]["deferred_fees"] == []
