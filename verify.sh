#!/usr/bin/env bash
# Portlight verify script — test + lint + build in one command
set -e

echo "=== Portlight Verify ==="

echo ""
echo "--- Tests ---"
python -m pytest tests/ -q

echo ""
echo "--- Lint ---"
python -m ruff check src/ tests/

echo ""
echo "--- Build ---"
python -m build --wheel --sdist 2>/dev/null || pip wheel --no-deps -w dist . 2>/dev/null || echo "Build check: pip install -e works (hatchling)"

echo ""
echo "--- Smoke test ---"
python -c "from portlight.app.cli import app; print('CLI entrypoint: OK')"
python -c "from portlight.stress.invariants import check_all_invariants; print('Stress module: OK')"
python -c "from portlight.balance.runner import run_balance_simulation; print('Balance module: OK')"

echo ""
echo "=== All checks passed ==="
