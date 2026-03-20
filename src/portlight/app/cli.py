"""Typer CLI — player-facing commands.

Every command produces an updated game screen. No raw success text.
The CLI feels like a commandable game, not a command library.
"""

from __future__ import annotations

import typer
from rich.console import Console

from portlight.app import views
from portlight.app.session import GameSession

app = typer.Typer(
    name="portlight",
    help="Portlight — trade-first maritime strategy game",
    no_args_is_help=True,
)
console = Console()


def _session() -> GameSession:
    """Load or fail with helpful message."""
    s = GameSession()
    if not s.load():
        console.print("[red]No saved game found.[/red] Start a new game with: [bold]portlight new YourName --type merchant[/bold]")
        raise typer.Exit(1)
    return s


# ---------------------------------------------------------------------------
# New game
# ---------------------------------------------------------------------------

@app.command()
def new(
    name: str = typer.Argument("Captain", help="Captain name"),
    captain_type: str = typer.Option("merchant", "--type", "-t", help="Captain type: merchant, smuggler, navigator"),
) -> None:
    """Start a new game. Choose your captain type to shape your career."""
    if captain_type not in ("merchant", "smuggler", "navigator"):
        console.print(f"[red]Unknown captain type: {captain_type}[/red]")
        console.print("Choose: [bold]merchant[/bold], [bold]smuggler[/bold], or [bold]navigator[/bold]")
        raise typer.Exit(1)
    s = GameSession()
    s.new(name, captain_type=captain_type)
    console.print("\n[bold green]A new voyage begins.[/bold green]\n")
    console.print(views.welcome_view(s.captain, s.captain_template, s.world, s.infra))


# ---------------------------------------------------------------------------
# Captain identity
# ---------------------------------------------------------------------------

@app.command()
def captain() -> None:
    """Show captain identity and advantages."""
    s = _session()
    t = s.captain_template
    if not t:
        console.print("[red]Unknown captain type[/red]")
        return
    console.print(views.captain_view(s.captain, t))


# ---------------------------------------------------------------------------
# Reputation
# ---------------------------------------------------------------------------

@app.command()
def reputation() -> None:
    """Show standing, customs heat, and commercial trust."""
    s = _session()
    console.print(views.reputation_view(s.captain.standing, s.captain))


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------

@app.command()
def status() -> None:
    """Show captain status."""
    s = _session()
    console.print(views.status_view(s.world, s.ledger, s.infra))


# ---------------------------------------------------------------------------
# Port
# ---------------------------------------------------------------------------

@app.command()
def port() -> None:
    """Show current port info."""
    s = _session()
    p = s.current_port
    if not p:
        console.print("[yellow]You're at sea. Use [bold]portlight advance[/bold] to continue sailing.[/yellow]")
        return
    console.print(views.port_view(p, s.captain))


# ---------------------------------------------------------------------------
# Market
# ---------------------------------------------------------------------------

@app.command()
def market() -> None:
    """Show market board for current port."""
    s = _session()
    p = s.current_port
    if not p:
        console.print("[yellow]You're at sea — no market here.[/yellow]")
        return
    console.print(views.market_view(p, s.captain))


# ---------------------------------------------------------------------------
# Cargo
# ---------------------------------------------------------------------------

@app.command()
def cargo() -> None:
    """Show cargo hold contents."""
    s = _session()
    console.print(views.cargo_view(s.captain))


# ---------------------------------------------------------------------------
# Buy
# ---------------------------------------------------------------------------

@app.command()
def buy(good: str, qty: int) -> None:
    """Buy goods from port market."""
    s = _session()
    result = s.buy(good, qty)
    if isinstance(result, str):
        console.print(f"[red]{result}[/red]")
        return
    # Show updated market + cargo after trade
    from portlight.app.formatting import silver
    console.print(f"\n[green]Bought {result.quantity}x {result.good_id} for {silver(result.total_price)}[/green]\n")
    console.print(views.market_view(s.current_port, s.captain))
    console.print(views.cargo_view(s.captain))


# ---------------------------------------------------------------------------
# Sell
# ---------------------------------------------------------------------------

@app.command()
def sell(good: str, qty: int) -> None:
    """Sell goods to port market."""
    s = _session()
    result = s.sell(good, qty)
    if isinstance(result, str):
        console.print(f"[red]{result}[/red]")
        return
    from portlight.app.formatting import silver
    # Show sale result
    console.print(f"\n[green]Sold {result.quantity}x {result.good_id} for {silver(result.total_price)}[/green]\n")
    console.print(views.market_view(s.current_port, s.captain))
    console.print(views.cargo_view(s.captain))


# ---------------------------------------------------------------------------
# Provision
# ---------------------------------------------------------------------------

@app.command()
def provision(days: int = typer.Argument(10, help="Days of provisions to buy")) -> None:
    """Buy provisions (2 silver per day)."""
    s = _session()
    err = s.provision(days)
    if err:
        console.print(f"[red]{err}[/red]")
        return
    from portlight.app.formatting import provision_status, silver
    console.print(f"[green]Provisioned for {days} days ({silver(days * 2)})[/green]")
    console.print(f"Provisions: {provision_status(s.captain.provisions)}")
    console.print(f"Silver: {silver(s.captain.silver)}")


# ---------------------------------------------------------------------------
# Repair
# ---------------------------------------------------------------------------

@app.command()
def repair(amount: int = typer.Argument(None, help="Hull points to repair (default: full)")) -> None:
    """Repair ship hull (3 silver per HP)."""
    s = _session()
    result = s.repair(amount)
    if isinstance(result, str):
        console.print(f"[red]{result}[/red]")
        return
    repaired, cost = result
    from portlight.app.formatting import hull_bar, silver
    console.print(f"[green]Repaired {repaired} hull points ({silver(cost)})[/green]")
    console.print(f"Hull: {hull_bar(s.captain.ship.hull, s.captain.ship.hull_max)}")
    console.print(f"Silver: {silver(s.captain.silver)}")


# ---------------------------------------------------------------------------
# Hire
# ---------------------------------------------------------------------------

@app.command()
def hire(count: int = typer.Argument(None, help="Crew to hire (default: fill)")) -> None:
    """Hire crew members (5 silver each)."""
    s = _session()
    if count is None:
        count = s.captain.ship.crew_max - s.captain.ship.crew if s.captain.ship else 0
    err = s.hire_crew(count)
    if err:
        console.print(f"[red]{err}[/red]")
        return
    from portlight.app.formatting import crew_status, silver
    ship = s.captain.ship
    from portlight.content.ships import SHIPS
    template = SHIPS.get(ship.template_id)
    crew_min = template.crew_min if template else 1
    console.print(f"[green]Hired {count} crew ({silver(count * 5)})[/green]")
    console.print(f"Crew: {crew_status(ship.crew, ship.crew_max, crew_min)}")


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.command()
def routes() -> None:
    """List available routes from current port."""
    s = _session()
    if s.at_sea:
        console.print("[yellow]You're at sea — check routes when you arrive.[/yellow]")
        return
    console.print(views.routes_view(s.world))


# ---------------------------------------------------------------------------
# Sail
# ---------------------------------------------------------------------------

@app.command()
def sail(destination: str) -> None:
    """Depart for a destination port."""
    s = _session()
    err = s.sail(destination)
    if err:
        console.print(f"[red]{err}[/red]")
        # Show routes to help
        if s.current_port:
            console.print()
            console.print(views.routes_view(s.world))
        return
    dest = s.world.ports.get(destination)
    dest_name = dest.name if dest else destination
    console.print(f"\n[bold cyan]Setting sail for {dest_name}![/bold cyan]\n")
    console.print(views.voyage_view(s.world))


# ---------------------------------------------------------------------------
# Advance
# ---------------------------------------------------------------------------

@app.command()
def advance(days: int = typer.Argument(1, help="Days to advance")) -> None:
    """Advance time (sail if at sea, wait if in port)."""
    s = _session()
    for _ in range(days):
        events = s.advance()

        if events:
            console.print(views.voyage_view(s.world, events))
        else:
            console.print(f"[dim]Day {s.world.day}. Markets shift.[/dim]")

        # Check if arrived
        if s.current_port:
            port = s.current_port
            console.print(f"\n[bold green]Arrived at {port.name}![/bold green]\n")
            console.print(views.port_view(port, s.captain))
            console.print(views.status_view(s.world, s.ledger, s.infra))
            break

        # Check if ship sank
        if s.captain.ship and s.captain.ship.hull <= 0:
            console.print("\n[bold red]Your ship has broken apart. The voyage ends here.[/bold red]")
            break


# ---------------------------------------------------------------------------
# Ledger
# ---------------------------------------------------------------------------

@app.command()
def ledger() -> None:
    """Show trade receipt ledger."""
    s = _session()
    console.print(views.ledger_view(s.ledger, s.captain))


# ---------------------------------------------------------------------------
# Shipyard
# ---------------------------------------------------------------------------

@app.command()
def shipyard(buy_ship: str = typer.Argument(None, help="Ship ID to purchase")) -> None:
    """View or buy ships at the shipyard."""
    s = _session()
    if not s.current_port:
        console.print("[yellow]Must be docked to visit the shipyard.[/yellow]")
        return

    if buy_ship:
        err = s.buy_ship(buy_ship)
        if err:
            console.print(f"[red]{err}[/red]")
        else:
            console.print("\n[bold green]Ship purchased![/bold green]\n")
            console.print(views.status_view(s.world, s.ledger, s.infra))
    else:
        console.print(views.shipyard_view(s.captain))


# ---------------------------------------------------------------------------
# Save / Load (explicit)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Contracts
# ---------------------------------------------------------------------------

@app.command()
def contracts() -> None:
    """Show the contract board at the current port."""
    s = _session()
    if not s.current_port:
        console.print("[yellow]Must be docked to view the contract board.[/yellow]")
        return
    console.print(views.contracts_view(s.board, s.world.day))


@app.command()
def obligations() -> None:
    """Show active contract obligations."""
    s = _session()
    console.print(views.obligations_view(s.board, s.world.day, s.world))


@app.command()
def accept(offer_id: str) -> None:
    """Accept a contract offer from the board."""
    s = _session()
    # Allow short IDs (first 8 chars)
    matched = next((o for o in s.board.offers if o.id.startswith(offer_id)), None)
    if not matched:
        console.print(f"[red]No offer matching '{offer_id}'. Check the board with: portlight contracts[/red]")
        return
    err = s.accept_contract(matched.id)
    if err:
        console.print(f"[red]{err}[/red]")
        return
    console.print(f"\n[bold green]Contract accepted: {matched.title}[/bold green]\n")
    console.print(views.obligations_view(s.board, s.world.day))


@app.command()
def abandon(offer_id: str) -> None:
    """Abandon an active contract (reputation cost)."""
    s = _session()
    # Allow short IDs
    matched = next((c for c in s.board.active if c.offer_id.startswith(offer_id)), None)
    if not matched:
        console.print(f"[red]No active contract matching '{offer_id}'. Check obligations with: portlight obligations[/red]")
        return
    err = s.abandon_contract_cmd(matched.offer_id)
    if err:
        console.print(f"[red]{err}[/red]")
        return
    console.print(f"\n[yellow]Contract abandoned: {matched.title}[/yellow]")
    console.print("[dim]Reputation penalty applied.[/dim]")


# ---------------------------------------------------------------------------
# Warehouses
# ---------------------------------------------------------------------------

@app.command()
def warehouse(
    action: str = typer.Argument(None, help="lease, deposit, withdraw, or omit to view"),
    arg1: str = typer.Argument(None, help="tier (for lease) or good_id (for deposit/withdraw)"),
    arg2: int = typer.Argument(None, help="quantity (for deposit/withdraw)"),
    source: str = typer.Option(None, "--source", "-s", help="Source port filter for withdraw"),
) -> None:
    """Manage warehouses: view, lease, deposit, or withdraw cargo."""
    s = _session()

    if action is None:
        # Show warehouse status
        port = s.current_port
        port_id = port.id if port else None
        port_name = port.name if port else None
        console.print(views.warehouse_view(s.infra, port_id, port_name))
        return

    if action == "lease":
        if not s.current_port:
            console.print("[yellow]Must be docked to lease a warehouse.[/yellow]")
            return
        if arg1 is None:
            # Show available tiers
            console.print(views.warehouse_lease_options(s.current_port.id))
            return
        from portlight.engine.infrastructure import WarehouseTier
        from portlight.content.infrastructure import available_tiers
        try:
            tier = WarehouseTier(arg1)
        except ValueError:
            console.print(f"[red]Unknown tier: {arg1}[/red]. Options: depot, regional, commercial")
            return
        tiers = available_tiers(s.current_port.id)
        spec = next((t for t in tiers if t.tier == tier), None)
        if not spec:
            console.print(f"[red]{s.current_port.name} does not support {arg1} warehouses.[/red]")
            return
        err = s.lease_warehouse_cmd(spec)
        if err:
            console.print(f"[red]{err}[/red]")
            return
        console.print(f"\n[bold green]Leased {spec.name} at {s.current_port.name}![/bold green]")
        console.print(f"Capacity: {spec.capacity} | Upkeep: {spec.upkeep_per_day}/day")
        console.print(f"Silver: {s.captain.silver}")
        return

    if action == "deposit":
        if arg1 is None or arg2 is None:
            console.print("[red]Usage: portlight warehouse deposit <good> <qty>[/red]")
            return
        result = s.deposit_cmd(arg1, arg2)
        if isinstance(result, str):
            console.print(f"[red]{result}[/red]")
            return
        console.print(f"[green]Deposited {result}x {arg1} into warehouse.[/green]")
        port = s.current_port
        console.print(views.warehouse_view(s.infra, port.id if port else None, port.name if port else None))
        return

    if action == "withdraw":
        if arg1 is None or arg2 is None:
            console.print("[red]Usage: portlight warehouse withdraw <good> <qty> [--source <port>][/red]")
            return
        result = s.withdraw_cmd(arg1, arg2, source)
        if isinstance(result, str):
            console.print(f"[red]{result}[/red]")
            return
        console.print(f"[green]Withdrew {result}x {arg1} from warehouse.[/green]")
        console.print(views.cargo_view(s.captain))
        return

    console.print(f"[red]Unknown warehouse action: {action}[/red]. Use: lease, deposit, withdraw")


# ---------------------------------------------------------------------------
# Broker offices
# ---------------------------------------------------------------------------

@app.command()
def office(
    action: str = typer.Argument(None, help="open, upgrade, or omit to view"),
    region: str = typer.Argument(None, help="Region name (Mediterranean, 'West Africa', 'East Indies')"),
) -> None:
    """Manage broker offices: view, open, or upgrade."""
    s = _session()

    if action is None:
        console.print(views.offices_view(s.infra))
        return

    if action in ("open", "upgrade"):
        if not s.current_port:
            console.print("[yellow]Must be docked to manage broker offices.[/yellow]")
            return
        port_region = s.current_port.region
        target_region = region or port_region

        from portlight.engine.infrastructure import BrokerTier, get_broker_tier
        from portlight.content.infrastructure import available_broker_tiers

        current = get_broker_tier(s.infra, target_region)
        tiers = available_broker_tiers(target_region)

        if not tiers:
            console.print(f"[red]No broker offices available in {target_region}.[/red]")
            return

        if region is None and action == "open":
            # Show options
            console.print(views.office_options_view(target_region, current.value))
            return

        # Find the right tier to open/upgrade to
        if action == "open" and current == BrokerTier.NONE:
            spec = tiers[0]  # Local tier
        elif action == "upgrade" and current == BrokerTier.LOCAL:
            spec = next((t for t in tiers if t.tier == BrokerTier.ESTABLISHED), None)
            if not spec:
                console.print(f"[red]No upgrade available in {target_region}.[/red]")
                return
        elif action == "open" and current != BrokerTier.NONE:
            console.print(f"[yellow]Already have a broker in {target_region}. Use [bold]portlight office upgrade[/bold] to upgrade.[/yellow]")
            return
        else:
            console.print(f"[yellow]Broker in {target_region} is already at maximum tier.[/yellow]")
            return

        err = s.open_broker_cmd(target_region, spec)
        if err:
            console.print(f"[red]{err}[/red]")
            return
        console.print(f"\n[bold green]{spec.name} opened![/bold green]")
        console.print(f"Board quality: +{int((spec.board_quality_bonus - 1) * 100)}% | Upkeep: {spec.upkeep_per_day}/day")
        return

    console.print(f"[red]Unknown office action: {action}[/red]. Use: open, upgrade")


# ---------------------------------------------------------------------------
# Licenses
# ---------------------------------------------------------------------------

@app.command()
def license(
    action: str = typer.Argument(None, help="buy or omit to view"),
    license_id: str = typer.Argument(None, help="License ID to purchase"),
) -> None:
    """View or purchase commercial licenses."""
    s = _session()

    if action is None:
        console.print(views.licenses_view(s.infra, s.captain.standing))
        return

    if action == "buy":
        if license_id is None:
            console.print("[red]Usage: portlight license buy <license_id>[/red]")
            console.print(views.licenses_view(s.infra, s.captain.standing))
            return
        from portlight.content.infrastructure import get_license_spec
        spec = get_license_spec(license_id)
        if not spec:
            # Try partial match
            from portlight.content.infrastructure import LICENSE_CATALOG
            matches = [s for s in LICENSE_CATALOG.values() if license_id in s.id]
            if len(matches) == 1:
                spec = matches[0]
            else:
                console.print(f"[red]Unknown license: {license_id}[/red]")
                return
        err = s.purchase_license_cmd(spec)
        if err:
            console.print(f"[red]{err}[/red]")
            return
        console.print(f"\n[bold green]License purchased: {spec.name}![/bold green]")
        console.print(f"Upkeep: {spec.upkeep_per_day}/day | Silver: {s.captain.silver}")
        return

    console.print(f"[red]Unknown license action: {action}[/red]. Use: buy")


# ---------------------------------------------------------------------------
# Insurance
# ---------------------------------------------------------------------------

@app.command()
def insure(
    action: str = typer.Argument(None, help="buy or omit to view"),
    policy_id: str = typer.Argument(None, help="Policy ID to purchase"),
    contract: str = typer.Option(None, "--contract", "-c", help="Contract ID for guarantee policies"),
) -> None:
    """View or purchase insurance policies."""
    s = _session()

    region = s.current_port.region if s.current_port else "Mediterranean"
    heat = s.captain.standing.customs_heat.get(region, 0)

    if action is None:
        console.print(views.insurance_view(s.infra, heat))
        return

    if action == "buy":
        if policy_id is None:
            console.print("[red]Usage: portlight insure buy <policy_id>[/red]")
            console.print(views.insurance_view(s.infra, heat))
            return
        from portlight.content.infrastructure import get_policy_spec
        spec = get_policy_spec(policy_id)
        if not spec:
            from portlight.content.infrastructure import POLICY_CATALOG
            matches = [p for p in POLICY_CATALOG.values() if policy_id in p.id]
            if len(matches) == 1:
                spec = matches[0]
            else:
                console.print(f"[red]Unknown policy: {policy_id}[/red]")
                return

        # Determine scope targets
        target_id = contract or ""
        voyage_origin = ""
        voyage_destination = ""
        if s.at_sea and s.world.voyage:
            voyage_origin = s.world.voyage.origin_id
            voyage_destination = s.world.voyage.destination_id
        elif s.current_port:
            voyage_origin = s.current_port.id

        err = s.purchase_policy_cmd(
            spec, target_id=target_id,
            voyage_origin=voyage_origin, voyage_destination=voyage_destination,
        )
        if err:
            console.print(f"[red]{err}[/red]")
            return

        # Show heat-adjusted premium
        heat_surcharge = max(0, heat) * spec.heat_premium_mult
        adj_premium = int(spec.premium * (1.0 + heat_surcharge))
        console.print(f"\n[bold green]Policy purchased: {spec.name}![/bold green]")
        console.print(f"Premium: {adj_premium} silver | Coverage: {int(spec.coverage_pct * 100)}% up to {spec.coverage_cap} silver")
        console.print(f"Silver: {s.captain.silver}")
        return

    console.print(f"[red]Unknown insure action: {action}[/red]. Use: buy")


# ---------------------------------------------------------------------------
# Credit
# ---------------------------------------------------------------------------

@app.command()
def credit(
    action: str = typer.Argument(None, help="open, draw, repay, or omit to view"),
    amount: int = typer.Argument(None, help="Amount to draw or repay"),
) -> None:
    """Manage credit line: view, open, draw, or repay."""
    s = _session()

    if action is None:
        console.print(views.credit_view(s.infra, s.captain.standing))
        return

    if action == "open":
        from portlight.content.infrastructure import available_credit_tiers
        from portlight.engine.infrastructure import check_credit_eligibility
        # Find the best tier the player qualifies for
        tiers = available_credit_tiers()
        best = None
        for spec in reversed(tiers):  # try highest first
            err = check_credit_eligibility(s.infra, spec, s.captain.standing)
            if err is None:
                best = spec
                break
        if best is None:
            console.print("[red]No credit tier available. Build trust and standing first.[/red]")
            console.print(views.credit_view(s.infra, s.captain.standing))
            return
        err = s.open_credit_cmd(best)
        if err:
            console.print(f"[red]{err}[/red]")
            return
        console.print(f"\n[bold green]Credit line opened: {best.name}![/bold green]")
        console.print(f"Limit: {best.credit_limit} | Rate: {int(best.interest_rate * 100)}% per {best.interest_period} days")
        return

    if action == "draw":
        if amount is None:
            console.print("[red]Usage: portlight credit draw <amount>[/red]")
            return
        err = s.draw_credit_cmd(amount)
        if err:
            console.print(f"[red]{err}[/red]")
            return
        from portlight.engine.infrastructure import _ensure_credit
        cred = _ensure_credit(s.infra)
        from portlight.app.formatting import silver
        console.print(f"[green]Drew {silver(amount)} on credit. Outstanding: {silver(cred.outstanding)}[/green]")
        console.print(f"Silver: {silver(s.captain.silver)}")
        return

    if action == "repay":
        if amount is None:
            console.print("[red]Usage: portlight credit repay <amount>[/red]")
            return
        err = s.repay_credit_cmd(amount)
        if err:
            console.print(f"[red]{err}[/red]")
            return
        from portlight.engine.infrastructure import _ensure_credit
        cred = _ensure_credit(s.infra)
        from portlight.app.formatting import silver
        remaining = cred.outstanding + cred.interest_accrued
        console.print(f"[green]Repaid {silver(amount)}. Remaining: {silver(remaining)}[/green]")
        console.print(f"Silver: {silver(s.captain.silver)}")
        return

    console.print(f"[red]Unknown credit action: {action}[/red]. Use: open, draw, repay")


# ---------------------------------------------------------------------------
# Milestones / Campaign
# ---------------------------------------------------------------------------

@app.command()
def milestones() -> None:
    """Show merchant career ledger: milestones, profile, and victory progress."""
    s = _session()
    snap = s._build_snapshot()
    console.print(views.milestones_view(s.campaign, snap))


# ---------------------------------------------------------------------------
# Guide - grouped command reference
# ---------------------------------------------------------------------------

@app.command()
def guide() -> None:
    """Show grouped command reference for all game actions."""
    from rich.panel import Panel
    lines: list[str] = []

    lines.append("[bold]Trading[/bold]")
    lines.append("  market          — view prices, stock, and what you can afford")
    lines.append("  buy <good> <n>  — buy goods from port market")
    lines.append("  sell <good> <n> — sell goods to port market")
    lines.append("  cargo           — view cargo hold contents")
    lines.append("")

    lines.append("[bold]Navigation[/bold]")
    lines.append("  routes          — list available routes from current port")
    lines.append("  sail <dest>     — depart for a destination port")
    lines.append("  advance [days]  — advance time (sail or wait)")
    lines.append("  port            — view current port info")
    lines.append("  provision [n]   — buy provisions")
    lines.append("  repair [n]      — repair hull")
    lines.append("  hire [n]        — hire crew")
    lines.append("")

    lines.append("[bold]Contracts[/bold]")
    lines.append("  contracts       — view contract board offers")
    lines.append("  accept <id>     — accept a contract offer")
    lines.append("  obligations     — view active contract obligations")
    lines.append("  abandon <id>    — abandon a contract (reputation cost)")
    lines.append("")

    lines.append("[bold]Infrastructure[/bold]")
    lines.append("  warehouse [action] — manage warehouses (lease, deposit, withdraw)")
    lines.append("  office [action]    — manage broker offices (open, upgrade)")
    lines.append("  license [buy <id>] — view or purchase licenses")
    lines.append("")

    lines.append("[bold]Finance[/bold]")
    lines.append("  insure [buy <id>]  — view or purchase insurance")
    lines.append("  credit [action]    — manage credit (open, draw, repay)")
    lines.append("")

    lines.append("[bold]Career[/bold]")
    lines.append("  captain         — view captain identity and advantages")
    lines.append("  reputation      — view standing, heat, and trust")
    lines.append("  milestones      — view career milestones and victory progress")
    lines.append("  status          — view captain overview")
    lines.append("  ledger          — view trade receipt history")
    lines.append("  shipyard [buy]  — view or buy ships")
    lines.append("")

    lines.append("[bold]System[/bold]")
    lines.append("  save            — explicitly save the game")
    lines.append("  load            — load a saved game")
    lines.append("  guide           — show this reference")

    console.print(Panel("\n".join(lines), title="[bold]Portlight Command Guide[/bold]", border_style="blue"))


# ---------------------------------------------------------------------------
# Save / Load (explicit)
# ---------------------------------------------------------------------------

@app.command()
def save() -> None:
    """Explicitly save the game."""
    s = _session()
    s._save()
    console.print("[green]Game saved.[/green]")


@app.command()
def load() -> None:
    """Load a saved game."""
    s = GameSession()
    if s.load():
        console.print("[green]Game loaded.[/green]")
        console.print(views.status_view(s.world, s.ledger, s.infra))
    else:
        console.print("[red]No saved game found.[/red]")


if __name__ == "__main__":
    app()
