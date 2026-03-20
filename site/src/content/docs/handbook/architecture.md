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
- Engine-first design: plain dataclasses, no ORM

## Module structure

```
src/portlight/
  engine/    — economy, voyage, contracts, reputation, infrastructure, campaign
  content/   — ports, goods, ships, routes, infrastructure specs, campaign thresholds
  app/       — Typer CLI (30 commands), Rich views, session manager
  balance/   — balance harness: policy bots, scenarios, runner, reporting
  stress/    — stress testing: invariants, scenarios, runner, reporting
  receipts/  — trade receipt schema and hashing
```

## Data flow

Every command goes through the **GameSession**, which mediates between the CLI and engine state:

1. CLI command calls session method
2. Session delegates to engine functions
3. Engine mutates dataclass state
4. Session auto-saves after every mutation

## Session advance tick order

Each day advances through a fixed sequence:

1. **Reputation tick** — heat decay
2. **Contract tick** — expiry, stale offers
3. **Infrastructure upkeep** — warehouse, broker, license deductions
4. **Credit tick** — interest accrual, due dates, defaults
5. **Market shift** — regional shocks
6. **Voyage events** — storms, pirates, inspections
7. **Campaign evaluation** — milestone checks
8. **Auto-save**

## Save format

JSON on the local filesystem. Returns 5-tuple:
`(WorldState, ReceiptLedger, ContractBoard, InfrastructureState, CampaignState)`

Backward compatibility via `.get()` defaults for new fields.

## Testing

- **609 tests** across 24 files
- **Balance harness** — 7 policy bots, 7 scenario packs, deterministic seeds
- **Stress testing** — 14 cross-system invariants, 9 compound scenarios
- **Invariant enforcement** — checked after every tick in stress runs
