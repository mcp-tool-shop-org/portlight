---
title: Trading Guide
description: Understanding the economy, finding profitable routes, and managing market dynamics.
sidebar:
  order: 2
---

## How prices work

Portlight's economy is scarcity-driven. Every port has goods it **produces** (high stock, cheap buy price) and goods it **consumes** (low stock, expensive buy price).

Your profit comes from buying where stock is high and selling where stock is low. The price difference minus port fees and travel costs is your real margin.

## Reading the market

```bash
portlight market
```

Key columns:
- **Buy price** — what it costs to purchase
- **Sell price** — what you'd get selling here (always lower than buy due to spread)
- **Stock** — current supply at this port

## Flood penalty

If you sell the same good repeatedly at the same port, a **flood penalty** appears: `(flooded: -25%)`. This reduces your sell price.

**How to manage it:**
- Diversify destinations — sell at different ports
- Diversify goods — don't carry only grain
- Wait — flood penalty decays over time

## Key trade routes

Prices are structural, not random. Some patterns:

- **Grain** is cheap at Porto Novo (produces it), expensive at Al-Manar (consumes it)
- **Timber** is cheap at Silva Bay, valuable at ports without shipyards
- **Silk and spice** offer high per-unit margins but are scarcer and attract inspection attention
- **Cotton** flows cheaply from West Africa, sells well in Mediterranean ports
- **Iron** exports from Iron Point at good margins

## Provenance

Every cargo item tracks where and when it was acquired. This matters for:
- **Contracts** — delivery must use cargo with tracked provenance from the right source
- **Inspections** — contraband cargo from suspicious regions draws more attention
- **Warehouses** — stored cargo preserves its provenance

## Ship upgrades

Three ship classes with increasing capability:

| Ship | Cargo | Speed | Cost |
|------|-------|-------|------|
| Sloop | Small | Slow | Starter |
| Brigantine | Medium | Moderate | ~2000 silver |
| Galleon | Large | Fast | ~5000 silver |

Check availability and prices: `portlight shipyard`

Upgrade when you can afford both the ship and the larger crew's daily wages.
