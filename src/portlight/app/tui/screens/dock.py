"""Dock-service dialogs -- provision, repair, hire, plus work/fire/hunt (TUI).

Reuses the TradeDialog/Input modal pattern from market.py and routes.py.
HarborSelectDialog is also the numbered picker for saves, captain type,
and contract accept/abandon.
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
    """Numbered picker -- harbor services, saves, captain type, contracts."""

    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    def __init__(self, options: list[tuple[str, str]], heading: str = "Harbor services") -> None:
        super().__init__()
        # (service_id, display line)
        self.options = options
        self.heading = heading

    def compose(self) -> ComposeResult:
        with Vertical(id="input-area"):
            lines = [f"[bold #e9c46a]\u2693 {self.heading}[/bold #e9c46a]", ""]
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
        if not text:
            self.notify("Enter name or number", severity="warning")
            return
        for sid, _label in self.options:
            if text == sid.lower():
                self.dismiss(sid)
                return
        for sid, _label in self.options:
            if sid.lower().startswith(text):
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
    """Open harbor picker then a quantity dialog; calls GameSession.provision/repair/hire_crew.

    Provision/repair/hire stay the closed harbor slice. Work/fire (and hunt)
    are extra docked options. At sea, H runs hunt and notifies flavor.
    """
    if not session.active:
        app.notify("No active game.", severity="warning")
        return
    if session.at_sea:
        _run_hunt(app, session)
        return
    port = session.current_port
    if not port:
        app.notify("\u2693 Must be docked for harbor services.", severity="warning")
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
        ("work", "Work docks  (earn 3-5 silver)"),
        ("fire", f"Fire crew  ({crew_now} aboard)"),
        ("hunt", "Hunt / forage  (provisions, pelts)"),
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
        elif service_id == "work":
            _run_work(app, session)
        elif service_id == "fire":
            _run_fire(app, session)
        elif service_id == "hunt":
            _run_hunt(app, session)

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


def _run_work(app, session: "GameSession") -> None:
    result = session.work()
    if isinstance(result, str):
        app.notify(f"\u2717 {result}", severity="error")
        return
    app.notify(
        f"\u2713 Worked the docks. Earned {result} silver.",
        severity="information",
        timeout=5,
    )
    app.refresh_views()


def _run_fire(app, session: "GameSession") -> None:
    ship = session.world.captain.ship if session.world else None
    if not ship:
        app.notify("No ship.", severity="warning")
        return
    from portlight.content.crew_roles import get_role_count
    from portlight.engine.models import CrewRole
    sailors = get_role_count(ship.roster, CrewRole.SAILOR)
    if sailors <= 0:
        app.notify("No sailors to fire.", severity="warning")
        return

    def on_qty(qty_str: str | None) -> None:
        if qty_str is None:
            return
        count = int(qty_str)
        err = session.fire_crew(count, "sailor")
        if err:
            app.notify(f"\u2717 {err}", severity="error")
            return
        app.notify(
            f"Fired {count} sailor(s).",
            severity="information",
            timeout=5,
        )
        app.refresh_views()

    app.push_screen(QtyDialog("Fire sailors", "per sailor", sailors, 0), on_qty)


def _run_hunt(app, session: "GameSession") -> None:
    result = session.hunt()
    if isinstance(result, str):
        app.notify(result, severity="warning")
        return
    parts: list[str] = []
    if result.flavor:
        parts.append(result.flavor)
    if result.success:
        if result.provisions_gained:
            parts.append(f"+{result.provisions_gained} provisions")
        if result.pelts_gained:
            parts.append(f"+{result.pelts_gained} pelts")
        if result.silver_gained:
            parts.append(f"+{result.silver_gained} silver")
    elif not result.flavor:
        parts.append("Nothing useful found.")
    if result.danger_text:
        parts.append(result.danger_text)
    if result.crew_lost:
        parts.append(f"Lost {result.crew_lost} crew")
    if result.hull_damage:
        parts.append(f"Hull -{result.hull_damage}")
    msg = " ".join(parts) if parts else "Hunt complete."
    severity = "warning" if (result.danger_text or result.crew_lost or result.hull_damage) else "information"
    app.notify(msg, severity=severity, timeout=6)
    app.refresh_views()


def execute_contracts_flow(app, session: "GameSession") -> None:
    """Numbered picker of board.offers + active; accept/abandon via GameSession."""
    if not session.active:
        app.notify("No active game.", severity="warning")
        return
    if session.current_port:
        session._refresh_board(session.current_port)

    options: list[tuple[str, str]] = []
    day = session.world.day
    for offer in session.board.offers:
        days_left = offer.deadline_day - day
        options.append((
            f"accept:{offer.id}",
            f"Accept   {offer.title}  +{offer.reward_silver}s  {days_left}d",
        ))
    from portlight.engine.contracts import ContractStatus
    for contract in session.board.active:
        status = getattr(contract, "status", None)
        if status == ContractStatus.COMPLETED:
            continue
        days_left = contract.deadline_day - day
        title = getattr(contract, "title", None) or getattr(contract, "description", "")
        options.append((
            f"abandon:{contract.offer_id}",
            f"Abandon  {title}  {days_left}d left",
        ))
    if not options:
        app.notify("No contract offers or active obligations.", severity="warning")
        return

    def on_pick(choice: str | None) -> None:
        if choice is None:
            return
        if choice.startswith("accept:"):
            oid = choice[7:]
            offer = next((o for o in session.board.offers if o.id == oid), None)
            err = session.accept_contract(oid)
            if err:
                app.notify(f"\u2717 {err}", severity="error")
                return
            title = offer.title if offer else oid
            deadline = offer.deadline_day if offer else "?"
            app.notify(
                f"\u2713 Accepted: {title}  deadline day {deadline}",
                severity="information",
                timeout=6,
            )
            app.refresh_views()
            return
        if choice.startswith("abandon:"):
            oid = choice[8:]
            contract = next((c for c in session.board.active if c.offer_id == oid), None)
            err = session.abandon_contract_cmd(oid)
            if err:
                app.notify(f"\u2717 {err}", severity="error")
                return
            title = contract.title if contract else oid
            app.notify(f"Abandoned: {title}", severity="warning", timeout=5)
            app.refresh_views()

    app.push_screen(HarborSelectDialog(options, heading="Contracts"), on_pick)


def execute_save_picker(app, session: "GameSession") -> None:
    """Inactive-session modal: saves/*.json (slot, captain, day) plus New."""
    from portlight.app.session import list_save_slots

    slots = list_save_slots(session.base_path)
    options: list[tuple[str, str]] = []
    for info in slots:
        cap = info.get("captain") or "Unknown"
        options.append((
            info["slot"],
            f"{info['slot']}  {cap}  day {info['day']}",
        ))
    options.append(("new", "New game"))

    def on_pick(choice: str | None) -> None:
        if choice is None:
            app.notify(
                "No save selected. Pick a slot or New.",
                severity="warning",
                timeout=6,
            )
            return
        if choice == "new":
            _run_new_game(app, session)
            return
        session.slot = choice
        if session.load():
            app.notify(f"Loaded slot '{choice}'.", timeout=4)
            app.refresh_views()
            resume = getattr(app, "_resume_encounter_if_pending", None)
            if callable(resume):
                resume()
        else:
            app.notify(f"Could not load slot '{choice}'.", severity="error")

    app.push_screen(HarborSelectDialog(options, heading="Save slots"), on_pick)


def _run_new_game(app, session: "GameSession") -> None:
    """Captain-type picker matching CLI CAPTAIN_ORDER, then GameSession.new."""
    from portlight.engine.captain_identity import CAPTAIN_ORDER, CAPTAIN_TEMPLATES

    options: list[tuple[str, str]] = []
    for ct in CAPTAIN_ORDER:
        tmpl = CAPTAIN_TEMPLATES[ct]
        options.append((ct.value, f"{tmpl.name}  --  {tmpl.title}"))

    def on_type(choice: str | None) -> None:
        if choice is None:
            return
        session.new("Captain", captain_type=choice)
        app.notify(f"A new voyage begins ({choice}).", timeout=5)
        app.refresh_views()

    app.push_screen(HarborSelectDialog(options, heading="Captain type"), on_type)
