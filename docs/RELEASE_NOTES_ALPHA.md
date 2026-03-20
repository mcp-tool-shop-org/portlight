# Release Notes — Alpha

## What Portlight is

Portlight is a trade-first maritime strategy game played in the terminal. You start as a captain with a small ship and limited silver, and build a merchant career through route arbitrage, contracts, infrastructure investment, financial leverage, and commercial reputation.

The game watches what you build and interprets your career: four victory paths and seven profile tags reflect the kind of trade house you actually created. Two players who both get rich in different ways will see different career profiles.

## What's in this release

### Economy
- 10 ports across 3 regions (Mediterranean, West Africa, East Indies)
- 8 tradeable goods with scarcity-driven pricing
- 17 routes with distance-based travel times
- Flood penalty on repeated sales at the same port
- Regional market shocks that create opportunities
- Provenance tracking on all cargo (port and region of acquisition)

### Voyages
- Multi-day travel with daily event resolution
- Storms, pirate encounters, calm seas, sightings
- Inspections based on customs heat and cargo suspicion
- Provisions, hull, and crew as real resources
- 3 ship classes: sloop, brigantine, galleon

### Captain Identity
- Merchant — legitimate trader, best prices, low inspection risk
- Smuggler — discreet operator, black market access, luxury margins
- Navigator — deep-water explorer, faster ships, early East Indies access
- 8-20% pricing gaps between captain types
- Distinct starting positions and access profiles

### Contracts
- 6 contract families with trust and standing gates
- Provenance-validated delivery (cargo must be tracked from purchase to destination)
- Real deadlines with expiry consequences
- Contract board with regional and broker-quality effects
- Completion rewards plus early delivery bonuses

### Reputation
- Regional standing across 3 regions
- Port-specific reputation
- Customs heat (rises from suspicious behavior, decays over time)
- Commercial trust (earned through reliable contract delivery)
- Multi-axis access model: trust, standing, and heat together determine what's available to you

### Infrastructure
- Warehouses: 3 tiers (depot, regional, commercial) — decouple buying from selling
- Broker offices: 2 tiers across 3 regions — improve contract quality
- 5 purchasable licenses — unlock contract families and reduce friction
- Real upkeep on all assets — default closes them

### Insurance
- Hull, premium cargo, and contract guarantee policies
- Coverage percentages and caps
- Heat surcharges (high-heat captains pay more)
- Claim resolution with denial conditions (contraband excluded, etc.)
- Voyage-scoped policies that expire on arrival

### Credit
- 3 tiers: merchant line, house credit, premier commercial
- Interest accrual on outstanding debt
- Payment deadlines with default consequences
- 3 defaults freezes credit line and damages trust
- Leverage with real risk

### Campaign
- 27 milestones across 6 families
- Career profile interpretation: 7 scored tags with confidence levels (forming, moderate, strong, dominant)
- Primary, secondary, and emerging profile tags
- 4 victory paths: Lawful Trade House, Shadow Network, Oceanic Reach, Commercial Empire
- Per-path diagnostics: met, missing, and blocked requirements
- Candidate strength scoring
- First-path-completed flag for career legacy

### Quality
- 609 tests across 24 files
- 14 cross-system invariants enforced under 9 compound stress scenarios
- Balance harness: 7 policy bots, 7 scenario packs, structured reporting
- Save/load round-trips verified under compound crisis states
- Welcome screen with contextual first-move guidance
- Market flood explanation inline
- Contract deadline sail-time context
- Daily upkeep cost display
- Grouped command reference (`portlight guide`)

## Known limitations

See [KNOWN_ISSUES.md](KNOWN_ISSUES.md) for specific items. Key notes:

- Balance is actively being tuned — some captain types and strategies are stronger than others
- Saves may break across alpha versions
- CLI is the intended interface; there is no GUI
- Insurance and credit are functional but under-adopted in simulated play
- Contract completion rates in automated testing are lower than expected (strategy gap, not engine gap)
