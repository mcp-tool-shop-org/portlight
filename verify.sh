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
python -m build --wheel --sdist

echo ""
echo "--- Smoke test (installed wheel) ---"
shopt -s nullglob
wheels=(dist/*.whl)
if (( ${#wheels[@]} != 1 )); then
  echo "ERROR: expected exactly one wheel in dist/, found ${#wheels[@]}" >&2
  ls -la dist/ >&2 || true
  exit 1
fi
# Import the built artifact, not an editable install / PYTHONPATH checkout.
SMOKE_DIR="$(mktemp -d)"
python -m pip install --no-deps --force-reinstall --target "$SMOKE_DIR" "${wheels[0]}"
PYTHONPATH="$SMOKE_DIR${PYTHONPATH:+:$PYTHONPATH}" python -c "from portlight.app.cli import app; print('CLI entrypoint: OK')"
PYTHONPATH="$SMOKE_DIR${PYTHONPATH:+:$PYTHONPATH}" python -c "from portlight.stress.invariants import check_all_invariants; print('Stress module: OK')"
PYTHONPATH="$SMOKE_DIR${PYTHONPATH:+:$PYTHONPATH}" python -c "from portlight.balance.runner import run_balance_simulation; print('Balance module: OK')"

echo ""
echo "=== All checks passed ==="
