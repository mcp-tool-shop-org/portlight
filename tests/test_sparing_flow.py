"""Tests for the sparing flow — spare/take-all post-victory consequences.

Verifies that sparing and taking-all produce different outcomes across:
captain memory, underworld standing, companion morale, and silver reward.
"""

from __future__ import annotations

import random
from pathlib import Path

import pytest

from portlight.app import cli
from portlight.app.session import GameSession
from portlight.engine.captain_memory import (
    CaptainMemory,
    CaptainRelationship,
    record_encounter,
)
from portlight.engine.models import EncounterState, PendingDuel
from portlight.engine.save import load_game, save_game
from portlight.engine.underworld import record_duel_outcome


def _rng(seed: int = 42) -> random.Random:
    return random.Random(seed)


def _make_encounter(strength: int = 7) -> EncounterState:
    return EncounterState(
        enemy_captain_id="gnaw",
        enemy_captain_name="Gnaw",
        enemy_faction_id="iron_wolves",
        enemy_personality="aggressive",
        enemy_strength=strength,
        enemy_region="Mediterranean",
        enemy_ship_hull=40,
        enemy_ship_hull_max=40,
        enemy_ship_cannons=4,
        enemy_ship_maneuver=0.5,
        enemy_ship_speed=6.0,
        enemy_ship_crew=8,
        enemy_ship_crew_max=12,
        phase="resolved",
        boarding_progress=2,
        boarding_threshold=2,
    )


def _pending_gnaw(strength: int = 7) -> PendingDuel:
    return PendingDuel(
        captain_id="gnaw",
        captain_name="Gnaw",
        faction_id="iron_wolves",
        personality="aggressive",
        strength=strength,
        region="Mediterranean",
    )


def _reset_cli_combat() -> None:
    cli._active_encounter = None
    cli._player_combatant = None
    cli._opponent_combatant = None
    cli._pending_victory = False


@pytest.fixture
def reset_cli_combat():
    _reset_cli_combat()
    yield
    _reset_cli_combat()


# ---------------------------------------------------------------------------
# Captain memory: spare vs take-all
# ---------------------------------------------------------------------------

class TestCaptainMemory:
    def test_spare_boosts_respect(self):
        mem = CaptainMemory(captain_id="scarlet_ana")
        enc = record_encounter(mem, 10, "Med", "player_won", player_spared=True)
        assert enc.respect_delta > 0
        assert mem.relationship.respect > 0

    def test_spare_reduces_grudge(self):
        mem = CaptainMemory(captain_id="scarlet_ana", relationship=CaptainRelationship(grudge=30))
        record_encounter(mem, 10, "Med", "player_won", player_spared=True)
        assert mem.relationship.grudge < 30  # reduced

    def test_take_all_increases_grudge(self):
        mem = CaptainMemory(captain_id="gnaw")
        record_encounter(mem, 10, "Med", "player_won", player_spared=False)
        assert mem.relationship.grudge > 0

    def test_spare_tracks_count(self):
        mem = CaptainMemory(captain_id="scarlet_ana")
        record_encounter(mem, 10, "Med", "player_won", player_spared=True)
        assert mem.times_spared == 1
        record_encounter(mem, 20, "Med", "player_won", player_spared=True)
        assert mem.times_spared == 2

    def test_spare_vs_take_all_respect_difference(self):
        mem_spare = CaptainMemory(captain_id="test")
        mem_take = CaptainMemory(captain_id="test")
        record_encounter(mem_spare, 10, "Med", "player_won", player_spared=True)
        record_encounter(mem_take, 10, "Med", "player_won", player_spared=False)
        assert mem_spare.relationship.respect > mem_take.relationship.respect

    def test_spare_vs_take_all_fear_difference(self):
        mem_spare = CaptainMemory(captain_id="test")
        mem_take = CaptainMemory(captain_id="test")
        record_encounter(mem_spare, 10, "Med", "player_won", player_spared=True)
        record_encounter(mem_take, 10, "Med", "player_won", player_spared=False)
        assert mem_spare.relationship.fear < mem_take.relationship.fear


# ---------------------------------------------------------------------------
# Underworld standing
# ---------------------------------------------------------------------------

class TestUnderworldStanding:
    def test_spare_gives_more_standing(self):
        standing = {}
        delta_spare = record_duel_outcome(standing.copy(), "crimson_tide", True, spared=True)
        delta_take = record_duel_outcome(standing.copy(), "crimson_tide", True, spared=False)
        assert delta_spare > delta_take  # sparing = +5, taking = +2

    def test_spare_gives_5_standing(self):
        standing = {}
        delta = record_duel_outcome(standing, "crimson_tide", True, spared=True)
        assert delta == 5

    def test_take_all_gives_2_standing(self):
        standing = {}
        delta = record_duel_outcome(standing, "crimson_tide", True, spared=False)
        assert delta == 2


# ---------------------------------------------------------------------------
# Companion morale
# ---------------------------------------------------------------------------

class TestCompanionMorale:
    def test_sparing_boosts_gentle_surgeon(self):
        from portlight.engine.companion_engine import CompanionState, PartyState, apply_morale_trigger
        party = PartyState(companions=[
            CompanionState(companion_id="dr_amara", role_id="surgeon", morale=50, personality="gentle"),
        ])
        reactions = apply_morale_trigger(party, "spared_enemy")
        assert len(reactions) == 1
        assert reactions[0][1] > 0  # positive delta

    def test_taking_all_upsets_gentle(self):
        from portlight.engine.companion_engine import CompanionState, PartyState, apply_morale_trigger
        party = PartyState(companions=[
            CompanionState(companion_id="dr_amara", role_id="surgeon", morale=50, personality="gentle"),
        ])
        reactions = apply_morale_trigger(party, "took_all")
        assert len(reactions) == 1
        assert reactions[0][1] < 0  # negative

    def test_taking_all_pleases_smuggler(self):
        from portlight.engine.companion_engine import CompanionState, PartyState, apply_morale_trigger
        party = PartyState(companions=[
            CompanionState(companion_id="shadow_kai", role_id="smuggler", morale=50, personality="pragmatic"),
        ])
        reactions = apply_morale_trigger(party, "took_all")
        deltas = [r[1] for r in reactions]
        assert any(d > 0 for d in deltas)

    def test_sparing_vs_taking_morale_divergence(self):
        """Gentle surgeon should have very different morale after spare vs take-all."""
        from portlight.engine.companion_engine import CompanionState, PartyState, apply_morale_trigger

        party_spare = PartyState(companions=[
            CompanionState(companion_id="dr_amara", role_id="surgeon", morale=50, personality="gentle"),
        ])
        party_take = PartyState(companions=[
            CompanionState(companion_id="dr_amara", role_id="surgeon", morale=50, personality="gentle"),
        ])
        apply_morale_trigger(party_spare, "spared_enemy")
        apply_morale_trigger(party_take, "took_all")
        spare_morale = party_spare.companions[0].morale
        take_morale = party_take.companions[0].morale
        assert spare_morale > take_morale


# ---------------------------------------------------------------------------
# Silver reward
# ---------------------------------------------------------------------------

class TestSilverReward:
    def test_take_all_gives_more_silver(self, tmp_path: Path, monkeypatch, reset_cli_combat):
        """Take-all must pay more silver than spare through the live CLI finalizer."""
        strength = 7
        s_spare = GameSession(base_path=tmp_path / "spare")
        s_spare.new("Hawk")
        s_take = GameSession(base_path=tmp_path / "take")
        s_take.new("Hawk")
        start_silver = s_spare.captain.silver
        assert s_take.captain.silver == start_silver

        monkeypatch.setattr(cli, "_session", lambda: s_spare)
        cli._active_encounter = _make_encounter(strength)
        cli._pending_victory = True
        cli.spare()
        spare_gain = s_spare.captain.silver - start_silver

        monkeypatch.setattr(cli, "_session", lambda: s_take)
        cli._active_encounter = _make_encounter(strength)
        cli._pending_victory = True
        cli.take_all()
        take_gain = s_take.captain.silver - start_silver

        assert spare_gain > 0
        assert take_gain > spare_gain


# ---------------------------------------------------------------------------
# Encounter state persistence
# ---------------------------------------------------------------------------

class TestEncounterPersistence:
    """Verify that victory state survives save/load (bug fix: encounter persistence)."""

    def test_pending_victory_survives_save_load_and_restore(
        self, tmp_path: Path, reset_cli_combat,
    ):
        """pending_victory must survive save_game/load_game and cli._restore_encounter."""
        s = GameSession(base_path=tmp_path)
        s.new("Hawk")
        s.world.pirates.pending_duel = _pending_gnaw(7)
        cli._active_encounter = _make_encounter(7)
        cli._pending_victory = True
        cli._sync_encounter_phase(s)
        assert s.world.pirates.encounter_state.get("pending_victory") is True

        save_game(
            s.world, s.ledger, s.board, s.infra, s.campaign, s.narrative,
            base_path=tmp_path, slot=s.slot,
        )
        _reset_cli_combat()

        result = load_game(base_path=tmp_path, slot=s.slot)
        assert result is not None
        loaded_world, *_ = result
        assert loaded_world.pirates.encounter_state.get("pending_victory") is True
        assert loaded_world.pirates.encounter_state.get("boarding_progress") == 2
        assert loaded_world.pirates.pending_duel is not None
        assert loaded_world.pirates.pending_duel.captain_id == "gnaw"

        s2 = GameSession(base_path=tmp_path, slot=s.slot)
        assert s2.load()
        cli._restore_encounter(s2)
        assert cli._pending_victory is True
        assert cli._active_encounter is not None
        assert cli._active_encounter.phase == "resolved"
        assert cli._active_encounter.enemy_captain_id == "gnaw"
        assert cli._active_encounter.enemy_strength == 7

    def test_empty_estate_does_not_set_pending_victory(
        self, tmp_path: Path, reset_cli_combat,
    ):
        """Empty encounter_state after save/load must not arm _pending_victory."""
        s = GameSession(base_path=tmp_path)
        s.new("Hawk")
        s.world.pirates.pending_duel = _pending_gnaw(7)
        s.world.pirates.encounter_phase = "duel"
        s.world.pirates.encounter_state = {}
        save_game(
            s.world, s.ledger, s.board, s.infra, s.campaign, s.narrative,
            base_path=tmp_path, slot=s.slot,
        )

        result = load_game(base_path=tmp_path, slot=s.slot)
        assert result is not None
        assert result[0].pirates.encounter_state == {}

        s2 = GameSession(base_path=tmp_path, slot=s.slot)
        assert s2.load()
        cli._restore_encounter(s2)
        assert cli._pending_victory is False
        assert cli._active_encounter is not None
        assert cli._active_encounter.phase == "duel"
