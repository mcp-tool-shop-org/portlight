"""World factory — assembles a fresh WorldState from content data."""

from __future__ import annotations

import copy
import time

from portlight.content.goods import GOODS
from portlight.content.ports import PORTS
from portlight.content.routes import ROUTES
from portlight.content.ships import SHIPS, create_ship_from_template
from portlight.engine.economy import recalculate_prices
from portlight.engine.models import Captain, VoyageState, VoyageStatus, WorldState


def new_game(captain_name: str = "Captain", starting_port: str = "porto_novo") -> WorldState:
    """Create a fresh game world with initial market prices computed."""
    ports = copy.deepcopy(PORTS)
    routes = list(ROUTES)

    # Starting ship
    sloop = SHIPS["coastal_sloop"]
    ship = create_ship_from_template(sloop)

    captain = Captain(
        name=captain_name,
        silver=500,
        ship=ship,
        provisions=30,
    )

    world = WorldState(
        captain=captain,
        ports=ports,
        routes=routes,
        voyage=VoyageState(
            origin_id=starting_port,
            destination_id=starting_port,
            distance=0,
            status=VoyageStatus.IN_PORT,
        ),
        day=1,
        seed=int(time.time()),
    )

    # Compute initial prices
    for port in world.ports.values():
        recalculate_prices(port, GOODS)

    return world
