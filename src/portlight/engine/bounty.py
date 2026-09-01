"""Bounty engine — hunt named pirates for reward.

The bounty board generates targets from known pirate captains.
Defeating a target lets the player claim the reward.

Contract:
  - generate_bounty_board(pirates, rng) -> list[BountyTarget]
  - accept_bounty(captain, target_id) -> str | None
  - claim_bounty(captain, pirates, target_id) -> int | str
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from portlight.engine.models import Captain, PirateState


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


# Known pirate captains and their base bounties
_PIRATE_BOUNTIES = [
    ("scarlet_ana", "Scarlet Ana", "crimson_tide", "North Atlantic", 150, "moderate",
     "Commander of The Crimson Tide. Raids merchant convoys in the North Atlantic."),
    ("gnaw", "Gnaw", "iron_wolves", "Mediterranean", 200, "hard",
     "Iron Wolves enforcer. Brutal boarding tactics. High kill count."),
    ("shadow_vex", "Shadow Vex", "shadow_fleet", "East Indies", 180, "moderate",
     "Ghost of the East Indies. Smuggling network mastermind."),
    ("brass_jack", "Brass Jack", "crimson_tide", "West Africa", 120, "easy",
     "Small-time raider operating off the West African coast."),
    ("the_drowned_king", "The Drowned King", "iron_wolves", "South Seas", 300, "deadly",
     "Fleet commander. Controls the southern shipping lanes."),
]


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
        if cid not in defeated_ids
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
    if target_id in captain.active_bounties:
        return "Already hunting this target"
    if target_id in _claimed_ids(captain):
        return "Bounty already claimed"
    if len(captain.active_bounties) >= 3:
        return "Maximum 3 active bounties"
    captain.active_bounties.append(target_id)
    return None


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
