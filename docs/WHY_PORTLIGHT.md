# Why Portlight

## Trade-first, not survival-first

Most maritime games lead with danger: storms sink your ship, pirates steal your cargo, starvation ends your run. Portlight has all of those — but they're not the point.

The point is trade. Finding margin. Timing cargo. Building the infrastructure that turns a profitable route into a commercial operation. The storms matter because they threaten your cargo timing, not because the game wants to kill you.

## Prices are alive

Portlight's economy is scarcity-driven. Every port has goods it produces cheaply (high stock, low local affinity for consumption) and goods it consumes hungrily (low stock, high demand). When you sell grain at a port that already has plenty, the price drops — and keeps dropping if you dump repeatedly (flood penalty). When you buy silk at a port where it's scarce, the price climbs.

This means profitable routes exist because of structural economic differences between ports, not because someone hardcoded "sell silk here for 2x." And those routes degrade if you or the market over-exploit them.

## Contracts and provenance

Contracts don't just say "deliver 20 grain." They require provenance — the grain must be tracked from purchase to delivery. You can't fake completion by buying at the destination port. This makes warehousing strategic: staged cargo at the right port means faster contract completion.

Contract families gate behind trust and standing. You earn access to better contracts by being commercially reliable, not by grinding a single number.

## Infrastructure as commercial advantage

Warehouses, broker offices, and licenses aren't upgrades that buff your stats. They change how you trade:

- **Warehouses** let you decouple buying from selling. Buy when cheap, store, sell when the market is right. Timing play.
- **Brokers** improve the quality of contract offers in a region. Information advantage.
- **Licenses** unlock contract families and reduce friction. Access advantage.

Each has real upkeep. Leasing infrastructure you can't sustain is worse than not having it.

## Finance has teeth

Credit lets you move faster — draw silver to fund a bigger cargo run or lease infrastructure before you can afford it outright. But interest accrues, payment deadlines are real, and three defaults freeze your credit line and damage your commercial trust.

Insurance covers real losses — storm damage, cargo loss, contract failure. But policies have coverage caps, exclusion conditions, and heat surcharges. High-heat smugglers pay more for coverage and face denial conditions.

## The career is interpreted, not chosen

You don't pick a victory path at the start. You trade, and the game reads what you built. Your career profile emerges from evidence: trade patterns, contract history, infrastructure portfolio, route diversity, financial discipline.

The four victory paths — Lawful Trade House, Shadow Network, Oceanic Reach, Commercial Empire — represent distinct commercial identities. Two players who both get rich but in different ways will see different career profiles and qualify for different paths.

## The CLI is the product

Portlight is a terminal game, not a terminal game waiting to become a GUI game. The CLI is designed for the rhythm of trade decisions: inspect, decide, execute, read the result. Rich terminal rendering makes the information dense and legible.

The `guide` command shows all commands grouped by purpose. The welcome screen after `portlight new` gives you concrete first moves. Flood penalties are explained inline. Contract deadlines show sail-time context. The interface teaches you the game as you play.

## What Portlight is not

- It's not a roguelike. Runs are long, building over dozens of days.
- It's not a tycoon game. You're one captain, not a corporation.
- It's not a narrative game. There's no plot — your commercial history is the story.
- It's not finished. This is an alpha with active balance tuning. But the systems are real, the truth model is tested, and the career arc works end to end.
