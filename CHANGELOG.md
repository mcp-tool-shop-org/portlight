# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [2.0.1] - 2026-03-25

### Added

- 4 version consistency tests (semver, >= 1.0.0, pyproject match, CHANGELOG)

### Fixed

- `__version__` was hardcoded — now reads dynamically from package metadata via importlib.metadata

## [2.0.0] - 2026-03-22

### Added

- **World expansion** — 20 ports across 5 regions (was 10/3), 43 routes, 17 goods, 5 ship classes
- **134 NPCs** — every port has 6-7 named NPCs with personality, agenda, standing-aware greetings, and relationship webs
- **Pirate ecosystem** — 4 factions (Crimson Tide, Monsoon Syndicate, Deep Reef Brotherhood, Iron Wolves), 8 named captains, bounty hunting, underworld standing
- **Full RPG combat** — personal combat with stance triangle (thrust/slash/parry), 7 melee weapons, 7 ranged weapons, 6 armor types, regional fighting styles, injury system
- **Naval combat** — ship-to-ship encounters with cannons, maneuver, boarding actions
- **Companion engine** — 5 officer roles (marine, navigator, surgeon, smuggler, quartermaster), named companions per region, morale system
- **Sea culture** — 87 route-specific encounters, 24 NPC sightings, 12 superstitions, 10 crew morale states, 20 seasonal weather narratives
- **Seasonal system** — 4 seasons (360-day cycle), 20 seasonal port profiles with danger/speed/market modifiers
- **Port politics** — 7 trade blocs, 21 bloc relationships, 20 political profiles, 25 cross-port NPC relationships
- **World cultures** — 5 regional cultures with ethos/sacred goods/proverbs/festivals, 20 port cultures with landmarks/customs/rumors
- **Bounty hunter class** — 9th playable character archetype with wanted system and breach tracking
- **Duel system** — turn-based personal combat with abilities, companions, crew bonuses
- **Anti-soft-lock** — emergency work/hunt/loan system prevents stranding
- **TUI interface** — Textual-based screens for combat, dashboard, routes, market, encounters
- **Print-and-Play** — `portlight print-and-play` CLI command generates a complete board game PDF kit
- 1,805+ tests across 72 files (was 609/24)

### Changed

- Economy rebalanced for 20-port world with regional scarcity dynamics
- Contract system expanded to 22 templates across 6 families
- Save format upgraded to v12 with full migration chain
- Victory path thresholds tuned for expanded world

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
