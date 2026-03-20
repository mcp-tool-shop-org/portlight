# First Voyage

A concrete walkthrough of early-game trading. This covers your first 10-15 days: choosing a captain, understanding the market, making profitable runs, and knowing when each system matters.

## Choose your captain

```bash
portlight new "Your Name" --type merchant
```

Each captain starts in a different position:

- **Merchant** starts in Porto Novo (Mediterranean) with 500 silver. Legitimate operator — best prices, lowest inspection risk. Start here.
- **Smuggler** starts in Sun Harbor (West Africa) with 400 silver. Black market access, luxury margins, but customs are watching.
- **Navigator** starts in Porto Novo with 450 silver. Faster ships and better range, but thinner starting capital.

The welcome screen shows your captain advantages, what's cheap and expensive at your starting port, and concrete first commands.

## Read the market

```bash
portlight market
```

The market table shows every good available at your port:

- **Buy price** — what it costs you to purchase
- **Sell price** — what you'd get selling here (always lower than buy — that's the spread)
- **Stock** — current supply at this port

**Key insight:** Goods with high stock are cheap because the port produces them. Goods with low stock are expensive because the port consumes them. Your profit comes from buying where stock is high and selling where stock is low.

If you see `(flooded: -25%)` next to a sell price, that means you (or the market) have been dumping that good here. The sell price is temporarily depressed. Trade elsewhere or wait for recovery.

## Make your first trade

From Porto Novo, grain is cheap (high stock, high local affinity for production).

```bash
portlight buy grain 10
portlight cargo
```

Check `cargo` to confirm you're loaded. Now find where grain sells well:

```bash
portlight routes
```

Routes show destinations, distance, and estimated travel time. Al-Manar is a Mediterranean port that consumes grain — low stock, low affinity. Good target.

```bash
portlight sail al_manar
```

You're now at sea. Advance day by day:

```bash
portlight advance
```

Each day at sea consumes 1 provision and may trigger events — calm seas, storms, sightings. Your ship's hull, crew, and provisions are real resources. When you arrive:

```bash
portlight sell grain 10
```

Check your profit:

```bash
portlight status
```

## Understand flood penalty

If you sell 20 grain at Al-Manar, then immediately buy more and sell another 20, the second sale earns less. The flood penalty rises when you repeatedly sell the same good at the same port. The market shows the penalty percentage.

**What to do about it:**
- Diversify destinations — sell at different ports
- Diversify goods — don't carry only grain
- Wait — flood penalty decays over time

## When to diversify

After 3-5 profitable grain runs, you'll notice margins thinning. This is normal. The economy is reacting to your trades. Time to explore:

- **Silk and spice** sell for more per unit but are scarcer and riskier (luxury goods attract inspection attention for smugglers)
- **Cotton and iron** offer steady mid-tier margins between West Africa and other regions
- **Timber** from Silva Bay to ports without shipyards

Check markets at every port you visit. The best trades aren't always the obvious ones.

## When to consider contracts

```bash
portlight contracts
```

The contract board shows offers at your current port. Each has:
- A good to deliver
- A destination
- A quantity and deadline
- A reward

Early contracts are simple procurement: deliver X goods to Y port within Z days. The reward is often better than raw trade margin, plus completing contracts builds commercial trust, which unlocks better contracts.

**When to take one:** When you're already planning to trade that route anyway. A contract that aligns with your next 2-3 voyages is free money. A contract that forces you to rush to an unfamiliar port might cost more than it pays.

```bash
portlight accept <offer_id>
portlight obligations
```

The obligations view shows deadline context: how many days left, and estimated sail time to the destination.

## When you're close to a ship upgrade

```bash
portlight shipyard
```

The shipyard shows available ships and their costs. The sloop is your starter — small cargo hold, slow. The brigantine is the first real upgrade: more cargo, faster, better storm resistance.

The in-game hint system will tell you when you're within 200 silver of an upgrade. Don't rush it — an upgrade you can't sustain (provisions for a bigger crew, for example) is worse than a profitable sloop.

## Provisions, hull, and crew

Before every voyage:
- **Check provisions:** `portlight status` shows remaining days. Buy more with `portlight provision 10`.
- **Check hull:** If damaged from storms, repair with `portlight repair`.
- **Check crew:** Full crew means full speed. Hire with `portlight hire`.

Running out of provisions at sea is bad. Running out of hull is worse.

## Next steps

After 10-15 days of profitable trading, you'll have enough silver and understanding to start thinking about:

- **Warehouses** — stage cargo at ports for timing advantage
- **Brokers** — improve contract quality in a region
- **Licenses** — unlock premium contracts and reduce friction

See [COMMANDS.md](COMMANDS.md) for the full command reference and [CAREER_PATHS.md](CAREER_PATHS.md) for what the game is tracking about your commercial identity.
