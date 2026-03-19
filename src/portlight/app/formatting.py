"""Formatting primitives — money, quantities, condition, scarcity, risk.

These are the building blocks for views. They turn raw numbers into
game-meaningful language that helps the player read situations.
"""

from __future__ import annotations


def silver(amount: int) -> str:
    """Format silver amount with icon."""
    return f"[yellow]{amount:,}[/yellow] silver"


def silver_delta(amount: int) -> str:
    """Format a gain/loss in silver."""
    if amount > 0:
        return f"[green]+{amount:,}[/green]"
    elif amount < 0:
        return f"[red]{amount:,}[/red]"
    return "[dim]0[/dim]"


def cargo_bar(used: float, capacity: int) -> str:
    """Visual cargo usage: [████░░░░] 24/80."""
    ratio = used / capacity if capacity > 0 else 0
    filled = int(ratio * 10)
    empty = 10 - filled
    color = "green" if ratio < 0.7 else "yellow" if ratio < 0.9 else "red"
    bar = f"[{color}]{'█' * filled}{'░' * empty}[/{color}]"
    return f"{bar} {int(used)}/{capacity}"


def hull_bar(current: int, maximum: int) -> str:
    """Visual hull condition."""
    ratio = current / maximum if maximum > 0 else 0
    filled = int(ratio * 10)
    empty = 10 - filled
    color = "green" if ratio > 0.6 else "yellow" if ratio > 0.3 else "red"
    bar = f"[{color}]{'█' * filled}{'░' * empty}[/{color}]"
    return f"{bar} {current}/{maximum}"


def provision_status(provisions: int) -> str:
    """Provisions with urgency coloring."""
    if provisions > 20:
        return f"[green]{provisions} days[/green]"
    elif provisions > 10:
        return f"[yellow]{provisions} days[/yellow]"
    elif provisions > 0:
        return f"[red]{provisions} days[/red]"
    return "[bold red]EMPTY[/bold red]"


def scarcity_tag(stock_current: int, stock_target: int) -> str:
    """Readable scarcity indicator for a market slot."""
    if stock_target == 0:
        return "[dim]—[/dim]"
    ratio = stock_current / stock_target
    if ratio < 0.3:
        return "[bold red]Scarce[/bold red]"
    elif ratio < 0.7:
        return "[yellow]Low[/yellow]"
    elif ratio < 1.3:
        return "[dim]Normal[/dim]"
    elif ratio < 2.0:
        return "[cyan]Plentiful[/cyan]"
    return "[bold cyan]Abundant[/bold cyan]"


def risk_tag(danger: float) -> str:
    """Route risk level from danger float."""
    if danger < 0.08:
        return "[green]Safe[/green]"
    elif danger < 0.12:
        return "[dim]Low risk[/dim]"
    elif danger < 0.16:
        return "[yellow]Moderate[/yellow]"
    elif danger < 0.20:
        return "[red]Dangerous[/red]"
    return "[bold red]Perilous[/bold red]"


def travel_time(distance: int, speed: float) -> str:
    """Estimated travel days."""
    days = max(1, round(distance / speed))
    if days == 1:
        return "1 day"
    return f"{days} days"


def profit_tag(buy_price: int, sell_price: int) -> str:
    """Quick profit/loss indicator for a potential trade."""
    diff = sell_price - buy_price
    if diff > 0:
        pct = int(diff / buy_price * 100) if buy_price > 0 else 0
        return f"[green]+{diff} ({pct}%)[/green]"
    elif diff < 0:
        return f"[red]{diff}[/red]"
    return "[dim]break-even[/dim]"


def upgrade_distance(current_silver: int, ship_price: int) -> str:
    """How far the player is from affording a ship upgrade."""
    gap = ship_price - current_silver
    if gap <= 0:
        return "[bold green]Can afford now![/bold green]"
    return f"[yellow]{gap:,}[/yellow] silver away"


def crew_status(crew: int, crew_max: int, crew_min: int) -> str:
    """Crew count with status coloring."""
    if crew >= crew_max:
        return f"[green]{crew}/{crew_max}[/green]"
    elif crew > crew_min:
        return f"[yellow]{crew}/{crew_max}[/yellow]"
    elif crew == crew_min:
        return f"[dim]{crew}/{crew_max} (skeleton)[/dim]"
    return f"[bold red]{crew}/{crew_max} (undermanned!)[/bold red]"
