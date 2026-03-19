"""Phase 1 ship templates — 3 classes, progression path."""

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
    ),
]}


def create_ship_from_template(template: ShipTemplate, name: str | None = None) -> "Ship":
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
