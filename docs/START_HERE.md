# Start Here

This is a 10-minute guide to your first Portlight session. By the end, you'll have made your first profitable trade and understand the basic rhythm of the game.

## Install and start

```bash
pip install -e ".[dev]"
portlight new "Your Name" --type merchant
```

The welcome screen shows your captain identity, the port you're docked at, what's cheap and expensive locally, and suggested first moves.

Three captain types are available:
- `merchant` — best prices, lowest inspection risk, trust grows fast
- `smuggler` — black market access, luxury margins, but higher heat
- `navigator` — faster ships, longer range, early East Indies access

Start with `merchant` for your first run. The other types reward experience.

## Your first trade

```bash
portlight market
```

The market shows every good at your current port: buy price, sell price, stock levels. Look for goods with high stock — they're cheap here because the port produces them.

```bash
portlight buy grain 10
```

Buy something cheap. Grain at a Mediterranean port is usually a safe bet.

```bash
portlight routes
```

This shows where you can sail from here, with distance and travel time. Look for a destination where your cargo is consumed (low stock, high demand).

```bash
portlight sail al_manar
portlight advance
```

Sail and advance through the voyage. Events may happen — storms, sightings, inspections. `advance` moves time forward one day at a time.

```bash
portlight sell grain 10
```

Sell at the destination. The margin between your buy price and sell price is your profit.

```bash
portlight ledger
```

The ledger shows your trade receipt history with verifiable entries.

## What to focus on early

**Profit per voyage.** Your goal in the first 10-20 days is to learn which routes are profitable. Buy where stock is high, sell where it's consumed. The price difference minus port fees and travel costs is your real margin.

**Provisions.** You consume provisions every day at sea. If you run out, your crew suffers. Buy provisions before long voyages: `portlight provision 15`.

**Ship condition.** Storms and events damage your hull. Repair at port: `portlight repair`.

## What to ignore at first

**Contracts.** Available early, but don't stress about them until you understand route profitability. Check them with `portlight contracts` when you're ready.

**Infrastructure.** Warehouses, brokers, and licenses cost silver and have daily upkeep. Wait until you have a steady income loop before investing. You'll know it's time when you have 500+ silver and a predictable route.

**Insurance and credit.** These are mid-game tools. Insurance protects against losses you can't absorb. Credit accelerates moves you can't afford yet. Both have costs and risks. Ignore them until you understand the upkeep economy.

**Victory paths.** The game tracks your career milestones automatically. You don't need to optimize for them early. Just trade well and check `portlight milestones` occasionally to see what the game recognizes.

## When to care about each system

| Silver range | Day range | What opens up |
|-------------|-----------|---------------|
| 0-500 | Days 1-10 | Basic trading, route discovery, provisioning |
| 500-2000 | Days 10-25 | Ship upgrades, first warehouse, first broker, simple contracts |
| 2000-5000 | Days 25-50 | Licenses, insurance, credit, multi-region trading |
| 5000+ | Days 50+ | Victory path pursuit, full infrastructure portfolio |

These are rough guides, not hard gates. Play at your own pace.

## Reading the career ledger

```bash
portlight milestones
```

This shows:
- **Completed milestones** — specific achievements the game has recognized from your trade history
- **Victory path progress** — how close you are to each of the four commercial destinies
- **Career profile** — what kind of trader the game thinks you are, based on evidence

The career profile isn't a choice you make. It's an interpretation of what you've actually done. Two players with different strategies will see different profiles.

## Key commands

| What you want to do | Command |
|---------------------|---------|
| See everything at once | `portlight status` |
| Find profitable goods | `portlight market` |
| Check your cargo | `portlight cargo` |
| See where you can go | `portlight routes` |
| Travel somewhere | `portlight sail <destination>` |
| Pass time | `portlight advance` |
| See all commands | `portlight guide` |

## Next steps

Once you're comfortable with basic trading, read [FIRST_VOYAGE.md](FIRST_VOYAGE.md) for a detailed walkthrough of early-game strategy, or jump to [COMMANDS.md](COMMANDS.md) for the full command reference.
