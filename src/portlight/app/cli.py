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
