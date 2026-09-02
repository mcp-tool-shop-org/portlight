# Status

Portlight **2.1.0** is a shipped game, not an alpha. This file used to describe the 10-port alpha. It now describes what is live.

## What is live

- **Economy** — 20 ports, 18 goods, 43 routes. Flood penalty, market shocks, provenance.
- **Voyages** — Storms, pirates, inspections, provisions, hull, crew. Named pirate duels prefer an active bounty.
- **Nine captains** — Merchant through Bounty Hunter. Interactive roster on `portlight new` without `--type`.
- **TUI** — Full play path: save/new, harbor, contracts, infra, shipyard, fleet, campaign panel. Same save as the CLI.
- **Contracts** — Seven families, 24 templates.
- **Infrastructure** — Warehouses (3 tiers). Brokers Local + Established in all five regions. Seven licenses (five regional charters + two global).
- **Bounty hunt** — Board lists live captains only. `bounty accept` then `bounty hunt` spawns that captain.
- **Career** — 27 milestones, 7 profile tags, 4 victory paths. Dashboard shows the ledger; advance toasts new beats.
- **Print-and-play** — Kit-sized PDF (not a 71-page landscape explosion).

## Verification

- **1,853 tests**
- **14 cross-system invariants** under 9 compound stress scenarios
- **Balance harness** — 7 policy bots, 7 scenario packs
- Save format **v12** with a full migration chain
- Ruff-clean. Python 3.11 / 3.12 / 3.13

## What is not this release

Insurance file/claim is still CLI-only in the TUI (deferred). Convoy AI is not in. Trusted Publishing is live as workflow `release.yml` + environment `release` — do not recreate publishers.
