---
title: Getting Started
description: Install Portlight and play your first 10 minutes.
sidebar:
  order: 1
---

## Install

```bash
pip install portlight
```

Requires Python 3.11+. No Python? Use `npx @mcptoolshop/portlight` instead.

## Start a new game

```bash
portlight new "Your Name" --type merchant
```

Or run `portlight captain-select` for the interactive roster with all nine captains.

### Captain types

| Captain | Home | Edge | Trade-off |
|---------|------|------|-----------|
| **Merchant** | Porto Novo | Best prices, trust grows fast | Heat penalties doubled |
| **Smuggler** | Corsair's Rest | Black market, contraband trade | Higher heat, more inspections |
| **Navigator** | Monsoon Reach | Faster ships, longer range | Weaker initial standing |
| **Privateer** | Ironhaven | Naval combat, boarding advantage | Poor merchant reputation |
| **Corsair** | Corsair's Rest | Balanced combat + trade | Master of none |
| **Scholar** | Jade Port | Information advantage | Low capital, fragile |
| **Merchant Prince** | Porto Novo | High starting capital | Higher fees, pirate target |
| **Dockhand** | Crosswind Isle | Cheapest crew | Lowest starting capital |
| **Bounty Hunter** | Stormwall | Combat mastery | Poor prices, distrusted |

Start with **merchant** for your first run. It has the smoothest early game.

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
- **The map.** Run `portlight map` to see the world, routes, and your position.

## What to ignore at first

- **Contracts** — wait until you understand route profitability
- **Infrastructure** — wait until you have 500+ silver and a steady income loop
- **Insurance and credit** — mid-game tools, not early priorities
- **Victory paths** — tracked automatically, check with `portlight milestones`
- **Combat gear** — buy a weapon when you can afford it, not before

## System unlock timeline

| Silver | Day | What opens up |
|--------|-----|---------------|
| 0-500 | 1-10 | Basic trading, route discovery, first weapon |
| 500-2000 | 10-25 | Ship upgrades, first warehouse, simple contracts |
| 2000-5000 | 25-50 | Licenses, insurance, credit, multi-region trading |
| 5000+ | 50+ | Victory path pursuit, full infrastructure, endgame waters |
