"""Tests for tools/playtest_bridge.py: the ai-playtest rpc bridge.

Proves: the protocol round-trips; the same seed and actions give the same game; every
action the bridge lists is either played or refused with the game's own message; and
the game can tell six scripted play styles apart (the persona gate), so a model run
measures the model, not the game's inability to separate styles.
"""

from __future__ import annotations

import importlib.util
import json
import random
import socket
import sys
from pathlib import Path

import pytest

_TOOLS = Path(__file__).resolve().parent.parent / "tools"
_spec = importlib.util.spec_from_file_location("playtest_bridge", _TOOLS / "playtest_bridge.py")
pb = importlib.util.module_from_spec(_spec)
sys.modules["playtest_bridge"] = pb
_spec.loader.exec_module(pb)

SEED = 42


def read_truth(path: Path) -> list[dict]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return [r for r in rows if "turn" in r]


@pytest.fixture
def make_game(tmp_path):
    games = []

    def _make(seed=SEED, captain="merchant", truth="truth.jsonl"):
        g = pb.PortlightGame(seed=seed, captain=captain,
                             truth_path=str(tmp_path / truth) if truth else None)
        games.append(g)
        return g

    yield _make
    for g in games:
        g.close()


def ids(obs: dict) -> list[str]:
    return [a["id"] for a in obs["actions"]["options"]]


# ---------------------------------------------------------------------------
# 1. Protocol round trip
# ---------------------------------------------------------------------------

class _Client:
    def __init__(self, port: int):
        self.sock = socket.create_connection(("127.0.0.1", port), timeout=10)
        self.file = self.sock.makefile("rwb")
        self.next_id = 0

    def call(self, method: str, params: dict | None = None) -> dict:
        msg = {"id": self.next_id, "method": method}
        if params is not None:
            msg["params"] = params
        self.next_id += 1
        self.file.write((json.dumps(msg) + "\n").encode())
        self.file.flush()
        reply = json.loads(self.file.readline())
        assert reply["id"] == msg["id"]
        return reply

    def close(self):
        self.file.close()
        self.sock.close()


class TestProtocol:
    def test_round_trip(self, make_game):
        game = make_game()
        server = pb.PlaytestServer(game, "127.0.0.1", 0)  # ephemeral port
        server.start()
        try:
            c = _Client(server.port)

            hello = c.call("hello", {"protocol": 1})["result"]
            assert hello["protocol"] == 1 and hello["game"] == "portlight"

            obs = c.call("observe")["result"]
            assert isinstance(obs["text"], str) and "Porto Novo" in obs["text"]
            assert "\x1b" not in obs["text"]
            assert obs["state"]["captain"]["silver"] == 550
            assert obs["actions"]["kind"] == "choice"
            assert obs["done"] is False
            options = obs["actions"]["options"]
            assert all(set(o) == {"id", "label"} for o in options)
            assert "buy:grain:5" in [o["id"] for o in options]

            # act: a trade changes silver and prices, and says what happened
            after = c.call("act", {"kind": "choose", "id": "buy:grain:5"})["result"]
            assert after["state"]["captain"]["silver"] < 550
            assert "Bought 5x grain" in after["text"]
            assert after["state"]["cargo"][0]["good_id"] == "grain"

            # the scripted-setup channel: act with a line
            line = c.call("act", {"kind": "line", "line": "status"})["result"]
            assert "Last:" in line["text"]

            # an action the game refuses comes back as text, not an rpc error
            bad = c.call("act", {"kind": "choose", "id": "buy:grain:9999"})
            assert "error" not in bad
            assert "Last:" in bad["result"]["text"]

            # reset returns to the starting world
            fresh = c.call("reset")["result"]
            assert fresh["state"]["captain"]["silver"] == 550 and fresh["state"]["cargo"] == []
            assert fresh["state"]["day"] == 1

            # unknown method is an rpc error, not a crash
            assert "error" in c.call("nope")

            # quit ends the session
            quit_obs = c.call("quit")["result"]
            assert quit_obs["done"] is True and quit_obs["reason"] == "quit"
            c.close()

            # the server outlives a client: a new connection starts from the starting world
            c2 = _Client(server.port)
            assert c2.call("hello", {"protocol": 1})["result"]["protocol"] == 1
            assert c2.call("observe")["result"]["state"]["captain"]["silver"] == 550
            c2.close()
        finally:
            server.shutdown()
            server.server_close()

    def test_in_game_quit_ends_the_run(self, make_game):
        game = make_game()
        obs = game.act({"id": "quit"})
        assert obs["done"] is True and obs["reason"] == "quit"
        assert obs["actions"]["options"] == []
        assert game.reset() is None
        assert game.observation()["done"] is False


# ---------------------------------------------------------------------------
# 2. Determinism
# ---------------------------------------------------------------------------

def _walk(game, n: int, rng_seed: int) -> list[str]:
    """Play n steps chosen by a seeded RNG; return the action ids played."""
    rng = random.Random(rng_seed)
    played = []
    obs = game.observation()
    for _ in range(n):
        if obs["done"]:
            break
        choices = [i for i in ids(obs) if i != "quit"]
        pick = rng.choice(choices)
        played.append(pick)
        obs = game.act({"id": pick})
    return played


def _replay(game, actions: list[str]) -> dict:
    obs = game.observation()
    for a in actions:
        obs = game.act({"id": a})
    return obs


class TestDeterminism:
    def test_same_seed_same_actions_same_game(self, make_game):
        a = make_game(truth="a.jsonl")
        actions = _walk(a, 120, rng_seed=5)
        assert len(actions) >= 60, "the walk ended too early to prove anything"
        b = make_game(truth="b.jsonl")
        final_b = _replay(b, actions)
        final_a = a.observation()

        truth_a = read_truth(a_path := Path(a.truth_path))
        truth_b = read_truth(Path(b.truth_path))
        assert truth_a == truth_b
        assert len(truth_a) == len(actions)
        assert final_a["state"] == final_b["state"]
        assert final_a["text"] == final_b["text"]
        assert a_path.exists()

    def test_reset_replays_the_same_game(self, make_game):
        g = make_game()
        actions = _walk(g, 80, rng_seed=11)
        first = g.observation()["state"]
        g.reset()
        again = _replay(g, actions)["state"]
        assert again == first

    def test_different_seed_is_a_different_game(self, make_game):
        a, b = make_game(seed=1), make_game(seed=2)
        # the opening market is fixed; the contract board and the days that follow are seeded
        assert a.observation()["state"]["board"] != b.observation()["state"]["board"]
        for _ in range(4):
            a.act({"id": "advance"})
            b.act({"id": "advance"})
        assert a.observation()["state"]["market"] != b.observation()["state"]["market"]


# ---------------------------------------------------------------------------
# 3. Every listed action is playable or refused with the game's own message
# ---------------------------------------------------------------------------

class TestListedActions:
    @pytest.mark.parametrize("seed,rng_seed", [(42, 1), (7, 2), (123, 3)])
    def test_two_hundred_random_steps(self, make_game, seed, rng_seed):
        game = make_game(seed=seed)
        rng = random.Random(rng_seed)
        obs = game.observation()
        steps = 0
        for _ in range(200):
            if obs["done"]:
                break
            options = obs["actions"]["options"]
            assert options, f"empty action list while the game is running:\n{obs['text']}"
            assert len(options) <= 40
            assert len({o["id"] for o in options}) == len(options), "duplicate action ids"
            assert {"status", "save", "help", "quit"} <= {o["id"] for o in options}
            pick = rng.choice([o for o in options if o["id"] != "quit"])
            obs = game.act({"id": pick["id"]})
            steps += 1
            assert obs["text"].strip() and "\x1b" not in obs["text"]
        # a lost ship is a legitimate end; being stuck or crashing is not
        assert steps == 200 or obs["reason"] in ("lose", "win")

        rows = read_truth(Path(game.truth_path))
        assert len(rows) == steps
        assert not [r for r in rows if "error" in r], "the game raised an exception"
        for r in rows:
            assert r["result"] in ("ok", "rejected")
            if r["result"] == "rejected":
                assert r["note"].strip(), "a rejection must carry the game's message"
                assert "rejected" in r["events"]

    def test_unlisted_and_malformed_ids_are_refused_not_crashed(self, make_game):
        game = make_game()
        for bad in ["", "nonsense", "buy", "buy:grain", "buy:grain:x", "sell:grain:all",
                    "sail:atlantis", "encounter:fight", "naval:broadside", "capture:3", "spare"]:
            obs = game.act({"id": bad})
            assert obs["done"] is False
        rows = read_truth(Path(game.truth_path))
        assert all(r["result"] == "rejected" for r in rows)
        assert not [r for r in rows if "error" in r]

    def test_truth_is_not_in_the_observation(self, make_game):
        game = make_game()
        obs = game.act({"id": "buy:grain:5"})
        blob = json.dumps(obs)
        assert "events" not in blob and "truth" not in blob.lower()

    def test_observation_text_carries_what_a_player_needs(self, make_game):
        game = make_game()
        text = game.observation()["text"]
        for needle in ("Porto Novo", "Day 1", "Silver 550", "Hull", "Crew", "Provisions",
                       "Cargo", "Market", "grain", "Lanes you can sail", "Goal:"):
            assert needle in text, needle
        game.act({"id": "buy:grain:5"})
        game.act({"id": "sail:silva_bay"})
        at_sea = game.observation()["text"]
        assert "At sea" in at_sea and "Silva Bay" in at_sea and "5 grain" in at_sea
        assert "Market at" not in at_sea


# ---------------------------------------------------------------------------
# 4. The persona gate
# ---------------------------------------------------------------------------
#
# Scripted policies: plain functions of the observation, no models. Each plays 60 turns
# on the same seed. The truth logs are then scored. The gate proves the game can tell
# these play styles apart before anyone pays for a model run: each persona has to lead
# every other persona on its own statistic, and beat the control by a clear margin.

TURNS = 60

ENCOUNTER_FAMILIES = ("encounter:", "naval:", "fight:", "capture:", "spare", "take-all")


def pick(options: list[str], *prefs: str) -> str | None:
    """First listed action matching the earliest preference (exact id or id prefix)."""
    for pref in prefs:
        for oid in options:
            if oid == pref or (pref.endswith(":") and oid.startswith(pref)):
                return oid
    return None


def in_encounter(options: list[str]) -> bool:
    return any(o.startswith(ENCOUNTER_FAMILIES) for o in options if o not in ("status", "save", "help", "quit"))


def encounter_move(options: list[str], mood: str) -> str:
    """How each style answers a pirate: fight, bargain, or run."""
    prefs = {
        "fight": ["encounter:fight", "naval:broadside", "naval:close", "fight:slash", "fight:thrust",
                  "take-all", "capture:0", "naval:evade"],
        "bargain": ["encounter:negotiate", "naval:evade", "naval:flee", "fight:parry", "spare", "capture:0"],
        "run": ["encounter:flee", "naval:flee", "naval:evade", "fight:dodge", "fight:parry", "spare", "capture:0"],
    }[mood]
    return pick(options, *prefs) or next(o for o in options if o.startswith(ENCOUNTER_FAMILIES))


def upkeep(st: dict, options: list[str]) -> str | None:
    """The chores any captain does so the ship keeps sailing: mend, crew up, victual."""
    ship, cap = st["ship"], st["captain"]
    if "repair" in options and ship["hull"] < ship["hull_max"] and cap["silver"] > 30:
        return "repair"
    if "hire:1" in options and ship["crew"] < 4 and cap["silver"] > 30:
        return "hire:1"
    if "provision:10" in options and cap["provisions"] < 10 and cap["silver"] > 60:
        return "provision:10"
    return None


def lanes_from(st: dict, options: list[str]) -> list[dict]:
    return [r for r in st["routes"] if f"sail:{r['destination_id']}" in options]


def policy_control():
    """Fixed simple loop that does nothing in particular."""
    loop = ["advance", "status", "advance", "help"]
    state = {"i": 0}

    def act(obs):
        options = ids(obs)
        if in_encounter(options):
            return encounter_move(options, "run")
        a = loop[state["i"] % len(loop)]
        state["i"] += 1
        return a if a in options else "status"
    return act


def policy_trader():
    """Sell what came from elsewhere, buy what is plentiful, sail the shortest lane."""
    def act(obs):
        options, st = ids(obs), obs["state"]
        if in_encounter(options):
            return encounter_move(options, "run")
        if st["at_sea"]:
            return pick(options, "advance:5", "advance")
        chore = upkeep(st, options)
        if chore:
            return chore
        here = st["port"]["id"]
        carried = {c["good_id"] for c in st["cargo"] if c["acquired_port"] != here}
        for oid in options:
            if oid.startswith("sell:") and oid.split(":")[1] in carried:
                return oid
        held = sum(c["quantity"] for c in st["cargo"])
        if held < st["ship"]["cargo_capacity"] // 2:
            best, best_ratio = None, 0.0
            for slot in st["market"]:
                ratio = slot["stock_current"] / max(1, slot["stock_target"])
                cand = pick(options, f"buy:{slot['good_id']}:max", f"buy:{slot['good_id']}:5")
                if cand and ratio > best_ratio:
                    best, best_ratio = cand, ratio
            if best:
                return best
        lanes = sorted(lanes_from(st, options), key=lambda r: r["distance"])
        if lanes:
            return f"sail:{lanes[0]['destination_id']}"
        return pick(options, "work", "advance", "status")
    return act


def policy_explorer():
    """Sail to the least-visited port, always."""
    visits: dict[str, int] = {}

    def act(obs):
        options, st = ids(obs), obs["state"]
        if in_encounter(options):
            return encounter_move(options, "run")
        if st["at_sea"]:
            return pick(options, "advance:5", "advance")
        chore = upkeep(st, options)
        if chore:
            return chore
        here = st["port"]["id"]
        visits[here] = visits.get(here, 0) + 1
        lanes = lanes_from(st, options)
        if lanes:
            lanes.sort(key=lambda r: (visits.get(r["destination_id"], 0), r["distance"]))
            return f"sail:{lanes[0]['destination_id']}"
        return pick(options, "work", "advance", "status")
    return act


def policy_hunter():
    """Hunt, and go looking for pirates to fight."""
    state = {"n": 0}

    def act(obs):
        options, st = ids(obs), obs["state"]
        if in_encounter(options):
            return encounter_move(options, "fight")
        state["n"] += 1
        if st["at_sea"]:
            # alternate hunting with sailing on, so the voyage still ends
            return pick(options, "hunt") if state["n"] % 2 else pick(options, "advance:5", "advance")
        chore = upkeep(st, options)
        if chore:
            return chore
        if state["n"] % 5 == 0:
            for r in sorted(lanes_from(st, options), key=lambda r: -r["danger"]):
                return f"sail:{r['destination_id']}"
        return pick(options, "hunt", "advance")
    return act


def policy_grinder():
    """Work the docks and keep the ship mended; sail only now and then."""
    state = {"n": 0}

    def act(obs):
        options, st = ids(obs), obs["state"]
        if in_encounter(options):
            return encounter_move(options, "run")
        state["n"] += 1
        if st["at_sea"]:
            return pick(options, "advance:5", "advance")
        chore = upkeep(st, options)
        if chore:
            return chore
        if state["n"] % 30 == 0:
            lanes = lanes_from(st, options)
            if lanes:
                return f"sail:{lanes[0]['destination_id']}"
        return pick(options, "work", "advance")
    return act


def policy_quitter():
    """Tries to do something the game refuses, tries again, and gives up on the second refusal."""
    state = {"refused": 0}

    def act(obs):
        options = ids(obs)
        if in_encounter(options):
            return encounter_move(options, "run")
        state["refused"] = state["refused"] + 1 if obs.get("_last_result") == "rejected" else 0
        if state["refused"] >= 2:
            return "quit"
        return "repair" if "repair" in options else pick(options, "advance", "status")
    return act


POLICIES = {
    "control": policy_control,
    "trader": policy_trader,
    "explorer": policy_explorer,
    "hunter": policy_hunter,
    "grinder": policy_grinder,
    "quitter": policy_quitter,
}


def play(make_game, name: str, seed: int = SEED) -> list[dict]:
    game = make_game(seed=seed, truth=f"{name}.jsonl")
    policy = POLICIES[name]()
    obs = game.observation()
    last = None
    for _ in range(TURNS):
        if obs["done"]:
            break
        obs["_last_result"] = last
        choice = policy(obs)
        obs = game.act({"id": choice})
        last = read_truth(Path(game.truth_path))[-1]["result"]
        if choice == "quit":
            break
    return read_truth(Path(game.truth_path))


def stats(rows: list[dict]) -> dict:
    n = len(rows)
    ok = [r for r in rows if r["result"] == "ok"]
    share = lambda pred: sum(1 for r in ok if pred(r["action"])) / n
    visited = {r["port"] for r in rows if r["port"]}
    quit_turn = next((r["turn"] for r in rows if r["action"] == "quit"), n)
    return {
        "turns": n,
        "trade": share(lambda a: a.startswith(("buy:", "sell:"))),
        "ports": len(visited),
        "hunt_enc": share(lambda a: a == "hunt" or a.startswith(ENCOUNTER_FAMILIES)),
        "work": share(lambda a: a == "work"),
        "quit_turn": quit_turn,
    }


@pytest.fixture(params=[SEED, 7, 2024], ids=lambda s: f"seed{s}")
def persona_table(make_game, request):
    seed = request.param
    table = {name: stats(play(make_game, name, seed)) for name in POLICIES}
    print(f"\npersona gate (seed {seed}, {TURNS} turns)")
    print(f"{'persona':9} {'turns':>5} {'trade':>6} {'ports':>5} {'hunt+enc':>8} {'work':>6} {'quit@':>5}")
    for name, s in table.items():
        print(f"{name:9} {s['turns']:5d} {s['trade']:6.2f} {s['ports']:5d} {s['hunt_enc']:8.2f} "
              f"{s['work']:6.2f} {s['quit_turn']:5d}")
    return table


class TestPersonaGate:
    def test_every_persona_leads_on_its_own_statistic(self, persona_table):
        t = persona_table
        others = lambda me: [n for n in t if n != me]

        # Share statistics: higher is more that style. Margin over control: 15 points.
        for persona, key in (("trader", "trade"), ("hunter", "hunt_enc"), ("grinder", "work")):
            mine = t[persona][key]
            for other in others(persona):
                assert mine > t[other][key], f"{persona} does not lead {other} on {key}: {t}"
            assert mine >= t["control"][key] + 0.15, f"{persona} barely beats control on {key}: {t}"

        # Exploration: distinct ports docked at. Margin over control: 3 ports.
        for other in others("explorer"):
            assert t["explorer"]["ports"] > t[other]["ports"], f"explorer does not lead {other}: {t}"
        assert t["explorer"]["ports"] >= t["control"]["ports"] + 3

        # Quitting: fewer turns before quitting is more quitter. The others never quit.
        for other in others("quitter"):
            assert t["quitter"]["quit_turn"] < t[other]["quit_turn"], f"quitter does not lead {other}: {t}"
        assert t["quitter"]["quit_turn"] <= t["control"]["quit_turn"] / 2

    def test_the_styles_are_not_the_same_game(self, persona_table):
        """No two personas may produce the same profile."""
        profiles = [tuple(round(v, 2) for k, v in s.items() if k != "turns") for s in persona_table.values()]
        assert len(set(profiles)) == len(profiles)
