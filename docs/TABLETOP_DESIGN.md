# Tabletop Design Notes

Developer-facing design rationale for the Portlight Print-and-Play board game adaptation.

## Design Thesis

**Merchant adventure under pressure.** Not a generic trading euro, not a combat game with cargo pasted on.

At its best, Portlight as a board game is: a route-and-risk trade game where players read markets, race contracts, manage reputation/heat, and decide when to play honest versus dangerous.

## What Carries from Digital

These translate directly and form the game's backbone:

- **Board** — the port map and routes are spatial strategy
- **Goods** — cards with region-specific value modifiers
- **Contracts** — the strongest tabletop hook; creates urgency and route planning
- **Captain archetypes** — asymmetric play with distinct moral economies
- **Reputation / heat** — consequence tracks without simulation overhead
- **Events** — weather, pirates, inspections as deck material
- **Ship progression** — long-arc identity and strategy differentiation
- **Victory paths** — 4 distinct win conditions for replayability

## What Was Simplified Hard

The tabletop version uses sharp, tactile abstractions instead of simulation density:

### Market simulation
Digital: hidden numeric scarcity model, tick-based restock, flood penalties.
Tabletop: visible market cards at each port, port reference cards show demand, simple flood rule (3+ same good = -2/unit).

### Combat
Digital: stance triangle, stamina, injuries, weapon stats, 7 melee + 7 ranged types.
Tabletop: one-roll resolution. Fight/Pay/Flee for pirates. 2d6 check for inspections. A decision point, not a subsystem.

### NPCs
Digital: 134 named NPCs with personality, standing-aware greetings, relationship webs.
Tabletop: NPCs become deck effects, contract flavor text, and event encounters. Not full agents.

### Economy
Digital: per-good restock rates, affinity multipliers, spread calculations.
Tabletop: base prices on cards, demand shown on port reference cards. Players can eyeball margins.

## Three Central Design Pillars

### 1. Contract Play
Contracts are the strongest objective engine. They create:
- Route planning (I need silk at Jade Port, delivered to Ironhaven)
- Timing pressure (3 rounds left, can I make it?)
- Cargo decisions (do I fill up on contracts or speculate on market trades?)
- Player collision (we both want that contract, and both need spice from the same port)

### 2. Reputation vs Heat
This is what makes Portlight feel like Portlight:
- Safer legal play improves access (trust tiers, better contracts)
- Riskier illegal play pays more (contraband margins) but raises heat
- Different captains lean into different moral economies
- The Smuggler and Merchant are playing fundamentally different games

### 3. Regional Market Identity
Every region feels economically distinct:
- Mediterranean: grain/timber hub, safe starting routes
- North Atlantic: iron/weapons, strict inspections, military trade
- West Africa: cotton/rum/pearls, cheaper provisions
- East Indies: luxury goods (silk/spice/porcelain), monsoon risk, highest margins
- South Seas: pearls/medicines, remote endgame region

## Scaling Decisions

### Digital-to-tabletop value scaling
Digital silver values are ~20x higher than tabletop. This keeps arithmetic manageable:
- Digital ship prices: 0 / 450 / 800 / 2200 / 5000
- Tabletop ship prices: 0 / 20 / 40 / 80 / 150

### Movement abstraction
Digital routes use day counts (14-80 days). Tabletop uses movement points (1-4 cost):
- Short routes (same region): 1 point
- Medium routes (adjacent regions): 2 points
- Long routes (cross-region): 3 points
- Extreme routes (dangerous shortcuts): 4 points

Ship speed is inverted: digital fast ships (speed 8-9) get more movement points; digital slow ships (speed 3-4) get fewer.

### Cargo as hand size
Digital cargo is unit-based (30-200 capacity). Tabletop cargo is card-based (5-20 cards). Each goods card represents a meaningful trade unit.

## Drift Risks (What to Avoid)

- **Spreadsheet cardboard** — if buying/selling is just arithmetic, the soul dies
- **Piracy as main game** — pirates are pressure and spice, not the product
- **Deck overload** — too many cards becomes homework; the game needs ~120 total cards, not 300
- **Digital complexity preserved** — the tabletop needs elegant pressure, not exhaustive simulation

## Visual Law

Clean utilitarian with maritime flavor. Late-18th-century merchant ledger filtered through modern board-game usability.

- Information-dominant: routes, ports, goods, prices always readable
- Theme in framing (icons, labels, dividers), not wallpaper (textures, stains)
- Grayscale-first design: everything works without color
- 5 muted region accent colors (slate blue, muted rust, ochre, sea green, dusky teal)
- Two-font system: serif headers, sans-serif rules/stats
- No decorative pirate fonts. Ever.

Full visual spec in the plan file.

## Content Sourcing

All card content is generated from Portlight's structured Python dataclasses:
- `portlight.content.ports.PORTS` — 20 ports with market profiles
- `portlight.content.goods.GOODS` — 17 goods with base prices
- `portlight.content.routes.ROUTES` — route connections with distances
- `portlight.content.ships.SHIPS` — 5 ship classes with stats
- `portlight.content.contracts.TEMPLATES` — 22 contract templates
- `portlight.content.seasons` — seasonal profiles
- `portlight.content.factions` — pirate faction data

Board game values (costs, movement points, etc.) are defined as tabletop-specific constants in the generator module, not the digital game's exact numbers.

## Generator Architecture

`src/portlight/printandplay/` module:
- `generator.py` — orchestrates PDF creation
- `cards.py` — card layout functions
- `board.py` — game board with port map and routes
- `rules.py` — rulebook pages
- `assets.py` — palette, fonts, layout constants

CLI: `portlight print-and-play [--output PATH]`
Dependency: `fpdf2>=2.8` (optional extra)
