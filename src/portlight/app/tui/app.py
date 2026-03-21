"""PortlightApp — main Textual application.

Launches with GameSession, shows dashboard with status sidebar
and tab-switchable content area. Keyboard-driven navigation.
"""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.binding import Binding

from portlight.app.session import GameSession
from portlight.app.tui.theme import APP_CSS


class PortlightApp(App):
    """Portlight interactive terminal UI."""

    TITLE = "Portlight"
    CSS = APP_CSS

    BINDINGS = [
        Binding("d", "switch_tab('dashboard')", "Dashboard", priority=True),
        Binding("m", "switch_tab('market')", "Market", priority=True),
        Binding("r", "switch_tab('routes')", "Routes", priority=True),
        Binding("c", "switch_tab('cargo')", "Cargo", priority=True),
        Binding("i", "switch_tab('inventory')", "Inventory", priority=True),
        Binding("f", "switch_tab('fleet')", "Fleet", priority=True),
        Binding("k", "switch_tab('contracts')", "Contracts", priority=True),
        Binding("p", "switch_tab('port')", "Port", priority=True),
        Binding("l", "switch_tab('ledger')", "Ledger", priority=True),
        Binding("w", "switch_tab('infrastructure')", "Infra", priority=True),
        Binding("question_mark", "switch_tab('help')", "Help", priority=True),
        Binding("b", "buy", "Buy", priority=True),
        Binding("s", "sell", "Sell", priority=True),
        Binding("g", "sail", "Sail", priority=True),
        Binding("a", "advance", "Advance", priority=True),
        Binding("q", "quit", "Quit", priority=True),
    ]

    def __init__(self, session: GameSession | None = None) -> None:
        super().__init__()
        self.session = session or GameSession()
        self._current_tab = "dashboard"

    def compose(self) -> ComposeResult:
        from portlight.app.tui.screens.dashboard import DashboardScreen
        yield DashboardScreen(self.session)

    def on_mount(self) -> None:
        if not self.session.active:
            if not self.session.load():
                self.notify(
                    "No save found. Run 'portlight new <name>' first, then 'portlight tui'.",
                    severity="error",
                    timeout=8,
                )

    def action_switch_tab(self, tab: str) -> None:
        """Switch the content area to a different tab."""
        if not self.session.active:
            self.notify("No active game.", severity="warning")
            return
        self._current_tab = tab
        dashboard = self.query_one("DashboardScreen", expect_type=None)
        if dashboard is not None:
            dashboard.switch_tab(tab)

    def action_buy(self) -> None:
        """Open buy dialog."""
        if not self.session.active:
            return
        from portlight.app.tui.screens.market import execute_buy_flow
        execute_buy_flow(self, self.session)

    def action_sell(self) -> None:
        """Open sell dialog."""
        if not self.session.active:
            return
        from portlight.app.tui.screens.market import execute_sell_flow
        execute_sell_flow(self, self.session)

    def action_sail(self) -> None:
        """Open sail dialog."""
        if not self.session.active:
            return
        from portlight.app.tui.screens.routes import execute_sail_flow
        execute_sail_flow(self, self.session)

    def action_advance(self) -> None:
        """Advance one day."""
        if not self.session.active:
            return
        from portlight.app.tui.screens.routes import execute_advance
        execute_advance(self, self.session)

    def refresh_views(self) -> None:
        """Refresh all visible views after a state mutation."""
        dashboard = self.query_one("DashboardScreen", expect_type=None)
        if dashboard is not None:
            dashboard.refresh_all()
