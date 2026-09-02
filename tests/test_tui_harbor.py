"""TUI Harbor (H) dock loop — provision, repair, hire_crew via dialogs."""

from __future__ import annotations

from pathlib import Path

import pytest

textual = pytest.importorskip("textual", reason="textual not installed")

from textual.widgets import Input  # noqa: E402

from portlight.app.session import GameSession  # noqa: E402
from portlight.app.tui.app import PortlightApp  # noqa: E402
from portlight.app.tui.screens.dock import (  # noqa: E402
    HarborSelectDialog,
    QtyDialog,
    execute_harbor_flow,
)


def _make_session(tmp_path: Path) -> GameSession:
    s = GameSession(base_path=tmp_path, slot="tui_harbor_test")
    s.new("Captain Blackwood", captain_type="merchant")
    return s


def _capture_notify(app) -> list[str]:
    seen: list[str] = []
    orig = app.notify

    def _wrapped(message, *args, **kwargs):
        seen.append(str(message))
        return orig(message, *args, **kwargs)

    app.notify = _wrapped
    return seen


async def _submit_input(app, pilot, widget_id: str, value: str) -> None:
    await pilot.pause()
    inp = app.screen.query_one(f"#{widget_id}", Input)
    inp.value = value
    await inp.action_submit()
    await pilot.pause()


async def _harbor_choice(pilot, app, choice: str, qty: str) -> None:
    """Press H, submit HarborSelectDialog, then QtyDialog. Production flow."""
    await pilot.press("h")
    await pilot.pause()
    assert isinstance(app.screen, HarborSelectDialog)
    await _submit_input(app, pilot, "harbor-input", choice)
    assert isinstance(app.screen, QtyDialog)
    await _submit_input(app, pilot, "qty-input", qty)


@pytest.mark.asyncio
async def test_harbor_provision_mutates_state(tmp_path: Path):
    """H -> 1 (provision) -> qty runs GameSession.provision."""
    session = _make_session(tmp_path)
    app = PortlightApp(session=session)
    assert session.current_port is not None
    silver_before = session.world.captain.silver
    prov_before = session.world.captain.provisions

    async with app.run_test() as pilot:
        await _harbor_choice(pilot, app, "1", "1")

    assert session.world.captain.provisions == prov_before + 1
    assert session.world.captain.silver < silver_before
    assert execute_harbor_flow.__name__ == "execute_harbor_flow"


@pytest.mark.asyncio
async def test_harbor_repair_mutates_state(tmp_path: Path):
    """H -> 2 (repair) -> qty runs GameSession.repair."""
    session = _make_session(tmp_path)
    ship = session.world.captain.ship
    ship.hull = ship.hull_max - 5
    hull_before = ship.hull
    silver_before = session.world.captain.silver
    app = PortlightApp(session=session)

    async with app.run_test() as pilot:
        await _harbor_choice(pilot, app, "2", "1")

    assert session.world.captain.ship.hull == hull_before + 1
    assert session.world.captain.silver < silver_before


@pytest.mark.asyncio
async def test_harbor_hire_crew_mutates_state(tmp_path: Path):
    """H -> 3 (hire) -> qty runs GameSession.hire_crew."""
    session = _make_session(tmp_path)
    ship = session.world.captain.ship
    crew_before = ship.crew
    silver_before = session.world.captain.silver
    app = PortlightApp(session=session)

    async with app.run_test() as pilot:
        await _harbor_choice(pilot, app, "3", "1")

    assert session.world.captain.ship.crew == crew_before + 1
    assert session.world.captain.silver < silver_before


async def _harbor_select(pilot, app, choice: str) -> None:
    """Press H and submit HarborSelectDialog. Production flow, no qty."""
    await pilot.press("h")
    await pilot.pause()
    assert isinstance(app.screen, HarborSelectDialog)
    await _submit_input(app, pilot, "harbor-input", choice)


@pytest.mark.asyncio
async def test_harbor_at_sea_hunts(tmp_path: Path):
    """At-sea H runs hunt and does not open the dock picker."""
    session = _make_session(tmp_path)
    err = session.sail("al_manar")
    assert err is None
    assert session.at_sea
    day_before = session.world.day
    cap_day_before = session.world.captain.day
    app = PortlightApp(session=session)
    notes = _capture_notify(app)

    async with app.run_test() as pilot:
        await pilot.press("h")
        await pilot.pause()
        assert not isinstance(app.screen, HarborSelectDialog)

    assert notes, "at-sea H should notify hunt flavor or a hunt error"
    assert not any("Must be docked" in n for n in notes)
    assert session.world.day > day_before or session.world.captain.day > cap_day_before


@pytest.mark.asyncio
async def test_harbor_work_no_qty_earns_silver_and_day(tmp_path: Path):
    """H -> 4 (work) skips QtyDialog and runs GameSession.work."""
    session = _make_session(tmp_path)
    silver_before = session.world.captain.silver
    day_before = session.world.day
    app = PortlightApp(session=session)

    async with app.run_test() as pilot:
        await pilot.press("h")
        await pilot.pause()
        assert isinstance(app.screen, HarborSelectDialog)
        sids = [sid for sid, _label in app.screen.options]
        assert sids[3:6] == ["work", "fire", "hunt"]
        await _submit_input(app, pilot, "harbor-input", "4")
        assert not isinstance(app.screen, QtyDialog)

    assert session.world.captain.silver > silver_before
    assert session.world.day == day_before + 1


@pytest.mark.asyncio
async def test_harbor_fire_qty_drops_crew(tmp_path: Path):
    """H -> 5 (fire) -> QtyDialog qty 1 runs GameSession.fire_crew."""
    session = _make_session(tmp_path)
    crew_before = session.world.captain.ship.crew
    assert crew_before >= 1
    app = PortlightApp(session=session)

    async with app.run_test() as pilot:
        await _harbor_select(pilot, app, "5")
        assert isinstance(app.screen, QtyDialog)
        await _submit_input(app, pilot, "qty-input", "1")

    assert session.world.captain.ship.crew == crew_before - 1


@pytest.mark.asyncio
async def test_harbor_hunt_docked_no_qty(tmp_path: Path):
    """H -> 6 (hunt) skips QtyDialog and runs GameSession.hunt while docked."""
    session = _make_session(tmp_path)
    day_before = session.world.day
    prov_before = session.world.captain.provisions
    pelts_before = sum(
        c.quantity for c in session.world.captain.cargo if c.good_id == "pelts"
    )
    app = PortlightApp(session=session)
    notes = _capture_notify(app)

    async with app.run_test() as pilot:
        await _harbor_select(pilot, app, "6")
        assert not isinstance(app.screen, QtyDialog)

    pelts_after = sum(
        c.quantity for c in session.world.captain.cargo if c.good_id == "pelts"
    )
    hunted = (
        session.world.day > day_before
        or session.world.captain.provisions > prov_before
        or pelts_after > pelts_before
        or any(n and "Must be docked" not in n for n in notes)
    )
    assert hunted
    assert session.world.day == day_before + 1
    assert not any("Must be docked" in n for n in notes)


def test_session_work_and_hunt_api(tmp_path: Path):
    """GameSession.work / hunt mutate state without going through the TUI."""
    session = _make_session(tmp_path)
    silver_before = session.world.captain.silver
    day_before = session.world.day
    earned = session.work()
    assert isinstance(earned, int)
    assert earned >= 3
    assert session.world.captain.silver == silver_before + earned
    assert session.world.day == day_before + 1

    result = session.hunt()
    assert not isinstance(result, str)
    assert session.world.day == day_before + 2
    assert hasattr(result, "provisions_gained")
    assert hasattr(result, "pelts_gained")
