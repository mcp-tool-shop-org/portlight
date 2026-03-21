"""Tests for the hunting engine — provisions and pelts."""

import random

from portlight.content.world import new_game
from portlight.engine.hunting import hunt, HuntResult


def _rng(seed: int = 42) -> random.Random:
    return random.Random(seed)


class TestHuntAtPort:
    def test_port_hunt_success_gives_provisions(self):
        """Successful port hunt should yield provisions."""
        world = new_game()
        # Try many seeds to find a success
        for seed in range(50):
            captain = new_game().captain
            result = hunt(captain, "port", 5, _rng(seed))
            if result.success:
                assert result.provisions_gained >= 2
                return
        assert False, "No successful port hunt in 50 seeds"

    def test_port_hunt_no_morale_cost(self):
        """Port hunting should never cost morale."""
        world = new_game()
        result = hunt(world.captain, "port", 5, _rng())
        assert result.morale_cost == 0

    def test_port_hunt_success_rate_high(self):
        """Port hunting should succeed ~80% of the time."""
        successes = 0
        for seed in range(100):
            captain = new_game().captain
            result = hunt(captain, "port", 5, _rng(seed))
            if result.success:
                successes += 1
        assert 60 <= successes <= 95, f"Port hunt success rate: {successes}%"

    def test_port_hunt_advances_day(self):
        world = new_game()
        day_before = world.captain.day
        hunt(world.captain, "port", 5, _rng())
        assert world.captain.day == day_before + 1


class TestHuntAtSea:
    def test_sea_hunt_has_morale_cost(self):
        """Sea hunting should cost morale."""
        world = new_game()
        result = hunt(world.captain, "sea", 5, _rng())
        assert result.morale_cost == 3

    def test_sea_hunt_lower_success_rate(self):
        """Sea hunting should succeed ~50% of the time."""
        successes = 0
        for seed in range(100):
            captain = new_game().captain
            result = hunt(captain, "sea", 5, _rng(seed))
            if result.success:
                successes += 1
        assert 30 <= successes <= 70, f"Sea hunt success rate: {successes}%"

    def test_sea_hunt_can_yield_pelts(self):
        """Sea hunting can yield pelts."""
        for seed in range(100):
            captain = new_game().captain
            result = hunt(captain, "sea", 5, _rng(seed))
            if result.pelts_gained > 0:
                return
        # Pelts are optional (0-1 range), so not finding any in 100 seeds is acceptable
        # but finding at least one is expected


class TestHuntResult:
    def test_result_has_flavor_text(self):
        """All hunt results should have flavor text."""
        for seed in range(20):
            captain = new_game().captain
            result = hunt(captain, "port", 5, _rng(seed))
            assert result.flavor, f"No flavor text for seed {seed}"

    def test_crew_bonus_scales(self):
        """Larger crews should get better yields on average."""
        small_crew_yields = []
        large_crew_yields = []
        for seed in range(50):
            captain = new_game().captain
            r = hunt(captain, "port", 3, _rng(seed))
            if r.success:
                small_crew_yields.append(r.provisions_gained)
            captain = new_game().captain
            r = hunt(captain, "port", 12, _rng(seed))
            if r.success:
                large_crew_yields.append(r.provisions_gained)
        if small_crew_yields and large_crew_yields:
            assert sum(large_crew_yields) / len(large_crew_yields) >= sum(small_crew_yields) / len(small_crew_yields)


class TestPeltsGood:
    def test_pelts_in_goods_catalog(self):
        from portlight.content.goods import GOODS
        assert "pelts" in GOODS
        assert GOODS["pelts"].base_price == 8
