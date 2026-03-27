---
title: Command Reference
description: All Portlight commands grouped by purpose.
sidebar:
  order: 3
---

Run `portlight guide` in-game to see this reference in the terminal.

## Trading

| Command | What it does |
|---------|-------------|
| `portlight market` | View prices, stock, and affordability at current port |
| `portlight buy <good> <qty>` | Buy goods from port market |
| `portlight sell <good> <qty>` | Sell goods to port market |
| `portlight cargo` | View cargo hold contents with provenance |

## Navigation

| Command | What it does |
|---------|-------------|
| `portlight routes` | List available routes with distance and travel time |
| `portlight sail <dest>` | Depart for a destination port |
| `portlight advance [days]` | Advance time (travel at sea, wait in port) |
| `portlight port` | View current port info |
| `portlight provision [n]` | Buy provisions (default: 10 days) |
| `portlight repair [n]` | Repair hull damage |
| `portlight hire [n]` | Hire crew (specify role with `--role`) |
| `portlight fire [n]` | Fire crew members (specify role with `--role`) |
| `portlight crew` | Show crew roster breakdown |
| `portlight hunt` | Hunt or forage for provisions, pelts, and silver (works at port or sea) |
| `portlight work` | Work the docks for a day to earn silver (safety valve when stranded) |

## Combat

| Command | What it does |
|---------|-------------|
| `portlight duel` | Fight a pirate captain in a sword duel (stances: thrust, slash, parry) |
| `portlight fight` | Execute a personal combat action |
| `portlight encounter` | Respond to a pirate encounter: negotiate, flee, or fight |
| `portlight naval` | Execute a naval combat action |
| `portlight capture` | Capture a defeated enemy ship as a prize |
| `portlight spare` | Show mercy to a defeated pirate captain (gains respect, reduces grudge) |
| `portlight take-all` | Take everything from a defeated captain (more silver, more grudge) |
| `portlight bounty` | View the bounty board, accept targets, or claim rewards |

## Equipment

| Command | What it does |
|---------|-------------|
| `portlight inventory` | Show all personal gear: armor, weapons, styles, ranged, injuries, cargo |
| `portlight equip` | Equip or unequip armor and melee weapons |
| `portlight merchant` | Browse or buy from port merchants |
| `portlight sell-gear` | Sell a weapon or armor back to the port for 50% value |
| `portlight armory` | View or buy ranged weapons and ammunition |
| `portlight train` | Learn a fighting style from a regional master |
| `portlight equip-style` | Equip or unequip a fighting style |
| `portlight maintain` | Maintain a weapon to prevent quality degradation |
| `portlight smith` | Upgrade weapon quality at a smith (requires shipyard port) |
| `portlight injuries` | Show current injuries and healing status |
| `portlight learn-skill` | Learn or advance a skill from a trainer at this port |
| `portlight field-repair` | Repair a weapon at sea (requires Journeyman blacksmith skill) |

## Fleet

| Command | What it does |
|---------|-------------|
| `portlight shipyard [buy]` | View or buy ships at the shipyard |
| `portlight drydock` | Restore degraded hull_max at a shipyard (costs 5x normal repair rate) |
| `portlight fleet` | Show all ships in your fleet |
| `portlight dock` | Park current ship and switch to another at the same port |
| `portlight board` | Switch to a docked ship at the same port |
| `portlight transfer` | Move cargo between ships at the same port |
| `portlight rename` | Rename your flagship or a fleet ship |
| `portlight upgrade` | Browse or install ship upgrades at the shipyard |

## Contracts

| Command | What it does |
|---------|-------------|
| `portlight contracts` | View contract board offers |
| `portlight accept <id>` | Accept a contract offer |
| `portlight obligations` | View active obligations with deadlines |
| `portlight abandon <id>` | Abandon a contract (reputation cost) |

## Companions

| Command | What it does |
|---------|-------------|
| `portlight recruit` | Recruit a companion at this port |
| `portlight dismiss-companion` | Dismiss a companion from your party |
| `portlight party` | Show your companion party |

## Infrastructure

| Command | What it does |
|---------|-------------|
| `portlight warehouse [action]` | Manage warehouses: `lease`, `deposit`, `withdraw`, `list` |
| `portlight office [action]` | Manage broker offices: `open`, `upgrade` |
| `portlight license [buy <id>]` | View or purchase licenses |

## Finance

| Command | What it does |
|---------|-------------|
| `portlight insure [buy <id>]` | View or purchase insurance policies |
| `portlight credit [action]` | Manage credit: `open`, `draw`, `repay`, `status` |

## Career

| Command | What it does |
|---------|-------------|
| `portlight captain` | View captain identity and advantages |
| `portlight reputation` | View standing, heat, and trust across all regions |
| `portlight milestones` | View milestones and victory path progress |
| `portlight status` | View captain overview with daily costs |
| `portlight ledger` | View trade receipt history |

## World

| Command | What it does |
|---------|-------------|
| `portlight map` | View the world map with ports, routes, and your position |

## Interface

| Command | What it does |
|---------|-------------|
| `portlight tui` | Launch the full-screen TUI dashboard |

## System

| Command | What it does |
|---------|-------------|
| `portlight new <name>` | Start a new game (omit `--type` for interactive captain roster) |
| `portlight save` | Explicitly save the game |
| `portlight load` | Load a saved game |
| `portlight guide` | Show grouped command reference |
| `portlight print-and-play` | Generate the Print-and-Play board game PDF kit |
