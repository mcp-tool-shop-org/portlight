"""TUI Contracts -- K-twice opens accept/abandon picker via execute_contracts_flow."""

from __future__ import annotations

from pathlib import Path

import pytest

textual = pytest.importorskip("textual", reason="textual not installed")

from portlight.app.session import GameSession  # noqa: E402
from portlight.app.tui.app import PortlightApp  # noqa: E402
from portlight.app.tui.screens.dock import (  # noqa: E402
    HarborSelectDialog,
    execute_contracts_flow,
)
from tests.test_tui_harbor import (  # noqa: E402
    _capture_notify,
    _make_session,
    _submit_input,
)


def _docked_with_offers(tmp_path: Path) -> GameSession:
    session = _make_session(tmp_path)
    port = session.current_port
    assert port is not None
    session._refresh_board(port)
    assert session.board.offers, "starting port must have contract offers"
    return session


@pytest.mark.asyncio
async def test_contracts_k_twice_accepts_first_offer(tmp_path: Path):
    """k (tab) then k (execute_contracts_flow) submit 1 runs accept_contract."""
    session = _docked_with_offers(tmp_path)
    app = PortlightApp(session=session)

    async with app.run_test() as pilot:
        await pilot.press("k")
        await pilot.pause()
        assert app._current_tab == "contracts"
        await pilot.press("k")
        await pilot.pause()
        assert isinstance(app.screen, HarborSelectDialog)
        assert app.screen.heading == "Contracts"
        n_offers = len(session.board.offers)
        n_active = len(session.board.active)
        first = app.screen.options[0][0]
        assert first.startswith("accept:")
        await _submit_input(app, pilot, "harbor-input", "1")

    assert len(session.board.active) == n_active + 1
    assert len(session.board.offers) == n_offers - 1
    assert execute_contracts_flow.__name__ == "execute_contracts_flow"


@pytest.mark.asyncio
async def test_contracts_k_twice_abandon_shortens_active(tmp_path: Path):
    """After accept, K-twice then abandon row drops board.active."""
    session = _docked_with_offers(tmp_path)
    app = PortlightApp(session=session)

    async with app.run_test() as pilot:
        await pilot.press("k")
        await pilot.pause()
        await pilot.press("k")
        await pilot.pause()
        assert isinstance(app.screen, HarborSelectDialog)
        await _submit_input(app, pilot, "harbor-input", "1")
        assert session.board.active
        accepted_id = session.board.active[-1].offer_id
        n_active = len(session.board.active)

        await pilot.press("d")
        await pilot.pause()
        await pilot.press("k")
        await pilot.pause()
        await pilot.press("k")
        await pilot.pause()
        assert isinstance(app.screen, HarborSelectDialog)
        assert app.screen.heading == "Contracts"
        await _submit_input(app, pilot, "harbor-input", f"abandon:{accepted_id}")

    assert len(session.board.active) == n_active - 1
    assert all(c.offer_id != accepted_id for c in session.board.active)


@pytest.mark.asyncio
async def test_contracts_empty_board_notifies(tmp_path: Path):
    """No offers/active notifies instead of a blank picker."""
    session = _make_session(tmp_path)
    err = session.sail("al_manar")
    assert err is None
    session.board.offers.clear()
    session.board.active.clear()
    app = PortlightApp(session=session)
    notes = _capture_notify(app)

    async with app.run_test() as pilot:
        await pilot.press("k")
        await pilot.pause()
        await pilot.press("k")
        await pilot.pause()
        assert not isinstance(app.screen, HarborSelectDialog)

    assert any("No contract offers or active obligations" in n for n in notes)
