"""TUI inactive-session save picker -- New game and load existing slot."""

from __future__ import annotations

from pathlib import Path

import pytest

textual = pytest.importorskip("textual", reason="textual not installed")

from portlight.app.session import GameSession, list_save_slots  # noqa: E402
from portlight.app.tui.app import PortlightApp  # noqa: E402
from portlight.app.tui.screens.dock import (  # noqa: E402
    HarborSelectDialog,
    execute_save_picker,
)
from portlight.engine.captain_identity import CAPTAIN_ORDER  # noqa: E402
from tests.test_tui_harbor import _submit_input  # noqa: E402


@pytest.mark.asyncio
async def test_inactive_mount_save_picker_new_game(tmp_path: Path):
    """on_mount with no save pushes Save slots; new + CAPTAIN_ORDER id starts a game."""
    session = GameSession(base_path=tmp_path, slot="picker_new")
    assert not session.active
    captain_id = next(ct.value for ct in CAPTAIN_ORDER if ct.value == "merchant")
    app = PortlightApp(session=session)

    async with app.run_test() as pilot:
        await pilot.pause()
        assert isinstance(app.screen, HarborSelectDialog)
        assert app.screen.heading == "Save slots"
        await _submit_input(app, pilot, "harbor-input", "new")
        assert isinstance(app.screen, HarborSelectDialog)
        assert app.screen.heading == "Captain type"
        await _submit_input(app, pilot, "harbor-input", captain_id)

    assert session.active
    assert session.world.captain.captain_type == captain_id
    assert execute_save_picker.__name__ == "execute_save_picker"


@pytest.mark.asyncio
async def test_inactive_mount_save_picker_loads_existing_slot(tmp_path: Path):
    """Existing slot appears in list_save_slots; picking it load()s captain.name."""
    saved_slot = "rook"
    saved = GameSession(base_path=tmp_path, slot=saved_slot)
    saved.new("Captain Rook", captain_type="merchant", seed=42)
    saved._save()

    rows = list_save_slots(tmp_path)
    assert any(row["slot"] == saved_slot for row in rows)
    assert any(row.get("captain") == "Captain Rook" for row in rows)

    session = GameSession(base_path=tmp_path, slot="empty")
    assert not session.active
    app = PortlightApp(session=session)

    async with app.run_test() as pilot:
        await pilot.pause()
        assert isinstance(app.screen, HarborSelectDialog)
        assert app.screen.heading == "Save slots"
        await _submit_input(app, pilot, "harbor-input", saved_slot)

    assert session.slot == saved_slot
    assert session.active
    assert session.captain.name == "Captain Rook"
    assert session.load()
    assert session.captain.name == "Captain Rook"
