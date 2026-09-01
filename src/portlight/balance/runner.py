"""Balance runner — execute seeded simulations with policy bots.

Takes a BalanceRunConfig, runs a game using a policy profile,
and returns structured RunMetrics.
"""

from __future__ import annotations

import random
import tempfile
from contextlib import contextmanager
from pathlib import Path

from portlight.balance.collectors import (
    collect_run_metrics,
    compute_net_worth,
    record_route_arrival,
    record_route_sale,
    update_timing,
)
from portlight.balance.policies import ActionPlan, choose_actions
from portlight.balance.scenarios import SCENARIOS, BalanceScenario
from portlight.balance.types import (
    BalanceRunConfig,
    PhaseTiming,
    RouteRunMetrics,
    RunMetrics,
)

_NW_BANDS = (20, 40, 60, 80, 100)


def run_balance_simulation(config: BalanceRunConfig) -> RunMetrics:
    """Run a single balance simulation and return metrics."""
    from portlight.app.session import GameSession

    scenario = SCENARIOS.get(config.scenario_id)

    with tempfile.TemporaryDirectory() as tmp:
        # Seed module-level random BEFORE session creation for full determinism.
        random.seed(config.seed)

        session = GameSession(Path(tmp))
        session.new("BalanceBot", captain_type=config.captain_type, seed=config.seed)
        session.auto_resolve_duels = True

        # Ensure session RNG matches the deterministic seed
        session._rng = random.Random(config.seed)

        if scenario is not None:
            _apply_premium_goods_bias(session, scenario.premium_goods_bias)

        route_tracker: dict[str, RouteRunMetrics] = {}
        timing = PhaseTiming()
        nw_at: dict[int, int] = {}

        with _scenario_world_mods(scenario):
            _run_days(session, config, route_tracker, timing, nw_at)

        metrics = collect_run_metrics(session, config, route_tracker, timing)
        metrics.net_worth_at_20 = nw_at.get(20, 0)
        metrics.net_worth_at_40 = nw_at.get(40, 0)
        metrics.net_worth_at_60 = nw_at.get(60, 0)
        metrics.net_worth_at_80 = nw_at.get(80, 0)
        metrics.net_worth_at_100 = nw_at.get(100, 0)
        return metrics


def _run_days(
    session,
    config: BalanceRunConfig,
    route_tracker: dict[str, RouteRunMetrics],
    timing: PhaseTiming,
    nw_at: dict[int, int],
) -> None:
    """Advance until world.day reaches max_days. One calendar tick per iteration."""
    guard = 0
    max_guard = max(config.max_days * 3, 10)
    while (
        session.active
        and session.world.day < config.max_days
        and guard < max_guard
    ):
        guard += 1
        was_at_sea = session.at_sea
        origin_id = (
            session.world.voyage.origin_id if session.world.voyage else None
        )

        actions = [
            a for a in choose_actions(session, config.policy_id)
            if a.action != "advance"
        ]
        _execute_actions(session, actions, route_tracker)

        if session.active:
            session.advance()

        if (
            was_at_sea
            and not session.at_sea
            and origin_id
            and session.current_port
        ):
            record_route_arrival(
                route_tracker, origin_id, session.current_port.id,
            )

        update_timing(timing, session, session.world.day)
        _snapshot_net_worth(session, nw_at)

        if session.captain.silver <= 0 and session.captain.provisions <= 0:
            break
        if config.stop_on_victory and session.campaign.completed_paths:
            break


def _snapshot_net_worth(session, nw_at: dict[int, int]) -> None:
    """Store net worth the first time world.day reaches each band. No backfill."""
    day = session.world.day
    for band in _NW_BANDS:
        if band not in nw_at and day >= band:
            nw_at[band] = compute_net_worth(session)


def _apply_premium_goods_bias(session, bias: float) -> None:
    """Scale luxury stock/target so premium_goods_bias actually changes the world."""
    if bias == 1.0:
        return
    from portlight.content.goods import GOODS
    from portlight.engine.models import GoodCategory

    for port in session.world.ports.values():
        for slot in port.market:
            good = GOODS.get(slot.good_id)
            if good is None or good.category != GoodCategory.LUXURY:
                continue
            slot.stock_current = max(0, int(round(slot.stock_current * bias)))
            slot.stock_target = max(1, int(round(slot.stock_target * bias)))
        session._recalc(port)


@contextmanager
def _scenario_world_mods(scenario: BalanceScenario | None):
    """Wire shock/enforcement/contract modifiers into engine calls for this run.

    Session already imported tick_markets and generate_offers by name, so both
    the engine module and the session module are patched. Restored on exit.
    """
    if scenario is None:
        yield
        return

    import portlight.app.session as session_mod
    import portlight.engine.contracts as contracts_mod
    import portlight.engine.economy as economy_mod
    import portlight.engine.reputation as reputation_mod

    orig_tick = economy_mod.tick_markets
    orig_session_tick = session_mod.tick_markets
    orig_insp = reputation_mod.get_inspection_modifier
    orig_offers = contracts_mod.generate_offers
    orig_session_offers = session_mod.generate_offers

    shock_mult = scenario.shock_frequency_mult
    enf_mult = scenario.enforcement_mult
    board_bias = scenario.contract_board_bias

    def tick_markets(ports, days=1, rng=None, current_day=0):
        rng = rng or random.Random()
        if shock_mult != 1.0:
            rng = _ShockScaledRng(rng, shock_mult)
        return orig_tick(ports, days=days, rng=rng, current_day=current_day)

    def get_inspection_modifier(rep, region):
        return orig_insp(rep, region) * enf_mult

    def generate_offers(*args, **kwargs):
        effects = dict(kwargs.get("board_effects") or {})
        effects["premium_offer_mult"] = (
            effects.get("premium_offer_mult", 1.0) * board_bias
        )
        effects["board_quality_bonus"] = (
            effects.get("board_quality_bonus", 1.0) * board_bias
        )
        kwargs["board_effects"] = effects
        return orig_offers(*args, **kwargs)

    economy_mod.tick_markets = tick_markets
    session_mod.tick_markets = tick_markets
    reputation_mod.get_inspection_modifier = get_inspection_modifier
    contracts_mod.generate_offers = generate_offers
    session_mod.generate_offers = generate_offers
    try:
        yield
    finally:
        economy_mod.tick_markets = orig_tick
        session_mod.tick_markets = orig_session_tick
        reputation_mod.get_inspection_modifier = orig_insp
        contracts_mod.generate_offers = orig_offers
        session_mod.generate_offers = orig_session_offers


class _ShockScaledRng:
    """Scale rng.random() so tick_markets shock thresholds track shock_frequency_mult.

    P(random() < p * mult) == P(random()/mult < p) for mult > 0.
    randint/choice are unscaled (shock magnitude / slot pick).
    """

    def __init__(self, inner, scale: float):
        self._inner = inner
        self._scale = scale

    def random(self) -> float:
        v = self._inner.random()
        if self._scale <= 0:
            return 1.0
        return min(1.0, v / self._scale)

    def randint(self, a: int, b: int) -> int:
        return self._inner.randint(a, b)

    def choice(self, seq):
        return self._inner.choice(seq)


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
        good_id = args["good"]
        qty = args["qty"]
        cargo_item = next(
            (c for c in session.captain.cargo if c.good_id == good_id), None,
        )
        cost = 0
        if cargo_item is not None and cargo_item.quantity > 0:
            cost = int(round(cargo_item.cost_basis * qty / cargo_item.quantity))
        result = session.sell(good_id, qty)
        if hasattr(result, "total_price"):
            port = session.current_port
            if port and session.world.voyage:
                origin = session.world.voyage.origin_id
                record_route_sale(
                    route_tracker, origin, port.id, result.total_price, cost,
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
        session.hire_crew(args.get("count", 99), args.get("role", "sailor"))

    elif a == "hire_role":
        session.hire_crew(args.get("count", 1), args.get("role", "sailor"))

    elif a == "fire_role":
        session.fire_crew(count=args.get("count", 1), role=args.get("role", "sailor"))

    elif a == "buy_ship":
        session.buy_ship(args["ship_id"])

    elif a == "install_upgrade":
        session.install_upgrade(args["upgrade_id"])

    elif a == "sell_fleet_ship":
        session.sell_fleet_ship(args["ship_name"])

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
