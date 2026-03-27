---
title: Architecture
description: How Portlight is built — modules, data flow, and design principles.
sidebar:
  order: 5
---

## Stack

- **Python 3.11+** with Hatchling build system
- **Typer** for CLI commands
- **Rich** for terminal rendering
- **Textual** for TUI interface (optional)
- **fpdf2** for Print-and-Play PDF generation (optional)
- Engine-first design: plain dataclasses, no ORM

## Module structure

```
src/portlight/
  engine/       — economy, voyage, contracts, reputation, infrastructure,
                  campaign, combat (personal + naval), companions, seasons,
                  bounty, fleet, skills, weapon quality, injuries, narrative
  content/      — ports (20), goods (18), ships (5), routes (43),
                  contracts (24 templates), factions (4), companions (10),
                  melee weapons (8), ranged weapons (8), fighting styles (5),
                  ship upgrades (18), armor, seasons, cultures,
                  port institutions (134 NPCs)
  app/          — Typer CLI (50+ commands), Rich views, TUI screens,
                  session manager, captain selection
  balance/      — balance harness: 7 policy bots, 7 scenarios, reporting
  stress/       — stress testing: 14 invariants, 9 compound scenarios
  receipts/     — trade receipt schema and hashing
  printandplay/ — board game PDF generator (cards, board, rules)
```

## Data flow

Every command goes through the **GameSession**, which mediates between the CLI and engine state:

1. CLI command calls session method
2. Session delegates to engine functions
3. Engine mutates dataclass state
4. Session auto-saves after every mutation

## Session advance tick order

Each day advances through a fixed sequence:

1. **Reputation tick** — heat decay, standing adjustments
2. **Contract tick** — expiry, stale offers, board refresh
3. **Infrastructure upkeep** — warehouse, broker, license deductions
4. **Credit tick** — interest accrual, due dates, defaults
5. **Market shift** — restock, regional shocks, seasonal demand
6. **Voyage events** — storms, pirates, inspections, cultural encounters
7. **Companion tick** — morale shifts, departure triggers
8. **Campaign evaluation** — milestone checks, profile tag scoring
9. **Auto-save**

## Save format

JSON on the local filesystem. Save version 12 with full migration chain (v1-v12).

Compound state tuple:
`(WorldState, ReceiptLedger, ContractBoard, InfrastructureState, CampaignState)`

## Testing

- **1,836 tests** across 72+ files
- **Balance harness** — 7 policy bots, 7 scenario packs, deterministic seeds
- **Stress testing** — 14 cross-system invariants, 9 compound scenarios
- **Invariant enforcement** — checked after every tick in stress runs
- **Print-and-Play tests** — content sourcing validation, PDF output verification
- CI: Python 3.11 + 3.12 + 3.13 matrix, ruff lint, paths-gated triggers
