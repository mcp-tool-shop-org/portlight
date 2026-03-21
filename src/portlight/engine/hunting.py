"""Hunting engine — forage for provisions and pelts.

Anti-soft-lock mechanic: gives stranded captains a way to gather
provisions (reducing daily costs) and pelts (tradeable commodity).

Contract:
  - hunt(captain, location, crew_count, rng) -> HuntResult
  - location: "port" (reliable) or "sea" (risky)
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from portlight.engine.models import Captain


@dataclass
class HuntResult:
    """Outcome of a hunting expedition."""
    success: bool
    provisions_gained: int = 0
    pelts_gained: int = 0
    morale_cost: int = 0
    flavor: str = ""


# Flavor text pools
_PORT_SUCCESS = [
    "Your crew hauls in a decent catch from the harbor waters. Fresh fish for everyone.",
    "The nearby woods yield rabbits and wild herbs. The cook is pleased.",
    "Local trappers trade tips with your crew. A productive morning.",
    "Shore birds and shellfish — not glamorous, but the provisions hold is fuller.",
]

_PORT_FAIL = [
    "The crew spends the day fishing but catches nothing worth keeping.",
    "Rain drives the hunting party back early. A wasted effort.",
]

_SEA_SUCCESS = [
    "A school of fish passes beneath the hull. The crew drops nets and hauls aboard a good catch.",
    "The lookout spots a seal colony on a rocky outcrop. Your crew returns with pelts and meat.",
    "Drifting kelp beds teem with crabs and small fish. Easy pickings for hungry sailors.",
]

_SEA_FAIL = [
    "The sea gives nothing today. Your crew stares at empty nets.",
    "A promising fishing spot turns up nothing but jellyfish and seaweed.",
    "The waters are too deep and too cold. Nothing bites.",
]


def hunt(
    captain: "Captain",
    location: str,
    crew_count: int,
    rng: random.Random,
) -> HuntResult:
    """Hunt for provisions and pelts.

    Args:
        captain: The player captain (day is advanced).
        location: "port" (80% success, no morale cost) or "sea" (50% success, morale cost).
        crew_count: Number of crew members (affects yield).
        rng: Random number generator.

    Returns:
        HuntResult with provisions/pelts gained.
    """
    if location == "port":
        success_chance = 0.8
        morale_cost = 0
    else:
        success_chance = 0.5
        morale_cost = 3

    success = rng.random() < success_chance
    crew_bonus = min(crew_count // 3, 2)  # up to +2 from large crew

    if success:
        if location == "port":
            provisions = rng.randint(2, 4) + crew_bonus
            pelts = rng.randint(0, 2)
            flavor = rng.choice(_PORT_SUCCESS)
        else:
            provisions = rng.randint(1, 3) + crew_bonus
            pelts = rng.randint(0, 1)
            flavor = rng.choice(_SEA_SUCCESS)
    else:
        provisions = 0
        pelts = 0
        flavor = rng.choice(_PORT_FAIL if location == "port" else _SEA_FAIL)

    captain.day += 1

    return HuntResult(
        success=success,
        provisions_gained=provisions,
        pelts_gained=pelts,
        morale_cost=morale_cost,
        flavor=flavor,
    )
