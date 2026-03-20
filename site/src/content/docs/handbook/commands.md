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
| `portlight hire [n]` | Hire crew (default: fill to capacity) |

## Contracts

| Command | What it does |
|---------|-------------|
| `portlight contracts` | View contract board offers |
| `portlight accept <id>` | Accept a contract offer |
| `portlight obligations` | View active obligations with deadlines |
| `portlight abandon <id>` | Abandon a contract (reputation cost) |

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
| `portlight reputation` | View standing, heat, and trust |
| `portlight milestones` | View milestones and victory path progress |
| `portlight status` | View captain overview with daily costs |
| `portlight ledger` | View trade receipt history |
| `portlight shipyard [buy]` | View or buy ships |

## System

| Command | What it does |
|---------|-------------|
| `portlight save` | Explicitly save the game |
| `portlight load` | Load a saved game |
| `portlight guide` | Show grouped command reference |
