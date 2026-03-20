# Command Reference

All Portlight commands, grouped by purpose. Run `portlight guide` in-game to see this reference in the terminal.

## Trading

### `portlight market`
View prices, stock levels, and affordability at your current port. Shows buy/sell prices, stock, and flood penalty if active.

**When you use it:** Before every trade decision. This is the most-used command in the game.

**Example:** `portlight market`

### `portlight buy <good> <qty>`
Buy goods from the port market into your cargo hold.

**When you use it:** When you've identified something cheap at the current port that sells high elsewhere.

**Example:** `portlight buy grain 15`

### `portlight sell <good> <qty>`
Sell goods from your cargo to the port market. Shifts reputation, may trigger flood penalty.

**When you use it:** At a destination where the good is consumed (low stock, high demand).

**Example:** `portlight sell grain 15`

### `portlight cargo`
View your current cargo hold: goods, quantities, cost basis, provenance.

**When you use it:** To check what you're carrying and where it came from.

**Example:** `portlight cargo`

## Navigation

### `portlight routes`
List available routes from your current port with distance and travel time.

**When you use it:** When deciding where to sail next.

**Example:** `portlight routes`

### `portlight sail <destination>`
Depart for a destination port. Requires provisions and crew.

**When you use it:** When loaded with cargo and ready to travel.

**Example:** `portlight sail al_manar`

### `portlight advance [days]`
Advance time by one or more days. At sea: progresses your voyage. In port: passes time.

**When you use it:** After sailing (to travel) or in port (to wait for market recovery or contract deadlines).

**Example:** `portlight advance` or `portlight advance 5`

### `portlight port`
View information about your current port: features, fees, region.

**When you use it:** When arriving at a new port or checking local services.

**Example:** `portlight port`

### `portlight provision [days]`
Buy provisions (food/water) for the voyage. Default: 10 days.

**When you use it:** Before long voyages. Running out at sea is dangerous.

**Example:** `portlight provision 15`

### `portlight repair [amount]`
Repair hull damage at port. Default: full repair.

**When you use it:** After storms or combat events.

**Example:** `portlight repair`

### `portlight hire [count]`
Hire crew at port. Default: fill to capacity.

**When you use it:** When below optimal crew (slower sailing speed).

**Example:** `portlight hire`

## Contracts

### `portlight contracts`
View the contract board: available offers at your current port.

**When you use it:** When checking what delivery opportunities are available.

**Example:** `portlight contracts`

### `portlight accept <offer_id>`
Accept a contract offer from the board. Creates an obligation with a deadline.

**When you use it:** When a contract aligns with your planned routes.

**Example:** `portlight accept a1b2c3`

### `portlight obligations`
View your active contract obligations: deadlines, progress, sail-time estimates.

**When you use it:** To track what you owe and how much time you have.

**Example:** `portlight obligations`

### `portlight abandon <offer_id>`
Abandon an active contract. Damages trust and standing.

**When you use it:** Only when the cost of completing is clearly worse than the reputation hit.

**Example:** `portlight abandon a1b2c3`

## Infrastructure

### `portlight warehouse [action]`
Manage warehouses. Actions: `lease`, `deposit <good> <qty>`, `withdraw <good> <qty>`, `list`.

**When you use it:** When you want to stage cargo at a port — buy when cheap, store, sell when the market is right.

**Example:**
- `portlight warehouse lease depot` — open a basic warehouse at current port
- `portlight warehouse deposit grain 20` — move grain from cargo to warehouse
- `portlight warehouse withdraw grain 10` — move grain from warehouse to cargo
- `portlight warehouse list` — see inventory at current port

### `portlight office [action]`
Manage broker offices. Actions: `open`, `upgrade`.

**When you use it:** When you want better contract quality in a region. Brokers improve the premium offer weighting on the board.

**Example:** `portlight office open` — open a local broker at your current region

### `portlight license [buy <id>]`
View available licenses or purchase one. Licenses unlock contract families, reduce customs friction, or open premium access.

**When you use it:** When your standing and trust are high enough to qualify and you want to unlock new opportunities.

**Example:**
- `portlight license` — see available licenses
- `portlight license buy med_trade_charter` — purchase a specific license

## Finance

### `portlight insure [buy <id>]`
View insurance options or purchase a policy. Policies cover hull damage, cargo loss, or contract failure.

**When you use it:** When you're carrying valuable cargo on risky routes, or when a contract failure would be devastating.

**Example:**
- `portlight insure` — see available policies
- `portlight insure buy hull_basic` — purchase hull insurance

### `portlight credit [action]`
Manage credit. Actions: `open`, `draw <amount>`, `repay <amount>`, `status`.

**When you use it:** When you need capital faster than your trade income provides. Credit has interest and default risk.

**Example:**
- `portlight credit open` — open a credit line (requires trust/standing)
- `portlight credit draw 200` — borrow 200 silver
- `portlight credit repay 100` — repay 100 silver of outstanding debt

## Career

### `portlight captain`
View your captain identity: type, advantages, pricing modifiers, starting profile.

**When you use it:** To remind yourself of your archetype's strengths and trade-offs.

**Example:** `portlight captain`

### `portlight reputation`
View your full reputation state: regional standing, port standing, customs heat, commercial trust, and recent incidents.

**When you use it:** When deciding whether you qualify for contracts, licenses, or credit. Also useful to track heat pressure.

**Example:** `portlight reputation`

### `portlight milestones`
View career milestones (completed and in progress), victory path diagnostics, and career profile interpretation.

**When you use it:** To see what the game recognizes about your trading career and how close you are to victory paths.

**Example:** `portlight milestones`

### `portlight status`
Overview panel: silver, ship, cargo summary, daily upkeep costs, infrastructure summary.

**When you use it:** Quick snapshot of your overall position.

**Example:** `portlight status`

### `portlight ledger`
View your trade receipt history — every buy and sell with prices, quantities, and provenance.

**When you use it:** To review your trade performance and verify receipt integrity.

**Example:** `portlight ledger`

### `portlight shipyard [buy <ship_id>]`
View available ships or purchase one. Ships differ in cargo capacity, speed, hull strength, crew needs, and storm resistance.

**When you use it:** When you have enough silver for an upgrade and the crew/provisions to sustain a bigger ship.

**Example:**
- `portlight shipyard` — see available ships and prices
- `portlight shipyard buy brigantine` — purchase a brigantine

## System

### `portlight save`
Explicitly save the game. (Auto-save happens after every action.)

**Example:** `portlight save`

### `portlight load`
Load a previously saved game.

**Example:** `portlight load`

### `portlight guide`
Show the in-game grouped command reference.

**Example:** `portlight guide`
