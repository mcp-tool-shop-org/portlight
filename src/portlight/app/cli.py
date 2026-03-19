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
        console.print("[red]No saved game found.[/red] Start one with: [bold]portlight new[/bold]")
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
    console.print(f"\n[bold green]A new voyage begins.[/bold green]\n")
    console.print(views.captain_view(s.captain, s.captain_template))
    console.print(views.port_view(s.current_port, s.captain))
    console.print(views.status_view(s.world, s.ledger))


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
    console.print(views.status_view(s.world, s.ledger))


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
    from portlight.app.formatting import silver, silver_delta
    cost_basis = 0
    # Estimate profit from receipt
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
            console.print(views.status_view(s.world, s.ledger))
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
            console.print(f"\n[bold green]Ship purchased![/bold green]\n")
            console.print(views.status_view(s.world, s.ledger))
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
    console.print(views.obligations_view(s.board, s.world.day))


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
        console.print(views.status_view(s.world, s.ledger))
    else:
        console.print("[red]No saved game found.[/red]")


if __name__ == "__main__":
    app()
