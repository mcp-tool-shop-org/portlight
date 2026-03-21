"""Tests for the contract breach tracking and wanted system."""

import random

from portlight.content.world import new_game
from portlight.engine.contracts import (
    abandon_contract,
    tick_contracts,
    _record_breach,
    get_breach_count_for_family,
    ContractBoard,
    ContractOffer,
    ContractStatus,
    ActiveContract,
)


class TestBreachRecording:
    def test_abandon_records_breach(self):
        """Abandoning a contract should create a breach record."""
        world = new_game()
        board = ContractBoard()
        contract = ActiveContract(
            offer_id="test_01",
            template_id="t01",
            title="Test Contract",
            good_id="grain",
            required_quantity=10,
            reward_silver=200,
            bonus_reward=30,
            destination_port_id="ironhaven",
            source_region="North Atlantic",
            deadline_day=20,
            family="procurement",
            accepted_day=1,
        )
        contract.status = ContractStatus.ACCEPTED
        board.active.append(contract)

        outcome = abandon_contract(board, "test_01", day=5, captain=world.captain)
        assert not isinstance(outcome, str)
        assert len(world.captain.breach_records) == 1
        assert world.captain.breach_records[0]["contract_id"] == "test_01"

    def test_expired_contract_records_breach(self):
        """Expired contracts should create breach records."""
        world = new_game()
        board = ContractBoard()
        contract = ActiveContract(
            offer_id="test_02",
            template_id="t02",
            title="Expired Test",
            good_id="timber",
            required_quantity=5,
            reward_silver=100,
            bonus_reward=20,
            destination_port_id="stormwall",
            source_region="North Atlantic",
            deadline_day=10,
            family="procurement",
            accepted_day=1,
        )
        contract.status = ContractStatus.ACCEPTED
        board.active.append(contract)

        outcomes = tick_contracts(board, day=11, captain=world.captain)
        assert len(outcomes) == 1
        assert len(world.captain.breach_records) == 1


class TestWantedLevel:
    def test_two_breaches_sets_watched(self):
        world = new_game()
        _record_breach(world.captain, "c1", 5, "porto_novo", "procurement")
        assert world.captain.wanted_level == 0  # 1 breach = nothing
        _record_breach(world.captain, "c2", 10, "ironhaven", "procurement")
        assert world.captain.wanted_level == 1  # watched

    def test_three_breaches_sets_wanted(self):
        world = new_game()
        for i in range(3):
            _record_breach(world.captain, f"c{i}", i * 5, "porto_novo", "procurement")
        assert world.captain.wanted_level == 2  # wanted

    def test_five_breaches_sets_hunted(self):
        world = new_game()
        for i in range(5):
            _record_breach(world.captain, f"c{i}", i * 5, "porto_novo", "procurement")
        assert world.captain.wanted_level == 3  # hunted


class TestBreachFamilyCounting:
    def test_count_breaches_by_family(self):
        world = new_game()
        _record_breach(world.captain, "c1", 5, "porto_novo", "procurement")
        _record_breach(world.captain, "c2", 10, "ironhaven", "luxury_discreet")
        _record_breach(world.captain, "c3", 15, "stormwall", "procurement")
        assert get_breach_count_for_family(world.captain, "procurement") == 2
        assert get_breach_count_for_family(world.captain, "luxury_discreet") == 1
        assert get_breach_count_for_family(world.captain, "smuggling") == 0
