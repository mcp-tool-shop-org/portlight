"""Ship stat resolution — compute effective stats from base template + upgrades.

Ship dataclass fields hold base values from the template. These functions
compute effective values by applying upgrade bonuses. Call these at the
point where the stat matters (voyage speed, naval combat, etc.).

Pure functions — no state mutation.
"""

from __future__ import annotations

from portlight.engine.models import (
    Ship,
    ShipTemplate,
    UpgradeTemplate,
)


def resolve_speed(
    ship: Ship,
    upgrades_catalog: dict[str, UpgradeTemplate],
) -> float:
    """Effective speed = base + upgrade bonuses - penalties."""
    bonus = 0.0
    penalty = 0.0
    for inst in ship.upgrades:
        tmpl = upgrades_catalog.get(inst.upgrade_id)
        if tmpl:
            bonus += tmpl.speed_bonus
            penalty += tmpl.speed_penalty
    return max(0.5, ship.speed + bonus - penalty)


def resolve_hull_max(
    ship: Ship,
    upgrades_catalog: dict[str, UpgradeTemplate],
) -> int:
    """Effective hull max = base + upgrade bonuses."""
    bonus = 0
    for inst in ship.upgrades:
        tmpl = upgrades_catalog.get(inst.upgrade_id)
        if tmpl:
            bonus += tmpl.hull_max_bonus
    return ship.hull_max + bonus


def resolve_cargo_capacity(
    ship: Ship,
    upgrades_catalog: dict[str, UpgradeTemplate],
) -> int:
    """Effective cargo capacity = base + upgrade bonuses."""
    bonus = 0
    for inst in ship.upgrades:
        tmpl = upgrades_catalog.get(inst.upgrade_id)
        if tmpl:
            bonus += tmpl.cargo_bonus
    return ship.cargo_capacity + bonus


def resolve_cannons(
    ship: Ship,
    upgrades_catalog: dict[str, UpgradeTemplate],
) -> int:
    """Effective cannon count = base + upgrade bonuses."""
    bonus = 0
    for inst in ship.upgrades:
        tmpl = upgrades_catalog.get(inst.upgrade_id)
        if tmpl:
            bonus += tmpl.cannon_bonus
    return ship.cannons + bonus


def resolve_maneuver(
    ship: Ship,
    upgrades_catalog: dict[str, UpgradeTemplate],
) -> float:
    """Effective maneuver = base + upgrade bonuses, clamped to [0, 1]."""
    bonus = 0.0
    for inst in ship.upgrades:
        tmpl = upgrades_catalog.get(inst.upgrade_id)
        if tmpl:
            bonus += tmpl.maneuver_bonus
    return max(0.0, min(1.0, ship.maneuver + bonus))


def resolve_storm_resist(
    ship: Ship,
    template: ShipTemplate,
    upgrades_catalog: dict[str, UpgradeTemplate],
) -> float:
    """Effective storm resistance = template base + upgrade bonuses, capped at 0.9."""
    bonus = 0.0
    for inst in ship.upgrades:
        tmpl = upgrades_catalog.get(inst.upgrade_id)
        if tmpl:
            bonus += tmpl.storm_resist_bonus
    return min(0.9, template.storm_resist + bonus)


def resolve_crew_max(
    ship: Ship,
    upgrades_catalog: dict[str, UpgradeTemplate],
) -> int:
    """Effective crew max = base + upgrade bonuses."""
    bonus = 0
    for inst in ship.upgrades:
        tmpl = upgrades_catalog.get(inst.upgrade_id)
        if tmpl:
            bonus += tmpl.crew_max_bonus
    return ship.crew_max + bonus


def has_special(
    ship: Ship,
    special: str,
    upgrades_catalog: dict[str, UpgradeTemplate],
) -> bool:
    """Check if any installed upgrade has the given special tag."""
    for inst in ship.upgrades:
        tmpl = upgrades_catalog.get(inst.upgrade_id)
        if tmpl and tmpl.special == special:
            return True
    return False


def resolved_ship(
    ship: Ship,
    upgrades_catalog: dict[str, UpgradeTemplate],
) -> Ship:
    """Return a copy of the ship with effective stats applied.

    Use this at the boundary when passing a ship to pure combat/voyage
    functions that read stats directly from the Ship object.
    The returned copy shares the same upgrades list (not a deep copy).
    """
    return Ship(
        template_id=ship.template_id,
        name=ship.name,
        hull=ship.hull,
        hull_max=resolve_hull_max(ship, upgrades_catalog),
        cargo_capacity=resolve_cargo_capacity(ship, upgrades_catalog),
        speed=resolve_speed(ship, upgrades_catalog),
        crew=ship.crew,
        crew_max=resolve_crew_max(ship, upgrades_catalog),
        cannons=resolve_cannons(ship, upgrades_catalog),
        maneuver=resolve_maneuver(ship, upgrades_catalog),
        upgrades=ship.upgrades,
        upgrade_slots=ship.upgrade_slots,
    )


def resolve_all(
    ship: Ship,
    template: ShipTemplate,
    upgrades_catalog: dict[str, UpgradeTemplate],
) -> dict:
    """Compute all resolved stats as a dict. Useful for views."""
    return {
        "speed": resolve_speed(ship, upgrades_catalog),
        "hull_max": resolve_hull_max(ship, upgrades_catalog),
        "cargo_capacity": resolve_cargo_capacity(ship, upgrades_catalog),
        "cannons": resolve_cannons(ship, upgrades_catalog),
        "maneuver": resolve_maneuver(ship, upgrades_catalog),
        "storm_resist": resolve_storm_resist(ship, template, upgrades_catalog),
        "crew_max": resolve_crew_max(ship, upgrades_catalog),
    }
