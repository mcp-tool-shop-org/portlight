# Scorecard

> Score a repo before remediation. Fill this out first, then use SHIP_GATE.md to fix.

**Repo:** mcp-tool-shop-org/portlight
**Date:** 2026-03-22
**Type tags:** `[all]` `[pypi]` `[cli]`

## Pre-Remediation Assessment

| Category | Score | Notes |
|----------|-------|-------|
| A. Security | 10/10 | SECURITY.md, threat model in README, no secrets, no telemetry, saves constrained to saves/ and artifacts/ |
| B. Error Handling | 9/10 | Rich-formatted errors, exit codes 0/1 via Typer, no raw stacks. Minor: game CLI doesn't need structured API errors (SKIP justified) |
| C. Operator Docs | 10/10 | README comprehensive + 7 translations, CHANGELOG, LICENSE, --help accurate, 10 docs guides, 49K world handbook |
| D. Shipping Hygiene | 9/10 | verify.sh exists, version matches manifest, clean wheel build, python_requires set. Minor: CI exists but was added post-initial-gate |
| E. Identity (soft) | 10/10 | Logo, translations (7 languages), landing page (Astro+Starlight), GitHub metadata complete |
| **Overall** | **48/50** | |

## Key Gaps

1. Version in SHIP_GATE.md was stale (said v0.1.0-alpha, now fixed to v2.0.0)
2. README test count was outdated (said 609, now 1,805+)
3. SCORECARD.md was unfilled template (now populated)

## Remediation Priority

| Priority | Item | Estimated effort |
|----------|------|-----------------|
| 1 | Version bump to v2.0.0 across all manifests | 5 min |
| 2 | Update test count in README and CHANGELOG | 5 min |
| 3 | Fill SCORECARD with actual audit results | 10 min |

## Post-Remediation

| Category | Before | After |
|----------|--------|-------|
| A. Security | 10/10 | 10/10 |
| B. Error Handling | 9/10 | 9/10 |
| C. Operator Docs | 9/10 | 10/10 |
| D. Shipping Hygiene | 8/10 | 9/10 |
| E. Identity (soft) | 10/10 | 10/10 |
| **Overall** | 46/50 | **48/50** |
