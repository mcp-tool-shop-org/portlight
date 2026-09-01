"""Tests for the bounty hunting system."""

import random

from portlight.content.world import new_game
from portlight.engine.bounty import (
    generate_bounty_board,
    accept_bounty,
    claim_bounty,
    BountyTarget,
)
from portlight.engine.captain_identity import CaptainType, CAPTAIN_TEMPLATES
from portlight.engine.captain_memory import get_or_create_memory, record_encounter


def _rng(seed: int = 42) -> random.Random:
    return random.Random(seed)


def _record_player_win(world, captain_id: str, region: str = "North Atlantic"):
    """Seed a live CaptainMemory the same way combat does after a player win."""
    memory = get_or_create_memory(world.pirates.captain_memories, captain_id)
    record_encounter(memory, day=world.day, region=region, outcome="player_won")
    return memory


class TestBountyBoard:
    def test_board_generates_targets(self):
        world = new_game()
        targets = generate_bounty_board(world.pirates, _rng())
        assert len(targets) > 0
        assert len(targets) <= 3

    def test_targets_are_bounty_target_objects(self):
        world = new_game()
        targets = generate_bounty_board(world.pirates, _rng())
        for t in targets:
            assert isinstance(t, BountyTarget)
            assert t.reward > 0
            assert t.captain_name

    def test_defeated_pirates_excluded(self):
        """Pirates already defeated should not appear on the board."""
        world = new_game()
        memory = _record_player_win(world, "scarlet_ana")
        assert memory.times_defeated_by_player >= 1
        targets = generate_bounty_board(world.pirates, _rng(), max_targets=10)
        ids = [t.captain_id for t in targets]
        assert "scarlet_ana" not in ids


class TestAcceptBounty:
    def test_accept_bounty_success(self):
        world = new_game()
        err = accept_bounty(world.captain, "scarlet_ana")
        assert err is None
        assert "scarlet_ana" in world.captain.active_bounties

    def test_cannot_accept_duplicate(self):
        world = new_game()
        accept_bounty(world.captain, "scarlet_ana")
        err = accept_bounty(world.captain, "scarlet_ana")
        assert err is not None

    def test_max_three_bounties(self):
        world = new_game()
        accept_bounty(world.captain, "scarlet_ana")
        accept_bounty(world.captain, "gnaw")
        accept_bounty(world.captain, "shadow_vex")
        err = accept_bounty(world.captain, "brass_jack")
        assert err is not None


class TestClaimBounty:
    def test_claim_requires_defeat(self):
        world = new_game()
        accept_bounty(world.captain, "scarlet_ana")
        result = claim_bounty(world.captain, world.pirates, "scarlet_ana")
        assert isinstance(result, str)  # error — not defeated yet

    def test_claim_after_defeat(self):
        world = new_game()
        accept_bounty(world.captain, "scarlet_ana")
        memory = _record_player_win(world, "scarlet_ana")
        assert memory.times_defeated_by_player >= 1
        board_ids = [t.captain_id for t in generate_bounty_board(world.pirates, _rng(), max_targets=10)]
        assert "scarlet_ana" not in board_ids
        silver_before = world.captain.silver
        result = claim_bounty(world.captain, world.pirates, "scarlet_ana")
        assert isinstance(result, int)
        assert result == 150  # scarlet_ana's bounty
        assert world.captain.silver == silver_before + 150
        assert "scarlet_ana" not in world.captain.active_bounties

    def test_claim_without_accepting(self):
        world = new_game()
        _record_player_win(world, "gnaw", region="Mediterranean")
        result = claim_bounty(world.captain, world.pirates, "gnaw")
        assert isinstance(result, str)  # error — no active bounty

    def test_save_dict_memory_excludes_from_board(self):
        """Save-dict memories with times_defeated_by_player still count as defeated."""
        world = new_game()
        world.pirates.captain_memories["brass_jack"] = {"times_defeated_by_player": 1}
        targets = generate_bounty_board(world.pirates, _rng(), max_targets=10)
        assert "brass_jack" not in [t.captain_id for t in targets]


class TestBountyHunterTemplate:
    def test_template_exists(self):
        assert CaptainType.BOUNTY_HUNTER in CAPTAIN_TEMPLATES

    def test_template_fields(self):
        t = CAPTAIN_TEMPLATES[CaptainType.BOUNTY_HUNTER]
        assert t.starting_silver == 425
        assert t.starting_ship_id == "swift_cutter"
        assert t.pricing.buy_price_mult == 1.05
        assert t.inspection.inspection_chance_mult == 0.6
        assert len(t.strengths) >= 3
        assert len(t.weaknesses) >= 3

    def test_new_game_as_bounty_hunter(self):
        from portlight.content.world import new_game
        world = new_game(captain_type=CaptainType.BOUNTY_HUNTER, captain_name="Hunter")
        assert world.captain.captain_type == "bounty_hunter"
        assert world.captain.silver == 425
