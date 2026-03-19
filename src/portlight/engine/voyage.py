"""Voyage engine — travel state machine, provision consumption, route events.

Contract:
  - depart(world, destination_id) → VoyageState | error string
  - advance_day(world, rng) → list[VoyageEvent]  (may include arrival)
  - arrive(world) → settles captain in destination port

State machine:
  IN_PORT → depart() → AT_SEA → advance_day() loops → ARRIVED → arrive() → IN_PORT
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

from portlight.engine.models import Route, VoyageState, VoyageStatus

if TYPE_CHECKING:
    from portlight.engine.models import WorldState


class EventType(str, Enum):
    STORM = "storm"
    PIRATES = "pirates"
    INSPECTION = "inspection"
    CALM_SEAS = "calm_seas"
    FAVORABLE_WIND = "favorable_wind"
    PROVISIONS_SPOILED = "provisions_spoiled"
    NOTHING = "nothing"


@dataclass
class VoyageEvent:
    """One thing that happened during a day at sea."""
    event_type: EventType
    message: str
    hull_delta: int = 0
    provision_delta: int = 0
    silver_delta: int = 0
    crew_delta: int = 0
    speed_modifier: float = 1.0      # multiplied into progress for this day


# ---------------------------------------------------------------------------
# Event table (Phase 1 — simple weighted random)
# ---------------------------------------------------------------------------

_EVENT_WEIGHTS: list[tuple[EventType, float]] = [
    (EventType.NOTHING, 0.45),
    (EventType.CALM_SEAS, 0.15),
    (EventType.FAVORABLE_WIND, 0.10),
    (EventType.STORM, 0.12),
    (EventType.PIRATES, 0.08),
    (EventType.INSPECTION, 0.05),
    (EventType.PROVISIONS_SPOILED, 0.05),
]


def _pick_event(danger: float, rng: random.Random) -> EventType:
    """Weighted random event, danger level scales hostile events."""
    weights = []
    for etype, base_w in _EVENT_WEIGHTS:
        w = base_w
        if etype in (EventType.STORM, EventType.PIRATES):
            w *= (1 + danger)
        weights.append(w)
    return rng.choices([e for e, _ in _EVENT_WEIGHTS], weights=weights, k=1)[0]


def _resolve_event(event_type: EventType, rng: random.Random) -> VoyageEvent:
    """Generate concrete effects for an event type."""
    match event_type:
        case EventType.STORM:
            dmg = rng.randint(5, 15)
            return VoyageEvent(EventType.STORM, "A violent storm batters the ship.", hull_delta=-dmg, speed_modifier=0.5)
        case EventType.PIRATES:
            loss = rng.randint(10, 40)
            dmg = rng.randint(3, 10)
            return VoyageEvent(EventType.PIRATES, "Pirates attack! You fight them off.", hull_delta=-dmg, silver_delta=-loss)
        case EventType.INSPECTION:
            fee = rng.randint(5, 20)
            return VoyageEvent(EventType.INSPECTION, "A patrol inspects your cargo and levies a fee.", silver_delta=-fee)
        case EventType.FAVORABLE_WIND:
            return VoyageEvent(EventType.FAVORABLE_WIND, "Strong tailwinds speed your journey.", speed_modifier=1.5)
        case EventType.PROVISIONS_SPOILED:
            spoil = rng.randint(2, 5)
            return VoyageEvent(EventType.PROVISIONS_SPOILED, "Some provisions have spoiled.", provision_delta=-spoil)
        case EventType.CALM_SEAS:
            return VoyageEvent(EventType.CALM_SEAS, "Calm seas. The crew rests well.", speed_modifier=0.8)
        case _:
            return VoyageEvent(EventType.NOTHING, "An uneventful day at sea.")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def find_route(world: WorldState, origin_id: str, dest_id: str) -> Route | None:
    """Find a route between two ports (bidirectional)."""
    for r in world.routes:
        if (r.port_a == origin_id and r.port_b == dest_id) or \
           (r.port_a == dest_id and r.port_b == origin_id):
            return r
    return None


def depart(world: WorldState, destination_id: str) -> VoyageState | str:
    """Begin a voyage from current port to destination."""
    captain = world.captain
    if captain.ship is None:
        return "No ship"
    if world.voyage and world.voyage.status == VoyageStatus.AT_SEA:
        return "Already at sea"

    # Determine current port
    current_port_id = world.voyage.destination_id if world.voyage else None
    if current_port_id is None:
        # First voyage — need a starting port
        return "Not docked at any port"

    if current_port_id == destination_id:
        return "Already at this port"

    route = find_route(world, current_port_id, destination_id)
    if route is None:
        return f"No route from {current_port_id} to {destination_id}"

    # Pay port fee
    port = world.ports.get(current_port_id)
    if port and port.port_fee > captain.silver:
        return f"Need {port.port_fee} silver for port fee, have {captain.silver}"
    if port:
        captain.silver -= port.port_fee

    voyage = VoyageState(
        origin_id=current_port_id,
        destination_id=destination_id,
        distance=route.distance,
        status=VoyageStatus.AT_SEA,
    )
    world.voyage = voyage
    return voyage


def advance_day(world: WorldState, rng: random.Random | None = None) -> list[VoyageEvent]:
    """Advance one day at sea. Returns events that occurred."""
    rng = rng or random.Random()
    voyage = world.voyage
    captain = world.captain

    if voyage is None or voyage.status != VoyageStatus.AT_SEA:
        return []
    if captain.ship is None:
        return []

    events: list[VoyageEvent] = []

    # Consume provisions
    captain.provisions -= 1
    if captain.provisions < 0:
        captain.provisions = 0
        # Starvation damage
        events.append(VoyageEvent(EventType.NOTHING, "No provisions! The crew suffers.", crew_delta=-1))

    # Route event
    route = find_route(world, voyage.origin_id, voyage.destination_id)
    danger = route.danger if route else 0.1
    event_type = _pick_event(danger, rng)
    event = _resolve_event(event_type, rng)
    events.append(event)

    # Apply event effects
    captain.ship.hull = max(0, captain.ship.hull + event.hull_delta)
    captain.provisions = max(0, captain.provisions + event.provision_delta)
    captain.silver = max(0, captain.silver + event.silver_delta)
    captain.ship.crew = max(0, captain.ship.crew + event.crew_delta)

    # Progress
    base_speed = captain.ship.speed
    day_progress = int(base_speed * event.speed_modifier)
    voyage.progress += day_progress
    voyage.days_elapsed += 1
    world.day += 1
    captain.day += 1

    # Check arrival
    if voyage.progress >= voyage.distance:
        voyage.status = VoyageStatus.ARRIVED

    return events


def arrive(world: WorldState) -> str | None:
    """Complete arrival at destination port. Returns None on success, error on failure."""
    voyage = world.voyage
    if voyage is None or voyage.status != VoyageStatus.ARRIVED:
        return "Not arrived yet"
    voyage.status = VoyageStatus.IN_PORT
    return None
