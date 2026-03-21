"""Balance runner — execute seeded simulations with policy bots.

Takes a BalanceRunConfig, runs a game using a policy profile,
and returns structured RunMetrics.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from portlight.balance.collectors import (
    collect_run_metrics,
    compute_net_worth,
    update_route_tracker,
    update_timing,
)
from portlight.balance.policies import ActionPlan, choose_actions
from portlight.balance.types import (
    BalanceRunConfig,
    PhaseTiming,
    RouteRunMetrics,
    RunMetrics,
)


def run_balance_simulation(config: BalanceRunConfig) -> RunMetrics:
    """Run a single balance simulation and return metrics."""
    from portlight.app.session import GameSession

    with tempfile.TemporaryDirectory() as tmp:
        session = GameSession(Path(tmp))
        session.new("BalanceBot", captain_type=config.captain_type)

        # Override seed for reproducibility — both the session RNG and
        # module-level random (used by contract destination selection)
        import random
        random.seed(config.seed)
        session._rng = random.Random(config.seed)
        session.world.seed = config.seed

        route_tracker: dict[str, RouteRunMetrics] = {}
        timing = PhaseTiming()

        for day in range(config.max_days):
            if not session.active:
                break

            # Get actions from policy bot
            actions = choose_actions(session, config.policy_id)

            # Execute actions
            _execute_actions(session, actions, route_tracker)

            # If still in port and no sail happened, advance anyway
            if not session.at_sea and session.current_port:
                # Already acted in port, advance to next day
                session.advance()
            elif session.at_sea:
                # At sea — just advance
                session.advance()

            # Auto-resolve pending duels (bots can't respond to duel prompts)
            if session.world.pirates.pending_duel is not None:
                from portlight.engine.duel import resolve_duel
                from portlight.engine.models import PirateEncounterRecord
                pd = session.world.pirates.pending_duel
                # Bot fights with random stances
                stances = [session._rng.choice(["thrust", "slash", "parry"]) for _ in range(5)]
                result = resolve_duel(
                    player_stances=stances,
                    opponent_id=pd.captain_id, opponent_name=pd.captain_name,
                    opponent_personality=pd.personality, opponent_strength=pd.strength,
                    rng=session._rng,
                    player_crew=session.captain.ship.crew if session.captain.ship else 5,
                )
                session.captain.silver = max(0, session.captain.silver + result.silver_delta)
                outcome_str = "duel_win" if result.player_won else ("duel_draw" if result.draw else "duel_loss")
                session.world.pirates.encounters.append(PirateEncounterRecord(
                    captain_id=pd.captain_id, faction_id=pd.faction_id,
                    day=session.world.day, outcome=outcome_str, region=pd.region,
                ))
                if result.player_won:
                    session.world.pirates.duels_won += 1
                elif not result.draw:
                    session.world.pirates.duels_lost += 1
                session.world.pirates.pending_duel = None

            # Track timing events
            update_timing(timing, session, session.world.day)

            # Stop conditions
            if session.captain.silver <= 0 and session.captain.provisions <= 0:
                break  # bankruptcy
            if config.stop_on_victory and session.campaign.completed_paths:
                break

        # Collect day-band net worth snapshots
        metrics = collect_run_metrics(session, config, route_tracker, timing)
        # We need to capture these during the run; for now use final state
        metrics.net_worth_at_20 = _nw_estimate(session, 20)
        metrics.net_worth_at_40 = _nw_estimate(session, 40)
        metrics.net_worth_at_60 = _nw_estimate(session, 60)

        return metrics


def _nw_estimate(session, target_day: int) -> int:
    """Rough net worth estimate (final value scaled by day fraction)."""
    # In a full implementation we'd snapshot during the run.
    # For now return final net worth if we ran past target_day.
    if session.world.day >= target_day:
        return compute_net_worth(session)
    return 0


def _execute_actions(
    session,
    actions: list[ActionPlan],
    route_tracker: dict[str, RouteRunMetrics],
) -> None:
    """Execute a list of policy actions against the session."""
    for action in actions:
        try:
            _execute_one(session, action, route_tracker)
        except Exception as exc:
            import logging
            logging.getLogger(__name__).debug(
                "Policy bot action %s failed: %s", action.action, exc,
            )
            continue  # policy bots shouldn't crash the harness


def _execute_one(
    session,
    action: ActionPlan,
    route_tracker: dict[str, RouteRunMetrics],
) -> None:
    """Execute a single action."""
    a = action.action
    args = action.args

    if a == "buy":
        session.buy(args["good"], args["qty"])

    elif a == "sell":
        result = session.sell(args["good"], args["qty"])
        # Track route profit when we sell (approximation)
        if hasattr(result, 'total_price'):
            port = session.current_port
            if port and session.world.voyage:
                origin = session.world.voyage.origin_id
                update_route_tracker(
                    route_tracker, origin, port.id, result.total_price,
                )

    elif a == "sail":
        session.sail(args["destination"])

    elif a == "advance":
        session.advance()

    elif a == "provision":
        session.provision(args.get("days", 10))

    elif a == "repair":
        session.repair()

    elif a == "hire":
        session.hire_crew(args.get("count", 99))

    elif a == "buy_ship":
        session.buy_ship(args["ship_id"])

    elif a == "accept_contract":
        session.accept_contract(args["offer_id"])

    elif a == "lease_warehouse":
        from portlight.content.infrastructure import WAREHOUSE_TIERS
        from portlight.engine.infrastructure import WarehouseTier
        tier_name = args.get("tier", "depot")
        try:
            tier = WarehouseTier(tier_name)
        except ValueError:
            return
        spec = WAREHOUSE_TIERS.get(tier)
        if spec:
            session.lease_warehouse_cmd(spec)

    elif a == "open_broker":
        region = args.get("region", "")
        from portlight.content.infrastructure import available_broker_tiers
        from portlight.engine.infrastructure import BrokerTier, get_broker_tier
        current = get_broker_tier(session.infra, region)
        tiers = available_broker_tiers(region)
        if current == BrokerTier.NONE and tiers:
            session.open_broker_cmd(region, tiers[0])

    elif a == "open_credit":
        from portlight.content.infrastructure import available_credit_tiers
        from portlight.engine.infrastructure import check_credit_eligibility
        tiers = available_credit_tiers()
        for spec in reversed(tiers):
            err = check_credit_eligibility(
                session.infra, spec, session.captain.standing,
            )
            if err is None:
                session.open_credit_cmd(spec)
                break

    elif a == "draw_credit":
        amount = args.get("amount", 100)
        session.draw_credit_cmd(amount)

    elif a == "repay_credit":
        amount = args.get("amount", 100)
        session.repay_credit_cmd(amount)


def run_batch(configs: list[BalanceRunConfig]) -> list[RunMetrics]:
    """Run a batch of simulations and return all metrics."""
    return [run_balance_simulation(c) for c in configs]
