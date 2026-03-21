"""Dashboard screen — status sidebar + tabbed content area."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.text import Text
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Footer, Static

if TYPE_CHECKING:
    from portlight.app.session import GameSession

from textual.app import ComposeResult


class StatusSidebar(Static):
    """Persistent captain status sidebar."""

    def __init__(self, session: "GameSession") -> None:
        super().__init__("", id="status-sidebar")
        self.session = session

    def on_mount(self) -> None:
        self.refresh_status()

    def refresh_status(self) -> None:
        if not self.session.active:
            self.update("[dim]No active game[/dim]")
            return

        w = self.session.world
        cap = w.captain
        ship = cap.ship

        lines: list[str] = []
        lines.append(f"[bold]{cap.name}[/bold]")
        lines.append(f"Day [cyan]{w.day}[/cyan]")
        lines.append("")
        lines.append(f"Silver: [yellow]{cap.silver:,}[/yellow]")
        lines.append("")

        if ship:
            lines.append(f"[bold]{ship.name}[/bold]")
            lines.append(f"  ({ship.template_id})")

            from portlight.content.upgrades import UPGRADES as _UPG
            from portlight.engine.ship_stats import resolve_cargo_capacity, resolve_hull_max
            eff_cargo = resolve_cargo_capacity(ship, _UPG)
            eff_hull = resolve_hull_max(ship, _UPG)
            cargo_used = sum(c.quantity for c in cap.cargo)

            hull_pct = ship.hull / eff_hull if eff_hull > 0 else 0
            hull_color = "green" if hull_pct > 0.6 else "yellow" if hull_pct > 0.3 else "red"
            lines.append(f"Hull:  [{hull_color}]{ship.hull}/{eff_hull}[/{hull_color}]")

            cargo_pct = cargo_used / eff_cargo if eff_cargo > 0 else 0
            cargo_color = "green" if cargo_pct < 0.7 else "yellow" if cargo_pct < 0.9 else "red"
            lines.append(f"Cargo: [{cargo_color}]{cargo_used}/{eff_cargo}[/{cargo_color}]")

            lines.append(f"Crew:  {ship.crew}/{ship.crew_max}")
        lines.append(f"Prov:  {cap.provisions} days")
        lines.append("")

        # Location
        if w.voyage:
            from portlight.engine.models import VoyageStatus
            if w.voyage.status == VoyageStatus.AT_SEA:
                pct = int(w.voyage.progress / max(w.voyage.distance, 1) * 100)
                dest = w.ports.get(w.voyage.destination_id)
                dest_name = dest.name if dest else w.voyage.destination_id
                lines.append("[cyan]At sea[/cyan]")
                lines.append(f"  -> {dest_name}")
                lines.append(f"  {pct}% ({w.voyage.days_elapsed}d)")
            else:
                port = w.ports.get(w.voyage.destination_id)
                lines.append(f"Port: [bold]{port.name if port else '???'}[/bold]")

        self.update("\n".join(lines))


class ContentArea(Widget):
    """Switchable content area that renders different views."""

    def __init__(self, session: "GameSession") -> None:
        super().__init__(id="content-area")
        self.session = session
        self._current_tab = "dashboard"
        self._static = Static("", classes="view-panel")

    def compose(self) -> ComposeResult:
        yield self._static

    def on_mount(self) -> None:
        self.switch_tab("dashboard")

    def switch_tab(self, tab: str) -> None:
        self._current_tab = tab
        self._render_tab()

    def _render_tab(self) -> None:
        """Render the current tab's view into the static widget."""
        if not self.session.active:
            self._static.update("[dim]No active game[/dim]")
            return

        renderable = self._get_view()
        self._static.update(renderable)

    def _get_view(self):
        """Get the Rich renderable for the current tab."""
        from portlight.app import views

        s = self.session
        w = s.world
        cap = w.captain
        tab = self._current_tab

        if tab == "dashboard":
            return views.status_view(w, s.ledger, s.infra)
        elif tab == "market":
            port = s.current_port
            if port:
                return views.market_view(port, cap)
            return Text("Not docked at a port.", style="yellow")
        elif tab == "cargo":
            return views.cargo_view(cap)
        elif tab == "routes":
            return views.routes_view(w)
        elif tab == "port":
            port = s.current_port
            if port:
                return views.port_view(port, cap)
            return Text("Not docked at a port.", style="yellow")
        elif tab == "fleet":
            return views.fleet_view(cap)
        elif tab == "inventory":
            return self._inventory_view()
        elif tab == "contracts":
            return views.contracts_view(s.board, w.day)
        elif tab == "ledger":
            return views.ledger_view(s.ledger, cap)
        elif tab == "infrastructure":
            return self._infra_view()
        elif tab == "help":
            return self._help_view()
        return Text(f"Unknown tab: {tab}", style="red")

    def _inventory_view(self):
        """Build inventory view data from captain state."""
        from portlight.app.combat_views import inventory_view
        cap = self.session.world.captain

        gear_data = {
            "armor": None,
            "melee": None,
            "ranged": None,
            "style": None,
            "injuries": [],
            "cargo_summary": [],
            "silver": cap.silver,
        }

        if hasattr(cap, "armor") and cap.armor:
            gear_data["armor"] = {
                "name": cap.armor.name,
                "dr": cap.armor.damage_reduction,
                "dodge_penalty": getattr(cap.armor, "dodge_penalty", 0),
            }
        if hasattr(cap, "melee_weapon") and cap.melee_weapon:
            gear_data["melee"] = {
                "name": cap.melee_weapon.name,
                "damage": cap.melee_weapon.base_damage,
                "speed": getattr(cap.melee_weapon, "speed_modifier", 0),
            }
        if hasattr(cap, "ranged") and cap.ranged:
            gear_data["ranged"] = {
                "name": cap.ranged.name,
                "damage": cap.ranged.base_damage,
                "ammo": getattr(cap.ranged, "ammo", 0),
            }
        if hasattr(cap, "fighting_style") and cap.fighting_style:
            gear_data["style"] = {"name": cap.fighting_style.name}
        if hasattr(cap, "injuries"):
            gear_data["injuries"] = [
                {"name": inj.name, "severity": inj.severity, "days_remaining": inj.days_remaining}
                for inj in cap.injuries
            ]
        gear_data["cargo_summary"] = [
            {"good_id": c.good_id, "quantity": c.quantity}
            for c in cap.cargo
        ]

        return inventory_view(gear_data)

    def _infra_view(self):
        """Composite infrastructure view."""
        from rich.console import Group
        from portlight.app.views import (
            warehouse_view, offices_view, licenses_view,
            insurance_view, credit_view,
        )
        s = self.session
        parts = []
        parts.append(warehouse_view(s.infra, s.world, s.world.captain))
        parts.append(offices_view(s.infra))
        if s.world.captain.standing:
            parts.append(licenses_view(s.infra, s.world.captain.standing))
            parts.append(credit_view(s.infra, s.world.captain.standing))
        heat = 0
        if s.world.captain.standing:
            heat = max(s.world.captain.standing.customs_heat.values(), default=0)
        parts.append(insurance_view(s.infra, heat))
        return Group(*parts)

    def _help_view(self):
        """Keybinding help screen."""
        from rich.panel import Panel
        lines = [
            "[bold]Navigation[/bold]",
            "  [cyan]D[/cyan] Dashboard    [cyan]M[/cyan] Market     [cyan]R[/cyan] Routes",
            "  [cyan]C[/cyan] Cargo        [cyan]I[/cyan] Inventory  [cyan]F[/cyan] Fleet",
            "  [cyan]K[/cyan] Contracts    [cyan]P[/cyan] Port       [cyan]L[/cyan] Ledger",
            "  [cyan]W[/cyan] Infra        [cyan]?[/cyan] Help       [cyan]Q[/cyan] Quit",
            "",
            "[bold]Actions (when in port)[/bold]",
            "  [cyan]B[/cyan] Buy goods    [cyan]S[/cyan] Sell goods",
            "  [cyan]G[/cyan] Sail (go)    [cyan]A[/cyan] Advance day",
            "",
            "[bold]Combat[/bold]",
            "  [cyan]T[/cyan] Thrust       [cyan]Z[/cyan] Slash      [cyan]X[/cyan] Parry",
            "  [cyan]O[/cyan] Shoot        [cyan]E[/cyan] Dodge/Evade",
            "",
            "[bold]General[/bold]",
            "  [cyan]Esc[/cyan] Back / Cancel",
            "  [cyan]Enter[/cyan] Confirm selection",
        ]
        return Panel("\n".join(lines), title="[bold]Keybindings[/bold]", border_style="cyan")


class TabBar(Static):
    """Bottom tab bar showing available screens."""

    TAB_LABELS = [
        ("D", "Dashboard"), ("M", "Market"), ("R", "Routes"),
        ("C", "Cargo"), ("I", "Inventory"), ("F", "Fleet"),
        ("K", "Contracts"), ("P", "Port"), ("L", "Ledger"),
        ("W", "Infra"), ("?", "Help"),
    ]

    def __init__(self) -> None:
        super().__init__("", id="footer-bar")
        self._active = "dashboard"

    def on_mount(self) -> None:
        self._render_tabs()

    def set_active(self, tab: str) -> None:
        self._active = tab
        self._render_tabs()

    def _render_tabs(self) -> None:
        tab_map = {
            "D": "dashboard", "M": "market", "R": "routes",
            "C": "cargo", "I": "inventory", "F": "fleet",
            "K": "contracts", "P": "port", "L": "ledger",
            "W": "infrastructure", "?": "help",
        }
        parts = []
        for key, label in self.TAB_LABELS:
            tab_id = tab_map.get(key, label.lower())
            if tab_id == self._active:
                parts.append(f"[bold reverse] {key} {label} [/bold reverse]")
            else:
                parts.append(f"[dim] {key}[/dim] {label}")
        self.update(" ".join(parts))


class DashboardScreen(Widget):
    """Main screen combining sidebar, content area, and tab bar."""

    def __init__(self, session: "GameSession") -> None:
        super().__init__()
        self.session = session
        self._sidebar = StatusSidebar(session)
        self._content = ContentArea(session)
        self._tabbar = TabBar()

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield self._sidebar
            yield self._content
        yield self._tabbar
        yield Footer()

    def switch_tab(self, tab: str) -> None:
        self._content.switch_tab(tab)
        self._tabbar.set_active(tab)

    def refresh_all(self) -> None:
        self._sidebar.refresh_status()
        self._content._render_tab()
