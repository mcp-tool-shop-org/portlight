---
title: For Beginners
description: New to Portlight? Start here for a gentle introduction.
sidebar:
  order: 99
---

## What is Portlight?

Portlight is a single-player trading game that runs entirely in your terminal. You play as a ship captain buying and selling goods across a network of 20 ports spread over five ocean regions. The goal is to build a successful merchant career through smart trading, route planning, and business investments.

Unlike most trading games where prices are random, Portlight simulates a real economy. Every port produces certain goods cheaply and needs other goods badly. When you sell a lot of grain at one port, the price drops. When you discover a port that desperately needs silk, you can profit from that structural gap. Your decisions shape prices, and your reputation follows you from port to port.

The game tracks everything you do and scores your career across multiple dimensions. There is no single "win" button. Instead, four different victory paths recognize different styles of play: legitimate trade empires, shadow smuggling networks, long-haul oceanic routes, and diversified commercial operations.

## Who is this for?

Portlight is built for players who enjoy:

- **Strategy games** where decisions compound over time
- **Terminal-based games** (no graphics, no browser, just your command line)
- **Economic simulation** with real supply-and-demand mechanics
- **Sandbox play** where you choose your own goals and pace

No prior experience with trading games or terminal tools is needed beyond knowing how to type commands and press Enter. If you can use `cd` and `ls` in a terminal, you can play Portlight.

## Prerequisites

Before you start, make sure you have:

- **Python 3.11 or newer** installed on your system. Check with `python --version` or `python3 --version`.
- **pip** (Python's package manager). It comes bundled with Python on most systems.
- **A terminal** you are comfortable typing in (Terminal on Mac, PowerShell or Windows Terminal on Windows, any shell on Linux).

If you do not have Python, you can use the npm wrapper instead: `npx @mcptoolshop/portlight`. This requires Node.js 18 or newer.

## Your first 5 minutes

**Step 1 -- Install Portlight**

```bash
pip install portlight
```

**Step 2 -- Start a new game**

```bash
portlight new "Your Name" --type merchant
```

Pick `merchant` for your first game. Merchants get better prices and build trust faster, which makes the early game smoother. You will see a summary of your captain and starting port (Porto Novo in the Mediterranean).

**Step 3 -- Check the local market**

```bash
portlight market
```

This shows every good available at your current port, with buy prices, sell prices, and current stock. Look for goods with high stock -- those are cheap to buy here.

**Step 4 -- Buy cheap goods**

```bash
portlight buy grain 10
```

Grain is produced in Porto Novo, so it is cheap here. Buy what you can afford.

**Step 5 -- Find a destination**

```bash
portlight routes
```

This lists ports you can sail to, how far away they are, and how long the trip takes. Pick a short route for your first voyage. Al-Manar is a good first destination.

**Step 6 -- Sail and travel**

```bash
portlight sail al_manar
portlight advance
```

The `sail` command sets your destination. The `advance` command moves time forward day by day. You will see weather, events, and your provisions ticking down as you travel.

**Step 7 -- Sell at a profit**

```bash
portlight sell grain 10
```

If grain is cheaper where you bought it and more expensive where you are now, you pocket the difference. That margin is your profit. Congratulations -- you just completed your first trade.

## Common mistakes

**Running out of provisions.** Your crew eats one provision per day at sea. Before any voyage, buy provisions with `portlight provision 15` (or however many days you need). If you run out, your crew loses morale and you take penalties. Always check your voyage length against your provision count.

**Selling the same good at the same port repeatedly.** Portlight applies a flood penalty when you dump the same commodity at one location over and over. Your sell price drops each time. Spread your sales across different ports and different goods to avoid this.

**Ignoring ship condition.** Storms damage your hull during voyages. If your hull drops too low, you are in trouble. Repair at port with `portlight repair` before it gets critical. Pay attention to your hull status after every voyage.

**Trying to do everything at once.** Contracts, infrastructure, insurance, combat, companions -- Portlight has many systems, but they unlock gradually. For your first 10-20 game days, focus only on buying, sailing, and selling. Everything else can wait until you have a steady income loop.

**Forgetting to save.** The game auto-saves after every action, but you can also run `portlight save` manually. Your saves live in a local `saves/` directory and never leave your machine.

## Next steps

Once you are comfortable with basic trading, explore these handbook pages:

- [Getting Started](../getting-started/) -- captain types, system unlock timeline, and what to focus on early
- [Trading Guide](../trading/) -- the full economy explained: regions, goods, ship progression, and seasons
- [Commands](../commands/) -- every command in the game, grouped by purpose
- [Career Paths](../career-paths/) -- how the game scores your career and the four victory paths

## Glossary

| Term | Meaning |
|------|---------|
| **Port** | A named location where you can buy goods, sell goods, repair your ship, and access services. There are 20 ports across 5 regions. |
| **Good** | A tradeable commodity (grain, silk, iron, spice, etc.). There are 18 goods in the game, including 3 contraband items. |
| **Route** | A sea path connecting two ports. Each route has a distance, travel time, and danger level that changes by season. |
| **Provisions** | Food and water for your crew. You consume one per day at sea. Buy them at port before departing. |
| **Hull** | Your ship's structural health. Storms and combat reduce it. Repair at port with `portlight repair`. |
| **Silver** | The game's currency. You earn it by selling goods at a profit. You spend it on cargo, provisions, repairs, crew, and upgrades. |
| **Heat** | Customs attention. Smuggling and suspicious cargo raise your heat, which leads to inspections and port denials. |
| **Trust** | Commercial reputation. Higher trust unlocks better contracts and premium port access. |
| **Standing** | Your reputation within a specific region. Higher standing opens doors in that region's ports. |
| **Contract** | A delivery job with a deadline and reward. Accept contracts at the contract board (`portlight contracts`). |
| **Flood penalty** | A price reduction applied when you sell the same good repeatedly at the same port. Diversify to avoid it. |
| **Provenance** | The tracked origin of your cargo. Contracts verify that your delivered goods came from legitimate sources. |
| **Captain type** | Your starting class (Merchant, Smuggler, Navigator, etc.). Each starts in a different port with different advantages. |
| **Victory path** | One of four career outcomes the game recognizes: Lawful Trade House, Shadow Network, Oceanic Reach, or Commercial Empire. |
| **TUI** | Text User Interface. Launch with `portlight tui` for a full-screen dashboard (requires the optional `textual` package). |
