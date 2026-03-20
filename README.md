<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/portlight/readme.png" width="800" alt="Portlight">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/portlight/actions"><img src="https://github.com/mcp-tool-shop-org/portlight/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/mcp-tool-shop-org/portlight/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/portlight/"><img src="https://img.shields.io/badge/docs-landing_page-blue" alt="Landing Page"></a>
</p>

A trade-first maritime strategy CLI where you build a merchant career through route arbitrage, contracts, infrastructure, finance, and commercial reputation across a living regional economy.

## Why Portlight

Most trading games flatten trade into a number that goes up. Portlight treats trade as a commercial discipline:

- **Prices react to your trades.** Dump grain at a port and the price crashes. Every sale shifts the local market.
- **Ports have real economic identities.** Porto Novo produces grain cheaply. Al-Manar consumes silk hungrily. These aren't random — they're structural.
- **Voyages carry risk.** Storms, pirates, inspections. Your provisions, hull, and crew matter.
- **Contracts require proof.** Deliver the right goods to the right port with tracked provenance. No faking it.
- **Infrastructure changes how you trade.** Warehouses let you stage cargo. Brokers improve contract quality. Licenses unlock premium access.
- **Finance is leverage with teeth.** Credit lets you move faster. Default, and doors close.
- **The game reads what you built.** Your trade history, infrastructure, reputation, and routes form a career profile. The game tells you what kind of trade house you actually are.

## The Core Loop

1. Inspect the market — find what's cheap here and expensive elsewhere
2. Buy cargo — load your hold
3. Sail — cross routes under weather, crew, and provision pressure
4. Sell — earn margin, shift the local market
5. Reinvest — upgrade your ship, lease a warehouse, open a broker office
6. Build access — earn trust, reduce heat, unlock contracts and licenses
7. Pursue a commercial destiny — four distinct victory paths based on what you actually built

## Quick Start

```bash
# Install
pip install -e ".[dev]"

# Start a new game
portlight new "Captain Hawk" --type merchant

# Look at what's for sale
portlight market

# Buy cheap goods
portlight buy grain 10

# Check available routes
portlight routes

# Sail to where grain sells high
portlight sail al_manar

# Advance through the voyage
portlight advance

# Sell at destination
portlight sell grain 10

# See your trade history
portlight ledger

# Check your career progress
portlight milestones
```

See [docs/START_HERE.md](docs/START_HERE.md) for a guided first session and [docs/FIRST_VOYAGE.md](docs/FIRST_VOYAGE.md) for a detailed early-game walkthrough.

## Captain Types

| Captain | Identity | Edge | Trade-off |
|---------|----------|------|-----------|
| **Merchant** | Licensed trader, Mediterranean base | Better prices, lower inspection rates, trust grows faster | No black market access |
| **Smuggler** | Discreet operator, West Africa base | Black market access, luxury margins, contraband trade | Higher heat, more inspections |
| **Navigator** | Deep-water explorer, Mediterranean base | Faster ships, longer range, East Indies access early | Weaker initial commercial standing |

## Systems

**Economy** — Scarcity-driven pricing across 10 ports, 8 goods, 17 routes. Flood penalties punish dumping. Market shocks create regional opportunities.

**Voyages** — Multi-day travel with weather events, pirate encounters, inspections. Provisions, hull, and crew are real resources.

**Captains** — Three distinct archetypes with 8-20% pricing gaps, unique starting positions, and different access profiles.

**Contracts** — Six contract families gated by trust and standing. Provenance-validated delivery. Real deadlines with real consequences.

**Reputation** — Regional standing, port-specific reputation, customs heat, and commercial trust. A multi-axis access model that opens and closes doors.

**Infrastructure** — Warehouses (3 tiers), broker offices (2 tiers across 3 regions), and 5 purchasable licenses. Each changes trade timing, scale, or access.

**Insurance** — Hull, cargo, and contract guarantee policies. Heat surcharges. Claim resolution with denial conditions.

**Credit** — Three tiers of credit with interest accrual, payment deadlines, and default consequences. Leverage with real risk.

**Career** — 27 milestones across 6 families. Career profile interpretation (primary/secondary/emerging tags). Four victory paths: Lawful Trade House, Shadow Network, Oceanic Reach, and Commercial Empire.

## Victory Paths

- **Lawful Trade House** — Disciplined legitimacy. High trust, premium contracts, clean reputation, infrastructure breadth.
- **Shadow Network** — Profitable discreet trade. Luxury margins under scrutiny, heat management, resilient operations.
- **Oceanic Reach** — Long-haul commercial power. East Indies access, distant infrastructure, premium route mastery.
- **Commercial Empire** — Integrated multi-region operation. Infrastructure in every region, diversified revenue, financial leverage.

See [docs/CAREER_PATHS.md](docs/CAREER_PATHS.md) for detailed player-facing descriptions.

## Command Reference

Run `portlight guide` in-game for a grouped command reference, or see [docs/COMMANDS.md](docs/COMMANDS.md).

| Group | Commands |
|-------|----------|
| Trading | `market`, `buy`, `sell`, `cargo` |
| Navigation | `routes`, `sail`, `advance`, `port`, `provision`, `repair`, `hire` |
| Contracts | `contracts`, `accept`, `obligations`, `abandon` |
| Infrastructure | `warehouse`, `office`, `license` |
| Finance | `insure`, `credit` |
| Career | `captain`, `reputation`, `milestones`, `status`, `ledger`, `shipyard` |
| System | `save`, `load`, `guide` |

## Alpha Status

Portlight is in alpha. The core systems are complete and stress-tested, but balance is actively being tuned.

**What's solid:**
- All systems functional end-to-end
- 609 tests across 24 files
- 14 cross-system invariants enforced under 9 compound stress scenarios
- Balance harness with 7 policy bots across 7 scenario packs

**What's being tuned:**
- Smuggler scaling (currently under-performing on ship progression)
- Mediterranean route concentration (Porto Novo / Silva Bay dominates traffic)
- Contract completion rates (delivery logic gaps in automated runs)
- Insurance adoption (currently near zero in simulated play)

See [docs/ALPHA_STATUS.md](docs/ALPHA_STATUS.md) for details and [docs/KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md) for specific items.

## Security and Data

Portlight is a **local-only CLI game**. It makes zero network connections during gameplay. Data touched: local save files (`saves/`) and report artifacts (`artifacts/`), all JSON on the local filesystem. No secrets, credentials, telemetry, or remote services. No elevated permissions required. See [SECURITY.md](SECURITY.md) for the full policy.

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run balance simulation
python tools/run_balance.py

# Run stress tests
python tools/run_stress.py

# Lint
ruff check src/ tests/
```

## License

MIT

---

Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
