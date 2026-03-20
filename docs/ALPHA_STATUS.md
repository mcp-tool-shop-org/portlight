# Alpha Status

Portlight is in alpha. This document describes what is complete, what is being tuned, and what players should expect.

## What is complete

Every core system is implemented, tested, and stress-verified:

- **Economy** — scarcity-driven pricing across 10 ports, 8 goods, 17 routes. Flood penalty, market shocks, provenance tracking.
- **Voyages** — multi-day travel with storms, pirates, inspections, provisions, hull, and crew.
- **Captain identity** — three archetypes (merchant, smuggler, navigator) with 8-20% pricing gaps and distinct access profiles.
- **Contracts** — six families with trust/standing gates, provenance-validated delivery, deadline tracking, and board effects.
- **Reputation** — regional standing, customs heat, commercial trust, port standing. Multi-axis access model.
- **Infrastructure** — warehouses (3 tiers), broker offices (2 tiers across 3 regions), 5 licenses. Real upkeep with closure on default.
- **Insurance** — hull, cargo, and contract guarantee policies. Heat surcharges, coverage caps, denial conditions.
- **Credit** — 3 tiers with interest accrual, payment deadlines, default consequences (3 defaults freeze line).
- **Campaign** — 27 milestones across 6 families, career profile interpretation (7 tags with confidence levels), 4 victory paths with met/missing/blocked diagnostics.
- **Save/load** — full compound state round-trip (economy + contracts + infrastructure + insurance + credit + campaign).

## Verification

- **609 tests** across 24 test files
- **14 cross-system invariants** (laws that must hold under any game state)
- **9 compound stress scenarios** — debt spiral, warehouse neglect, insured luxury loss, contract expiry under pressure, heat/license conflict, legitimization pivot, oceanic overextension, victory-then-stress, save/load mid-crisis
- **Balance harness** — 7 policy bots, 7 scenario packs, 3 captain types, structured report generation

All stress scenarios pass with zero invariant violations. The game never produces negative silver, duplicate contract outcomes, or corrupted campaign state under compound pressure.

## What the balance harness currently shows

From the most recent 105-run simulation (mixed_volatility scenario, all policies, all captains):

**Captain parity:**
- Navigator reaches brigantine fastest (day 11)
- Merchant reaches brigantine by day 20
- Smuggler does not reach brigantine in current tuning
- Merchant leads in net worth at day 40 (12,396 silver)
- Smuggler leads overall net worth (13,985) via high-margin luxury trades

**Route concentration:**
- Porto Novo / Silva Bay dominates 31% of all traffic
- Mediterranean is over-concentrated; West Africa and East Indies are under-explored by policy bots

**Contracts:**
- Zero contracts completed across all automated runs (delivery logic gap in policy bots, not in the contract engine itself)
- Contract board generates offers correctly; the gap is in bot strategy, not game mechanics

**Insurance:**
- Zero insurance adoption across all automated runs
- Policies are available and functional; bots don't evaluate risk well enough to purchase

**Victory paths:**
- Shadow Network is the strongest candidate (28% of runs reach candidacy)
- Oceanic Reach appears for 10% of navigator runs
- Lawful Trade House and Commercial Empire have zero candidacy (both require contract completions and infrastructure breadth that bots don't achieve)

## What is being tuned

- **Smuggler ship progression** — smuggler should reach brigantine through luxury margins, currently under-scaling
- **Route diversity** — Mediterranean concentration should be reduced; West African and East Indies routes need to be more attractive to automated players
- **Contract completion rates** — policy bots need to prioritize contract fulfillment; the engine works, the strategy doesn't
- **Insurance adoption** — policy bots need risk evaluation; the system works, the strategic incentive is invisible to bots
- **Victory path thresholds** — Lawful Trade House and Commercial Empire may need threshold adjustments based on achievable play patterns

## What players should expect

- Core gameplay works end-to-end. You can trade, build infrastructure, manage finance, and pursue victory paths.
- Balance is actively being tuned. Some strategies may be significantly stronger than others.
- Saves may break across alpha versions if data formats change.
- The CLI is the intended primary interface. There is no GUI.
- The game is designed for extended play (60-120+ days per run), not quick sessions.

## What is explicitly not being solved yet

- GUI or web interface
- Multiplayer
- Procedural world generation (ports/routes are curated content)
- Sound or visual effects
- Tutorial beyond the welcome screen and docs
- Save migration between versions
