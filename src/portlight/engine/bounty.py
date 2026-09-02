"""Bounty engine — hunt named pirates for reward.

The bounty board generates targets from known pirate captains.
Defeating a target lets the player claim the reward.

Contract:
  - generate_bounty_board(pirates, rng) -> list[BountyTarget]
  - accept_bounty(captain, target_id) -> str | None
  - hunt_bounty(world, captain, target_id, rng) -> EncounterState | str
  - claim_bounty(captain, pirates, target_id) -> int | str

Board, accept, and hunt only use ids that exist in
portlight.content.factions.PIRATE_CAPTAINS. Ghost ids never list or spawn.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

from portlight.content.factions import PIRATE_CAPTAINS

if TYPE_CHECKING:
    from portlight.engine.models import Captain, EncounterState, PirateState, WorldState


@dataclass
class BountyTarget:
    """A pirate captain with a price on their head."""
    captain_id: str
    captain_name: str
    faction_id: str
    region: str
    reward: int
    difficulty: str  # easy, moderate, hard, deadly
    description: str


def _times_defeated_by_player(mem: object) -> int:
    """Defeats on a CaptainMemory or its save-dict form."""
    if mem is None:
        return 0
    if isinstance(mem, dict):
        value = mem.get("times_defeated_by_player")
        if value is None:
            value = mem.get("times_defeated", 0)
        return int(value or 0)
    value = getattr(mem, "times_defeated_by_player", None)
    if value is None:
        value = getattr(mem, "times_defeated", 0)
    return int(value or 0)


# Live PIRATE_CAPTAINS only — regional spread across the Known World.
# Ghost ids (shadow_vex, brass_jack, the_drowned_king) must never appear here.
_PIRATE_BOUNTIES = [
    ("scarlet_ana", "Scarlet Ana", "crimson_tide", "North Atlantic", 150, "moderate",
     "Captain of the Crimson Tide's diplomatic fleet. Deals first, fights well."),
    ("the_butcher", "The Butcher", "crimson_tide", "Mediterranean", 220, "hard",
     "Crimson Tide enforcer. No diplomacy. Takes what he wants."),
    ("raj_the_quiet", "Raj the Quiet", "monsoon_syndicate", "East Indies", 120, "easy",
     "Syndicate spymaster. Knows your hold before you open it."),
    ("typhoon_mei", "Typhoon Mei", "monsoon_syndicate", "East Indies", 200, "hard",
     "The monsoon in human form. Controls the eastern sea lanes with chaos."),
    ("old_coral", "Old Coral", "deep_reef", "South Seas", 160, "moderate",
     "Brotherhood elder. Fifty years on the reef. Respects courage."),
    ("the_diver", "The Diver", "deep_reef", "West Africa", 180, "hard",
     "Boards from the waterline and is gone before steel is drawn."),
    ("sergeant_kruze", "Sergeant Kruze", "iron_wolves", "North Atlantic", 200, "hard",
     "Former garrison sergeant. Runs piracy like a military operation."),
    ("gnaw", "Gnaw", "iron_wolves", "North Atlantic", 200, "hard",
     "Most feared pirate in the North Atlantic. Destroys what he cannot take."),
]


def _is_live_captain(target_id: str) -> bool:
    """True when target_id is a real PIRATE_CAPTAINS row."""
    return target_id in PIRATE_CAPTAINS


def generate_bounty_board(
    pirates: "PirateState",
    rng: random.Random,
    max_targets: int = 3,
) -> list[BountyTarget]:
    """Generate bounty targets from the pirate pool.

    Filters out already-defeated captains (those with positive
    times_defeated_by_player in captain_memories) and selects a random subset.
    """
    defeated_ids = set()
    for cid, mem in pirates.captain_memories.items():
        if _times_defeated_by_player(mem) > 0:
            defeated_ids.add(cid)

    available = [
        BountyTarget(
            captain_id=cid, captain_name=name, faction_id=fid,
            region=region, reward=reward, difficulty=diff, description=desc,
        )
        for cid, name, fid, region, reward, diff, desc in _PIRATE_BOUNTIES
        if cid not in defeated_ids and _is_live_captain(cid)
    ]

    if len(available) <= max_targets:
        return available
    return rng.sample(available, max_targets)


def _claimed_ids(captain: "Captain") -> list[str]:
    """Paid-out bounty ids. Default empty list on captains that lack the field."""
    claimed = getattr(captain, "claimed_bounties", None)
    if claimed is None:
        captain.claimed_bounties = []
        return captain.claimed_bounties
    return claimed


def accept_bounty(captain: "Captain", target_id: str) -> str | None:
    """Accept a bounty target. Returns error string or None."""
    if not _is_live_captain(target_id):
        return "Unknown captain"
    if target_id in captain.active_bounties:
        return "Already hunting this target"
    if target_id in _claimed_ids(captain):
        return "Bounty already claimed"
    if len(captain.active_bounties) >= 3:
        return "Maximum 3 active bounties"
    captain.active_bounties.append(target_id)
    return None


def hunt_bounty(
    world: "WorldState",
    captain: "Captain",
    target_id: str,
    rng: random.Random,
) -> "EncounterState | str":
    """Spawn an encounter against an accepted, living bounty target.

    Requires target_id in captain.active_bounties and in PIRATE_CAPTAINS.
    Builds EncounterState the way create_encounter does, with that captain locked.
    Returns EncounterState on success, or an error string.
    """
    if not _is_live_captain(target_id):
        return "Unknown captain"
    if target_id in _claimed_ids(captain):
        return "Bounty already claimed"
    if target_id not in captain.active_bounties:
        return "No active bounty for this target"

    from portlight.engine.encounter import create_encounter

    voyage = getattr(world, "voyage", None)
    dest_id = voyage.destination_id if voyage is not None else "porto_novo"
    enc = create_encounter(
        world.ports, dest_id, rng, target_captain_id=target_id,
    )
    if enc is None:
        return "Unknown captain"
    return enc


def claim_bounty(
    captain: "Captain",
    pirates: "PirateState",
    target_id: str,
) -> int | str:
    """Claim a bounty reward after defeating the target.

    Returns silver earned on success, or error string.
    """
    if target_id not in captain.active_bounties:
        return "No active bounty for this target"

    claimed = _claimed_ids(captain)
    if target_id in claimed:
        return "Bounty already claimed"

    mem = pirates.captain_memories.get(target_id)
    if _times_defeated_by_player(mem) <= 0:
        return "Target not yet defeated. Find and defeat them at sea."

    # Find reward
    reward = 0
    for entry in _PIRATE_BOUNTIES:
        if entry[0] == target_id:
            reward = entry[4]
            break

    if reward == 0:
        return "Unknown bounty target"

    captain.silver += reward
    captain.active_bounties.remove(target_id)
    if target_id not in claimed:
        claimed.append(target_id)
    return reward
