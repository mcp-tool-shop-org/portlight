"""Core data models for Portlight.

Every game-state object is a plain dataclass. No ORM, no framework magic.
The engine operates on these; the app renders them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ---------------------------------------------------------------------------
# Goods
# ---------------------------------------------------------------------------

class GoodCategory(str, Enum):
    """Broad good classification — affects event interactions."""
    COMMODITY = "commodity"      # grain, timber, iron
    LUXURY = "luxury"           # silk, spice, porcelain
    PROVISION = "provision"     # food, water, rum
    CONTRABAND = "contraband"   # opium, black powder


@dataclass
class Good:
    """Static definition of a tradeable good."""
    id: str                          # e.g. "grain", "silk"
    name: str
    category: GoodCategory
    base_price: int                  # reference price (silver)
    weight_per_unit: float = 1.0     # cargo hold units per qty


# ---------------------------------------------------------------------------
# Market slot (per-port, per-good)
# ---------------------------------------------------------------------------

@dataclass
class MarketSlot:
    """One good's market state at one port. Mutated by the economy engine."""
    good_id: str
    stock_current: int
    stock_target: int
    restock_rate: float              # units restored per day toward target
    local_affinity: float = 1.0      # >1 = port produces, <1 = port consumes
    spread: float = 0.15             # buy/sell spread fraction (prevents round-trip)
    buy_price: int = 0               # computed by economy engine
    sell_price: int = 0              # computed by economy engine


# ---------------------------------------------------------------------------
# Ports
# ---------------------------------------------------------------------------

class PortFeature(str, Enum):
    """Special port capabilities."""
    SHIPYARD = "shipyard"
    BLACK_MARKET = "black_market"
    SAFE_HARBOR = "safe_harbor"


@dataclass
class Port:
    """Static port definition + mutable market state."""
    id: str                          # e.g. "porto_novo"
    name: str
    description: str
    region: str                      # flavor grouping
    features: list[PortFeature] = field(default_factory=list)
    market: list[MarketSlot] = field(default_factory=list)
    port_fee: int = 5                # fixed docking cost


# ---------------------------------------------------------------------------
# Ships
# ---------------------------------------------------------------------------

class ShipClass(str, Enum):
    """Ship tier — determines upgrade path."""
    SLOOP = "sloop"
    BRIGANTINE = "brigantine"
    GALLEON = "galleon"


@dataclass
class ShipTemplate:
    """Static ship blueprint. Players buy from shipyards."""
    id: str
    name: str
    ship_class: ShipClass
    cargo_capacity: int              # max cargo weight units
    speed: float                     # distance per day
    hull_max: int                    # hit points
    crew_min: int                    # minimum crew to sail
    crew_max: int                    # optimal crew
    price: int                       # purchase cost in silver


@dataclass
class Ship:
    """Player's active ship instance."""
    template_id: str
    name: str
    hull: int                        # current HP
    hull_max: int
    cargo_capacity: int
    speed: float
    crew: int
    crew_max: int


# ---------------------------------------------------------------------------
# Captain (player state)
# ---------------------------------------------------------------------------

@dataclass
class CargoItem:
    """One stack of goods in the hold."""
    good_id: str
    quantity: int
    cost_basis: int = 0              # total purchase cost (for P&L tracking)


@dataclass
class Captain:
    """The player character."""
    name: str = "Captain"
    silver: int = 500                # starting capital
    reputation: int = 0              # earned through trades
    ship: Ship | None = None
    cargo: list[CargoItem] = field(default_factory=list)
    provisions: int = 30             # days of food/water
    day: int = 1                     # current game day


# ---------------------------------------------------------------------------
# Voyage
# ---------------------------------------------------------------------------

class VoyageStatus(str, Enum):
    IN_PORT = "in_port"
    AT_SEA = "at_sea"
    ARRIVED = "arrived"


@dataclass
class VoyageState:
    """Tracks an active voyage between two ports."""
    origin_id: str
    destination_id: str
    distance: int                    # total distance units
    progress: int = 0                # distance covered so far
    days_elapsed: int = 0
    status: VoyageStatus = VoyageStatus.IN_PORT


# ---------------------------------------------------------------------------
# Route map
# ---------------------------------------------------------------------------

@dataclass
class Route:
    """A navigable connection between two ports."""
    port_a: str
    port_b: str
    distance: int
    danger: float = 0.1             # base event probability per day


# ---------------------------------------------------------------------------
# World state (top-level game state)
# ---------------------------------------------------------------------------

@dataclass
class WorldState:
    """Complete game state — serialized for save/load."""
    captain: Captain = field(default_factory=Captain)
    ports: dict[str, Port] = field(default_factory=dict)
    routes: list[Route] = field(default_factory=list)
    voyage: VoyageState | None = None
    day: int = 1
    seed: int = 0                    # RNG seed for reproducibility
