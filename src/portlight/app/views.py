"""Rich views - game-facing screens that answer player questions.

Each view is a function that returns a Rich renderable (Panel, Table, Group).
Views never mutate game state. They read and present.

Captain screen answers: who am I, what advantages, what posture, what next.
Reputation screen answers: where do I stand, what's open, what's endangered.
Port screen answers: what's cheap, what's expensive, what do I hold, readiness.
Market screen answers: buy/sell prices, scarcity, what I can afford.
Route screen answers: where can I go, how long, how risky, can I provision it.
Ledger screen answers: what trades made money, what routes work, upgrade progress.
Shipyard screen answers: what ships, how they compare, can I afford one.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.columns import Columns
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from portlight.app import formatting as fmt
from portlight.content.goods import GOODS
from portlight.content.ships import SHIPS

if TYPE_CHECKING:
    from portlight.engine.captain_identity import CaptainTemplate
    from portlight.engine.models import Captain, Port, ReputationState, Route, Ship, WorldState
    from portlight.receipts.models import ReceiptLedger


# ---------------------------------------------------------------------------
# Captain view - identity, advantages, posture
# ---------------------------------------------------------------------------

def captain_view(captain: "Captain", template: "CaptainTemplate") -> Panel:
    """Captain identity screen: who you are, your modifiers, your posture."""
    lines: list[str] = []
    lines.append(f"[bold]{captain.name}[/bold] - {template.title}")
    lines.append(f"[italic]{template.description}[/italic]")
    lines.append("")

    # Pricing modifiers
    p = template.pricing
    lines.append("[bold]Trade Profile[/bold]")
    lines.append(f"  Buy prices:    {fmt.modifier_str(p.buy_price_mult, invert=True)}")
    lines.append(f"  Sell prices:   {fmt.modifier_str(p.sell_price_mult)}")
    if p.luxury_sell_bonus > 0:
        lines.append(f"  Luxury bonus:  [green]+{int(p.luxury_sell_bonus * 100)}% on silk/spice/porcelain[/green]")
    lines.append(f"  Port fees:     {fmt.modifier_str(p.port_fee_mult, invert=True)}")
    lines.append("")

    # Voyage modifiers
    v = template.voyage
    lines.append("[bold]Voyage Profile[/bold]")
    lines.append(f"  Provision burn:  {fmt.modifier_str(v.provision_burn, invert=True)}")
    if v.speed_bonus > 0:
        lines.append(f"  Speed bonus:     [green]+{v.speed_bonus}[/green]")
    if v.storm_resist_bonus > 0:
        lines.append(f"  Storm resist:    [green]+{int(v.storm_resist_bonus * 100)}%[/green]")
    lines.append(f"  Cargo damage:    {fmt.modifier_str(v.cargo_damage_mult, invert=True)}")
    lines.append("")

    # Inspection profile
    i = template.inspection
    lines.append("[bold]Inspection Profile[/bold]")
    lines.append(f"  Frequency:  {fmt.modifier_str(i.inspection_chance_mult, invert=True)}")
    if i.seizure_risk > 0:
        lines.append(f"  Seizure:    [red]{int(i.seizure_risk * 100)}% per inspection[/red]")
    lines.append(f"  Fines:      {fmt.modifier_str(i.fine_mult, invert=True)}")
    lines.append("")

    # Strengths / weaknesses
    lines.append("[bold green]Strengths[/bold green]")
    for s in template.strengths:
        lines.append(f"  + {s}")
    lines.append("[bold red]Weaknesses[/bold red]")
    for w in template.weaknesses:
        lines.append(f"  - {w}")

    return Panel("\n".join(lines), title=f"[bold]{template.name}[/bold]", border_style="blue")


# ---------------------------------------------------------------------------
# Reputation view - standing, heat, trust
# ---------------------------------------------------------------------------

def reputation_view(standing: "ReputationState", captain: "Captain") -> Panel:
    """Reputation screen: standing, heat, trust, access effects, recent incidents."""
    from portlight.engine.reputation import (
        get_fee_modifier,
        get_inspection_modifier,
        get_service_modifier,
        get_trust_tier,
    )

    lines: list[str] = []

    # Regional standing with fee effects
    lines.append("[bold]Regional Standing[/bold]")
    for region, value in standing.regional_standing.items():
        fee_mod = get_fee_modifier(standing, region)
        effect = ""
        if fee_mod < 1.0:
            effect = f"  [green]({int((1 - fee_mod) * 100)}% cheaper fees)[/green]"
        elif fee_mod > 1.0:
            effect = f"  [red](+{int((fee_mod - 1) * 100)}% fees)[/red]"
        lines.append(f"  {region:20s} {fmt.standing_tag(value)} ({value}){effect}")
    lines.append("")

    # Customs heat with inspection effects
    lines.append("[bold]Customs Heat[/bold]")
    for region, value in standing.customs_heat.items():
        insp_mod = get_inspection_modifier(standing, region)
        effect = ""
        if insp_mod > 1.0:
            effect = f"  [red](+{int((insp_mod - 1) * 100)}% inspections)[/red]"
        lines.append(f"  {region:20s} {fmt.heat_tag(value)} ({value}){effect}")
    lines.append("")

    # Commercial trust with tier
    trust_tier = get_trust_tier(standing)
    lines.append("[bold]Commercial Trust[/bold]")
    lines.append(f"  {fmt.trust_tag(standing.commercial_trust)} ({standing.commercial_trust}) - tier: [bold]{trust_tier}[/bold]")
    lines.append("")

    # Port standing with service effects (top 5 by value)
    if standing.port_standing:
        lines.append("[bold]Port Standing[/bold]")
        sorted_ports = sorted(standing.port_standing.items(), key=lambda x: x[1], reverse=True)
        for port_id, value in sorted_ports[:8]:
            svc_mod = get_service_modifier(standing, port_id)
            effect = ""
            if svc_mod < 1.0:
                effect = f"  [green]({int((1 - svc_mod) * 100)}% cheaper services)[/green]"
            lines.append(f"  {port_id:20s} {fmt.standing_tag(value)} ({value}){effect}")
        lines.append("")

    # Recent incidents (last 5)
    if standing.recent_incidents:
        lines.append("[bold]Recent Incidents[/bold]")
        for inc in standing.recent_incidents[:5]:
            # Color based on whether it was good or bad
            if inc.heat_delta > 0:
                icon = "[red]![/red]"
            elif inc.standing_delta > 0 or inc.trust_delta > 0:
                icon = "[green]+[/green]"
            else:
                icon = "[dim].[/dim]"
            lines.append(f"  {icon} Day {inc.day} at {inc.port_id}: {inc.description}")

    return Panel("\n".join(lines), title="[bold]Reputation[/bold]", border_style="cyan")


# ---------------------------------------------------------------------------
# Status view - the captain's dashboard
# ---------------------------------------------------------------------------

def status_view(world: "WorldState", ledger: "ReceiptLedger") -> Panel:
    """Captain overview: silver, ship, cargo, provisions, position, upgrade distance."""
    captain = world.captain
    ship = captain.ship

    lines: list[str] = []
    lines.append(f"[bold]{captain.name}[/bold]  Day {world.day}")
    lines.append(f"Silver: {fmt.silver(captain.silver)}")

    if ship:
        lines.append(f"Ship: [bold]{ship.name}[/bold] ({ship.template_id})")
        cargo_used = sum(c.quantity for c in captain.cargo)
        lines.append(f"Cargo: {fmt.cargo_bar(cargo_used, ship.cargo_capacity)}")
        lines.append(f"Hull:  {fmt.hull_bar(ship.hull, ship.hull_max)}")
        lines.append(f"Crew:  {fmt.crew_status(ship.crew, ship.crew_max, _crew_min(ship))}")
    lines.append(f"Provisions: {fmt.provision_status(captain.provisions)}")

    # Current location
    if world.voyage:
        from portlight.engine.models import VoyageStatus
        if world.voyage.status == VoyageStatus.AT_SEA:
            pct = int(world.voyage.progress / max(world.voyage.distance, 1) * 100)
            dest_name = world.ports.get(world.voyage.destination_id)
            dest_label = dest_name.name if dest_name else world.voyage.destination_id
            lines.append(f"[bold cyan]At sea[/bold cyan] → {dest_label} ({pct}% complete, day {world.voyage.days_elapsed})")
        else:
            port = world.ports.get(world.voyage.destination_id)
            lines.append(f"Docked at [bold]{port.name if port else '???'}[/bold]")

    # Upgrade tracker
    next_ship = _next_upgrade(ship, captain.silver)
    if next_ship:
        lines.append(f"Next upgrade: {next_ship.name} - {fmt.upgrade_distance(captain.silver, next_ship.price)}")

    # Net P&L
    if ledger.receipts:
        lines.append(f"Net P&L: {fmt.silver_delta(ledger.net_profit)} ({len(ledger.receipts)} trades)")

    return Panel("\n".join(lines), title="[bold]Captain Status[/bold]", border_style="blue")


# ---------------------------------------------------------------------------
# Port view - arrival screen
# ---------------------------------------------------------------------------

def port_view(port: "Port", captain: "Captain") -> Panel:
    """Port arrival screen: name, features, notable market conditions."""
    lines: list[str] = []
    lines.append(f"[italic]{port.description}[/italic]")
    lines.append(f"Region: {port.region}  |  Port fee: {fmt.silver(port.port_fee)}")
    lines.append(f"Provisions: {port.provision_cost}/day  |  Repairs: {port.repair_cost}/hp  |  Crew: {port.crew_cost}/head")

    if port.features:
        feats = ", ".join(f.value.replace("_", " ").title() for f in port.features)
        lines.append(f"Facilities: [cyan]{feats}[/cyan]")

    # Market highlights
    cheap = []
    expensive = []
    for slot in port.market:
        good = GOODS.get(slot.good_id)
        if not good:
            continue
        ratio = slot.stock_current / max(slot.stock_target, 1)
        if ratio > 1.3:
            cheap.append(f"[green]{good.name}[/green]")
        elif ratio < 0.5:
            expensive.append(f"[red]{good.name}[/red]")

    if cheap:
        lines.append(f"Cheap here: {', '.join(cheap)}")
    if expensive:
        lines.append(f"Pricey here: {', '.join(expensive)}")

    # Cargo summary
    if captain.cargo:
        cargo_names = [f"{c.quantity}x {GOODS[c.good_id].name}" for c in captain.cargo if c.good_id in GOODS]
        lines.append(f"You carry: {', '.join(cargo_names)}")
    else:
        lines.append("[dim]Hold is empty[/dim]")

    return Panel("\n".join(lines), title=f"[bold]{port.name}[/bold]", border_style="cyan")


# ---------------------------------------------------------------------------
# Market view - the trading screen
# ---------------------------------------------------------------------------

def market_view(port: "Port", captain: "Captain") -> Panel:
    """Full market board: buy/sell prices, scarcity, what you hold, what you can afford."""
    table = Table(title=f"{port.name} Market", show_header=True, header_style="bold")
    table.add_column("Good", style="bold")
    table.add_column("Buy", justify="right")
    table.add_column("Sell", justify="right")
    table.add_column("Stock", justify="center")
    table.add_column("Status")
    table.add_column("You Hold", justify="right")
    table.add_column("Can Buy", justify="right")

    for slot in port.market:
        good = GOODS.get(slot.good_id)
        if not good:
            continue
        held = sum(c.quantity for c in captain.cargo if c.good_id == slot.good_id)
        affordable = captain.silver // slot.buy_price if slot.buy_price > 0 else 0
        # Cap by available stock and cargo space
        ship = captain.ship
        if ship:
            cargo_used = sum(c.quantity for c in captain.cargo)
            space = ship.cargo_capacity - int(cargo_used)
            affordable = min(affordable, slot.stock_current, max(0, space))

        # Show flood penalty as sell price warning
        sell_str = str(slot.sell_price)
        if slot.flood_penalty > 0.1:
            sell_str = f"[red]{slot.sell_price}[/red] (flooded)"
        elif slot.flood_penalty > 0:
            sell_str = f"[yellow]{slot.sell_price}[/yellow]"

        table.add_row(
            good.name,
            str(slot.buy_price),
            sell_str,
            f"{slot.stock_current}/{slot.stock_target}",
            fmt.scarcity_tag(slot.stock_current, slot.stock_target),
            str(held) if held > 0 else "[dim]-[/dim]",
            str(affordable) if affordable > 0 else "[dim]-[/dim]",
        )

    return Panel(table, border_style="green")


# ---------------------------------------------------------------------------
# Cargo view
# ---------------------------------------------------------------------------

def cargo_view(captain: "Captain") -> Panel:
    """What's in the hold, cost basis, current value hints."""
    if not captain.cargo:
        return Panel("[dim]Hold is empty[/dim]", title="[bold]Cargo[/bold]", border_style="yellow")

    table = Table(show_header=True, header_style="bold")
    table.add_column("Good", style="bold")
    table.add_column("Qty", justify="right")
    table.add_column("Avg Cost", justify="right")
    table.add_column("Total Cost", justify="right")

    for item in captain.cargo:
        good = GOODS.get(item.good_id)
        name = good.name if good else item.good_id
        avg = item.cost_basis // item.quantity if item.quantity > 0 else 0
        table.add_row(name, str(item.quantity), str(avg), str(item.cost_basis))

    ship = captain.ship
    if ship:
        cargo_used = sum(c.quantity for c in captain.cargo)
        footer = f"\nCargo: {fmt.cargo_bar(cargo_used, ship.cargo_capacity)}"
    else:
        footer = ""

    return Panel(Group(table, Text.from_markup(footer) if footer else Text("")),
                 title="[bold]Cargo Hold[/bold]", border_style="yellow")


# ---------------------------------------------------------------------------
# Routes view - where can I go
# ---------------------------------------------------------------------------

def routes_view(world: "WorldState") -> Panel:
    """Available routes from current port with travel time, risk, provision cost."""
    current_port_id = world.voyage.destination_id if world.voyage else None
    ship = world.captain.ship

    table = Table(title="Available Routes", show_header=True, header_style="bold")
    table.add_column("Destination", style="bold")
    table.add_column("Region")
    table.add_column("Distance", justify="right")
    table.add_column("Est. Days", justify="right")
    table.add_column("Risk")
    table.add_column("Min Ship")
    table.add_column("Provisions", justify="right")

    from portlight.engine.voyage import check_route_suitability

    routes = _routes_from(world.routes, current_port_id)
    for route in routes:
        dest_id = route.port_b if route.port_a == current_port_id else route.port_a
        dest_port = world.ports.get(dest_id)
        if not dest_port:
            continue
        speed = ship.speed if ship else 4
        est_days = max(1, round(route.distance / speed))
        prov_needed = est_days + 2  # buffer

        prov_ok = world.captain.provisions >= prov_needed
        prov_color = "green" if prov_ok else "red"

        # Ship suitability
        suit_warning = check_route_suitability(route, ship) if ship else None
        if suit_warning and "BLOCKED" in suit_warning:
            ship_col = f"[bold red]{route.min_ship_class.title()}[/bold red]"
        elif suit_warning:
            ship_col = f"[yellow]{route.min_ship_class.title()}[/yellow]"
        else:
            ship_col = f"[dim]{route.min_ship_class.title()}[/dim]"

        table.add_row(
            dest_port.name,
            dest_port.region,
            str(route.distance),
            fmt.travel_time(route.distance, speed),
            fmt.risk_tag(route.danger),
            ship_col,
            f"[{prov_color}]{prov_needed} days[/{prov_color}]",
        )

    if not routes:
        return Panel("[dim]No routes available from here[/dim]", title="Routes", border_style="magenta")

    return Panel(table, border_style="magenta")


# ---------------------------------------------------------------------------
# Voyage view - at sea screen
# ---------------------------------------------------------------------------

def voyage_view(world: "WorldState", events: list | None = None) -> Panel:
    """At-sea status: progress, recent events, ship condition."""
    voyage = world.voyage
    captain = world.captain

    lines: list[str] = []

    if voyage:
        origin = world.ports.get(voyage.origin_id)
        dest = world.ports.get(voyage.destination_id)
        origin_name = origin.name if origin else voyage.origin_id
        dest_name = dest.name if dest else voyage.destination_id

        pct = int(voyage.progress / max(voyage.distance, 1) * 100)
        # Progress bar
        filled = pct // 10
        empty = 10 - filled
        bar = f"[cyan]{'#' * filled}{'-' * empty}[/cyan]"
        lines.append(f"{origin_name} {bar} {dest_name}")
        lines.append(f"Day {voyage.days_elapsed} at sea  |  {pct}% complete")
    else:
        lines.append("[dim]Not at sea[/dim]")

    if captain.ship:
        lines.append(f"Hull: {fmt.hull_bar(captain.ship.hull, captain.ship.hull_max)}")
        lines.append(f"Crew: {fmt.crew_status(captain.ship.crew, captain.ship.crew_max, _crew_min(captain.ship))}")
    lines.append(f"Provisions: {fmt.provision_status(captain.provisions)}")
    lines.append(f"Silver: {fmt.silver(captain.silver)}")

    if events:
        lines.append("")
        for event in events:
            lines.append(f"  {_event_icon(event.event_type.value)} {event.message}")

    return Panel("\n".join(lines), title="[bold]At Sea[/bold]", border_style="cyan")


# ---------------------------------------------------------------------------
# Ledger view
# ---------------------------------------------------------------------------

def ledger_view(ledger: "ReceiptLedger", captain: "Captain") -> Panel:
    """Trade history with P&L, route analysis, upgrade tracker."""
    if not ledger.receipts:
        return Panel("[dim]No trades recorded yet[/dim]", title="[bold]Trade Ledger[/bold]", border_style="white")

    table = Table(show_header=True, header_style="bold")
    table.add_column("Day", justify="right")
    table.add_column("Port")
    table.add_column("Action", justify="center")
    table.add_column("Good")
    table.add_column("Qty", justify="right")
    table.add_column("Price", justify="right")
    table.add_column("Total", justify="right")

    # Show last 15 receipts
    recent = ledger.receipts[-15:]
    for r in recent:
        action_style = "[green]BUY[/green]" if r.action.value == "buy" else "[red]SELL[/red]"
        good = GOODS.get(r.good_id)
        good_name = good.name if good else r.good_id
        table.add_row(
            str(r.day), r.port_id, action_style, good_name,
            str(r.quantity), str(r.unit_price), str(r.total_price),
        )

    summary_lines = []
    summary_lines.append(f"Total bought: {fmt.silver(ledger.total_buys)}")
    summary_lines.append(f"Total sold:   {fmt.silver(ledger.total_sells)}")
    summary_lines.append(f"Net P&L:      {fmt.silver_delta(ledger.net_profit)}")
    summary_lines.append(f"Trades:       {len(ledger.receipts)}")

    # Upgrade tracker
    next_ship = _next_upgrade(captain.ship, captain.silver)
    if next_ship:
        summary_lines.append(f"Next ship:    {next_ship.name} - {fmt.upgrade_distance(captain.silver, next_ship.price)}")

    summary = "\n".join(summary_lines)

    return Panel(Group(table, Text(""), Text.from_markup(summary)),
                 title="[bold]Trade Ledger[/bold]", border_style="white")


# ---------------------------------------------------------------------------
# Shipyard view
# ---------------------------------------------------------------------------

def shipyard_view(captain: "Captain") -> Panel:
    """Ship comparison panel for upgrade decisions."""
    current = captain.ship

    table = Table(title="Shipyard", show_header=True, header_style="bold")
    table.add_column("Ship", style="bold")
    table.add_column("Class")
    table.add_column("Cargo", justify="right")
    table.add_column("Speed", justify="right")
    table.add_column("Hull", justify="right")
    table.add_column("Crew", justify="right")
    table.add_column("Wage/day", justify="right")
    table.add_column("Storm Res.", justify="right")
    table.add_column("Price", justify="right")
    table.add_column("Status")

    for template in SHIPS.values():
        is_current = current and current.template_id == template.id
        status = "[bold cyan]* Current[/bold cyan]" if is_current else fmt.upgrade_distance(captain.silver, template.price)

        # Comparison arrows
        cargo_cmp = _compare(template.cargo_capacity, current.cargo_capacity if current else 0)
        speed_cmp = _compare(template.speed, current.speed if current else 0)
        hull_cmp = _compare(template.hull_max, current.hull_max if current else 0)

        # Daily wage cost (wage * crew_min is the minimum operating cost)
        wage_str = f"{template.daily_wage * template.crew_min}-{template.daily_wage * template.crew_max}"
        storm_str = f"{int(template.storm_resist * 100)}%" if template.storm_resist > 0 else "[dim]-[/dim]"

        table.add_row(
            template.name,
            template.ship_class.value.title(),
            f"{template.cargo_capacity} {cargo_cmp}",
            f"{template.speed} {speed_cmp}",
            f"{template.hull_max} {hull_cmp}",
            f"{template.crew_min}-{template.crew_max}",
            wage_str,
            storm_str,
            fmt.silver(template.price) if template.price > 0 else "[dim]-[/dim]",
            status,
        )

    return Panel(table, border_style="yellow")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _routes_from(routes: list["Route"], port_id: str | None) -> list["Route"]:
    if port_id is None:
        return []
    return [r for r in routes if r.port_a == port_id or r.port_b == port_id]


def _next_upgrade(ship: "Ship | None", silver: int) -> "ShipTemplate | None":
    """Find the cheapest ship the player doesn't have yet."""
    if ship is None:
        return None
    for template in sorted(SHIPS.values(), key=lambda s: s.price):
        if template.id != ship.template_id and template.price > 0:
            return template
    return None


def _compare(new: float, current: float) -> str:
    if new > current:
        return "[green]+[/green]"
    elif new < current:
        return "[red]-[/red]"
    return ""


def _crew_min(ship: "Ship") -> int:
    """Get crew_min from template."""
    template = SHIPS.get(ship.template_id)
    return template.crew_min if template else 1


def _event_icon(event_type: str) -> str:
    icons = {
        "storm": "[red]*[/red]",
        "pirates": "[red]![/red]",
        "inspection": "[yellow]?[/yellow]",
        "favorable_wind": "[green]>[/green]",
        "calm_seas": "[cyan]~[/cyan]",
        "provisions_spoiled": "[red]x[/red]",
        "nothing": "[dim].[/dim]",
    }
    return icons.get(event_type, "·")
