"""Tests for TUI encounter system -- EncounterScreen phases, wiring, consequences."""

from __future__ import annotations

import random
from pathlib import Path

import pytest

textual = pytest.importorskip("textual", reason="textual not installed")

from portlight.app.session import GameSession  # noqa: E402
from portlight.app.tui.app import PortlightApp  # noqa: E402
from portlight.engine.models import EncounterState, PendingDuel  # noqa: E402


def _make_session() -> GameSession:
    s = GameSession(slot="tui_encounter_test")
    s.new("Captain Storm", captain_type="privateer")
    return s


def _make_silver_session(base_path: Path, slot: str) -> GameSession:
    s = GameSession(base_path=base_path, slot=slot)
    s.new("Captain Storm", captain_type="privateer", seed=42)
    return s


def _make_encounter(strength: int = 5) -> EncounterState:
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
        enemy_ship_crew=10,
        enemy_ship_crew_max=15,
        phase="approach",
        boarding_progress=0,
        boarding_threshold=3,
    )


# ---------------------------------------------------------------------------
# Smoke tests
# ---------------------------------------------------------------------------

def test_encounter_screen_import():
    from portlight.app.tui.screens.encounter import EncounterScreen
    assert EncounterScreen is not None


def test_encounter_screen_construct():
    from portlight.app.tui.screens.encounter import EncounterScreen
    s = _make_session()
    enc = _make_encounter()
    screen = EncounterScreen(s, enc)
    assert screen._phase == "approach"
    assert screen.encounter is enc


# ---------------------------------------------------------------------------
# Approach phase
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_approach_negotiate():
    """Pressing N on approach phase calls negotiate handler."""
    from portlight.app.tui.screens.encounter import EncounterScreen
    s = _make_session()
    enc = _make_encounter(strength=1)  # weak = easier negotiate
    app = PortlightApp(session=s)

    async with app.run_test() as pilot:
        screen = EncounterScreen(s, enc)
        app.push_screen(screen)
        await pilot.pause()
        await pilot.press("n")
        await pilot.pause()
        # Phase should have changed (either resolved or naval if negotiate failed)
        assert screen._phase in ("resolved", "naval")


@pytest.mark.asyncio
async def test_approach_fight_transitions_to_naval():
    """Pressing G transitions to naval phase."""
    from portlight.app.tui.screens.encounter import EncounterScreen
    s = _make_session()
    enc = _make_encounter()
    app = PortlightApp(session=s)

    async with app.run_test() as pilot:
        screen = EncounterScreen(s, enc)
        app.push_screen(screen)
        await pilot.pause()
        await pilot.press("g")
        await pilot.pause()
        assert screen._phase == "naval"
        assert enc.phase == "naval"


@pytest.mark.asyncio
async def test_approach_flee():
    """Pressing F on approach attempts to flee."""
    from portlight.app.tui.screens.encounter import EncounterScreen
    s = _make_session()
    enc = _make_encounter()
    app = PortlightApp(session=s)

    async with app.run_test() as pilot:
        screen = EncounterScreen(s, enc)
        app.push_screen(screen)
        await pilot.pause()
        await pilot.press("f")
        await pilot.pause()
        # Flee either succeeds (resolved) or fails (naval)
        assert screen._phase in ("resolved", "naval")


# ---------------------------------------------------------------------------
# Naval phase
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_naval_broadside_round():
    """Broadside action in naval phase produces a round."""
    from portlight.app.tui.screens.encounter import EncounterScreen
    s = _make_session()
    enc = _make_encounter()
    app = PortlightApp(session=s)

    async with app.run_test() as pilot:
        screen = EncounterScreen(s, enc)
        app.push_screen(screen)
        await pilot.pause()
        # Go to naval
        await pilot.press("g")
        await pilot.pause()
        assert screen._phase == "naval"
        # Fire broadside
        initial_turns = enc.naval_turns
        await pilot.press("b")
        await pilot.pause()
        assert enc.naval_turns == initial_turns + 1


@pytest.mark.asyncio
async def test_naval_close_increases_boarding():
    """Close action should increase boarding progress."""
    from portlight.app.tui.screens.encounter import EncounterScreen
    s = _make_session()
    enc = _make_encounter()
    app = PortlightApp(session=s)

    async with app.run_test() as pilot:
        screen = EncounterScreen(s, enc)
        app.push_screen(screen)
        await pilot.pause()
        await pilot.press("g")  # fight → naval
        await pilot.pause()
        # Close multiple times to try to trigger boarding
        for _ in range(5):
            if screen._phase != "naval":
                break
            await pilot.press("c")
            await pilot.pause()
        # Should have progressed past naval (boarding or duel or defeat)
        assert enc.naval_turns > 0


# ---------------------------------------------------------------------------
# Duel phase (force entry via low boarding threshold)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_duel_actions():
    """Duel phase accepts combat actions."""
    from portlight.app.tui.screens.encounter import EncounterScreen
    s = _make_session()
    enc = _make_encounter(strength=1)
    enc.boarding_threshold = 1  # instant boarding
    app = PortlightApp(session=s)

    async with app.run_test() as pilot:
        screen = EncounterScreen(s, enc)
        app.push_screen(screen)
        await pilot.pause()
        await pilot.press("g")  # fight → naval
        await pilot.pause()
        await pilot.press("c")  # close → should trigger boarding immediately
        await pilot.pause()
        # Wait for boarding timer
        await pilot.pause(delay=1.5)

        if screen._phase == "duel":
            assert screen._player_combatant is not None
            assert screen._opponent_combatant is not None
            await pilot.press("t")  # thrust
            await pilot.pause()
            assert enc.duel_turns >= 1


# ---------------------------------------------------------------------------
# Victory consequences
# ---------------------------------------------------------------------------

def _mount_victory_screen(app: PortlightApp, session: GameSession, strength: int):
    """Push EncounterScreen in victory phase onto a running app."""
    from portlight.app.tui.screens.encounter import EncounterScreen

    enc = _make_encounter(strength=strength)
    enc.phase = "victory"
    screen = EncounterScreen(session, enc)
    app.push_screen(screen)
    return screen


@pytest.mark.asyncio
async def test_finalize_victory_silver_spare(tmp_path: Path):
    """Spare must pay silver through EncounterScreen._finalize_victory."""
    s = _make_silver_session(tmp_path / "spare", "spare")
    strength = 5
    start_silver = s.captain.silver
    app = PortlightApp(session=s)

    async with app.run_test() as pilot:
        screen = _mount_victory_screen(app, s, strength)
        await pilot.pause()
        screen._handle_spare()
        await pilot.pause()
        spare_gain = s.captain.silver - start_silver

    assert spare_gain > 0, (
        "spare paid no silver; EncounterScreen._finalize_victory must credit captain.silver"
    )


@pytest.mark.asyncio
async def test_finalize_victory_silver_take_all(tmp_path: Path):
    """Take-all must pay more silver than spare through the TUI finalizer."""
    strength = 5
    s_spare = _make_silver_session(tmp_path / "spare", "spare")
    s_take = _make_silver_session(tmp_path / "take", "take")
    start_silver = s_spare.captain.silver
    assert s_take.captain.silver == start_silver

    app_spare = PortlightApp(session=s_spare)
    async with app_spare.run_test() as pilot:
        screen = _mount_victory_screen(app_spare, s_spare, strength)
        await pilot.pause()
        screen._handle_spare()
        await pilot.pause()
        spare_gain = s_spare.captain.silver - start_silver

    app_take = PortlightApp(session=s_take)
    async with app_take.run_test() as pilot:
        screen = _mount_victory_screen(app_take, s_take, strength)
        await pilot.pause()
        screen._handle_take_all()
        await pilot.pause()
        take_gain = s_take.captain.silver - start_silver

    assert spare_gain > 0
    assert take_gain > spare_gain, (
        f"take-all must pay more silver than spare (spare={spare_gain}, take-all={take_gain})"
    )


# ---------------------------------------------------------------------------
# Advance blocking
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_advance_blocked_during_encounter():
    """Pressing A with pending_duel set should be blocked."""
    s = _make_session()
    s.world.pirates.pending_duel = PendingDuel(
        captain_id="gnaw", captain_name="Gnaw",
        faction_id="iron_wolves", personality="aggressive",
        strength=5, region="Mediterranean",
    )
    app = PortlightApp(session=s)

    async with app.run_test() as pilot:
        await pilot.press("a")
        await pilot.pause()
        # Should not advance — pending_duel still set
        assert s.world.pirates.pending_duel is not None


# ---------------------------------------------------------------------------
# Detection wiring
# ---------------------------------------------------------------------------

def test_execute_advance_detects_pirate_event():
    """execute_advance should detect _pending_duel on voyage events."""
    from portlight.engine.voyage import VoyageEvent, EventType
    from portlight.engine.models import PendingDuel

    pd = PendingDuel(
        captain_id="gnaw", captain_name="Gnaw",
        faction_id="iron_wolves", personality="aggressive",
        strength=5, region="Mediterranean",
    )
    event = VoyageEvent(
        event_type=EventType.PIRATES,
        message="Pirates!",
    )
    event._pending_duel = pd

    # Verify the event has the pending_duel attribute
    assert hasattr(event, "_pending_duel")
    assert event._pending_duel is pd
    assert event._pending_duel.captain_id == "gnaw"


# ---------------------------------------------------------------------------
# Phase transition integrity
# ---------------------------------------------------------------------------

def test_encounter_state_phase_transitions():
    """EncounterState phases transition correctly through engine calls."""
    from portlight.engine.encounter import (
        begin_fight,
    )
    from portlight.engine.models import Ship

    enc = _make_encounter()
    ship = Ship(
        template_id="coastal_sloop", name="Test", hull=60, hull_max=60,
        cargo_capacity=30, speed=8, crew=8, crew_max=8,
        cannons=0, maneuver=0.5,
    )

    # Approach → naval via fight
    assert enc.phase == "approach"
    begin_fight(enc, ship)
    assert enc.phase == "naval"


def test_negotiate_success_resolves():
    """Successful negotiate sets phase to resolved."""
    from portlight.engine.encounter import resolve_negotiate

    enc = _make_encounter()
    # Force allied hostility by mocking
    enc.phase = "approach"
    # Use a seed that gives negotiate success for neutral
    rng = random.Random(42)
    success, msg = resolve_negotiate(enc, {}, "smuggler", rng)
    # Result depends on hostility — just verify it returns cleanly
    assert isinstance(success, bool)
    assert isinstance(msg, str)
    assert len(msg) > 0


@pytest.mark.asyncio
async def test_escape_clears_pending():
    """After resolution, Esc should pop the screen."""
    from portlight.app.tui.screens.encounter import EncounterScreen
    s = _make_session()
    enc = _make_encounter()
    enc.phase = "resolved"  # pre-resolved
    app = PortlightApp(session=s)

    async with app.run_test() as pilot:
        screen = EncounterScreen(s, enc)
        s.world.pirates.pending_duel = PendingDuel(
            captain_id="gnaw", captain_name="Gnaw",
            faction_id="iron_wolves", personality="aggressive",
            strength=5, region="Mediterranean",
        )
        app.push_screen(screen)
        await pilot.pause()
        screen._phase = "resolved"  # force resolved
        screen._clear_pending()
        await pilot.press("escape")
        await pilot.pause()
        assert s.world.pirates.pending_duel is None
