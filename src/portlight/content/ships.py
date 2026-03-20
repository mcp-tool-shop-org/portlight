"""Phase 2 ship templates - 3 classes, each changes the game shape.

Sloop: fast, fragile, small hold. Mediterranean-safe. Gets punished on long hauls.
Brigantine: balanced, opens West Africa reliably and East Indies hub.
  More cargo = bulk routes viable. Higher crew = real wage pressure.
Galleon: slow fortress. Makes long-haul luxury profitable.
  Huge hold but expensive crew, slow speed means more provisions burned.
  Storm-resistant - the only ship that can reliably survive perilous routes.
"""

from portlight.engine.models import ShipClass, ShipTemplate

SHIPS: dict[str, ShipTemplate] = {s.id: s for s in [
    ShipTemplate(
        id="coastal_sloop",
        name="Coastal Sloop",
        ship_class=ShipClass.SLOOP,
        cargo_capacity=30,
        speed=8,
        hull_max=60,
        crew_min=3,
        crew_max=8,
        price=0,  # starting ship
        daily_wage=1,
        storm_resist=0.0,
    ),
    ShipTemplate(
        id="trade_brigantine",
        name="Trade Brigantine",
        ship_class=ShipClass.BRIGANTINE,
        cargo_capacity=80,
        speed=6,
        hull_max=100,
        crew_min=8,
        crew_max=20,
        price=800,
        daily_wage=2,
        storm_resist=0.3,  # absorbs 30% storm damage
    ),
    ShipTemplate(
        id="merchant_galleon",
        name="Merchant Galleon",
        ship_class=ShipClass.GALLEON,
        cargo_capacity=150,
        speed=4,
        hull_max=160,
        crew_min=15,
        crew_max=40,
        price=2200,
        daily_wage=3,
        storm_resist=0.6,  # absorbs 60% storm damage
    ),
]}


def create_ship_from_template(template: ShipTemplate, name: str | None = None) -> "Ship":  # noqa: F821
    """Instantiate a Ship from a template."""
    from portlight.engine.models import Ship
    return Ship(
        template_id=template.id,
        name=name or template.name,
        hull=template.hull_max,
        hull_max=template.hull_max,
        cargo_capacity=template.cargo_capacity,
        speed=template.speed,
        crew=template.crew_min,
        crew_max=template.crew_max,
    )
