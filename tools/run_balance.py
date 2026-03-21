#!/usr/bin/env python3
"""Run balance simulation batch and generate reports.

Usage:
    python tools/run_balance.py                          # full matrix
    python tools/run_balance.py --scenario mixed_volatility
    python tools/run_balance.py --captain navigator --policy long_haul_optimizer
    python tools/run_balance.py --scenario stable_baseline --max-days 60
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from portlight.balance.reporting import (
    build_batch_report,
    write_json_report,
    write_markdown_report,
)
from portlight.balance.runner import run_balance_simulation
from portlight.balance.scenarios import SCENARIOS, get_scenario
from portlight.balance.types import BalanceRunConfig, PolicyId


CAPTAINS = ["merchant", "smuggler", "navigator"]
ALL_POLICIES = list(PolicyId)


def build_configs(
    scenarios: list[str] | None = None,
    captains: list[str] | None = None,
    policies: list[str] | None = None,
    max_days: int = 120,
) -> list[BalanceRunConfig]:
    """Build run configurations from filters."""
    scenario_ids = scenarios or list(SCENARIOS.keys())
    captain_types = captains or CAPTAINS
    policy_ids = policies or [p.value for p in ALL_POLICIES]

    configs = []
    for sid in scenario_ids:
        scenario = get_scenario(sid)
        for captain in captain_types:
            for policy_str in policy_ids:
                policy = PolicyId(policy_str)
                for seed in scenario.seeds:
                    configs.append(BalanceRunConfig(
                        scenario_id=sid,
                        seed=seed,
                        captain_type=captain,
                        policy_id=policy,
                        max_days=max_days,
                    ))
    return configs


def main() -> None:
    parser = argparse.ArgumentParser(description="Run balance simulations")
    parser.add_argument("--scenario", nargs="*", help="Scenario IDs")
    parser.add_argument("--captain", nargs="*", help="Captain types")
    parser.add_argument("--policy", nargs="*", help="Policy IDs")
    parser.add_argument("--max-days", type=int, default=120)
    parser.add_argument(
        "--output", default="artifacts/balance",
        help="Output directory",
    )
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    configs = build_configs(
        scenarios=args.scenario,
        captains=args.captain,
        policies=args.policy,
        max_days=args.max_days,
    )

    if not args.quiet:
        print(f"Running {len(configs)} simulations...")

    start = time.time()
    all_metrics = []
    for i, config in enumerate(configs):
        if not args.quiet and (i + 1) % 10 == 0:
            print(f"  [{i + 1}/{len(configs)}] {config.captain_type}/{config.policy_id.value}/{config.scenario_id}")
        metrics = run_balance_simulation(config)
        all_metrics.append(metrics)

    elapsed = time.time() - start
    if not args.quiet:
        print(f"\nCompleted {len(all_metrics)} runs in {elapsed:.1f}s")

    # Build and write reports
    scenario_label = args.scenario[0] if args.scenario and len(args.scenario) == 1 else "mixed"
    report = build_batch_report(all_metrics, scenario_label)

    out_dir = Path(args.output)
    write_json_report(report, out_dir / "balance-report.json")
    write_markdown_report(report, out_dir / "balance-report.md")

    if not args.quiet:
        print(f"\nReports written to {out_dir}/")
        print("  balance-report.json")
        print("  balance-report.md")

        # Quick summary
        for ca in report.captain_aggregates:
            brig = f"day {ca.median_brigantine_day:.0f}" if ca.median_brigantine_day > 0 else "never"
            print(
                f"  {ca.captain_type:10s}: "
                f"brigantine={brig}, "
                f"contracts={ca.mean_contracts_completed:.1f}, "
                f"inspections={ca.mean_inspections:.1f}"
            )


if __name__ == "__main__":
    main()
