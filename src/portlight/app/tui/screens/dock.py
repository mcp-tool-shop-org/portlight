"""Dock-service dialogs -- provision, repair, hire, plus work/fire/hunt (TUI).

Reuses the TradeDialog/Input modal pattern from market.py and routes.py.
HarborSelectDialog is also the numbered picker for saves, captain type,
contract accept/abandon, infrastructure, shipyard, and fleet.
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
    """Numbered picker -- harbor, saves, captain type, contracts, infra, shipyard, fleet."""

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


def execute_infra_flow(app, session: "GameSession") -> None:
    """Numbered picker of warehouse / broker / license / credit actions.

    Insurance is deferred. Warehouse lease/deposit/withdraw require dock.
    Nested HarborSelectDialog + QtyDialog, same stack as harbor hire.
    """
    if not session.active:
        app.notify("No active game.", severity="warning")
        return

    options = [
        ("lease", "Lease warehouse"),
        ("deposit", "Deposit cargo"),
        ("withdraw", "Withdraw cargo"),
        ("broker", "Open/upgrade broker"),
        ("license", "Buy license"),
        ("credit_open", "Open credit"),
        ("credit_draw", "Draw credit"),
        ("credit_repay", "Repay credit"),
    ]

    def on_pick(choice: str | None) -> None:
        if choice is None:
            return
        if choice == "lease":
            _infra_lease(app, session)
        elif choice == "deposit":
            _infra_deposit(app, session)
        elif choice == "withdraw":
            _infra_withdraw(app, session)
        elif choice == "broker":
            _infra_broker(app, session)
        elif choice == "license":
            _infra_license(app, session)
        elif choice == "credit_open":
            _infra_credit_open(app, session)
        elif choice == "credit_draw":
            _infra_credit_draw(app, session)
        elif choice == "credit_repay":
            _infra_credit_repay(app, session)

    app.push_screen(HarborSelectDialog(options, heading="Infrastructure"), on_pick)


def _require_docked(app, session: "GameSession"):
    """Return current port, or notify and return None when at sea."""
    port = session.current_port
    if not port:
        app.notify("\u2693 Must be docked.", severity="warning")
        return None
    return port


def _infra_lease(app, session: "GameSession") -> None:
    port = _require_docked(app, session)
    if port is None:
        return
    from portlight.content.infrastructure import available_tiers

    tiers = available_tiers(port.id)
    if not tiers:
        app.notify("No warehouse facilities at this port.", severity="warning")
        return

    options = [
        (
            spec.tier.value,
            f"{spec.name}  {spec.capacity} cap  {spec.lease_cost}s  {spec.upkeep_per_day}/day",
        )
        for spec in tiers
    ]

    def on_tier(choice: str | None) -> None:
        if choice is None:
            return
        spec = next((t for t in tiers if t.tier.value == choice), None)
        if spec is None:
            app.notify(f"Unknown tier: {choice}", severity="warning")
            return
        err = session.lease_warehouse_cmd(spec)
        if err:
            app.notify(f"\u2717 {err}", severity="error")
            return
        app.notify(
            f"\u2713 Leased {spec.name} at {port.name}",
            severity="information",
            timeout=5,
        )
        app.refresh_views()

    app.push_screen(HarborSelectDialog(options, heading="Lease warehouse"), on_tier)


def _infra_deposit(app, session: "GameSession") -> None:
    port = _require_docked(app, session)
    if port is None:
        return
    from portlight.content.goods import GOODS
    from portlight.engine.infrastructure import get_warehouse

    if get_warehouse(session.infra, port.id) is None:
        app.notify("No warehouse at this port.", severity="warning")
        return

    held: dict[str, int] = {}
    for item in session.world.captain.cargo:
        if item.quantity > 0:
            held[item.good_id] = held.get(item.good_id, 0) + item.quantity
    if not held:
        app.notify("No cargo to deposit.", severity="warning")
        return

    options = []
    for gid, qty in held.items():
        good = GOODS.get(gid)
        name = good.name if good else gid
        options.append((gid, f"{name}  {qty} in hold"))

    def on_good(good_id: str | None) -> None:
        if good_id is None:
            return
        max_qty = held.get(good_id, 0)
        if max_qty <= 0:
            app.notify("No cargo to deposit.", severity="warning")
            return
        good = GOODS.get(good_id)
        name = good.name if good else good_id

        def on_qty(qty_str: str | None) -> None:
            if qty_str is None:
                return
            result = session.deposit_cmd(good_id, int(qty_str))
            if isinstance(result, str):
                app.notify(f"\u2717 {result}", severity="error")
                return
            app.notify(
                f"\u2713 Deposited {result}x {name} into warehouse",
                severity="information",
                timeout=5,
            )
            app.refresh_views()

        app.push_screen(QtyDialog(f"Deposit {name}", "per unit", max_qty, 0), on_qty)

    app.push_screen(HarborSelectDialog(options, heading="Deposit cargo"), on_good)


def _infra_withdraw(app, session: "GameSession") -> None:
    port = _require_docked(app, session)
    if port is None:
        return
    from portlight.content.goods import GOODS
    from portlight.engine.infrastructure import get_warehouse

    warehouse = get_warehouse(session.infra, port.id)
    if warehouse is None:
        app.notify("No warehouse at this port.", severity="warning")
        return

    stored: dict[str, int] = {}
    for lot in warehouse.inventory:
        if lot.quantity > 0:
            stored[lot.good_id] = stored.get(lot.good_id, 0) + lot.quantity
    if not stored:
        app.notify("Warehouse is empty.", severity="warning")
        return

    options = []
    for gid, qty in stored.items():
        good = GOODS.get(gid)
        name = good.name if good else gid
        options.append((gid, f"{name}  {qty} stored"))

    def on_good(good_id: str | None) -> None:
        if good_id is None:
            return
        max_qty = stored.get(good_id, 0)
        if max_qty <= 0:
            app.notify("Warehouse is empty.", severity="warning")
            return
        good = GOODS.get(good_id)
        name = good.name if good else good_id

        def on_qty(qty_str: str | None) -> None:
            if qty_str is None:
                return
            result = session.withdraw_cmd(good_id, int(qty_str))
            if isinstance(result, str):
                app.notify(f"\u2717 {result}", severity="error")
                return
            app.notify(
                f"\u2713 Withdrew {result}x {name} from warehouse",
                severity="information",
                timeout=5,
            )
            app.refresh_views()

        app.push_screen(QtyDialog(f"Withdraw {name}", "per unit", max_qty, 0), on_qty)

    app.push_screen(HarborSelectDialog(options, heading="Withdraw cargo"), on_good)


def _infra_broker(app, session: "GameSession") -> None:
    port = _require_docked(app, session)
    if port is None:
        return
    from portlight.content.infrastructure import available_broker_tiers

    region = port.region
    tiers = available_broker_tiers(region)
    if not tiers:
        app.notify(f"No broker offices available in {region}.", severity="warning")
        return

    options = [
        (
            spec.tier.value,
            f"{spec.name}  {spec.purchase_cost}s  {spec.upkeep_per_day}/day",
        )
        for spec in tiers
    ]

    def on_tier(choice: str | None) -> None:
        if choice is None:
            return
        spec = next((t for t in tiers if t.tier.value == choice), None)
        if spec is None:
            app.notify(f"Unknown broker tier: {choice}", severity="warning")
            return
        err = session.open_broker_cmd(region, spec)
        if err:
            app.notify(f"\u2717 {err}", severity="error")
            return
        app.notify(
            f"\u2713 {spec.name} opened in {region}",
            severity="information",
            timeout=5,
        )
        app.refresh_views()

    app.push_screen(HarborSelectDialog(options, heading="Open/upgrade broker"), on_tier)


def _infra_license(app, session: "GameSession") -> None:
    from portlight.content.infrastructure import LICENSE_CATALOG

    specs = sorted(LICENSE_CATALOG.values(), key=lambda s: s.purchase_cost)
    if not specs:
        app.notify("No licenses in the catalog.", severity="warning")
        return

    options = []
    for spec in specs:
        region = spec.region_scope or "Global"
        options.append((
            spec.id,
            f"{spec.name}  {region}  {spec.purchase_cost}s",
        ))

    def on_lic(choice: str | None) -> None:
        if choice is None:
            return
        spec = LICENSE_CATALOG.get(choice)
        if spec is None:
            app.notify(f"Unknown license: {choice}", severity="warning")
            return
        err = session.purchase_license_cmd(spec)
        if err:
            app.notify(f"\u2717 {err}", severity="error")
            return
        app.notify(
            f"\u2713 License purchased: {spec.name}",
            severity="information",
            timeout=5,
        )
        app.refresh_views()

    app.push_screen(HarborSelectDialog(options, heading="Buy license"), on_lic)


def _infra_credit_open(app, session: "GameSession") -> None:
    from portlight.content.infrastructure import available_credit_tiers

    specs = available_credit_tiers()
    if not specs:
        app.notify("No credit tiers available.", severity="warning")
        return

    options = [
        (
            spec.tier.value,
            f"{spec.name}  limit {spec.credit_limit}s  "
            f"{int(spec.interest_rate * 100)}%/{spec.interest_period}d",
        )
        for spec in specs
    ]

    def on_tier(choice: str | None) -> None:
        if choice is None:
            return
        spec = next((s for s in specs if s.tier.value == choice), None)
        if spec is None:
            app.notify(f"Unknown credit tier: {choice}", severity="warning")
            return
        err = session.open_credit_cmd(spec)
        if err:
            app.notify(f"\u2717 {err}", severity="error")
            return
        app.notify(
            f"\u2713 Credit line opened: {spec.name}",
            severity="information",
            timeout=5,
        )
        app.refresh_views()

    app.push_screen(HarborSelectDialog(options, heading="Open credit"), on_tier)


def _infra_credit_draw(app, session: "GameSession") -> None:
    cred = session.infra.credit
    if cred is None or not cred.active:
        app.notify("No credit line established.", severity="warning")
        return
    available = cred.credit_limit - cred.outstanding
    if available <= 0:
        app.notify("No credit available to draw.", severity="warning")
        return

    def on_qty(qty_str: str | None) -> None:
        if qty_str is None:
            return
        amount = int(qty_str)
        err = session.draw_credit_cmd(amount)
        if err:
            app.notify(f"\u2717 {err}", severity="error")
            return
        app.notify(
            f"\u2713 Drew {amount:,} silver on credit",
            severity="information",
            timeout=5,
        )
        app.refresh_views()

    app.push_screen(QtyDialog("Draw credit", "to draw", available, 1), on_qty)


def _infra_credit_repay(app, session: "GameSession") -> None:
    cred = session.infra.credit
    if cred is None or not cred.active:
        app.notify("No credit line established.", severity="warning")
        return
    total_owed = cred.outstanding + cred.interest_accrued
    if total_owed <= 0:
        app.notify("No outstanding debt.", severity="warning")
        return
    silver = session.world.captain.silver
    max_qty = min(total_owed, silver)
    if max_qty <= 0:
        app.notify("Can't afford to repay credit.", severity="warning")
        return

    def on_qty(qty_str: str | None) -> None:
        if qty_str is None:
            return
        amount = int(qty_str)
        err = session.repay_credit_cmd(amount)
        if err:
            app.notify(f"\u2717 {err}", severity="error")
            return
        app.notify(
            f"\u2713 Repaid {amount:,} silver",
            severity="information",
            timeout=5,
        )
        app.refresh_views()

    app.push_screen(QtyDialog("Repay credit", "to repay", max_qty, 1), on_qty)


def _require_shipyard(app, session: "GameSession"):
    """Return current port when docked at a shipyard, else notify and return None."""
    port = _require_docked(app, session)
    if port is None:
        return None
    from portlight.engine.models import PortFeature
    if PortFeature.SHIPYARD not in port.features:
        app.notify(f"{port.name} has no shipyard.", severity="warning")
        return None
    return port


def execute_shipyard_flow(app, session: "GameSession") -> None:
    """P-twice on Port: buy hull, install/remove upgrade, dry-dock.

    Buy/install/remove/dry-dock require a docked shipyard. Nested
    HarborSelectDialog of SHIPS / UPGRADES, same stack as infra.
    """
    if not session.active:
        app.notify("No active game.", severity="warning")
        return
    port = session.current_port
    if not port:
        app.notify("\u2693 Must be docked to visit the shipyard.", severity="warning")
        return

    options = [
        ("buy", "Buy hull"),
        ("install", "Install upgrade"),
        ("remove", "Remove upgrade (no refund)"),
        ("drydock", "Dry-dock"),
    ]

    def on_pick(choice: str | None) -> None:
        if choice is None:
            return
        if choice == "buy":
            _shipyard_buy(app, session)
        elif choice == "install":
            _shipyard_install(app, session)
        elif choice == "remove":
            _shipyard_remove(app, session)
        elif choice == "drydock":
            _shipyard_drydock(app, session)

    app.push_screen(HarborSelectDialog(options, heading="Shipyard"), on_pick)


def _shipyard_buy(app, session: "GameSession") -> None:
    port = _require_shipyard(app, session)
    if port is None:
        return
    from portlight.content.ships import SHIPS

    cap = session.world.captain
    current_id = cap.ship.template_id if cap.ship else ""
    options: list[tuple[str, str]] = []
    for tmpl in SHIPS.values():
        if tmpl.id == current_id:
            status = "*current"
        elif tmpl.price <= 0:
            status = "starting hull"
        elif tmpl.price > cap.silver:
            status = f"need {tmpl.price}s"
        else:
            status = f"{tmpl.price}s"
        options.append((
            tmpl.id,
            f"{tmpl.name}  cargo {tmpl.cargo_capacity}  hull {tmpl.hull_max}  {status}",
        ))
    if not options:
        app.notify("No hulls in the catalog.", severity="warning")
        return

    def on_hull(ship_id: str | None) -> None:
        if ship_id is None:
            return
        err = session.buy_ship(ship_id)
        if err:
            app.notify(f"\u2717 {err}", severity="error")
            return
        tmpl = SHIPS.get(ship_id)
        name = tmpl.name if tmpl else ship_id
        app.notify(
            f"\u2713 Ship purchased: {name}",
            severity="information",
            timeout=5,
        )
        if session.last_jettison:
            from portlight.content.goods import GOODS
            bits = []
            for good_id, qty in session.last_jettison:
                good = GOODS.get(good_id)
                gname = good.name if good else good_id
                bits.append(f"{qty}x {gname}")
            app.notify(
                f"Cargo trimmed: {', '.join(bits)}",
                severity="warning",
                timeout=7,
            )
        app.refresh_views()

    app.push_screen(HarborSelectDialog(options, heading="Buy hull"), on_hull)


def _shipyard_install(app, session: "GameSession") -> None:
    port = _require_shipyard(app, session)
    if port is None:
        return
    from portlight.content.upgrades import UPGRADES

    ship = session.world.captain.ship if session.world else None
    if not ship:
        app.notify("No ship.", severity="warning")
        return
    slots_used = len(ship.upgrades)
    slots_max = ship.upgrade_slots
    if slots_used >= slots_max:
        app.notify(
            f"No upgrade slots remaining ({slots_max}/{slots_max} used)",
            severity="warning",
        )
        return
    installed = {inst.upgrade_id for inst in ship.upgrades}
    silver = session.world.captain.silver
    options: list[tuple[str, str]] = []
    for uid, tmpl in sorted(UPGRADES.items(), key=lambda x: (x[1].category.value, x[1].price)):
        if uid in installed:
            continue
        cat = tmpl.category.value.replace("_", " ")
        if tmpl.price > silver:
            status = f"need {tmpl.price}s"
        else:
            status = f"{tmpl.price}s"
        options.append((uid, f"{tmpl.name}  {cat}  {status}"))
    if not options:
        app.notify("No upgrades available to install.", severity="warning")
        return

    def on_upg(upgrade_id: str | None) -> None:
        if upgrade_id is None:
            return
        err = session.install_upgrade(upgrade_id)
        if err:
            app.notify(f"\u2717 {err}", severity="error")
            return
        tmpl = UPGRADES.get(upgrade_id)
        name = tmpl.name if tmpl else upgrade_id
        app.notify(
            f"\u2713 Upgrade installed: {name}",
            severity="information",
            timeout=5,
        )
        app.refresh_views()

    app.push_screen(HarborSelectDialog(options, heading="Install upgrade"), on_upg)


def _shipyard_remove(app, session: "GameSession") -> None:
    port = _require_shipyard(app, session)
    if port is None:
        return
    from portlight.content.upgrades import UPGRADES

    ship = session.world.captain.ship if session.world else None
    if not ship:
        app.notify("No ship.", severity="warning")
        return
    if not ship.upgrades:
        app.notify("No upgrades installed.", severity="warning")
        return
    options: list[tuple[str, str]] = []
    for inst in ship.upgrades:
        tmpl = UPGRADES.get(inst.upgrade_id)
        name = tmpl.name if tmpl else inst.upgrade_id
        options.append((inst.upgrade_id, f"{name}  (no refund)"))

    def on_upg(upgrade_id: str | None) -> None:
        if upgrade_id is None:
            return
        err = session.remove_upgrade(upgrade_id)
        if err:
            app.notify(f"\u2717 {err}", severity="error")
            return
        tmpl = UPGRADES.get(upgrade_id)
        name = tmpl.name if tmpl else upgrade_id
        app.notify(f"Removed {name} (no refund).", timeout=5)
        app.refresh_views()

    app.push_screen(HarborSelectDialog(options, heading="Remove upgrade"), on_upg)


def _shipyard_drydock(app, session: "GameSession") -> None:
    port = _require_shipyard(app, session)
    if port is None:
        return
    cap = session.world.captain
    options: list[tuple[str, str]] = []
    if cap.ship:
        s = cap.ship
        options.append((
            "flagship",
            f"{s.name}  *flagship  hull {s.hull}/{s.hull_max}",
        ))
    for owned in cap.fleet:
        if owned.docked_port_id != port.id:
            continue
        s = owned.ship
        options.append((
            s.name,
            f"{s.name}  hull {s.hull}/{s.hull_max}",
        ))
    if not options:
        app.notify("No ship to dry-dock.", severity="warning")
        return

    def on_ship(choice: str | None) -> None:
        if choice is None:
            return
        ship_name = None if choice == "flagship" else choice
        result = session.dry_dock(ship_name)
        if isinstance(result, str):
            app.notify(f"\u2717 {result}", severity="error")
            return
        restored, cost = result
        app.notify(
            f"\u2713 Dry dock complete. Restored {restored} hull for {cost:,} silver",
            severity="information",
            timeout=5,
        )
        app.refresh_views()

    app.push_screen(HarborSelectDialog(options, heading="Dry-dock"), on_ship)


def execute_fleet_flow(app, session: "GameSession") -> None:
    """F-twice on Fleet: board, dock current, transfer cargo, sell.

    Board/dock/transfer/sell require dock. Nested HarborSelectDialog of
    flagship + docked fleet ships; QtyDialog for transfer qty. No convoy orders.
    """
    if not session.active:
        app.notify("No active game.", severity="warning")
        return
    port = session.current_port
    if not port:
        app.notify("\u2693 Must be docked.", severity="warning")
        return

    flag = session.world.captain.ship
    flag_name = flag.name if flag else "flagship"
    options = [
        ("board", "Board a docked ship"),
        ("dock", f"Dock current  {flag_name}"),
        ("transfer", "Transfer cargo"),
        ("sell", "Sell a docked ship"),
    ]

    def on_pick(choice: str | None) -> None:
        if choice is None:
            return
        if choice == "board":
            _fleet_board(app, session)
        elif choice == "dock":
            _fleet_dock(app, session)
        elif choice == "transfer":
            _fleet_transfer(app, session)
        elif choice == "sell":
            _fleet_sell(app, session)

    app.push_screen(HarborSelectDialog(options, heading="Fleet"), on_pick)


def _docked_fleet_options(session: "GameSession") -> list[tuple[str, str]]:
    """(ship_name, label) for fleet ships docked at the current port."""
    port = session.current_port
    if not port or not session.world:
        return []
    options: list[tuple[str, str]] = []
    for owned in session.world.captain.fleet:
        if owned.docked_port_id != port.id:
            continue
        s = owned.ship
        klass = s.template_id.replace("_", " ")
        options.append((s.name, f"{s.name}  {klass}  hull {s.hull}/{s.hull_max}"))
    return options


def _ships_at_port(session: "GameSession") -> list[tuple[str, str, list]]:
    """(name, label, cargo) for flagship + fleet ships docked at this port."""
    if not session.world:
        return []
    cap = session.world.captain
    rows: list[tuple[str, str, list]] = []
    if cap.ship:
        rows.append((cap.ship.name, f"{cap.ship.name}  *flagship", cap.cargo))
    port = session.current_port
    if port:
        for owned in cap.fleet:
            if owned.docked_port_id != port.id:
                continue
            rows.append((owned.ship.name, f"{owned.ship.name}  docked", owned.cargo))
    return rows


def _fleet_board(app, session: "GameSession") -> None:
    port = _require_docked(app, session)
    if port is None:
        return
    options = _docked_fleet_options(session)
    if not options:
        app.notify("No docked fleet ships at this port.", severity="warning")
        return

    def on_ship(name: str | None) -> None:
        if name is None:
            return
        err = session.board_fleet_ship(name)
        if err:
            app.notify(f"\u2717 {err}", severity="error")
            return
        app.notify(
            f"\u2713 Boarded {name}",
            severity="information",
            timeout=5,
        )
        app.refresh_views()

    app.push_screen(HarborSelectDialog(options, heading="Board ship"), on_ship)


def _fleet_dock(app, session: "GameSession") -> None:
    port = _require_docked(app, session)
    if port is None:
        return
    err = session.dock_current_ship()
    if err:
        app.notify(f"\u2717 {err}", severity="error")
        return
    app.notify("\u2713 Switched ships.", severity="information", timeout=5)
    app.refresh_views()


def _fleet_sell(app, session: "GameSession") -> None:
    port = _require_shipyard(app, session)
    if port is None:
        return
    options = _docked_fleet_options(session)
    if not options:
        app.notify("No docked fleet ships at this port.", severity="warning")
        return

    def on_ship(name: str | None) -> None:
        if name is None:
            return
        result = session.sell_fleet_ship(name)
        if isinstance(result, str):
            app.notify(f"\u2717 {result}", severity="error")
            return
        silver, sold_name = result
        app.notify(
            f"\u2713 Sold {sold_name} for {silver:,} silver",
            severity="information",
            timeout=5,
        )
        app.refresh_views()

    app.push_screen(HarborSelectDialog(options, heading="Sell ship"), on_ship)


def _fleet_transfer(app, session: "GameSession") -> None:
    port = _require_docked(app, session)
    if port is None:
        return
    from portlight.content.goods import GOODS

    ships = _ships_at_port(session)
    if len(ships) < 2:
        app.notify("Need another ship at this port.", severity="warning")
        return
    from_opts = [(name, label) for name, label, _cargo in ships]

    def on_from(from_name: str | None) -> None:
        if from_name is None:
            return
        to_opts = [
            (name, label) for name, label, _c in ships
            if name.lower() != from_name.lower()
        ]
        if not to_opts:
            app.notify("Need a destination ship.", severity="warning")
            return

        def on_to(to_name: str | None) -> None:
            if to_name is None:
                return
            src_cargo = next(
                (c for n, _lab, c in ships if n.lower() == from_name.lower()),
                [],
            )
            held: dict[str, int] = {}
            for item in src_cargo:
                if item.quantity > 0:
                    held[item.good_id] = held.get(item.good_id, 0) + item.quantity
            if not held:
                app.notify("No cargo on that ship.", severity="warning")
                return
            good_opts: list[tuple[str, str]] = []
            for gid, qty in held.items():
                good = GOODS.get(gid)
                gname = good.name if good else gid
                good_opts.append((gid, f"{gname}  {qty}"))

            def on_good(good_id: str | None) -> None:
                if good_id is None:
                    return
                max_qty = held.get(good_id, 0)
                if max_qty <= 0:
                    app.notify("No cargo on that ship.", severity="warning")
                    return
                good = GOODS.get(good_id)
                gname = good.name if good else good_id

                def on_qty(qty_str: str | None) -> None:
                    if qty_str is None:
                        return
                    qty = int(qty_str)
                    err = session.transfer_fleet_cargo(
                        good_id, qty, from_name, to_name,
                    )
                    if err:
                        app.notify(f"\u2717 {err}", severity="error")
                        return
                    app.notify(
                        f"\u2713 Transferred {qty} {gname}",
                        severity="information",
                        timeout=5,
                    )
                    app.refresh_views()

                app.push_screen(
                    QtyDialog(f"Transfer {gname}", "per unit", max_qty, 0),
                    on_qty,
                )

            app.push_screen(
                HarborSelectDialog(good_opts, heading="Transfer good"),
                on_good,
            )

        app.push_screen(HarborSelectDialog(to_opts, heading="To ship"), on_to)

    app.push_screen(HarborSelectDialog(from_opts, heading="From ship"), on_from)


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
