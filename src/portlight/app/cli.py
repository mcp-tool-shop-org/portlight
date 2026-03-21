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
    global _active_encounter, _player_combatant, _opponent_combatant
    s = _session()
    for _ in range(days):
        events = s.advance()

        # Check for pirate encounter — intercept and create interactive encounter
        pirate_event = None
        for evt in events:
            if hasattr(evt, '_pending_duel') and evt._pending_duel is not None:
                pirate_event = evt
                break

        if pirate_event and pirate_event._pending_duel:
            console.print(views.voyage_view(s.world, events))
            # Create interactive encounter from the pending duel
            from portlight.engine.encounter import create_encounter
            enc = create_encounter(
                s.world.ports, s.world.voyage.destination_id if s.world.voyage else "porto_novo",
                s._rng,
            )
            if enc:
                # Override with the specific captain from the event
                pd = pirate_event._pending_duel
                enc.enemy_captain_id = pd.captain_id
                enc.enemy_captain_name = pd.captain_name
                enc.enemy_faction_id = pd.faction_id
                enc.enemy_personality = pd.personality
                enc.enemy_strength = pd.strength
                enc.enemy_region = pd.region

                _active_encounter = enc
                _player_combatant = None
                _opponent_combatant = None
                s.world.pirates.pending_duel = None  # clear old-style pending

                from portlight.app import combat_views
                from portlight.content.factions import FACTIONS, PIRATE_CAPTAINS
                faction = FACTIONS.get(pd.faction_id)
                captain_data = PIRATE_CAPTAINS.get(pd.captain_id)
                console.print(combat_views.encounter_view(
                    pd.captain_name,
                    faction.name if faction else "Unknown",
                    pd.personality, pd.strength,
                    f"{pd.captain_name}'s Ship",
                    captain_data.encounter_text if captain_data else "",
                ))
                console.print("\n[bold]Use [cyan]portlight encounter <negotiate|flee|fight>[/cyan][/bold]")
                break  # stop advancing — player must respond to encounter
            else:
                console.print(views.voyage_view(s.world, events))
        elif events:
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
# Duel
# ---------------------------------------------------------------------------

@app.command()
def duel(
    stances: str = typer.Argument(..., help="Comma-separated stances: thrust,slash,parry (5 rounds)"),
) -> None:
    """Fight a pirate captain in a sword duel. Stances: thrust, slash, parry."""
    s = _session()
    pending = s.world.pirates.pending_duel
    if pending is None:
        console.print("[yellow]No pirate has challenged you. Duels happen during pirate encounters at sea.[/yellow]")
        return

    # Parse stances
    stance_list = [st.strip().lower() for st in stances.split(",")]
    valid = {"thrust", "slash", "parry"}
    for st in stance_list:
        if st not in valid:
            console.print(f"[red]Invalid stance: {st}[/red]. Use: thrust, slash, parry")
            return
    if len(stance_list) < 3:
        console.print("[red]Provide at least 3 stances (e.g. thrust,parry,slash,thrust,parry)[/red]")
        return

    from portlight.engine.duel import resolve_duel
    from portlight.engine.models import PirateEncounterRecord

    result = resolve_duel(
        player_stances=stance_list,
        opponent_id=pending.captain_id,
        opponent_name=pending.captain_name,
        opponent_personality=pending.personality,
        opponent_strength=pending.strength,
        rng=s._rng,
        player_crew=s.captain.ship.crew if s.captain.ship else 5,
    )

    # Show round-by-round
    console.print(f"\n[bold]Duel vs {pending.captain_name}[/bold] (strength {pending.strength}, {pending.personality})\n")
    for i, r in enumerate(result.rounds, 1):
        outcome = "WIN" if r.damage_to_opponent > 0 and r.damage_to_player == 0 else (
            "LOSE" if r.damage_to_player > 0 and r.damage_to_opponent == 0 else "DRAW"
        )
        console.print(f"  Round {i}: You [{r.player_stance}] vs [{r.opponent_stance}] — {outcome}")
        console.print(f"    {r.flavor}")

    # Show result
    if result.player_won:
        console.print(f"\n[bold green]VICTORY![/bold green] You defeated {pending.captain_name}.")
    elif result.draw:
        console.print(f"\n[bold yellow]DRAW.[/bold yellow] Neither captain falls.")
    else:
        console.print(f"\n[bold red]DEFEAT.[/bold red] {pending.captain_name} bests you.")

    # Apply consequences
    s.captain.silver = max(0, s.captain.silver + result.silver_delta)
    from portlight.app.formatting import silver
    if result.silver_delta >= 0:
        console.print(f"  Silver: +{silver(result.silver_delta)}")
    else:
        console.print(f"  Silver: -{silver(abs(result.silver_delta))}")

    # Record encounter
    outcome_str = "duel_win" if result.player_won else ("duel_draw" if result.draw else "duel_loss")
    s.world.pirates.encounters.append(PirateEncounterRecord(
        captain_id=pending.captain_id,
        faction_id=pending.faction_id,
        day=s.world.day,
        outcome=outcome_str,
        region=pending.region,
    ))
    if result.player_won:
        s.world.pirates.duels_won += 1
    elif not result.draw:
        s.world.pirates.duels_lost += 1

    # Clear pending duel
    s.world.pirates.pending_duel = None
    s._save()


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
    lines.append("  duel <stances>  — fight a pirate captain (e.g. thrust,parry,slash)")
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


# ---------------------------------------------------------------------------
# Combat system commands (Phase 5+)
# ---------------------------------------------------------------------------

# Active encounter + combatant state held in module-level for interactive turns
_active_encounter: "EncounterState | None" = None
_player_combatant: "CombatantState | None" = None
_opponent_combatant: "CombatantState | None" = None


@app.command()
def encounter(
    choice: str = typer.Argument(..., help="negotiate, flee, or fight"),
) -> None:
    """Respond to a pirate encounter: negotiate, flee, or fight."""
    global _active_encounter
    from portlight.app import combat_views
    from portlight.engine.encounter import (
        begin_fight,
        resolve_flee,
        resolve_negotiate,
    )

    s = _session()
    if _active_encounter is None or _active_encounter.phase != "approach":
        console.print("[yellow]No active encounter. Encounters happen during pirate events at sea.[/yellow]")
        return

    enc = _active_encounter
    choice = choice.lower().strip()

    # Resolve ship stats (upgrades applied) for combat calculations
    from portlight.content.upgrades import UPGRADES
    from portlight.engine.ship_stats import resolved_ship
    combat_ship = resolved_ship(s.captain.ship, UPGRADES)

    if choice == "negotiate":
        success, msg = resolve_negotiate(
            enc, s.captain.standing.underworld_standing,
            s.captain.captain_type, s._rng,
        )
        console.print(f"\n{msg}")
        if not success:
            msg2 = begin_fight(enc, combat_ship)
            console.print(f"\n{msg2}")
            console.print(combat_views.naval_status_view(
                s.captain.ship.hull, s.captain.ship.hull_max,
                s.captain.ship.crew, s.captain.ship.cannons,
                enc.enemy_ship_hull, enc.enemy_ship_hull_max,
                enc.enemy_ship_crew, enc.enemy_ship_cannons,
                enc.boarding_progress, enc.boarding_threshold, 0,
            ))
        else:
            _active_encounter = None
        s._save()

    elif choice == "flee":
        escaped, dmg, msg = resolve_flee(enc, combat_ship, s._rng)
        console.print(f"\n{msg}")
        if dmg > 0:
            s.captain.ship.hull = max(0, s.captain.ship.hull - dmg)
        if escaped:
            _active_encounter = None
        else:
            msg2 = begin_fight(enc, combat_ship)
            console.print(f"\n{msg2}")
        s._save()

    elif choice == "fight":
        msg = begin_fight(enc, combat_ship)
        console.print(f"\n{msg}")
        console.print(combat_views.naval_status_view(
            s.captain.ship.hull, s.captain.ship.hull_max,
            s.captain.ship.crew, s.captain.ship.cannons,
            enc.enemy_ship_hull, enc.enemy_ship_hull_max,
            enc.enemy_ship_crew, enc.enemy_ship_cannons,
            enc.boarding_progress, enc.boarding_threshold, 0,
        ))
        s._save()

    else:
        console.print("[red]Choose: negotiate, flee, or fight[/red]")


@app.command()
def naval(
    action: str = typer.Argument(..., help="broadside, close, evade, or rake"),
) -> None:
    """Execute a naval combat action."""
    global _active_encounter
    from portlight.app import combat_views
    from portlight.engine.encounter import (
        get_encounter_naval_actions,
        resolve_boarding_phase,
        resolve_naval_turn,
    )

    s = _session()
    if _active_encounter is None or _active_encounter.phase != "naval":
        console.print("[yellow]Not in naval combat.[/yellow]")
        return

    enc = _active_encounter

    # Resolve ship stats (upgrades applied) for combat calculations
    from portlight.content.upgrades import UPGRADES
    from portlight.engine.ship_stats import resolved_ship, resolve_cannons
    effective_cannons = resolve_cannons(s.captain.ship, UPGRADES)
    valid = get_encounter_naval_actions(effective_cannons)
    action = action.lower().strip()
    if action not in valid:
        console.print(f"[red]Invalid action. Available: {', '.join(valid)}[/red]")
        return

    combat_ship = resolved_ship(s.captain.ship, UPGRADES)
    result = resolve_naval_turn(enc, action, combat_ship, s._rng)

    # Apply hull/crew damage to player ship
    s.captain.ship.hull = max(0, s.captain.ship.hull + result["player_hull_delta"])
    s.captain.ship.crew = max(0, s.captain.ship.crew + result["player_crew_delta"])

    console.print(combat_views.naval_round_view(result))

    if result["enemy_sunk"]:
        console.print("\n[bold green]Enemy ship sinks beneath the waves![/bold green]")
        s.world.pirates.naval_victories += 1
        _active_encounter = None
    elif result["boarding_triggered"]:
        console.print("\n[bold yellow]Boarding action![/bold yellow]")
        boarding = resolve_boarding_phase(enc, s.captain.ship.crew, s._rng)
        s.captain.ship.crew = max(0, s.captain.ship.crew - boarding["player_crew_lost"])
        console.print(f"\n{boarding['flavor']}")
        console.print("\n[bold]Personal combat begins! Use [cyan]portlight fight <action>[/cyan][/bold]")
    elif s.captain.ship.hull <= 0:
        console.print("\n[bold red]Your ship is sinking![/bold red]")
        s.world.pirates.naval_defeats += 1
        _active_encounter = None
    else:
        console.print(combat_views.naval_status_view(
            s.captain.ship.hull, s.captain.ship.hull_max,
            s.captain.ship.crew, s.captain.ship.cannons,
            enc.enemy_ship_hull, enc.enemy_ship_hull_max,
            enc.enemy_ship_crew, enc.enemy_ship_cannons,
            enc.boarding_progress, enc.boarding_threshold, enc.naval_turns,
        ))

    s._save()


@app.command()
def fight(
    action: str = typer.Argument(..., help="thrust, slash, parry, shoot, throw, dodge, or style action"),
) -> None:
    """Execute a personal combat action."""
    global _active_encounter, _player_combatant, _opponent_combatant
    from portlight.app import combat_views
    from portlight.engine.encounter import (
        create_duel_combatants,
        get_encounter_combat_actions,
        resolve_duel_turn,
    )
    from portlight.engine.injuries import create_injury

    s = _session()
    enc = _active_encounter
    if enc is None or enc.phase != "duel":
        console.print("[yellow]Not in personal combat.[/yellow]")
        return

    # Initialize combatants on first fight turn
    if _player_combatant is None or _opponent_combatant is None:
        gear = s.captain.combat_gear
        total_throwing = sum(gear.throwing_weapons.values()) if gear.throwing_weapons else 0
        _player_combatant, _opponent_combatant = create_duel_combatants(
            enc,
            player_crew=s.captain.ship.crew if s.captain.ship else 5,
            player_style=s.captain.active_style,
            player_injury_ids=[inj.injury_id for inj in s.captain.injuries],
            player_firearm=gear.firearm,
            player_ammo=gear.firearm_ammo,
            player_throwing=total_throwing,
            player_mechanical=gear.mechanical_weapon,
            player_mechanical_ammo=gear.mechanical_ammo,
        )

    p, o = _player_combatant, _opponent_combatant
    valid = get_encounter_combat_actions(p)
    action = action.lower().strip()
    if action not in valid:
        console.print(f"[red]Invalid action. Available: {', '.join(valid)}[/red]")
        return

    result = resolve_duel_turn(enc, action, p, o, s._rng)

    console.print(combat_views.combat_round_view({
        "turn": result.turn,
        "player_action": result.player_action,
        "opponent_action": result.opponent_action,
        "damage_to_opponent": result.damage_to_opponent,
        "damage_to_player": result.damage_to_player,
        "player_stamina_delta": result.player_stamina_delta,
        "injury_inflicted": result.injury_inflicted,
        "opponent_injury": result.opponent_injury,
        "flavor": result.flavor,
        "style_effect": result.style_effect,
    }))

    # Show status
    console.print(combat_views.combat_status_view(
        p.hp, p.hp_max, p.stamina, p.stamina_max,
        o.hp, o.hp_max, enc.enemy_captain_name,
        p.ammo, p.throwing_weapons, s.captain.active_style,
        [inj.injury_id for inj in s.captain.injuries] + (
            [result.injury_inflicted] if result.injury_inflicted else []
        ),
        get_encounter_combat_actions(p), result.turn,
    ))

    # Check fight over
    if enc.phase == "resolved":
        player_won = o.hp <= 0 and p.hp > 0
        draw = p.hp <= 0 and o.hp <= 0

        if player_won:
            silver_gain = 20 + enc.enemy_strength * 5
            s.captain.silver += silver_gain
            s.world.pirates.duels_won += 1
            console.print(f"\n[bold green]Victory! +{silver_gain} silver, +5 standing[/bold green]")
        elif draw:
            s.world.pirates.duels_won += 1  # mutual respect
            console.print("\n[bold yellow]Draw! Mutual respect earned.[/bold yellow]")
        else:
            silver_loss = 15 + enc.enemy_strength * 3
            s.captain.silver = max(0, s.captain.silver - silver_loss)
            s.world.pirates.duels_lost += 1
            console.print(f"\n[bold red]Defeated. -{silver_loss} silver.[/bold red]")

        # Apply injuries to captain
        if result.injury_inflicted:
            new_injury = create_injury(result.injury_inflicted, s.world.day)
            s.captain.injuries.append(new_injury)
            from portlight.content.injuries import INJURIES
            inj_def = INJURIES.get(result.injury_inflicted)
            if inj_def:
                console.print(f"\n[bold red]Injury: {inj_def.name} — {inj_def.description}[/bold red]")

        # Sync ammo back to captain
        gear = s.captain.combat_gear
        gear.firearm_ammo = p.ammo
        gear.mechanical_ammo = p.mechanical_ammo
        # Rough sync for throwing weapons
        if gear.throwing_weapons:
            total_before = sum(gear.throwing_weapons.values())
            spent = total_before - p.throwing_weapons
            for wid in gear.throwing_weapons:
                if spent <= 0:
                    break
                can_take = min(spent, gear.throwing_weapons[wid])
                gear.throwing_weapons[wid] -= can_take
                spent -= can_take

        _active_encounter = None
        _player_combatant = None
        _opponent_combatant = None

    s._save()


@app.command()
def train(
    style_id: str = typer.Argument(None, help="Style to learn (e.g. la_destreza, dambe)"),
) -> None:
    """Learn a fighting style from a regional master."""
    from portlight.app import combat_views
    from portlight.content.injuries import get_injured_body_parts
    from portlight.engine.training import can_learn_style, get_masters_at_port, learn_style

    s = _session()
    port = s.current_port
    if not port:
        console.print("[yellow]Must be docked at a port to train.[/yellow]")
        return

    masters = get_masters_at_port(port.id)
    if not masters and style_id is None:
        console.print("[dim]No fighting masters at this port.[/dim]")
        return

    if style_id is None:
        from portlight.content.fighting_styles import FIGHTING_STYLES
        master_dicts = []
        for m in masters:
            style = FIGHTING_STYLES.get(m.style_id)
            master_dicts.append({
                "name": m.name,
                "style": style.name if style else m.style_id,
                "style_id": m.style_id,
                "region": style.region if style else "",
                "cost": style.silver_cost if style else 0,
                "days": style.training_days if style else 0,
                "prereqs": style.prerequisite_styles if style else 0,
                "dialog": m.dialog,
                "description": m.description,
            })
        console.print(combat_views.training_view(
            port.name, master_dicts, s.captain.learned_styles, s.captain.silver,
        ))
        return

    injured_parts = get_injured_body_parts([inj.injury_id for inj in s.captain.injuries])
    error = can_learn_style(
        s.captain.learned_styles, injured_parts,
        s.captain.silver, port.id, style_id,
    )
    if error:
        console.print(f"[red]{error}[/red]")
        return

    from portlight.content.fighting_styles import FIGHTING_STYLES
    style = FIGHTING_STYLES[style_id]
    s.captain.learned_styles, s.captain.silver = learn_style(
        s.captain.learned_styles, s.captain.silver, style_id,
    )
    # Training days advance the clock
    for _ in range(style.training_days):
        s.advance()
    console.print(f"\n[bold green]Learned {style.name}![/bold green] ({style.training_days} days, {style.silver_cost} silver)")
    s._save()


@app.command(name="equip-style")
def equip_style(
    style_id: str = typer.Argument(None, help="Style to equip (or omit to unequip)"),
) -> None:
    """Equip or unequip a fighting style."""
    s = _session()
    if style_id is None:
        s.captain.active_style = None
        console.print("[dim]Fighting style unequipped.[/dim]")
        s._save()
        return

    if style_id not in s.captain.learned_styles:
        console.print(f"[red]You haven't learned {style_id}. Use [bold]portlight train[/bold] at the right port.[/red]")
        return

    from portlight.content.injuries import get_injured_body_parts
    from portlight.engine.training import check_style_usable
    injured_parts = get_injured_body_parts([inj.injury_id for inj in s.captain.injuries])
    if not check_style_usable(style_id, injured_parts):
        console.print(f"[red]Your injuries prevent using this style.[/red]")
        return

    s.captain.active_style = style_id
    from portlight.content.fighting_styles import FIGHTING_STYLES
    style = FIGHTING_STYLES[style_id]
    console.print(f"[bold green]Equipped: {style.name}[/bold green]")
    s._save()


@app.command()
def armory(
    buy: str = typer.Argument(None, help="Weapon or ammo ID to buy"),
    qty: int = typer.Argument(1, help="Quantity to buy"),
) -> None:
    """View or buy ranged weapons and ammunition."""
    from portlight.app import combat_views
    from portlight.content.ranged_weapons import AMMO, RANGED_WEAPONS, get_ammo_for_region, get_weapons_for_region

    s = _session()
    port = s.current_port
    if not port:
        console.print("[yellow]Must be docked to visit the armory.[/yellow]")
        return

    if buy is None:
        weapons = get_weapons_for_region(port.region)
        ammo = get_ammo_for_region(port.region)
        console.print(combat_views.armory_view(
            [{"id": w.id, "name": w.name, "type": w.weapon_type, "damage": f"{w.damage_min}-{w.damage_max}",
              "accuracy": f"{w.accuracy:.0%}", "cost": w.silver_cost, "reload": w.reload_turns}
             for w in weapons],
            {"firearm": s.captain.combat_gear.firearm, "firearm_ammo": s.captain.combat_gear.firearm_ammo,
             "throwing": s.captain.combat_gear.throwing_weapons,
             "mechanical": s.captain.combat_gear.mechanical_weapon,
             "mechanical_ammo": s.captain.combat_gear.mechanical_ammo},
        ))
        return

    gear = s.captain.combat_gear

    # Try weapon purchase
    if buy in RANGED_WEAPONS:
        weapon = RANGED_WEAPONS[buy]
        if port.region not in weapon.available_regions:
            console.print(f"[red]{weapon.name} not available in {port.region}.[/red]")
            return
        cost = weapon.silver_cost * qty
        if s.captain.silver < cost:
            console.print(f"[red]Need {cost} silver.[/red]")
            return
        s.captain.silver -= cost
        if weapon.weapon_type == "firearm":
            gear.firearm = buy
            console.print(f"[green]Bought {weapon.name}![/green]")
        elif weapon.weapon_type == "mechanical":
            gear.mechanical_weapon = buy
            console.print(f"[green]Bought {weapon.name}![/green]")
        elif weapon.weapon_type == "thrown":
            current = gear.throwing_weapons.get(buy, 0)
            gear.throwing_weapons[buy] = current + qty * weapon.ammo_per_purchase
            console.print(f"[green]Bought {qty * weapon.ammo_per_purchase}x {weapon.name}![/green]")
        s._save()
        return

    # Try ammo purchase
    if buy in AMMO:
        ammo_def = AMMO[buy]
        if port.region not in ammo_def.available_regions:
            console.print(f"[red]{ammo_def.name} not available in {port.region}.[/red]")
            return
        cost = ammo_def.silver_cost * qty
        if s.captain.silver < cost:
            console.print(f"[red]Need {cost} silver.[/red]")
            return
        s.captain.silver -= cost
        if ammo_def.weapon_type == "firearm":
            gear.firearm_ammo += qty * ammo_def.quantity
        elif ammo_def.weapon_type == "mechanical":
            gear.mechanical_ammo += qty * ammo_def.quantity
        console.print(f"[green]Bought {qty * ammo_def.quantity}x {ammo_def.name}![/green]")
        s._save()
        return

    console.print(f"[red]Unknown item: {buy}[/red]")


@app.command()
def injuries() -> None:
    """Show current injuries and healing status."""
    from portlight.app import combat_views
    from portlight.content.injuries import INJURIES

    s = _session()
    if not s.captain.injuries:
        console.print("[dim]No injuries. You're in fighting shape.[/dim]")
        return

    injury_data = []
    for inj in s.captain.injuries:
        defn = INJURIES.get(inj.injury_id)
        if defn:
            injury_data.append({
                "name": defn.name,
                "severity": defn.severity,
                "body_part": defn.body_part,
                "description": defn.description,
                "heal_remaining": inj.heal_remaining,
                "treated": inj.treated,
            })
    console.print(combat_views.injuries_view(injury_data))


if __name__ == "__main__":
    app()
