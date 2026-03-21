"""Smoke tests for Textual TUI — verifies imports and construction."""

from __future__ import annotations

import pytest


def test_tui_app_import():
    """PortlightApp can be imported."""
    from portlight.app.tui.app import PortlightApp
    assert PortlightApp is not None


def test_tui_app_construct():
    """PortlightApp can be constructed with a fresh session."""
    from portlight.app.tui.app import PortlightApp
    from portlight.app.session import GameSession
    session = GameSession()
    app = PortlightApp(session=session)
    assert app.session is session
    assert app._current_tab == "dashboard"


def test_dashboard_screen_import():
    """DashboardScreen can be imported."""
    from portlight.app.tui.screens.dashboard import DashboardScreen
    assert DashboardScreen is not None


def test_market_dialogs_import():
    """Market trade dialogs can be imported."""
    from portlight.app.tui.screens.market import TradeDialog, GoodSelectDialog
    assert TradeDialog is not None
    assert GoodSelectDialog is not None


def test_routes_dialogs_import():
    """Route/sail dialogs can be imported."""
    from portlight.app.tui.screens.routes import SailDialog
    assert SailDialog is not None


def test_combat_screen_import():
    """CombatScreen can be imported."""
    from portlight.app.tui.screens.combat import CombatScreen
    assert CombatScreen is not None


def test_theme_css():
    """Theme CSS is a non-empty string."""
    from portlight.app.tui.theme import APP_CSS
    assert isinstance(APP_CSS, str)
    assert len(APP_CSS) > 100


def test_dashboard_content_tabs():
    """ContentArea supports all expected tab names."""
    from portlight.app.tui.screens.dashboard import ContentArea
    from portlight.app.session import GameSession
    session = GameSession()
    content = ContentArea(session)
    expected_tabs = [
        "dashboard", "market", "cargo", "routes", "port",
        "fleet", "inventory", "contracts", "ledger",
        "infrastructure", "help",
    ]
    for tab in expected_tabs:
        content._current_tab = tab
        # Should not raise
        assert content._current_tab == tab


def test_app_bindings():
    """App has bindings for all navigation keys."""
    from portlight.app.tui.app import PortlightApp
    app = PortlightApp()
    binding_keys = {b.key for b in app.BINDINGS}
    expected = {"d", "m", "r", "c", "i", "f", "k", "p", "l", "w", "b", "s", "g", "a", "q"}
    assert expected.issubset(binding_keys)
