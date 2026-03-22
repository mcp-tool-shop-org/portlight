<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/portlight/readme.png" width="600" alt="Portlight">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/portlight/actions"><img src="https://github.com/mcp-tool-shop-org/portlight/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://pypi.org/project/portlight/"><img src="https://img.shields.io/pypi/v/portlight" alt="PyPI"></a>
  <a href="https://github.com/mcp-tool-shop-org/portlight/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/portlight/"><img src="https://img.shields.io/badge/docs-handbook-blue" alt="Handbook"></a>
</p>

Trade-first maritime strategy game. Build a merchant career across five regions through route arbitrage, contracts, infrastructure, finance, and reputation — all from the terminal.

## Install

```bash
pip install portlight
```

No Python? Use the npm wrapper instead:

```bash
npx @mcptoolshop/portlight
```

## Why Portlight

Most trading games flatten trade into a number that goes up. Portlight treats trade as a commercial discipline:

- **Prices react to your trades.** Dump grain at a port and the price crashes. Every sale shifts the local market.
- **Ports have real economic identities.** Porto Novo produces grain cheaply. Silk Haven exports silk at volume. These are structural, not random.
- **Voyages carry risk.** Storms, pirates, inspections, seasonal danger. Your provisions, hull, and crew matter.
- **Contracts require proof.** Deliver the right goods to the right port before the deadline. Provenance is tracked.
- **Infrastructure changes how you trade.** Warehouses stage cargo. Brokers improve contracts. Licenses unlock premium access.
- **Reputation opens and closes doors.** Commercial trust, customs heat, regional standing, and underworld connections — four axes that shape what you can do and where.
- **The game reads what you built.** Your trade history, infrastructure, reputation, and routes form a career profile. Four distinct victory paths based on what kind of merchant you actually became.

## The World

Five regions. Twenty ports. Forty-three routes. A living economy.

| Region | Ports | Character |
|--------|-------|-----------|
| **Mediterranean** | Porto Novo, Al-Manar, Silva Bay, Corsair's Rest | Grain, timber, spice markets. Safe starting waters. |
| **North Atlantic** | Ironhaven, Stormwall, Thornport | Iron, weapons, military trade. Strict inspections. |
| **West Africa** | Sun Harbor, Palm Cove, Iron Point, Pearl Shallows | Cotton, rum, pearls. Cheapest provisions. |
| **East Indies** | Jade Port, Monsoon Reach, Silk Haven, Crosswind Isle, Dragon's Gate, Spice Narrows | Silk, spice, porcelain, tea. Highest margins. Monsoon risk. |
| **South Seas** | Ember Isle, Typhoon Anchorage, Coral Throne | Pearls, medicines. Remote endgame waters. |

134 named NPCs across every port. Four pirate factions controlling different waters. Seasonal weather that shifts danger and demand. A culture layer with festivals, superstitions, and crew morale.

## Nine Captains

| Captain | Home | Edge | Trade-off |
|---------|------|------|-----------|
| **Merchant** | Porto Novo | Better prices, trust grows fast | Heat penalties doubled |
| **Smuggler** | Corsair's Rest | Black market, contraband trade | Higher heat, more inspections |
| **Navigator** | Monsoon Reach | Faster ships, longer range | Weaker initial standing |
| **Privateer** | Ironhaven | Naval combat, boarding advantage | Poor merchant reputation |
| **Corsair** | Corsair's Rest | Balanced combat + trade | Master of none |
| **Scholar** | Jade Port | Information advantage, better contracts | Low capital, fragile |
| **Merchant Prince** | Porto Novo | High starting capital, premium access | Higher fees, pirate target |
| **Dockhand** | Crosswind Isle | Cheapest crew, scrappy | Lowest starting capital |
| **Bounty Hunter** | Stormwall | Combat mastery, faction standing | Poor prices, distrusted |

Each captain starts in a different port, sees different contracts, and leans toward a different victory path. The game doesn't lock you in — it watches what you do and tells you what you built.

## Core Loop

```
Inspect market → Buy cargo → Sail → Sell → Reinvest → Build access → Pursue destiny
```

## Quick Start

```bash
portlight new "Captain Hawk" --type merchant
portlight market
portlight buy grain 10
portlight routes
portlight sail al_manar
portlight advance
portlight sell grain 10
portlight milestones
```

See [docs/START_HERE.md](docs/START_HERE.md) for a guided first session.

## Systems

**Economy** — Scarcity-driven pricing across 20 ports, 18 goods, 43 routes. Flood penalties punish dumping. Market shocks create opportunities. Regional demand modifiers mean every port has clear import/export identity.

**Voyages** — Multi-day travel with weather, pirate encounters, inspections. Provisions burn daily. Hull takes damage. Crew morale shifts. Seasonal danger zones change which routes are safe.

**Contracts** — Six families gated by trust and standing. Procurement, shortage relief, luxury discreet, return freight, circuit, and faction commissions. Real deadlines, real consequences.

**Reputation** — Four axes: regional standing, commercial trust, customs heat, and underworld connections. High trust unlocks premium contracts. High heat triggers inspections and port denials. Different captains play different moral economies.

**Combat** — Full personal combat (stance triangle: thrust/slash/parry) with 7 melee weapons, 7 ranged weapons, regional fighting styles. Naval combat with boarding and cannons. Short, brutal, consequential.

**Pirate Factions** — Crimson Tide (Mediterranean), Iron Wolves (North Atlantic), Deep Reef Brotherhood (South Seas), Monsoon Syndicate (East Indies). Each with territory, preferred goods, named captains, and attitude toward you.

**Infrastructure** — Warehouses (3 tiers), broker offices, 5 purchasable licenses. Real upkeep costs. Each changes trade timing, scale, or access.

**Finance** — Insurance (hull, cargo, contract guarantee) and credit (3 tiers with interest). Leverage with teeth.

**Companions** — Five officer roles (marine, navigator, surgeon, smuggler, quartermaster). Named companions with personality, morale, and departure triggers.

**Career** — 27 milestones across 6 families. 13 career profile tags. Four victory paths: Lawful Trade House, Shadow Network, Oceanic Reach, Commercial Empire.

## Victory Paths

- **Lawful Trade House** — Disciplined legitimacy. High trust, premium contracts, clean reputation, infrastructure breadth.
- **Shadow Network** — Profitable trade under scrutiny. Luxury margins, heat management, resilient operations.
- **Oceanic Reach** — Long-haul commercial power. East Indies access, distant infrastructure, route mastery.
- **Commercial Empire** — Integrated multi-region operation. Infrastructure everywhere, diversified revenue, financial leverage.

## Print-and-Play Board Game

Generate a complete board game adaptation — cards, board, rulebook, score tracks:

```bash
pip install portlight[printandplay]
portlight print-and-play
```

A 2-4 player competitive merchant adventure (~90 minutes) with asymmetric captains, contract racing, and reputation/heat tension. See [docs/PRINT_AND_PLAY_RULES.md](docs/PRINT_AND_PLAY_RULES.md) for the full rulebook.

## Command Reference

Run `portlight guide` for a grouped reference, or see [docs/COMMANDS.md](docs/COMMANDS.md).

| Group | Commands |
|-------|----------|
| Trading | `market`, `buy`, `sell`, `cargo` |
| Navigation | `routes`, `sail`, `advance`, `port`, `provision`, `repair`, `hire` |
| Contracts | `contracts`, `accept`, `obligations`, `abandon` |
| Infrastructure | `warehouse`, `office`, `license` |
| Finance | `insure`, `credit` |
| Career | `captain`, `reputation`, `milestones`, `status`, `ledger`, `shipyard` |
| World | `map`, `port` |
| Interface | `tui`, `captain-select` |
| System | `save`, `load`, `guide`, `print-and-play` |

## Quality

- 1,832 tests across 72+ files
- 14 cross-system invariants enforced under 9 compound stress scenarios
- Balance harness: 7 policy bots across 7 scenario packs
- Save format v12 with full migration chain
- Ruff-clean, Python 3.11/3.12/3.13

## Security

Local-only CLI game. Zero network connections during gameplay. Saves to `saves/` and `artifacts/` as JSON on local filesystem. No secrets, no telemetry, no elevated permissions. See [SECURITY.md](SECURITY.md).

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check src/ tests/
```

## License

MIT

---

Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
