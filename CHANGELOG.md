# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.1.0-alpha] - 2026-03-20

### Added

- **Economy** — scarcity-driven pricing across 10 ports, 8 goods, 17 routes with flood penalty and market shocks
- **Voyages** — multi-day travel with storms, pirates, inspections, provisions, hull, and crew
- **Captain identity** — merchant, smuggler, navigator with 8-20% pricing gaps and distinct access profiles
- **Contracts** — 6 families with trust/standing gates, provenance-validated delivery, deadline tracking
- **Reputation** — regional standing, customs heat, commercial trust, multi-axis access model
- **Infrastructure** — warehouses (3 tiers), broker offices (2 tiers × 3 regions), 5 licenses with real upkeep
- **Insurance** — hull, cargo, contract guarantee policies with heat surcharges and claim resolution
- **Credit** — 3 tiers with interest accrual, payment deadlines, default consequences
- **Campaign** — 27 milestones, 7 career profile tags, 4 victory paths with diagnostics
- **Save/load** — full compound state round-trip (economy + contracts + infrastructure + insurance + credit + campaign)
- **CLI** — 30 commands via Typer with Rich rendering, welcome screen, contextual hints, grouped guide
- **Onboarding** — welcome view, hint system, flood explanation, contract deadline context, daily upkeep display
- **Balance harness** — 7 policy bots, 7 scenario packs, structured JSON/markdown reporting
- **Stress testing** — 14 cross-system invariants, 9 compound stress scenarios, trace recording
- **Documentation** — README, START_HERE, FIRST_VOYAGE, COMMANDS, CAREER_PATHS, EXAMPLE_RUNS, ALPHA_STATUS, KNOWN_ISSUES, RELEASE_NOTES
- 609 tests across 24 files
