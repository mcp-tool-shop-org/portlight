"""Core data models for Portlight.

Every game-state object is a plain dataclass. No ORM, no framework magic.
The engine operates on these; the app renders them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


# ---------------------------------------------------------------------------
# Goods
# ---------------------------------------------------------------------------

class GoodCategory(str, Enum):
    """Broad good classification — affects event interactions."""
    COMMODITY = "commodity"      # grain, timber, iron, cotton, dyes
    LUXURY = "luxury"           # silk, spice, porcelain, pearls, tea
    PROVISION = "provision"     # food, water, rum, tobacco
    CONTRABAND = "contraband"   # opium, black powder
    MILITARY = "military"       # weapons, gunpowder
    MEDICINE = "medicine"       # medicines, herbs


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
    flood_penalty: float = 0.0       # 0-1, rises when player dumps repeatedly, decays over time


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
    provision_cost: int = 2          # silver per day of provisions
    repair_cost: int = 3             # silver per hull point
    crew_cost: int = 5               # silver per crew hire
    map_x: int = 0                   # abstract map x coordinate
    map_y: int = 0                   # abstract map y coordinate


# ---------------------------------------------------------------------------
# Ships
# ---------------------------------------------------------------------------

class ShipClass(str, Enum):
    """Ship tier — determines upgrade path."""
    SLOOP = "sloop"
    CUTTER = "cutter"
    BRIGANTINE = "brigantine"
    GALLEON = "galleon"
    MAN_OF_WAR = "man_of_war"


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
    daily_wage: int = 1              # silver per crew per day at sea
    storm_resist: float = 0.0        # fraction of storm damage absorbed (0-1)


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
# Reputation (multi-axis access model)
# ---------------------------------------------------------------------------

@dataclass
class ReputationIncident:
    """One recorded reputation-affecting event."""
    day: int
    port_id: str
    region: str
    incident_type: str       # "trade", "inspection", "seizure", "arrival", "contract"
    description: str
    heat_delta: int = 0
    standing_delta: int = 0
    trust_delta: int = 0


@dataclass
class ReputationState:
    """Tracks the player's standing across regions, ports, and institutions.

    This is not a single number. It's a topology that opens and closes doors.
    """
    # Regional standing (how established you are in each region)
    regional_standing: dict[str, int] = field(default_factory=lambda: {
        "Mediterranean": 0, "North Atlantic": 0, "West Africa": 0,
        "East Indies": 0, "South Seas": 0,
    })
    # Port-specific standing (major ports only, affects local services)
    port_standing: dict[str, int] = field(default_factory=dict)
    # Customs heat (anti-abuse pressure, rises from suspicious behavior)
    customs_heat: dict[str, int] = field(default_factory=lambda: {
        "Mediterranean": 0, "North Atlantic": 0, "West Africa": 0,
        "East Indies": 0, "South Seas": 0,
    })
    # Commercial trust (does the market believe you can deliver?)
    commercial_trust: int = 0
    # Recent incidents (capped at 20, newest first)
    recent_incidents: list[ReputationIncident] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Captain (player state)
# ---------------------------------------------------------------------------

@dataclass
class CargoItem:
    """One stack of goods in the hold with provenance tracking."""
    good_id: str
    quantity: int
    cost_basis: int = 0              # total purchase cost (for P&L tracking)
    acquired_port: str = ""          # port where this cargo was bought
    acquired_region: str = ""        # region where acquired
    acquired_day: int = 0            # game day of acquisition


@dataclass
class Captain:
    """The player character."""
    name: str = "Captain"
    captain_type: str = "merchant"   # CaptainType value string
    silver: int = 500                # starting capital
    reputation: int = 0              # legacy field (kept for compat)
    ship: Ship | None = None
    cargo: list[CargoItem] = field(default_factory=list)
    provisions: int = 30             # days of food/water
    day: int = 1                     # current game day
    standing: ReputationState = field(default_factory=ReputationState)


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
    min_ship_class: str = "sloop"   # minimum ship class to attempt this route
    lore_name: str = ""             # named trade route (e.g. "The Grain Road")
    lore: str = ""                  # historical flavor text


# ---------------------------------------------------------------------------
# World state (top-level game state)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Culture (static reference data + mutable festival state)
# ---------------------------------------------------------------------------

@dataclass
class Festival:
    """A recurring cultural event that affects port economics."""
    id: str
    name: str
    description: str
    region: str
    frequency_days: int              # roughly how often (stochastic trigger)
    market_effects: dict[str, float] = field(default_factory=dict)  # good_id → demand mult
    duration_days: int = 3
    standing_bonus: int = 0          # bonus standing for trading during festival


@dataclass
class RegionCulture:
    """Cultural identity of a trade region — static reference data."""
    id: str                          # "mediterranean", "north_atlantic", etc.
    region_name: str                 # canonical: "Mediterranean"
    cultural_name: str               # flavor: "The Middle Sea"
    ethos: str                       # 1-2 sentence cultural philosophy
    trade_philosophy: str            # how this culture views commerce
    sacred_goods: list[str] = field(default_factory=list)    # culturally revered
    forbidden_goods: list[str] = field(default_factory=list) # taboo/restricted
    prized_goods: list[str] = field(default_factory=list)    # socially valued
    greeting: str = ""               # merchant greeting on arrival
    farewell: str = ""               # parting words
    proverb: str = ""                # trade proverb
    festivals: list[Festival] = field(default_factory=list)
    weather_flavor: list[str] = field(default_factory=list)  # atmospheric text


@dataclass
class PortCulture:
    """Cultural flavor for a specific port — static reference data."""
    port_id: str
    landmark: str                    # a named cultural landmark
    local_custom: str                # a custom that colors trade here
    atmosphere: str                  # sensory: what it feels/smells/sounds like
    dock_scene: str                  # what you see when you arrive
    tavern_rumor: str                # a rumor you overhear
    cultural_group: str = ""         # local faction/guild name
    cultural_group_description: str = ""


@dataclass
class ActiveFestival:
    """A festival currently in progress."""
    festival_id: str
    port_id: str
    start_day: int
    end_day: int


@dataclass
class CulturalState:
    """Tracks cultural engagement — persisted in save files."""
    active_festivals: list[ActiveFestival] = field(default_factory=list)
    regions_entered: list[str] = field(default_factory=list)
    cultural_encounters: int = 0
    port_visits: dict[str, int] = field(default_factory=dict)  # port_id → count


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
    culture: CulturalState = field(default_factory=CulturalState)
