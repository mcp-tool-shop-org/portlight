"""Voyage engine - travel state machine, provision consumption, route events.

Phase 2 additions:
  - Ship class requirements on routes (warn or block)
  - Crew wages paid daily at sea
  - Storm damage reduced by ship storm_resist
  - Cargo-aware events (pirates target valuable cargo)
  - Opportunity events (flotsam, merchant encounter)
  - Undermanned penalty (speed reduction)

Phase 3A additions:
  - Captain identity modifiers (provision burn, speed, storm resist, cargo damage)
  - Inspection profile (frequency, seizure risk, fine multiplier)
  - Port fee multiplier from captain type
  - Reputation mutations from trade and inspection events

Contract:
  - depart(world, destination_id) -> VoyageState | error string
  - advance_day(world, rng) -> list[VoyageEvent]  (may include arrival)
  - arrive(world) -> settles captain in destination port
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

from portlight.engine.models import Route, VoyageState, VoyageStatus

if TYPE_CHECKING:
    from portlight.engine.captain_identity import CaptainTemplate
    from portlight.engine.models import Captain, Ship, WorldState


def _get_captain_mods(captain: "Captain") -> "CaptainTemplate | None":
    """Load captain template from captain_type string. Returns None for unknown types."""
    try:
        from portlight.engine.captain_identity import CAPTAIN_TEMPLATES, CaptainType
        ct = CaptainType(captain.captain_type)
        return CAPTAIN_TEMPLATES[ct]
    except (ValueError, KeyError):
        return None


class EventType(str, Enum):
    STORM = "storm"
    PIRATES = "pirates"
    INSPECTION = "inspection"
    CALM_SEAS = "calm_seas"
    FAVORABLE_WIND = "favorable_wind"
    PROVISIONS_SPOILED = "provisions_spoiled"
    CARGO_DAMAGED = "cargo_damaged"
    MERCHANT_ENCOUNTER = "merchant_encounter"
    FLOTSAM = "flotsam"
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
    speed_modifier: float = 1.0
    cargo_lost: dict[str, int] | None = None  # good_id -> qty lost


# ---------------------------------------------------------------------------
# Ship class ordering for route checks
# ---------------------------------------------------------------------------

_SHIP_CLASS_RANK = {"sloop": 0, "brigantine": 1, "galleon": 2}


def ship_class_rank(template_id: str) -> int:
    """Get numeric rank from template_id."""
    for cls_name, rank in _SHIP_CLASS_RANK.items():
        if cls_name in template_id:
            return rank
    return 0


# ---------------------------------------------------------------------------
# Event table (Phase 2)
# ---------------------------------------------------------------------------

_EVENT_WEIGHTS: list[tuple[EventType, float]] = [
    (EventType.NOTHING, 0.35),
    (EventType.CALM_SEAS, 0.12),
    (EventType.FAVORABLE_WIND, 0.10),
    (EventType.STORM, 0.12),
    (EventType.PIRATES, 0.08),
    (EventType.INSPECTION, 0.05),
    (EventType.PROVISIONS_SPOILED, 0.05),
    (EventType.CARGO_DAMAGED, 0.04),
    (EventType.MERCHANT_ENCOUNTER, 0.05),
    (EventType.FLOTSAM, 0.04),
]


def _pick_event(
    danger: float, rng: random.Random,
    inspection_mult: float = 1.0,
) -> EventType:
    """Weighted random event, danger level scales hostile events."""
    weights = []
    for etype, base_w in _EVENT_WEIGHTS:
        w = base_w
        if etype in (EventType.STORM, EventType.PIRATES, EventType.CARGO_DAMAGED):
            w *= (1 + danger * 2)
        elif etype in (EventType.MERCHANT_ENCOUNTER, EventType.FLOTSAM):
            w *= max(0.5, 1 - danger)  # less likely on dangerous routes
        elif etype == EventType.INSPECTION:
            w *= inspection_mult  # captain identity affects inspection frequency
        weights.append(w)
    return rng.choices([e for e, _ in _EVENT_WEIGHTS], weights=weights, k=1)[0]


def _resolve_event(
    event_type: EventType, rng: random.Random,
    captain: "Captain", ship: "Ship",
) -> VoyageEvent:
    """Generate concrete effects for an event type, aware of ship and cargo."""
    from portlight.content.ships import SHIPS
    template = SHIPS.get(ship.template_id)
    storm_resist = template.storm_resist if template else 0.0

    # Captain identity modifiers
    cap_mods = _get_captain_mods(captain)
    if cap_mods:
        storm_resist = min(0.8, storm_resist + cap_mods.voyage.storm_resist_bonus)
        cargo_dmg_mult = cap_mods.voyage.cargo_damage_mult
        insp = cap_mods.inspection
    else:
        cargo_dmg_mult = 1.0
        insp = None

    match event_type:
        case EventType.STORM:
            raw_dmg = rng.randint(5, 18)
            dmg = max(1, int(raw_dmg * (1 - storm_resist)))
            if storm_resist > 0.3:
                msg = f"A storm batters the ship. Your hull absorbs the worst of it. (-{dmg} hull)"
            else:
                msg = f"A violent storm batters the ship! (-{dmg} hull)"
            return VoyageEvent(EventType.STORM, msg, hull_delta=-dmg, speed_modifier=0.5)

        case EventType.PIRATES:
            # Pirates target valuable cargo
            cargo_value = sum(c.quantity * 10 for c in captain.cargo)  # rough estimate
            base_loss = rng.randint(10, 40)
            silver_loss = min(base_loss + cargo_value // 10, captain.silver)
            dmg = rng.randint(3, 12)
            dmg = max(1, int(dmg * (1 - storm_resist * 0.5)))
            return VoyageEvent(
                EventType.PIRATES,
                f"Pirates attack! You fight them off but lose {silver_loss} silver. (-{dmg} hull)",
                hull_delta=-dmg, silver_delta=-silver_loss,
            )

        case EventType.INSPECTION:
            fee = rng.randint(5, 25)
            fine_mult = insp.fine_mult if insp else 1.0
            fee = max(1, int(fee * fine_mult))
            # Seizure risk (smuggler penalty)
            seized_goods: dict[str, int] | None = None
            seizure_msg = ""
            if insp and insp.seizure_risk > 0 and captain.cargo:
                if rng.random() < insp.seizure_risk:
                    target = rng.choice(captain.cargo)
                    seized = min(target.quantity, rng.randint(1, 3))
                    seized_goods = {target.good_id: seized}
                    seizure_msg = f" They confiscate {seized} units of {target.good_id}!"
            msg = f"A patrol inspects your cargo and levies a {fee} silver fee.{seizure_msg}"
            return VoyageEvent(EventType.INSPECTION, msg,
                               silver_delta=-fee, cargo_lost=seized_goods)

        case EventType.FAVORABLE_WIND:
            return VoyageEvent(EventType.FAVORABLE_WIND,
                "Strong tailwinds speed your journey!", speed_modifier=1.5)

        case EventType.PROVISIONS_SPOILED:
            spoil = rng.randint(2, 6)
            return VoyageEvent(EventType.PROVISIONS_SPOILED,
                f"Some provisions have spoiled. (-{spoil} days)", provision_delta=-spoil)

        case EventType.CALM_SEAS:
            return VoyageEvent(EventType.CALM_SEAS,
                "Calm seas. Good for rest, bad for progress.", speed_modifier=0.6)

        case EventType.CARGO_DAMAGED:
            # Damage random cargo in hold (captain modifier reduces loss)
            if captain.cargo:
                target = rng.choice(captain.cargo)
                raw_lost = rng.randint(1, 3)
                lost = max(1, int(raw_lost * cargo_dmg_mult))
                lost = min(target.quantity, lost)
                return VoyageEvent(
                    EventType.CARGO_DAMAGED,
                    f"Rough seas damaged {lost} units of {target.good_id} in the hold.",
                    cargo_lost={target.good_id: lost},
                )
            return VoyageEvent(EventType.NOTHING, "An uneventful day at sea.")

        case EventType.MERCHANT_ENCOUNTER:
            gain = rng.randint(5, 20)
            return VoyageEvent(EventType.MERCHANT_ENCOUNTER,
                f"A passing merchant offers information and a small gift. (+{gain} silver)",
                silver_delta=gain)

        case EventType.FLOTSAM:
            prov = rng.randint(1, 4)
            return VoyageEvent(EventType.FLOTSAM,
                f"Floating wreckage yields salvageable supplies. (+{prov} provisions)",
                provision_delta=prov)

        case _:
            return VoyageEvent(EventType.NOTHING, "An uneventful day at sea.")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def find_route(world: "WorldState", origin_id: str, dest_id: str) -> Route | None:
    """Find a route between two ports (bidirectional)."""
    for r in world.routes:
        if (r.port_a == origin_id and r.port_b == dest_id) or \
           (r.port_a == dest_id and r.port_b == origin_id):
            return r
    return None


def check_route_suitability(route: Route, ship: "Ship") -> str | None:
    """Check if ship meets route requirements. Returns warning or None."""
    route_rank = _SHIP_CLASS_RANK.get(route.min_ship_class, 0)
    ship_rank = ship_class_rank(ship.template_id)
    if ship_rank < route_rank:
        if route_rank - ship_rank >= 2:
            return f"BLOCKED: This route requires at least a {route.min_ship_class}. Your {ship.name} cannot attempt it."
        return (f"WARNING: This route recommends a {route.min_ship_class}. "
                f"Your {ship.name} will face increased danger.")
    return None


def depart(world: "WorldState", destination_id: str) -> VoyageState | str:
    """Begin a voyage from current port to destination."""
    captain = world.captain
    if captain.ship is None:
        return "No ship"
    if world.voyage and world.voyage.status == VoyageStatus.AT_SEA:
        return "Already at sea"

    current_port_id = world.voyage.destination_id if world.voyage else None
    if current_port_id is None:
        return "Not docked at any port"
    if current_port_id == destination_id:
        return "Already at this port"

    route = find_route(world, current_port_id, destination_id)
    if route is None:
        return f"No route from {current_port_id} to {destination_id}"

    # Ship class check
    suitability = check_route_suitability(route, captain.ship)
    if suitability and suitability.startswith("BLOCKED"):
        return suitability

    # Pay port fee (captain modifier applies)
    port = world.ports.get(current_port_id)
    if port:
        cap_mods = _get_captain_mods(captain)
        fee_mult = cap_mods.pricing.port_fee_mult if cap_mods else 1.0
        fee = max(1, int(port.port_fee * fee_mult))
        if fee > captain.silver:
            return f"Need {fee} silver for port fee, have {captain.silver}"
        captain.silver -= fee

    voyage = VoyageState(
        origin_id=current_port_id,
        destination_id=destination_id,
        distance=route.distance,
        status=VoyageStatus.AT_SEA,
    )
    world.voyage = voyage
    return voyage


def advance_day(world: "WorldState", rng: random.Random | None = None) -> list[VoyageEvent]:
    """Advance one day at sea. Returns events that occurred."""
    rng = rng or random.Random()
    voyage = world.voyage
    captain = world.captain

    if voyage is None or voyage.status != VoyageStatus.AT_SEA:
        return []
    if captain.ship is None:
        return []

    events: list[VoyageEvent] = []

    # Captain modifiers
    cap_mods = _get_captain_mods(captain)
    provision_burn = cap_mods.voyage.provision_burn if cap_mods else 1.0
    speed_bonus = cap_mods.voyage.speed_bonus if cap_mods else 0.0
    inspection_mult = cap_mods.inspection.inspection_chance_mult if cap_mods else 1.0

    # Consume provisions (captain modifier affects burn rate)
    # provision_burn < 1.0 means some days you don't consume
    if provision_burn >= 1.0 or rng.random() < provision_burn:
        captain.provisions -= 1
    if captain.provisions < 0:
        captain.provisions = 0
        events.append(VoyageEvent(EventType.NOTHING,
            "No provisions! The crew suffers.", crew_delta=-1))

    # Crew wages (paid daily at sea)
    from portlight.content.ships import SHIPS
    template = SHIPS.get(captain.ship.template_id)
    daily_wage = template.daily_wage if template else 1
    wage_cost = daily_wage * captain.ship.crew
    if wage_cost > 0 and captain.silver >= wage_cost:
        captain.silver -= wage_cost
    elif wage_cost > 0:
        # Can't pay crew - morale hit
        events.append(VoyageEvent(EventType.NOTHING,
            "Can't pay crew wages! Morale drops.", crew_delta=-1))

    # Route event
    route = find_route(world, voyage.origin_id, voyage.destination_id)
    danger = route.danger if route else 0.1

    # Danger penalty for undersized ship
    if route:
        route_rank = _SHIP_CLASS_RANK.get(route.min_ship_class, 0)
        ship_rank = ship_class_rank(captain.ship.template_id)
        if ship_rank < route_rank:
            danger *= 1.5  # 50% more danger with unsuitable ship

    event_type = _pick_event(danger, rng, inspection_mult)
    event = _resolve_event(event_type, rng, captain, captain.ship)
    events.append(event)

    # Apply event effects
    captain.ship.hull = max(0, captain.ship.hull + event.hull_delta)
    captain.provisions = max(0, captain.provisions + event.provision_delta)
    captain.silver = max(0, captain.silver + event.silver_delta)
    captain.ship.crew = max(0, captain.ship.crew + event.crew_delta)

    # Apply cargo damage
    if event.cargo_lost:
        for good_id, lost in event.cargo_lost.items():
            for item in captain.cargo:
                if item.good_id == good_id:
                    item.quantity = max(0, item.quantity - lost)
                    if item.quantity == 0:
                        captain.cargo.remove(item)
                    break

    # Progress (undermanned penalty + captain speed bonus)
    base_speed = captain.ship.speed + speed_bonus
    crew_min = template.crew_min if template else 1
    if captain.ship.crew < crew_min:
        base_speed *= 0.5  # half speed when undermanned
    elif captain.ship.crew < captain.ship.crew_max:
        # Slight penalty when not fully crewed
        crew_ratio = captain.ship.crew / captain.ship.crew_max
        base_speed *= (0.7 + 0.3 * crew_ratio)

    day_progress = int(base_speed * event.speed_modifier)
    voyage.progress += day_progress
    voyage.days_elapsed += 1
    world.day += 1
    captain.day += 1

    # Check arrival
    if voyage.progress >= voyage.distance:
        voyage.status = VoyageStatus.ARRIVED

    return events


def arrive(world: "WorldState") -> str | None:
    """Complete arrival at destination port. Returns None on success, error on failure."""
    voyage = world.voyage
    if voyage is None or voyage.status != VoyageStatus.ARRIVED:
        return "Not arrived yet"
    voyage.status = VoyageStatus.IN_PORT
    return None
