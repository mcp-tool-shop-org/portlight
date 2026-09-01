"""Stress runner — execute scenarios with invariant enforcement after every tick.

Unlike the balance runner (which measures outcomes), the stress runner
measures truth: does the game ever enter an illegal state?
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from portlight.balance.policies import ActionPlan, choose_actions
from portlight.balance.types import PolicyId
from portlight.stress.invariants import check_all_invariants
from portlight.stress.types import (
    InvariantResult,
    StressRunReport,
    StressScenario,
    Subsystem,
    TraceEvent,
)


def run_stress_scenario(
    scenario: StressScenario,
    policy_id: PolicyId = PolicyId.OPPORTUNISTIC_TRADER,
) -> StressRunReport:
    """Run one stress scenario and return a report with invariant results."""
    from portlight.app.session import GameSession

    with tempfile.TemporaryDirectory() as tmp:
        session = GameSession(Path(tmp))
        session.new("StressBot", captain_type=scenario.captain_type)
        session.auto_resolve_duels = True

        import random
        session._rng = random.Random(scenario.seed)
        session.world.seed = scenario.seed

        report = StressRunReport(scenario_id=scenario.id)
        _inject_preconditions(session, scenario)

        missing = _missing_preconditions(session, scenario)
        if missing:
            msg = "Required preconditions missing after inject: " + ", ".join(missing)
            report.invariant_results.append(InvariantResult(
                name="missing_preconditions",
                subsystem=Subsystem.PERSISTENCE,
                passed=False,
                message=msg,
            ))
            report.invariant_failures += 1
            report.notes = msg
            report.days_survived = session.world.day
            report.final_silver = session.captain.silver if session.captain else 0
            return report

        trace: list[TraceEvent] = []

        failures = check_all_invariants(session)
        if failures:
            report.invariant_results.extend(failures)
            report.invariant_failures += len(failures)

        did_mid_crisis_reload = False
        guard = 0
        max_guard = max(scenario.max_days * 3, 10)
        while (
            session.active
            and session.world.day < scenario.max_days
            and guard < max_guard
        ):
            guard += 1
            current_day = session.world.day

            try:
                actions = [
                    a for a in choose_actions(session, policy_id)
                    if a.action != "advance"
                ]
                action_error = _execute_actions(session, actions)
            except Exception as e:
                action_error = e
                trace.append(TraceEvent(
                    day=current_day,
                    action="error",
                    detail=str(e),
                    silver_after=session.captain.silver if session.captain else 0,
                ))

            if action_error is not None:
                _record_exception(
                    report, trace, current_day, session,
                    "uncaught_action_exception", action_error,
                )

            try:
                if session.active:
                    session.advance()
            except Exception as e:
                trace.append(TraceEvent(
                    day=current_day,
                    action="advance_error",
                    detail=str(e),
                    silver_after=session.captain.silver if session.captain else 0,
                ))
                _record_exception(
                    report, trace, current_day, session,
                    "uncaught_advance_exception", e,
                )

            _clear_or_fail_pending_duel(session, report, trace)

            if (
                scenario.id == "save_load_mid_crisis"
                and not did_mid_crisis_reload
                and session.world.day > current_day
            ):
                did_mid_crisis_reload = True
                _save_reload_tick(session, report, trace)

            silver = session.captain.silver if session.captain else 0
            trace.append(TraceEvent(
                day=session.world.day,
                action="tick",
                silver_after=silver,
            ))

            failures = check_all_invariants(session)
            if failures:
                report.invariant_results.extend(failures)
                report.invariant_failures += len(failures)
                for f in failures:
                    trace.append(TraceEvent(
                        day=session.world.day,
                        action=f"invariant_violation:{f.name}",
                        detail=f.message,
                        silver_after=silver,
                    ))

            if session.captain.silver <= 0 and session.captain.provisions <= 0:
                trace.append(TraceEvent(
                    day=session.world.day,
                    action="bankruptcy",
                    silver_after=session.captain.silver,
                ))
                break

        report.trace = trace
        report.days_survived = session.world.day
        report.final_silver = session.captain.silver if session.captain else 0
        if session.captain and session.captain.ship:
            report.final_ship_class = session.captain.ship.template_id
        return report


def _record_exception(
    report: StressRunReport,
    trace: list[TraceEvent],
    day: int,
    session,
    name: str,
    exc: BaseException,
) -> None:
    result = InvariantResult(
        name=name,
        subsystem=Subsystem.PERSISTENCE,
        passed=False,
        message=str(exc),
    )
    report.invariant_results.append(result)
    report.invariant_failures += 1
    silver = session.captain.silver if session.captain else 0
    if not any(e.action == name for e in trace[-2:]):
        trace.append(TraceEvent(
            day=day, action=name, detail=str(exc), silver_after=silver,
        ))


def _clear_or_fail_pending_duel(session, report: StressRunReport, trace: list[TraceEvent]) -> None:
    """Auto-resolve leftover duels; fail the scenario if one remains after the tick."""
    pirates = getattr(session.world, "pirates", None)
    if pirates is None or pirates.pending_duel is None:
        return
    if session.auto_resolve_duels:
        try:
            session._resolve_pending_duel()
        except Exception as e:
            _record_exception(
                report, trace, session.world.day, session,
                "uncaught_advance_exception", e,
            )
    if pirates.pending_duel is not None:
        result = InvariantResult(
            name="pending_duel_unresolved",
            subsystem=Subsystem.ECONOMY,
            passed=False,
            message="pending_duel remained after tick",
        )
        report.invariant_results.append(result)
        report.invariant_failures += 1
        trace.append(TraceEvent(
            day=session.world.day,
            action="invariant_violation:pending_duel_unresolved",
            detail=result.message,
            silver_after=session.captain.silver if session.captain else 0,
        ))


def _save_reload_tick(session, report: StressRunReport, trace: list[TraceEvent]) -> None:
    """Real save/load mid-crisis. Fail persistence if the round-trip drops."""
    try:
        session._save()
        loaded = session.load()
        session.auto_resolve_duels = True
    except Exception as e:
        _record_exception(
            report, trace, session.world.day, session,
            "uncaught_action_exception", e,
        )
        return
    if not loaded:
        result = InvariantResult(
            name="save_load_failed",
            subsystem=Subsystem.PERSISTENCE,
            passed=False,
            message="session.load() returned False mid-crisis",
        )
        report.invariant_results.append(result)
        report.invariant_failures += 1
        trace.append(TraceEvent(
            day=session.world.day,
            action="invariant_violation:save_load_failed",
            detail=result.message,
            silver_after=session.captain.silver if session.captain else 0,
        ))


def _inject_preconditions(session, scenario: StressScenario) -> None:
    """Apply scenario preconditions, including the named compound objects."""
    if scenario.inject_silver is not None:
        session.captain.silver = scenario.inject_silver

    if scenario.inject_provisions is not None:
        session.captain.provisions = scenario.inject_provisions

    if scenario.inject_heat is not None:
        for region, heat in scenario.inject_heat.items():
            session.captain.standing.customs_heat[region] = heat

    if scenario.inject_trust is not None:
        session.captain.standing.commercial_trust = scenario.inject_trust

    if scenario.inject_standing is not None:
        for region, standing in scenario.inject_standing.items():
            session.captain.standing.regional_standing[region] = standing

    sid = scenario.id
    if sid in ("debt_spiral", "oceanic_overextension", "save_load_mid_crisis"):
        _inject_credit(session, drawn_to_limit=True)
    if sid in ("warehouse_neglect", "save_load_mid_crisis"):
        _inject_warehouse(session)
    if sid in ("insured_luxury_loss", "save_load_mid_crisis"):
        _inject_insurance_and_luxury(session)
    if sid in ("contract_expiry_under_pressure", "save_load_mid_crisis"):
        _inject_contracts(session, near_deadline=True)
    if sid == "heat_license_conflict":
        _inject_license(session)
    if sid == "save_load_mid_crisis":
        session._save()
        session._stress_save_load_ok = bool(session.load())
        session.auto_resolve_duels = True


def _inject_credit(session, *, drawn_to_limit: bool) -> None:
    from portlight.content.infrastructure import CREDIT_TIERS
    from portlight.engine.infrastructure import CreditState, CreditTier

    spec = CREDIT_TIERS[CreditTier.MERCHANT_LINE]
    limit = spec.credit_limit
    outstanding = limit if drawn_to_limit else 0
    session.infra.credit = CreditState(
        tier=CreditTier.MERCHANT_LINE,
        credit_limit=limit,
        outstanding=outstanding,
        interest_accrued=0,
        last_interest_day=session.world.day,
        next_due_day=session.world.day + spec.interest_period,
        defaults=0,
        total_borrowed=outstanding,
        total_repaid=0,
        active=True,
    )


def _inject_warehouse(session) -> None:
    from portlight.engine.infrastructure import StoredLot, WarehouseLease, WarehouseTier

    port = session.current_port
    port_id = port.id if port else "porto_novo"
    region = port.region if port else "Mediterranean"
    day = session.world.day
    session.infra.warehouses.append(WarehouseLease(
        id="stress_wh",
        port_id=port_id,
        tier=WarehouseTier.DEPOT,
        capacity=20,
        lease_cost=50,
        upkeep_per_day=8,
        inventory=[StoredLot(
            good_id="grain", quantity=12,
            acquired_port=port_id, acquired_region=region,
            acquired_day=max(0, day - 2), deposited_day=day,
        )],
        opened_day=day,
        upkeep_paid_through=day,
        active=True,
    ))


def _inject_insurance_and_luxury(session) -> None:
    from portlight.content.infrastructure import POLICY_CATALOG
    from portlight.engine.infrastructure import ActivePolicy, PolicyScope
    from portlight.engine.models import CargoItem

    spec = POLICY_CATALOG["cargo_premium"]
    session.infra.policies.append(ActivePolicy(
        id="stress_cargo_pol",
        spec_id=spec.id,
        family=spec.family,
        scope=PolicyScope.ACTIVE_CARGO,
        purchased_day=session.world.day,
        coverage_pct=spec.coverage_pct,
        coverage_cap=spec.coverage_cap,
        premium_paid=spec.premium,
        active=True,
    ))
    port = session.current_port
    session.captain.cargo.append(CargoItem(
        good_id="silk",
        quantity=4,
        cost_basis=280,
        acquired_port=port.id if port else "porto_novo",
        acquired_region=port.region if port else "Mediterranean",
        acquired_day=session.world.day,
    ))


def _inject_contracts(session, *, near_deadline: bool) -> None:
    from portlight.engine.contracts import ActiveContract, ContractFamily

    day = session.world.day
    dest = "al_manar"
    if session.current_port and session.current_port.id == dest:
        dest = "silva_bay"
    deadline = day + 3 if near_deadline else day + 20
    session.board.active.append(ActiveContract(
        offer_id="stress_c1",
        template_id="t_stress",
        family=ContractFamily.PROCUREMENT,
        title="Grain under pressure",
        accepted_day=day,
        deadline_day=deadline,
        destination_port_id=dest,
        good_id="grain",
        required_quantity=25,
        delivered_quantity=0,
        reward_silver=200,
    ))
    session.board.active.append(ActiveContract(
        offer_id="stress_c2",
        template_id="t_stress_2",
        family=ContractFamily.PROCUREMENT,
        title="Timber under pressure",
        accepted_day=day,
        deadline_day=deadline + 1,
        destination_port_id=dest,
        good_id="timber",
        required_quantity=15,
        delivered_quantity=0,
        reward_silver=150,
    ))


def _inject_license(session) -> None:
    from portlight.engine.infrastructure import OwnedLicense

    session.infra.licenses.append(OwnedLicense(
        license_id="med_trade_charter",
        purchased_day=session.world.day,
        upkeep_paid_through=session.world.day,
        active=True,
    ))


def _missing_preconditions(session, scenario: StressScenario) -> list[str]:
    """Named objects the scenario contract requires after inject."""
    missing: list[str] = []
    sid = scenario.id
    if sid in ("debt_spiral", "oceanic_overextension", "save_load_mid_crisis"):
        cred = session.infra.credit
        if not cred or not cred.active or cred.outstanding <= 0:
            missing.append("credit drawn to limit")
    if sid in ("warehouse_neglect", "save_load_mid_crisis"):
        if not any(w.active and w.inventory for w in session.infra.warehouses):
            missing.append("warehouse with cargo")
    if sid in ("insured_luxury_loss", "save_load_mid_crisis"):
        if not session.infra.policies:
            missing.append("insurance policy")
        if sid in ("insured_luxury_loss", "save_load_mid_crisis"):
            from portlight.content.goods import GOODS
            from portlight.engine.models import GoodCategory
            has_lux = False
            for item in session.captain.cargo:
                good = GOODS.get(item.good_id)
                if good is not None and good.category == GoodCategory.LUXURY:
                    has_lux = True
                    break
            if not has_lux:
                missing.append("luxury cargo")
    if sid in ("contract_expiry_under_pressure", "save_load_mid_crisis"):
        if not session.board.active:
            missing.append("active contracts")
    if sid == "heat_license_conflict":
        if not any(lic.active for lic in session.infra.licenses):
            missing.append("license")
    if sid == "save_load_mid_crisis":
        if not getattr(session, "_stress_save_load_ok", True):
            missing.append("save/load round-trip")
    return missing


def _execute_actions(session, actions: list[ActionPlan]) -> Exception | None:
    """Execute policy actions. Returns the first exception instead of swallowing it."""
    from portlight.balance.runner import _execute_one
    dummy_tracker: dict = {}
    for action in actions:
        try:
            _execute_one(session, action, dummy_tracker)
        except Exception as e:
            return e
    return None


def run_stress_batch(
    scenarios: list[StressScenario],
    policy_id: PolicyId = PolicyId.OPPORTUNISTIC_TRADER,
) -> list[StressRunReport]:
    """Run a batch of stress scenarios."""
    return [run_stress_scenario(s, policy_id) for s in scenarios]
