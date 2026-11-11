#!/usr/bin/env python
"""Playtest bridge: lets ai-playtest's model players play Portlight.

    python tools/playtest_bridge.py --port 7790 --seed 42 --captain merchant
    python tools/playtest_bridge.py --port 7790 --seed 42 --truth runs/truth.jsonl

Speaks the rpc protocol in ai-playtest's docs/engine-bridge.md: newline-delimited
JSON over TCP, one request and one reply per line (hello / observe / act / reset /
quit). The game runs IN-PROCESS through GameSession; nothing shells out to the CLI.

WHERE THE RULES COME FROM. This file reimplements no game rules.

* Trading, voyaging, provisioning, repair, hiring, work, hunt and contracts call the
  GameSession methods the CLI calls, and the game's own error strings come back as the
  result line.
* Pirate encounters (approach, naval, boarding, duel, prize, spare / take-all) are a
  state machine that lives in portlight.app.cli, not in the session. So the bridge calls
  those CLI command functions in-process (cli.advance, cli.encounter, cli.naval,
  cli.fight, cli.capture, cli.spare, cli.take_all) with the session swapped for the
  bridge's own and the Rich console swapped for a recorder. The module-level encounter
  globals in cli.py are reset when a game starts.
* Legal actions are read from the game: lanes are probed with engine.voyage.depart on a
  deep copy of the world, buys with engine.economy.execute_buy on a deep copy, naval and
  duel verbs come from the engine's own get_*_actions functions.

DETERMINISM. GameSession.new(seed=...) seeds world.seed and the session RNG from it, and
every engine call takes that RNG (or derives one from world.seed and the day). Nothing
here reads the clock or the global random module. Same seed + same actions = same game.
The one non-deterministic thing in the game is receipt timestamps, which are not exposed.

ONE GAME PER PROCESS. The encounter state in cli.py is module-global, so one process
plays one game at a time. A new TCP connection starts a fresh game; so does reset.

THE TRUTH LOG (--truth PATH) is the hidden answer key: one JSON line per turn. It is never
sent to the player. A `{"reset": true, ...}` marker line starts each game.
"""

from __future__ import annotations

import argparse
import contextlib
import copy
import io
import json
import re
import socketserver
import sys
import tempfile
import threading
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import typer
from rich.console import Console
from rich.text import Text

from portlight.app import cli, views
from portlight.app import formatting as fmt
from portlight.app.session import GameSession
from portlight.content.goods import GOODS
from portlight.engine.campaign import compute_victory_progress
from portlight.engine.economy import execute_buy
from portlight.engine.voyage import depart

PROTOCOL = 1
MAX_ACTIONS = 40
RESULT_CLIP = 900
STEPS_AT_SEA = 5

# Events the truth log may carry. "status" and "error" are bridge extras.
EVENT_KINDS = (
    "trade", "sail", "arrive", "encounter", "duel", "contract",
    "hunt", "work", "save", "help", "rejected", "status", "error",
)

_BOX = re.compile(r"[─-╿]")


def plain(markup: str) -> str:
    """Rich markup -> plain text."""
    try:
        return Text.from_markup(markup).plain
    except Exception:  # noqa: BLE001 - a stray bracket in game text must not crash the bridge
        return markup


# Lines the game prints for a CLI user that mean nothing to a player here: commands to type,
# and the ship gauges the observation already shows in its own header.
_HINT = re.compile(r"\s*(Use |Try )?`?portlight\s+[\w-]+[^.\n]*\.?")
_DROP_LINE = re.compile(r"(^At Sea$|^(Hull|Crew|Provisions|Silver):|^Day \d+ at sea|^\S.*\s[#-]{10}\s\S.*$)")


def clean(text: str, clip: int = RESULT_CLIP) -> str:
    """Strip Rich box drawing and ANSI, drop CLI-only hint lines, collapse whitespace."""
    text = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", text)
    lines: list[str] = []
    for raw in text.splitlines():
        line = _BOX.sub(" ", raw)
        line = line.strip(" |+-=")
        line = re.sub(r"\s{2,}", " ", line.strip())
        line = _HINT.sub("", line).strip()
        if line and not _DROP_LINE.search(line):
            lines.append(line)
    out = "\n".join(lines)
    return out if len(out) <= clip else out[: clip - 3].rstrip() + "..."


class _Recorder:
    """Stands in for cli.console: keeps the raw print arguments and renders plain text."""

    def __init__(self) -> None:
        self.items: list[tuple] = []
        self._buf = io.StringIO()
        self._con = Console(file=self._buf, width=220, color_system=None,
                            force_terminal=False, legacy_windows=False)

    def print(self, *args, **kwargs) -> None:
        self.items.append(args)
        self._con.print(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._con, name)

    def text(self, clip: int = RESULT_CLIP) -> str:
        return clean(self._buf.getvalue(), clip)

    def rejected(self) -> bool:
        """The CLI reports a refused command by printing [red]..[/red] or [yellow]..[/yellow] first."""
        if not self.items or not self.items[0] or not isinstance(self.items[0][0], str):
            return False
        first = self.items[0][0].lstrip()
        return first.startswith(("[red]", "[yellow]", "[bold red]Encounter in progress"))


class Result:
    __slots__ = ("error", "events", "kind", "line")

    def __init__(self, kind: str, line: str, events: list[str] | None = None, error: str = "") -> None:
        self.kind = kind          # "ok" | "rejected"
        self.line = line
        self.events = events or []
        self.error = error


class PortlightGame:
    """One Portlight run, driven in-process, speaking in action ids."""

    def __init__(self, seed: int = 42, captain: str = "merchant", name: str = "Captain",
                 truth_path: str | None = None) -> None:
        self.seed = seed
        self.captain_type = captain
        self.captain_name = name
        self.truth_path = truth_path
        self.session: GameSession | None = None
        self._tmp: tempfile.TemporaryDirectory | None = None
        self.turn = 0
        self.last_line = ""
        self.finished: str | None = None   # reason once done: win / lose / quit
        self._lock = threading.RLock()
        self.reset()

    # ----------------------------------------------------------------- lifecycle

    def reset(self) -> None:
        with self._lock:
            if self._tmp is not None:
                self._tmp.cleanup()
            self._tmp = tempfile.TemporaryDirectory(prefix="portlight-bridge-")
            self.session = GameSession(base_path=Path(self._tmp.name))
            self.session.new(self.captain_name, captain_type=self.captain_type, seed=self.seed)
            self._reset_cli_state()
            self.turn = 0
            self.finished = None
            self.last_line = ("A new voyage begins. You are a fresh captain with a small ship, "
                              "some silver and a hold to fill.")
            self._truth({"reset": True, "seed": self.seed, "captain": self.captain_type})

    @staticmethod
    def _reset_cli_state() -> None:
        """The encounter state machine keeps module-level globals in cli.py; clear them."""
        cli._active_encounter = None
        cli._player_combatant = None
        cli._opponent_combatant = None
        cli._pending_victory = False

    def close(self) -> None:
        with self._lock:
            if self._tmp is not None:
                self._tmp.cleanup()
                self._tmp = None
            self._reset_cli_state()

    # ----------------------------------------------------------------- CLI bridge

    @contextlib.contextmanager
    def _cli(self):
        """Run cli command functions against this session with output captured."""
        rec = _Recorder()
        saved_session, saved_console = cli._session, cli.console
        cli._session = lambda: self.session
        cli.console = rec
        try:
            yield rec
        finally:
            cli._session, cli.console = saved_session, saved_console

    def _cli_call(self, fn, *args) -> Result:
        with self._cli() as rec:
            try:
                fn(*args)
            except typer.Exit:
                pass
        text = rec.text()
        return Result("rejected" if rec.rejected() else "ok", text or "Nothing happened.")

    def _encounter(self):
        """The pending encounter (restored from the session if the module lost it)."""
        with self._cli():
            cli._restore_encounter(self.session)
        return cli._active_encounter

    # ----------------------------------------------------------------- state views

    def _ship(self):
        return self.session.captain.ship

    def _market_slots(self):
        port = self.session.current_port
        return list(port.market) if port else []

    @staticmethod
    def _held(captain, good_id: str) -> int:
        return sum(c.quantity for c in captain.cargo if c.good_id == good_id)

    def _max_buy(self, slot) -> int:
        """How many units the market board's 'Can Buy' column would show."""
        cap = self.session.captain
        ship = cap.ship
        if slot.buy_price <= 0 or ship is None:
            return 0
        afford = cap.silver // slot.buy_price
        space = ship.cargo_capacity - int(sum(c.quantity for c in cap.cargo))
        return max(0, min(afford, slot.stock_current, space))

    def _probe_buy(self, good_id: str, qty: int) -> bool:
        """Would the game accept this buy? Asked of the game's own execute_buy on a copy."""
        port = self.session.current_port
        if port is None or qty <= 0:
            return False
        cap, p = copy.deepcopy((self.session.captain, port))
        return not isinstance(execute_buy(cap, p, good_id, qty, GOODS), str)

    def _sail_block(self, dest_id: str) -> str | None:
        """Why the game would refuse this departure, or None. Asked of the game's own
        depart() on a deep copy of the world, so no rule is restated here."""
        res = depart(copy.deepcopy(self.session.world), dest_id)
        return res if isinstance(res, str) else None

    def _lanes(self) -> list:
        port = self.session.current_port
        if port is None:
            return []
        out = []
        for route in self.session.world.routes:
            if route.port_a == port.id:
                dest = route.port_b
            elif route.port_b == port.id:
                dest = route.port_a
            else:
                continue
            if dest in self.session.world.ports:
                out.append((dest, route))
        return out

    def _goal_line(self) -> str:
        try:
            names = [v.name for v in compute_victory_progress(self.session._build_snapshot())]
        except Exception:  # noqa: BLE001
            names = []
        if not names:
            return "Goal: build a trading career."
        return ("Goal: complete one of the victory paths ("
                + ", ".join(names) + "). Trade for silver, grow your standing, expand your ship and reach.")

    def _game_over(self) -> str | None:
        if self.finished:
            return self.finished
        s = self.session
        if s.campaign.completed_paths:
            return "win"
        ship = s.captain.ship
        if ship is None or ship.hull <= 0:
            return "lose"
        return None

    # ----------------------------------------------------------------- actions

    def actions(self) -> list[dict]:
        """The closed set of legal actions right now: [{id, label}, ...]."""
        if self._game_over():
            return []
        s = self.session
        cap = s.captain
        out: list[dict] = []

        def add(aid: str, label: str) -> None:
            out.append({"id": aid, "label": label})

        enc = self._encounter()
        droppable: list[dict] = []
        if enc is not None:
            self._encounter_actions(enc, add)
        elif s.at_sea:
            add("advance", "Sail on for a day")
            add(f"advance:{STEPS_AT_SEA}", f"Sail on for up to {STEPS_AT_SEA} days (stops on arrival or a sighting)")
            add("hunt", "Hunt or forage at sea (takes a day)")
        else:
            port = s.current_port
            for dest_id, route in self._lanes():
                if self._sail_block(dest_id):
                    continue
                dest = s.world.ports[dest_id]
                speed = cap.ship.speed if cap.ship else 4
                add(f"sail:{dest_id}",
                    f"Sail to {dest.name} ({plain(fmt.travel_time(route.distance, speed))}, "
                    f"{plain(fmt.risk_tag(route.danger)).lower()})")
            for slot in self._market_slots():
                good = GOODS.get(slot.good_id)
                if not good:
                    continue
                can = self._max_buy(slot)
                if can >= 5 and self._probe_buy(slot.good_id, 5):
                    add(f"buy:{slot.good_id}:5", f"Buy 5 {good.name} at {slot.buy_price} each")
                if (can > 5 or 0 < can < 5) and self._probe_buy(slot.good_id, can):
                    droppable.append({"id": f"buy:{slot.good_id}:max",
                                      "label": f"Buy as many {good.name} as you can ({can} at {slot.buy_price})"})
            held_ids = []
            for item in cap.cargo:
                if item.quantity > 0 and item.good_id not in held_ids:
                    held_ids.append(item.good_id)
            for gid in held_ids:
                slot = next((x for x in self._market_slots() if x.good_id == gid), None)
                good = GOODS.get(gid)
                if slot is None or good is None:
                    continue
                add(f"sell:{gid}:all",
                    f"Sell all {good.name} ({self._held(cap, gid)} held) at {slot.sell_price} each")
            add("advance", "Wait a day in port")
            add("provision:10", f"Buy 10 days of provisions ({port.provision_cost} silver/day base)")
            add("repair", "Repair the hull")
            add("hire:1", f"Hire one sailor ({port.crew_cost} silver)")
            add("work", "Work the docks for a day")
            add("hunt", "Hunt or forage near port (takes a day)")
            for offer in s.board.offers[:3]:
                droppable.append({"id": f"accept:{offer.id[:8]}",
                                  "label": f"Accept contract: {offer.title} ({offer.quantity} {offer.good_id}, "
                                           f"{offer.reward_silver} silver)"})
            for ac in s.board.active[:3]:
                droppable.append({"id": f"abandon:{ac.offer_id[:8]}",
                                  "label": f"Abandon contract: {ac.title} (costs reputation)"})

        tail = [
            {"id": "status", "label": "Look over your captain's status"},
            {"id": "save", "label": "Save the game"},
            {"id": "help", "label": "What can I do here?"},
            {"id": "quit", "label": "Stop playing"},
        ]
        room = MAX_ACTIONS - len(out) - len(tail)
        # Drop buy:max first, then contract actions, when the menu would run long.
        keep = [d for d in droppable if d["id"].startswith(("accept:", "abandon:"))][:3]
        rest = [d for d in droppable if d["id"].startswith("buy:")]
        for d in rest + keep:
            if room > 0:
                out.append(d)
                room -= 1
        # Keep contract actions grouped after trade actions in the listing.
        return out + tail

    def _encounter_actions(self, enc, add) -> None:
        phase = enc.phase
        if cli._pending_victory or phase == "resolved":
            add("spare", "Spare the defeated captain (respect, less silver)")
            add("take-all", "Take everything from the defeated captain (more silver, more grudge)")
        elif phase == "approach":
            add("encounter:negotiate", "Negotiate with the pirate captain")
            add("encounter:flee", "Try to flee")
            add("encounter:fight", "Fight")
        elif phase == "naval":
            for verb in cli._live_naval_actions(self.session):
                add(f"naval:{verb}", f"Naval action: {verb}")
        elif phase == "capture_available":
            from portlight.app.session import prize_crew_limits
            prize_min, _ = prize_crew_limits(self.session.captain, enc)
            add("capture:0", "Let the beaten ship go under")
            add(f"capture:{prize_min}", f"Capture the prize with a crew of {prize_min}")
        else:  # boarding / duel
            from portlight.engine.combat import CORE_ACTIONS
            from portlight.engine.encounter import get_encounter_combat_actions
            if cli._player_combatant is not None:
                verbs = get_encounter_combat_actions(cli._player_combatant)
            else:
                verbs = list(CORE_ACTIONS) + ["dodge"]
            for verb in verbs:
                add(f"fight:{verb}", f"Duel move: {verb}")

    # ------------------------------------------------------------------ perform

    def act(self, params: dict) -> dict:
        """Apply one action and return the next observation."""
        with self._lock:
            aid = params.get("id") or params.get("name") or params.get("line") or ""
            if not isinstance(aid, str):
                aid = str(aid)
            aid = aid.strip()
            if self._game_over():
                return self.observation()

            before = self._snapshot_facts()
            try:
                result = self._perform(aid)
            except Exception as exc:  # noqa: BLE001 - surface game bugs as data, never crash the bridge
                result = Result("rejected", f"The game raised {type(exc).__name__}: {exc}",
                                ["error"], error=f"{type(exc).__name__}: {exc}")
            self.turn += 1
            events = list(result.events)
            events += self._diff_events(before, aid, result)
            if result.kind == "rejected" and "rejected" not in events:
                events.append("rejected")
            self.last_line = result.line
            if aid == "quit":
                self.finished = "quit"
            else:
                over = self._game_over()
                if over:
                    self.finished = over
            self._truth_turn(aid, result, events)
            return self.observation()

    def _snapshot_facts(self) -> dict:
        s = self.session
        return {"at_sea": s.at_sea, "enc": cli._active_encounter is not None,
                "pending": s.world.pirates.pending_duel is not None}

    def _diff_events(self, before: dict, aid: str, result: Result) -> list[str]:
        """Events the game reported by what changed: arrival and a new encounter."""
        s = self.session
        ev: list[str] = []
        if result.kind != "ok":
            return ev
        if before["at_sea"] and not s.at_sea and s.current_port is not None:
            ev.append("arrive")
        now_enc = cli._active_encounter is not None or s.world.pirates.pending_duel is not None
        if now_enc and not (before["enc"] or before["pending"]):
            ev.append("encounter")
        return ev

    def _perform(self, aid: str) -> Result:
        s = self.session
        parts = aid.split(":")
        verb = parts[0]

        if verb == "quit":
            return Result("ok", "You stop playing.")
        if verb == "status":
            return Result("ok", clean(self._render(views.status_view(s.world, s.ledger, s.infra))), ["status"])
        if verb == "save":
            s._save()
            return Result("ok", "Game saved.", ["save"])
        if verb == "help":
            return Result("ok", self._help_text(), ["help"])

        # Any action id the game can be asked about is passed through to the game; the
        # game's own rules and error strings decide, so an id outside the listed menu is
        # refused by the game rather than by this file.
        if verb == "buy" and len(parts) == 3:
            return self._buy(parts[1], parts[2])
        if verb == "sell" and len(parts) == 3:
            return self._sell(parts[1], parts[2])
        if verb == "sail" and len(parts) == 2:
            err = s.sail(parts[1])
            if err:
                return Result("rejected", err)
            dest = s.world.ports.get(s.world.voyage.destination_id)
            return Result("ok", f"Setting sail for {dest.name if dest else parts[1]}. "
                                f"{s.world.voyage.distance} leagues of open water.", ["sail"])
        if verb == "advance":
            days = int(parts[1]) if len(parts) == 2 and parts[1].isdigit() else 1
            return self._cli_call(cli.advance, max(1, days))
        if verb == "provision":
            days = int(parts[1]) if len(parts) == 2 and parts[1].isdigit() else 10
            err = s.provision(days)
            if err:
                return Result("rejected", err)
            return Result("ok", f"Provisioned for {days} days for {s.last_provision_cost} silver. "
                                f"Provisions now {s.captain.provisions} days.")
        if verb == "repair":
            res = s.repair()
            if isinstance(res, str):
                return Result("rejected", res)
            return Result("ok", f"Repaired {res[0]} hull points for {res[1]} silver.")
        if verb == "hire":
            count = int(parts[1]) if len(parts) == 2 and parts[1].isdigit() else 1
            err = s.hire_crew(count, "sailor")
            if err:
                return Result("rejected", err)
            return Result("ok", f"Hired {count} sailor(s). Crew now "
                                f"{s.captain.ship.crew}/{s.captain.ship.crew_max}.")
        if verb == "work":
            earned = s.work()
            if isinstance(earned, str):
                return Result("rejected", earned)
            port = s.current_port
            return Result("ok", f"A day's work on the {port.name if port else 'harbor'} docks: "
                                f"hauled crates, mended rope. Earned {earned} silver. Day {s.captain.day}.", ["work"])
        if verb == "hunt":
            res = s.hunt()
            if isinstance(res, str):
                return Result("rejected", res)
            return Result("ok", self._hunt_line(res), ["hunt"])
        if verb == "accept" and len(parts) == 2:
            matched = next((o for o in s.board.offers if o.id.startswith(parts[1])), None)
            if matched is None:
                return Result("rejected", f"No offer matching '{parts[1]}' on the board.")
            err = s.accept_contract(matched.id)
            if err:
                return Result("rejected", err)
            return Result("ok", f"Contract accepted: {matched.title}.", ["contract"])
        if verb == "abandon" and len(parts) == 2:
            matched = next((c for c in s.board.active if c.offer_id.startswith(parts[1])), None)
            if matched is None:
                return Result("rejected", f"No active contract matching '{parts[1]}'.")
            err = s.abandon_contract_cmd(matched.offer_id)
            if err:
                return Result("rejected", err)
            return Result("ok", f"Contract abandoned: {matched.title}. Reputation penalty applied.", ["contract"])

        # Encounter family: the CLI owns this state machine.
        if verb == "encounter" and len(parts) == 2:
            return self._enc_call(cli.encounter, parts[1], "encounter")
        if verb == "naval" and len(parts) == 2:
            return self._enc_call(cli.naval, parts[1], "encounter")
        if verb == "fight" and len(parts) == 2:
            return self._enc_call(cli.fight, parts[1], "duel")
        if verb == "capture" and len(parts) == 2 and parts[1].isdigit():
            return self._enc_call(cli.capture, int(parts[1]), "encounter")
        if verb == "spare":
            return self._enc_call(cli.spare, None, "duel")
        if verb == "take-all":
            return self._enc_call(cli.take_all, None, "duel")

        return Result("rejected", f"Unknown action '{aid}'. Choose one from the list.")

    def _enc_call(self, fn, arg, kind: str) -> Result:
        self._encounter()   # restore module state if needed
        res = self._cli_call(fn, *(() if arg is None else (arg,)))
        if res.kind == "ok":
            res.events.append(kind)
        return res

    def _buy(self, good: str, qty_spec: str) -> Result:
        s = self.session
        if qty_spec == "max":
            slot = next((x for x in self._market_slots() if x.good_id == good), None)
            qty = self._max_buy(slot) if slot else 0
        elif qty_spec.isdigit():
            qty = int(qty_spec)
        else:
            return Result("rejected", f"Invalid quantity: {qty_spec}")
        res = s.buy(good, qty)
        if isinstance(res, str):
            return Result("rejected", res)
        return Result("ok", f"Bought {res.quantity}x {res.good_id} for {res.total_price} silver.", ["trade"])

    def _sell(self, good: str, qty_spec: str) -> Result:
        s = self.session
        if qty_spec == "all":
            qty = self._held(s.captain, good)
        elif qty_spec.isdigit():
            qty = int(qty_spec)
        else:
            return Result("rejected", f"Invalid quantity: {qty_spec}")
        res = s.sell(good, qty)
        if isinstance(res, str):
            return Result("rejected", res)
        return Result("ok", f"Sold {res.quantity}x {res.good_id} for {res.total_price} silver.", ["trade"])

    @staticmethod
    def _hunt_line(r) -> str:
        bits = [r.flavor]
        if r.success:
            if r.provisions_gained:
                bits.append(f"+{r.provisions_gained} provisions.")
            if r.pelts_gained:
                bits.append(f"+{r.pelts_gained} pelts (sell them at any port).")
            if r.silver_gained:
                bits.append(f"+{r.silver_gained} silver.")
        else:
            bits.append("Nothing useful found.")
        if r.danger_text:
            bits.append(r.danger_text)
        if r.crew_lost:
            bits.append(f"Lost {r.crew_lost} crew.")
        if r.hull_damage:
            bits.append(f"Hull damage: -{r.hull_damage}.")
        if r.morale_cost:
            bits.append(f"Morale -{r.morale_cost}.")
        return " ".join(b for b in bits if b)

    def _render(self, renderable) -> str:
        buf = io.StringIO()
        Console(file=buf, width=110, color_system=None, force_terminal=False,
                legacy_windows=False).print(renderable)
        return buf.getvalue()

    def _help_text(self) -> str:
        return (
            "You captain a small trading ship. Buy goods where they are cheap, sail to a port where they sell "
            "higher, and keep your hold, hull, crew and provisions in order. Sailing takes days; use 'advance' "
            "to pass them. Pirates may stop you at sea. If you run low on silver, work the docks or hunt. "
            + self._goal_line()
        )

    # ------------------------------------------------------------- observation

    def observation(self) -> dict:
        with self._lock:
            over = self._game_over()
            obs = {
                "text": self._text(),
                "state": self._state(),
                "actions": {"kind": "choice", "options": self.actions()},
                "done": bool(over),
            }
            if over:
                obs["reason"] = over
            return obs

    def _state(self) -> dict:
        s = self.session
        state = s.snapshot()
        ship = s.captain.ship
        state["ship"] = None if ship is None else {
            "hull": ship.hull, "hull_max": ship.hull_max,
            "crew": ship.crew, "crew_max": ship.crew_max,
            "cargo_capacity": ship.cargo_capacity,
        }
        enc = cli._active_encounter
        state["encounter"] = None if enc is None else {
            "phase": enc.phase, "enemy": enc.enemy_captain_name,
            "enemy_hull": enc.enemy_ship_hull, "enemy_crew": enc.enemy_ship_crew,
        }
        return state

    def _text(self) -> str:
        s = self.session
        cap = s.captain
        ship = cap.ship
        lines: list[str] = []
        over = self._game_over()

        if s.at_sea:
            v = s.world.voyage
            o = s.world.ports.get(v.origin_id)
            d = s.world.ports.get(v.destination_id)
            pct = min(100, int(v.progress / max(v.distance, 1) * 100))
            lines.append(f"Day {s.world.day}. At sea, bound from {o.name if o else v.origin_id} "
                         f"to {d.name if d else v.destination_id}: day {v.days_elapsed} of the voyage, {pct}% there.")
        elif s.current_port is not None:
            p = s.current_port
            lines.append(f"Day {s.world.day}. Docked at {p.name} ({p.region}). Port fee {p.port_fee} silver.")
        if ship is not None:
            used = int(sum(c.quantity for c in cap.cargo))
            lines.append(
                f"Silver {cap.silver}. Hull {ship.hull}/{ship.hull_max}. Crew {ship.crew}/{ship.crew_max}. "
                f"Provisions {plain(fmt.provision_status(cap.provisions))}. Hold {used}/{ship.cargo_capacity}."
            )
            lines.append("Ship: " + ship.name + " (" + ship.template_id.replace("_", " ") + ")")
        if cap.cargo:
            lines.append("Cargo: " + ", ".join(
                f"{c.quantity} {c.good_id} (cost {c.cost_basis}, bought at {c.acquired_port})" for c in cap.cargo if c.quantity > 0
            ))
        else:
            lines.append("Cargo: none.")

        enc = self._encounter() if not over else None
        if enc is not None:
            lines.append(self._encounter_text(enc))
        elif s.current_port is not None:
            p = s.current_port
            lines.append(f"Market at {p.name} (good id: buy / sell / stock / you hold):")
            for slot in p.market:
                good = GOODS.get(slot.good_id)
                if not good:
                    continue
                tag = plain(fmt.scarcity_tag(slot.stock_current, slot.stock_target))
                held = self._held(cap, slot.good_id)
                lines.append(f"  {slot.good_id} ({good.name}): buy {slot.buy_price}, sell {slot.sell_price}, "
                             f"stock {slot.stock_current}/{slot.stock_target} {tag}, hold {held}")
            lanes = []
            for dest_id, route in self._lanes():
                dest = s.world.ports[dest_id]
                speed = ship.speed if ship else 4
                block = self._sail_block(dest_id)
                lanes.append(f"{dest_id} ({dest.name}, {plain(fmt.travel_time(route.distance, speed))}, "
                             f"{plain(fmt.risk_tag(route.danger)).lower()}"
                             + (f"; cannot sail it now: {block}" if block else "") + ")")
            lines.append("Lanes you can sail: " + "; ".join(lanes) if lanes else "No lanes from here.")
            if s.board.offers:
                lines.append("Contract board: " + "; ".join(
                    f"{o.id[:8]} {o.title} - {o.quantity} {o.good_id} to {o.destination_port_id}, "
                    f"{o.reward_silver} silver, due day {o.deadline_day}" for o in s.board.offers[:3]))
        if s.board.active:
            lines.append("Active contracts: " + "; ".join(
                f"{c.offer_id[:8]} {c.title} - {c.delivered_quantity}/{c.required_quantity} {c.good_id} to "
                f"{c.destination_port_id}, due day {c.deadline_day}" for c in s.board.active))
        lines.append(self._goal_line())
        if over == "lose":
            lines.append("Your ship is lost. The voyage ends here.")
        elif over == "win":
            lines.append("You have completed a victory path.")
        elif over == "quit":
            lines.append("You stopped playing.")
        lines.append("Last: " + self.last_line)
        return "\n".join(lines)

    def _encounter_text(self, enc) -> str:
        head = (f"PIRATE ENCOUNTER: {enc.enemy_captain_name} ({enc.enemy_personality}, "
                f"strength {enc.enemy_strength}).")
        if cli._pending_victory or enc.phase == "resolved":
            return head + " You have beaten them. Choose mercy or plunder."
        if enc.phase == "approach":
            return head + (f" Their ship: hull {enc.enemy_ship_hull}/{enc.enemy_ship_hull_max}, "
                           f"crew {enc.enemy_ship_crew}, cannons {enc.enemy_ship_cannons}. "
                           "Negotiate, flee or fight?")
        if enc.phase == "naval":
            return head + (f" Naval fight, turn {enc.naval_turns}. Their hull {enc.enemy_ship_hull}/"
                           f"{enc.enemy_ship_hull_max}, crew {enc.enemy_ship_crew}, cannons {enc.enemy_ship_cannons}. "
                           f"Boarding {enc.boarding_progress}/{enc.boarding_threshold}.")
        if enc.phase == "capture_available":
            return head + " Their ship is sinking and can be taken as a prize if you assign a crew."
        p = cli._player_combatant
        o = cli._opponent_combatant
        if p is not None and o is not None:
            return head + (f" Duel, turn {enc.duel_turns}. You: {p.hp}/{p.hp_max} hp, {p.stamina}/{p.stamina_max} "
                           f"stamina. Them: {o.hp}/{o.hp_max} hp.")
        return head + " Boarding action: personal combat. Choose a move."

    # --------------------------------------------------------------- truth log

    def _truth(self, record: dict) -> None:
        if not self.truth_path:
            return
        path = Path(self.truth_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, sort_keys=True, ensure_ascii=True) + "\n")

    def _truth_turn(self, aid: str, result: Result, events: list[str]) -> None:
        s = self.session
        port = s.current_port
        rec = {
            "turn": self.turn,
            "action": aid,
            "result": result.kind,
            "port": port.id if port else None,
            "day": s.world.day,
            "silver": s.captain.silver,
            "events": events,
            "note": result.line[:200],
        }
        if result.error:
            rec["error"] = result.error
        self._truth(rec)

    # accessors used by tests
    @property
    def world(self):
        return self.session.world


# ===================================================================== server

class _Handler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        server: PlaytestServer = self.server  # type: ignore[assignment]
        game = server.game
        with game._lock:
            game.reset()          # a new connection starts from the starting world
        for raw in self.rfile:
            line = raw.decode("utf-8", "replace").strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                self._send({"error": {"message": "not JSON"}})
                continue
            if not isinstance(msg, dict):
                continue
            mid, method = msg.get("id", 0), msg.get("method", "")
            params = msg.get("params") or {}
            try:
                if method == "hello":
                    result = {"protocol": PROTOCOL, "game": "portlight",
                              "capabilities": ["observe", "act", "reset", "quit"]}
                elif method == "observe":
                    result = game.observation()
                elif method == "act":
                    result = game.act(params if isinstance(params, dict) else {})
                elif method == "reset":
                    with game._lock:
                        game.reset()
                    result = game.observation()
                elif method == "quit":
                    result = game.observation()
                    result["done"] = True
                    result["reason"] = "quit"
                    self._send({"id": mid, "result": result})
                    return
                else:
                    self._send({"id": mid, "error": {"message": f"unknown method {method!r}"}})
                    continue
            except Exception as exc:  # noqa: BLE001
                self._send({"id": mid, "error": {"message": f"{type(exc).__name__}: {exc}"}})
                continue
            self._send({"id": mid, "result": result})

    def _send(self, payload: dict) -> None:
        try:
            self.wfile.write((json.dumps(payload, ensure_ascii=True) + "\n").encode("utf-8"))
            self.wfile.flush()
        except OSError:
            pass


class PlaytestServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, game: PortlightGame, host: str = "127.0.0.1", port: int = 0) -> None:
        self.game = game
        super().__init__((host, port), _Handler)

    @property
    def port(self) -> int:
        return self.server_address[1]

    def start(self) -> threading.Thread:
        t = threading.Thread(target=self.serve_forever, daemon=True)
        t.start()
        return t


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Portlight playtest bridge (ai-playtest rpc protocol)")
    ap.add_argument("--port", type=int, default=7790)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--captain", default="merchant",
                    help="captain type: merchant, smuggler, navigator, privateer, corsair, scholar, "
                         "merchant_prince, dockhand, bounty_hunter")
    ap.add_argument("--name", default="Captain")
    ap.add_argument("--truth", default=None, help="write the hidden per-turn answer key (JSONL) here")
    args = ap.parse_args(argv)

    game = PortlightGame(seed=args.seed, captain=args.captain, name=args.name, truth_path=args.truth)
    server = PlaytestServer(game, args.host, args.port)
    sys.stdout.write(f"PLAYTEST_BRIDGE_PORT={server.port}\n")
    sys.stdout.flush()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        game.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
