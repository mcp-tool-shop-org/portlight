"""Run stress test suite.

Usage:
    python tools/run_stress.py                          # all scenarios
    python tools/run_stress.py --scenario debt_spiral   # single scenario
    python tools/run_stress.py --output artifacts/stress # custom output dir
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from portlight.balance.types import PolicyId
from portlight.stress.reporting import build_batch_report, write_json_report, write_markdown_report
from portlight.stress.runner import run_stress_scenario
from portlight.stress.scenarios import STRESS_SCENARIOS


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Portlight stress tests")
    parser.add_argument("--scenario", help="Run a single scenario by ID")
    parser.add_argument("--policy", default="opportunistic_trader",
                        help="Policy bot to use (default: opportunistic_trader)")
    parser.add_argument("--output", default="artifacts/stress",
                        help="Output directory for reports")
    parser.add_argument("--quiet", action="store_true", help="Suppress progress output")
    args = parser.parse_args()

    # Select scenarios
    if args.scenario:
        if args.scenario not in STRESS_SCENARIOS:
            print(f"Unknown scenario: {args.scenario}")
            print(f"Available: {', '.join(STRESS_SCENARIOS.keys())}")
            sys.exit(1)
        scenarios = [STRESS_SCENARIOS[args.scenario]]
    else:
        scenarios = list(STRESS_SCENARIOS.values())

    # Select policy
    try:
        policy_id = PolicyId(args.policy)
    except ValueError:
        print(f"Unknown policy: {args.policy}")
        sys.exit(1)

    # Run
    reports = []
    for scenario in scenarios:
        if not args.quiet:
            print(f"  Running {scenario.id}...", end=" ", flush=True)
        report = run_stress_scenario(scenario, policy_id)
        reports.append(report)
        if not args.quiet:
            status = "PASS" if report.passed else f"FAIL ({report.invariant_failures} violations)"
            print(status)

    # Report
    batch = build_batch_report(reports)
    out = Path(args.output)
    write_json_report(batch, out / "stress-report.json")
    write_markdown_report(batch, out / "stress-report.md")

    if not args.quiet:
        print(f"\n  {batch.total_scenarios} scenarios, {batch.total_failures} failures")
        print(f"  Reports: {out}/stress-report.{{json,md}}")

    sys.exit(1 if batch.total_failures > 0 else 0)


if __name__ == "__main__":
    main()
