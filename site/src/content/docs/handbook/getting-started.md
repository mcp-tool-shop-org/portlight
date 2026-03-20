---
title: Getting Started
description: Install Portlight and play your first 10 minutes.
sidebar:
  order: 1
---

## Install

```bash
pip install -e ".[dev]"
```

Requires Python 3.11+.

## Start a new game

```bash
portlight new "Your Name" --type merchant
```

Three captain types are available:

| Captain | Edge | Trade-off |
|---------|------|-----------|
| **Merchant** | Best prices, lowest inspection risk, trust grows fast | No black market access |
| **Smuggler** | Black market access, luxury margins, contraband trade | Higher heat, more inspections |
| **Navigator** | Faster ships, longer range, East Indies access early | Weaker initial commercial standing |

Start with **merchant** for your first run.

## Your first trade

```bash
portlight market          # See what's cheap here
portlight buy grain 10    # Buy cheap goods
portlight routes          # Find where grain sells high
portlight sail al_manar   # Sail to a destination
portlight advance         # Travel day by day
portlight sell grain 10   # Sell at the destination
portlight ledger          # See your trade history
```

## What to focus on early

- **Profit per voyage.** Buy where stock is high, sell where it's consumed.
- **Provisions.** You consume one per day at sea. Buy before long voyages: `portlight provision 15`.
- **Ship condition.** Repair storm damage at port: `portlight repair`.

## What to ignore at first

- **Contracts** — wait until you understand route profitability
- **Infrastructure** — wait until you have 500+ silver and a steady income loop
- **Insurance and credit** — mid-game tools, not early priorities
- **Victory paths** — tracked automatically, check with `portlight milestones`

## System unlock timeline

| Silver | Day | What opens up |
|--------|-----|---------------|
| 0-500 | 1-10 | Basic trading, route discovery |
| 500-2000 | 10-25 | Ship upgrades, first warehouse, simple contracts |
| 2000-5000 | 25-50 | Licenses, insurance, credit, multi-region trading |
| 5000+ | 50+ | Victory path pursuit, full infrastructure |
