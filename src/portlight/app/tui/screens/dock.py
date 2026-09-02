"""Dock-service dialogs — provision, repair, and hire (TUI).

Reuses the TradeDialog/Input modal pattern from market.py and routes.py.
Hunt/work/fire stay CLI-only; Help can hint at them.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Input, Static

if TYPE_CHECKING:
    from portlight.app.session import GameSession


class QtyDialog(ModalScreen[str | None]):
    """Quantity input with unit cost, matching TradeDialog."""

    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    def __init__(self, title: str, unit_label: str, max_qty: int, unit_cost: int) -> None:
        super().__init__()
        self.title_text = title
        self.unit_label = unit_label
        self.max_qty = max_qty
        self.unit_cost = unit_cost

    def compose(self) -> ComposeResult:
        total_max = self.unit_cost * self.max_qty
        with Vertical(id="input-area"):
            yield Static(
                f"[bold #e9c46a]\u2693 {self.title_text}[/bold #e9c46a]\n\n"
                f"  Rate: [yellow]{self.unit_cost}[/yellow] silver {self.unit_label}\n"
                f"  Max:  [cyan]{self.max_qty}[/cyan]"
                f" ([yellow]{total_max:,}[/yellow] silver)"
            )
            yield Input(
                placeholder=f"Quantity (1-{self.max_qty})",
                id="qty-input",
            )

    def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value.strip()
        if text.isdigit() and 0 < int(text) <= self.max_qty:
            self.dismiss(text)
        else:
            self.notify(f"Enter 1-{self.max_qty}", severity="warning")

    def action_cancel(self) -> None:
        self.dismiss(None)


class HarborSelectDialog(ModalScreen[str | None]):
    """Pick provision, repair, or hire — same numbered-list pattern as GoodSelectDialog."""

    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    def __init__(self, options: list[tuple[str, str]]) -> None:
        super().__init__()
        # (service_id, display line)
        self.options = options

    def compose(self) -> ComposeResult:
        with Vertical(id="input-area"):
            lines = ["[bold #e9c46a]\u2693 Harbor services[/bold #e9c46a]", ""]
            for i, (_sid, label) in enumerate(self.options, 1):
                lines.append(f"  [cyan]{i:2d}[/cyan]. {label}")
            lines.append("")
            yield Static("\n".join(lines))
            yield Input(placeholder="Enter name or number", id="harbor-input")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value.strip().lower()
        if text.isdigit():
            idx = int(text) - 1
            if 0 <= idx < len(self.options):
                self.dismiss(self.options[idx][0])
                return
        for sid, _label in self.options:
            if text == sid or sid.startswith(text):
                self.dismiss(sid)
                return
        self.notify(f"Unknown: {text}", severity="warning")

    def action_cancel(self) -> None:
        self.dismiss(None)


def _service_rates(session: "GameSession") -> tuple[int, int, int] | None:
    port = session.current_port
    if not port:
        return None
    svc_mult = session._service_mult()
    provision = max(1, int(port.provision_cost * svc_mult))
    repair = max(1, int(port.repair_cost * svc_mult))
    # hire_crew charges port.crew_cost for sailors (no service modifier)
    crew = port.crew_cost
    return provision, repair, crew


def execute_harbor_flow(app, session: "GameSession") -> None:
    """Open harbor picker then a quantity dialog; calls GameSession.provision/repair/hire_crew."""
    port = session.current_port
    if not port:
        app.notify("\u2693 Must be docked for harbor services.", severity="warning")
        return
    if not session.active:
        app.notify("No active game.", severity="warning")
        return

    rates = _service_rates(session)
    if rates is None:
        app.notify("\u2693 Must be docked for harbor services.", severity="warning")
        return
    cost_prov, cost_repair, cost_crew = rates
    cap = session.world.captain
    ship = cap.ship

    from portlight.content.upgrades import UPGRADES as _UPG
    from portlight.engine.ship_stats import resolve_crew_max

    hull_max = ship.hull_max if ship else 0
    hull_now = ship.hull if ship else 0
    hull_damage = max(0, hull_max - hull_now)
    crew_max = resolve_crew_max(ship, _UPG) if ship else 0
    crew_now = ship.crew if ship else 0
    crew_space = max(0, crew_max - crew_now)

    options = [
        ("provision", f"Provision  [yellow]{cost_prov}[/yellow]/day  (have {cap.provisions} days)"),
        ("repair", f"Repair     [yellow]{cost_repair}[/yellow]/hp  (hull {hull_now}/{hull_max})"),
        ("hire", f"Hire crew  [yellow]{cost_crew}[/yellow]/sailor  ({crew_now}/{crew_max})"),
    ]

    def on_service(service_id: str | None) -> None:
        if service_id is None:
            return
        if service_id == "provision":
            _run_provision(app, session, cost_prov)
        elif service_id == "repair":
            _run_repair(app, session, cost_repair, hull_damage)
        elif service_id == "hire":
            _run_hire(app, session, cost_crew, crew_space)

    app.push_screen(HarborSelectDialog(options), on_service)


def _run_provision(app, session: "GameSession", cost_per_day: int) -> None:
    silver = session.world.captain.silver
    if cost_per_day <= 0:
        app.notify("Cannot provision here.", severity="warning")
        return
    max_qty = silver // cost_per_day
    if max_qty <= 0:
        app.notify("Can't afford any provisions.", severity="warning")
        return

    def on_qty(qty_str: str | None) -> None:
        if qty_str is None:
            return
        days = int(qty_str)
        err = session.provision(days)
        if err:
            app.notify(f"\u2717 {err}", severity="error")
            return
        paid = session.last_provision_cost
        app.notify(
            f"\u2713 Provisioned {days} days for {paid:,} silver",
            severity="information",
            timeout=5,
        )
        app.refresh_views()

    app.push_screen(QtyDialog("Provision", "per day", max_qty, cost_per_day), on_qty)


def _run_repair(app, session: "GameSession", cost_per_hp: int, hull_damage: int) -> None:
    if hull_damage <= 0:
        app.notify("Ship is already in perfect condition.", severity="warning")
        return
    silver = session.world.captain.silver
    if cost_per_hp <= 0:
        app.notify("Cannot repair here.", severity="warning")
        return
    affordable = silver // cost_per_hp
    max_qty = min(hull_damage, affordable)
    if max_qty <= 0:
        app.notify("Can't afford any repairs.", severity="warning")
        return

    def on_qty(qty_str: str | None) -> None:
        if qty_str is None:
            return
        amount = int(qty_str)
        result = session.repair(amount)
        if isinstance(result, str):
            app.notify(f"\u2717 {result}", severity="error")
            return
        repaired, cost = result
        app.notify(
            f"\u2713 Repaired {repaired} hull for {cost:,} silver",
            severity="information",
            timeout=5,
        )
        app.refresh_views()

    app.push_screen(QtyDialog("Repair hull", "per hull point", max_qty, cost_per_hp), on_qty)


def _run_hire(app, session: "GameSession", cost_per: int, crew_space: int) -> None:
    if crew_space <= 0:
        app.notify("Crew is already full.", severity="warning")
        return
    silver = session.world.captain.silver
    if cost_per <= 0:
        max_qty = crew_space
    else:
        max_qty = min(crew_space, silver // cost_per)
    if max_qty <= 0:
        app.notify("Can't afford to hire crew.", severity="warning")
        return

    def on_qty(qty_str: str | None) -> None:
        if qty_str is None:
            return
        count = int(qty_str)
        err = session.hire_crew(count, "sailor")
        if err:
            app.notify(f"\u2717 {err}", severity="error")
            return
        app.notify(
            f"\u2713 Hired {count} sailor(s)",
            severity="information",
            timeout=5,
        )
        app.refresh_views()

    shown_cost = cost_per if cost_per > 0 else 0
    app.push_screen(QtyDialog("Hire sailors", "per sailor", max_qty, max(shown_cost, 0)), on_qty)
