---
title: Trading Guide
description: Understanding the economy, finding profitable routes, and managing market dynamics.
sidebar:
  order: 2
---

## How prices work

Portlight's economy is scarcity-driven across 20 ports and 18 goods. Every port has goods it **produces** (high stock, cheap buy price) and goods it **consumes** (low stock, high sell price).

Your profit comes from buying where stock is high and selling where stock is low. The price difference minus port fees and travel costs is your real margin.

## Reading the market

```bash
portlight market
```

Key columns:
- **Buy price** — what it costs to purchase
- **Sell price** — what you'd get selling here (always lower than buy due to spread)
- **Stock** — current supply at this port

## Five regions, five economies

| Region | Produces | Consumes | Character |
|--------|----------|----------|-----------|
| **Mediterranean** | Grain, timber, spice | Cotton, porcelain, dyes | Safe early routes, moderate margins |
| **North Atlantic** | Iron, weapons, tea | Silk, spice, medicines | Strict inspections, military trade |
| **West Africa** | Cotton, rum, iron, pearls | Grain, weapons, silk | Cheapest provisions, good export margins |
| **East Indies** | Silk, spice, porcelain, tea | Grain, iron, weapons | Highest luxury margins, monsoon risk |
| **South Seas** | Pearls, medicines, dyes | Most goods | Remote, endgame waters, premium prices |

## Flood penalty

If you sell the same good repeatedly at the same port, a **flood penalty** reduces your sell price.

**How to manage it:**
- Diversify destinations — sell at different ports
- Diversify goods — don't carry only grain
- Wait — flood penalty decays over time

## Key trade routes

Prices are structural, not random:

- **Grain** — cheap at Porto Novo, expensive at Al-Manar and East Indies ports
- **Timber** — cheap at Silva Bay, valuable at shipyard-hungry ports
- **Silk** — buy at Silk Haven (East Indies), sell anywhere in Mediterranean for high margins
- **Spice** — Al-Manar and Spice Narrows export cheaply, sells well in North Atlantic
- **Cotton** — flows cheaply from West Africa, sells well in Mediterranean
- **Iron** — Iron Point and Ironhaven produce, East Indies consumes
- **Pearls** — Pearl Shallows and Typhoon Anchorage export, highest per-unit value in the game
- **Contraband** — opium, black powder, stolen cargo. Black Market ports only. Massive margins, massive heat.

## Provenance

Every cargo item tracks where and when it was acquired. This matters for:
- **Contracts** — delivery must use cargo with tracked provenance
- **Inspections** — contraband from suspicious regions draws more attention
- **Warehouses** — stored cargo preserves its provenance

## Ship progression

Five ship classes with increasing capability:

| Ship | Cargo | Speed | Hull | Crew Cost | Price |
|------|-------|-------|------|-----------|-------|
| **Sloop** | 30 | 8 | 60 | 1/day | Free (start) |
| **Cutter** | 50 | 9 (fastest) | 70 | 1/day | 450 |
| **Brigantine** | 80 | 6 | 100 | 2/day | 800 |
| **Galleon** | 150 | 4 | 160 | 3/day | 2200 |
| **Man-of-War** | 200 | 3 | 220 | 4/day | 5000 |

Check availability: `portlight shipyard`

Upgrade when you can afford both the ship and the larger crew's daily wages. The Brigantine is the workhorse — it opens cross-region routes where real money lives.

## Seasons

Four seasons rotate on a 360-day cycle. Each shifts danger and demand:

- **Spring** — calm seas, Mediterranean awakens
- **Summer** — peak activity, East Indies monsoon (1.7x danger)
- **Autumn** — harvest, grain floods Mediterranean
- **Winter** — harsh North Atlantic (1.8x danger), medicine demand peaks
