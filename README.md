<p align="center">
  <a href="README.md">English</a> | <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/portlight/readme.png" width="400" alt="Portlight">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/portlight/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/portlight/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://pypi.org/project/portlight/"><img src="https://img.shields.io/pypi/v/portlight" alt="PyPI"></a>
  <a href="https://www.npmjs.com/package/@mcptoolshop/portlight"><img src="https://img.shields.io/npm/v/@mcptoolshop/portlight" alt="npm"></a>
  <a href="https://github.com/mcp-tool-shop-org/portlight/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/portlight/"><img src="https://img.shields.io/badge/landing-page-blue" alt="Landing Page"></a>
  <a href="https://mcp-tool-shop-org.github.io/portlight/handbook/"><img src="https://img.shields.io/badge/docs-handbook-blue" alt="Handbook"></a>
</p>

Portlight is a trade-first maritime strategy game for the terminal. You run a captain, a hold, and a reputation across twenty ports. Prices move when you sell. Contracts want provenance. Brokers and warehouses change what a voyage is worth. Four victory paths score the career you actually built — not the one you picked on day one.

Play in the **TUI** (`portlight tui`) or the **CLI**. Same save. Same world.

## Install

```bash
pip install "portlight[tui]"
```

Python 3.11+. The `tui` extra pulls Textual. CLI-only: `pip install portlight`.

No Python? The npm launcher fetches the GitHub Release binary:

```bash
npx @mcptoolshop/portlight
```

Print-and-play PDF kit: `pip install "portlight[printandplay]"`.

## Play

```bash
portlight tui
```

If there is no save, the TUI lists slots and **New**. Pick a captain type. Then:

| Key | What it does |
|-----|----------------|
| **D** | Dashboard (career / milestones live here) |
| **M / B / S** | Market · buy · sell |
| **G / A** | Sail picker · advance a day |
| **H** | Harbor: provision, repair, hire; also work, fire, hunt. At sea, H hunts. |
| **K** | Contracts. **K again** to accept or abandon. |
| **W** | Infra. **W again** to lease, deposit, withdraw, open a broker, buy a license, or draw credit. |
| **P** | Port. **P again** for shipyard (buy hull, upgrades, dry-dock). |
| **F** | Fleet. **F again** to board, dock, transfer, or sell a prize hull. |
| **V** | World map |
| **?** | Help |

CLI is the same game with typed commands:

```bash
portlight new "Captain Hawk" --type merchant
portlight market
portlight buy grain 10
portlight sail al_manar
portlight advance
portlight sell grain 10
portlight tui
```

`portlight --json status` dumps a stable dict (captain, port, cargo, market, routes, board) with no ANSI. `portlight saves` lists slots.

Guided first session: [docs/START_HERE.md](docs/START_HERE.md). Handbook: [https://mcp-tool-shop-org.github.io/portlight/handbook/](https://mcp-tool-shop-org.github.io/portlight/handbook/).

## Why Portlight

Most trading games flatten trade into a number that goes up. Portlight treats trade as a commercial discipline:

- **Prices react to your trades.** Dump grain and the local price crashes.
- **Ports have economic identities.** Porto Novo grows grain. Silk Haven exports silk. That is structure, not noise.
- **Voyages carry risk.** Storms, pirates, inspections, seasons. Provisions, hull, and crew are real costs.
- **Contracts require proof.** Right goods, right port, tracked provenance, real deadlines.
- **Infrastructure changes timing.** Warehouses stage cargo. Brokers improve the board. Licenses open premium access. All five live regions have broker offices and a regional charter.
- **Reputation is four axes.** Commercial trust, customs heat, regional standing, underworld. They open and close doors independently.
- **The game reads what you built.** Milestones and four victory paths score evidence, not a menu choice.

## The world

Five regions. Twenty ports. Forty-three routes.

| Region | Ports | Character |
|--------|-------|-----------|
| **Mediterranean** | Porto Novo, Al-Manar, Silva Bay, Corsair's Rest | Grain, timber, spice. Safe starting waters. |
| **North Atlantic** | Ironhaven, Stormwall, Thornport | Iron, weapons, garrison trade. Strict inspections. |
| **West Africa** | Sun Harbor, Palm Cove, Iron Point, Pearl Shallows | Cotton, rum, pearls. Cheap provisions. |
| **East Indies** | Jade Port, Monsoon Reach, Silk Haven, Crosswind Isle, Dragon's Gate, Spice Narrows | Silk, spice, porcelain, tea. Highest margins. Monsoon risk. |
| **South Seas** | Ember Isle, Typhoon Anchorage, Coral Throne | Pearls, medicines. Remote endgame waters. |

Eighteen goods (including pelts and contraband). One hundred thirty-four named NPCs. Four pirate factions with eight live named captains. Seasonal weather. Festivals, superstitions, crew morale.

## Nine captains

| Captain | Home | Edge | Trade-off |
|---------|------|------|-----------|
| **Merchant** | Porto Novo | Better prices, trust grows fast | Heat penalties doubled |
| **Smuggler** | Palm Cove | Black market, contraband | Higher heat, more inspections |
| **Navigator** | Silva Bay | Faster ships, longer range | Weaker initial standing |
| **Privateer** | Stormwall | Naval combat, boarding | Poor merchant reputation |
| **Corsair** | Corsair's Rest | Combat + trade | Master of none |
| **Scholar** | Monsoon Reach | Information, better contracts | Low capital, fragile |
| **Merchant Prince** | Al-Manar | High starting capital | Higher fees, pirate target |
| **Dockhand** | Crosswind Isle | Cheap crew | Lowest starting capital |
| **Bounty Hunter** | Crosswind Isle | Combat, faction standing | Poor prices, distrusted |

`portlight new "Name"` without `--type` opens the roster. Bounty Hunter is not a flavour label: `portlight bounty accept <id>` then `portlight bounty hunt <id>` forces the named captain. Ghost ids are gone; the board only lists live `PIRATE_CAPTAINS`.

## Systems

**Economy** — Scarcity pricing, flood penalties, market shocks, regional import/export identity.

**Voyages** — Multi-day travel. Weather, pirates, inspections. Named pirate duels prefer an active bounty when one matches the waters.

**Contracts** — Seven families, twenty-four templates. Trust and standing gates. Provenance-validated delivery.

**Reputation** — Regional standing, commercial trust, customs heat, underworld connections.

**Combat** — Personal stance triangle (thrust / slash / parry), melee and ranged, fighting styles (TUI **Y** fires the style special). Naval: broadside, close, evade, rake, flee. Prize capture with a real fleet hull.

**Infrastructure** — Three warehouse tiers. Broker offices: Local + Established in all five regions. Seven licenses (five regional charters including North Atlantic and South Seas, plus two global). Real upkeep.

**Finance** — Hull, cargo, and contract-guarantee insurance. Three credit tiers with interest and default.

**Fleet** — Multiple hulls, dock/board at the same port, cargo transfer, eighteen upgrades.

**Career** — Twenty-seven milestones, seven profile tags, four victory paths. Dashboard shows the ledger; day-advance toasts newly completed beats.

## Victory paths

- **Lawful Trade House** — High trust, premium contracts, clean reputation, infrastructure breadth.
- **Shadow Network** — Luxury margins under heat, survived seizures, still ahead.
- **Oceanic Reach** — East Indies standing, distant infrastructure, long-haul mastery.
- **Commercial Empire** — Multi-region warehouses, brokers, licenses, financial leverage.

## Print-and-play

```bash
pip install "portlight[printandplay]"
portlight print-and-play
```

Kit-sized PDF (portrait after the landscape board, silver track 0–100). Rulebook: [docs/PRINT_AND_PLAY_RULES.md](docs/PRINT_AND_PLAY_RULES.md).

## Command groups

Run `portlight guide` in-game, or [docs/COMMANDS.md](docs/COMMANDS.md).

| Group | Commands |
|-------|----------|
| Interface | `tui`, `saves`, `--json` |
| Trading | `market`, `buy`, `sell`, `cargo` |
| Navigation | `routes`, `sail`, `advance`, `port`, `provision`, `repair`, `hire`, `fire`, `crew`, `hunt`, `work` |
| Combat | `duel`, `fight`, `encounter`, `naval`, `capture`, `spare`, `take-all`, `bounty` (`list` / `accept` / `hunt` / `claim`) |
| Equipment | `inventory`, `equip`, `merchant`, `sell-gear`, `armory`, `train`, `equip-style`, `maintain`, `smith`, `field-repair`, `injuries`, `learn-skill` |
| Fleet | `shipyard`, `drydock`, `fleet`, `dock`, `board`, `transfer`, `rename`, `upgrade` |
| Contracts | `contracts`, `accept`, `obligations`, `abandon` |
| Companions | `recruit`, `dismiss-companion`, `party` |
| Infrastructure | `warehouse`, `office`, `license` |
| Finance | `insure`, `credit` |
| Career | `captain`, `reputation`, `milestones`, `status`, `ledger` |
| World | `map` |
| System | `save`, `load`, `guide`, `print-and-play` |

## Quality

- 1,853 tests
- 14 cross-system invariants under 9 compound stress scenarios
- Balance harness: 7 policy bots, 7 scenario packs
- Save format v12 with a full migration chain
- Ruff-clean. Python 3.11 / 3.12 / 3.13

## Security

Local-only game. No network during play. Saves to `saves/` and reports to `artifacts/` as JSON. No secrets, no telemetry, no elevated permissions. See [SECURITY.md](SECURITY.md).

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check src/ tests/
```

`verify.sh` runs tests, ruff, a wheel build, and a smoke-import of the built artifact.

## License

MIT

---

Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
