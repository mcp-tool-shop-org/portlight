"""Typer CLI — Phase 1 command interface.

Commands:
  portlight new [NAME]        — Start a new game
  portlight status            — Show captain, ship, cargo, silver
  portlight market            — Show current port's market board
  portlight buy GOOD QTY      — Buy goods
  portlight sell GOOD QTY     — Sell goods
  portlight ports             — List known ports and routes
  portlight sail DESTINATION  — Depart for a port
  portlight wait              — Advance one day (at sea or in port)
  portlight ledger            — Show trade receipt history
"""

import typer

app = typer.Typer(
    name="portlight",
    help="Portlight — trade-first maritime strategy game",
    no_args_is_help=True,
)


@app.command()
def new(name: str = typer.Argument("Captain", help="Captain name")) -> None:
    """Start a new game."""
    typer.echo(f"Starting new game as {name}... (not yet implemented)")


@app.command()
def status() -> None:
    """Show captain status."""
    typer.echo("Status display not yet implemented")


@app.command()
def market() -> None:
    """Show market board for current port."""
    typer.echo("Market board not yet implemented")


@app.command()
def buy(good: str, qty: int) -> None:
    """Buy goods from port market."""
    typer.echo(f"Buy {qty}x {good} — not yet implemented")


@app.command()
def sell(good: str, qty: int) -> None:
    """Sell goods to port market."""
    typer.echo(f"Sell {qty}x {good} — not yet implemented")


@app.command()
def ports() -> None:
    """List known ports and routes."""
    typer.echo("Port list not yet implemented")


@app.command()
def sail(destination: str) -> None:
    """Depart for a destination port."""
    typer.echo(f"Sail to {destination} — not yet implemented")


@app.command()
def wait() -> None:
    """Advance one day."""
    typer.echo("Wait — not yet implemented")


@app.command()
def ledger() -> None:
    """Show trade receipt ledger."""
    typer.echo("Ledger not yet implemented")


if __name__ == "__main__":
    app()
