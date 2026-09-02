---
title: The TUI
description: Play Portlight without typing command names — keys, dialogs, and the same save as the CLI.
sidebar:
  order: 2
---

`portlight tui` is a full game, not a status viewer. It uses the same `saves/` slot as the CLI.

Install the extra: `pip install "portlight[tui]"`.

## First launch

If the slot is empty, a **Save slots** dialog lists existing JSON files plus **New**. New walks the captain-type roster (same order as CLI). Load switches the slot and restores the run.

`portlight saves` lists those slots from the CLI. `portlight --json status` dumps the live state as JSON.

## Keys

| Key | Tab / action | Twice |
|-----|----------------|-------|
| D | Dashboard (career panel lives here) | — |
| M | Market | B buy, S sell |
| R | Routes | G sail, A advance a day |
| C | Cargo | — |
| I | Inventory | — |
| F | Fleet | **F again** — board, dock, transfer, sell a prize hull |
| K | Contracts | **K again** — accept or abandon |
| P | Port | **P again** — shipyard (buy hull, install/remove upgrade, dry-dock) |
| L | Ledger | — |
| W | Infra | **W again** — lease, deposit, withdraw, broker, license, credit |
| V | Map (pane-width, 1-char S/B/H markers) | — |
| H | Harbor | provision / repair / hire / work / fire / hunt. **At sea, H hunts.** |
| Y | Fighting-style special (in a duel, when ready) | — |
| ? | Help | — |
| Q | Quit | — |

Insurance file/claim is still CLI-only.

## Harbor and the EMPTY! sidebar

When provisions hit empty, the sidebar tells you to press **H**, not to type `portlight hunt`. Docked, H opens the harbor picker. At sea, H forages.

## Combat

Naval actions on screen match the engine: broadside, close, evade, rake, flee. After a sink, prize capture is a real prompt — not a fake duel victory. Flee calls `attempt_flee`.

## Campaign

Dashboard shows `milestones_view`. Advancing a day toasts newly completed milestone titles and victory-path names. You do not have to open a thirteenth tab.
