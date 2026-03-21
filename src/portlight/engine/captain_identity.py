"""Captain identity system — three archetypes that reshape commercial behavior.

Each captain type changes:
  - pricing (buy/sell modifiers, luxury handling)
  - voyage (provision burn, speed, storm resilience, inspection profile)
  - reputation (trust growth, heat growth, starting standing)
  - contracts (bias toward certain contract families)

These are not passive +5% perks. They change route choice, capital timing,
risk profile, and viable trade styles from the opening hours.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class CaptainType(str, Enum):
    """The three merchant archetypes."""
    MERCHANT = "merchant"
    SMUGGLER = "smuggler"
    NAVIGATOR = "navigator"


@dataclass(frozen=True)
class PricingModifiers:
    """How this captain affects market prices."""
    buy_price_mult: float = 1.0       # < 1 = cheaper buys
    sell_price_mult: float = 1.0      # > 1 = better sells
    luxury_sell_bonus: float = 0.0    # extra sell multiplier for luxury goods
    port_fee_mult: float = 1.0       # multiplier on port docking fees


@dataclass(frozen=True)
class VoyageModifiers:
    """How this captain affects life at sea."""
    provision_burn: float = 1.0       # daily provision consumption rate
    speed_bonus: float = 0.0          # flat addition to ship speed
    storm_resist_bonus: float = 0.0   # added to ship's storm_resist
    cargo_damage_mult: float = 1.0    # multiplier on cargo damage qty


@dataclass(frozen=True)
class InspectionProfile:
    """How authorities treat this captain."""
    inspection_chance_mult: float = 1.0   # multiplier on inspection event weight
    seizure_risk: float = 0.0             # base chance of cargo seizure during inspection
    fine_mult: float = 1.0               # multiplier on inspection fines


@dataclass(frozen=True)
class ReputationSeed:
    """Starting reputation values for this archetype."""
    commercial_trust: int = 0
    customs_heat: int = 0
    # Per-region starting standing
    mediterranean: int = 0
    west_africa: int = 0
    east_indies: int = 0


@dataclass(frozen=True)
class CaptainTemplate:
    """Full archetype definition. Immutable reference data."""
    id: CaptainType
    name: str
    title: str                           # e.g. "Licensed Merchant"
    description: str
    home_region: str
    home_port_id: str
    starting_silver: int
    starting_ship_id: str
    starting_provisions: int
    pricing: PricingModifiers = field(default_factory=PricingModifiers)
    voyage: VoyageModifiers = field(default_factory=VoyageModifiers)
    inspection: InspectionProfile = field(default_factory=InspectionProfile)
    reputation_seed: ReputationSeed = field(default_factory=ReputationSeed)
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# The three captains
# ---------------------------------------------------------------------------

CAPTAIN_TEMPLATES: dict[CaptainType, CaptainTemplate] = {
    CaptainType.MERCHANT: CaptainTemplate(
        id=CaptainType.MERCHANT,
        name="The Merchant",
        title="Licensed Trader",
        description=(
            "A legitimate operator with standing in the major ports. "
            "Your licenses open doors, your reputation keeps them open. "
            "Steady commerce and reliable delivery are your weapons."
        ),
        home_region="Mediterranean",
        home_port_id="porto_novo",
        starting_silver=550,             # slightly more capital
        starting_ship_id="coastal_sloop",
        starting_provisions=30,
        pricing=PricingModifiers(
            buy_price_mult=0.92,         # 8% cheaper buys (trusted buyer)
            sell_price_mult=1.05,        # 5% better sells (known supplier)
            luxury_sell_bonus=0.0,       # no special luxury edge
            port_fee_mult=0.7,           # 30% cheaper port fees (licensed)
        ),
        voyage=VoyageModifiers(
            provision_burn=1.0,          # normal consumption
            speed_bonus=0.0,             # no speed edge
            storm_resist_bonus=0.0,      # no storm edge
            cargo_damage_mult=1.0,       # normal cargo risk
        ),
        inspection=InspectionProfile(
            inspection_chance_mult=0.5,  # 50% fewer inspections (known trader)
            seizure_risk=0.0,            # clean record
            fine_mult=0.6,               # lower fines (good standing)
        ),
        reputation_seed=ReputationSeed(
            commercial_trust=15,         # starts with trust
            customs_heat=0,
            mediterranean=10,            # known in home region
            west_africa=0,
            east_indies=0,
        ),
        strengths=[
            "Better buy/sell prices at all ports",
            "Cheaper port fees (licensed operator)",
            "Fewer inspections, lower fines",
            "Starts with commercial trust and Med standing",
        ],
        weaknesses=[
            "No voyage advantages",
            "No luxury trade edge",
            "Must build reputation the hard way in distant regions",
        ],
    ),

    CaptainType.SMUGGLER: CaptainTemplate(
        id=CaptainType.SMUGGLER,
        name="The Smuggler",
        title="Shadow Trader",
        description=(
            "You trade where others won't and sell what others can't. "
            "Luxury margins are your bread and butter, but the law is always "
            "one bad inspection away. High risk, high reward."
        ),
        home_region="West Africa",
        home_port_id="palm_cove",        # remote, low scrutiny
        starting_silver=475,             # less starting capital, but resourceful
        starting_ship_id="coastal_sloop",
        starting_provisions=35,          # knows how to stock up
        pricing=PricingModifiers(
            buy_price_mult=1.0,          # no general buy edge
            sell_price_mult=0.97,        # 3% worse on staples (no network)
            luxury_sell_bonus=0.25,      # 25% bonus selling luxury goods
            port_fee_mult=1.0,           # normal port fees
        ),
        voyage=VoyageModifiers(
            provision_burn=0.9,          # 10% less provision use (resourceful)
            speed_bonus=0.0,
            storm_resist_bonus=0.0,
            cargo_damage_mult=0.8,       # 20% less cargo damage (careful packer)
        ),
        inspection=InspectionProfile(
            inspection_chance_mult=1.5,  # 50% more inspections (suspicious profile)
            seizure_risk=0.07,           # 7% chance of cargo seizure on inspection
            fine_mult=1.3,               # higher fines (no goodwill)
        ),
        reputation_seed=ReputationSeed(
            commercial_trust=0,          # no trust
            customs_heat=10,             # starts with some heat
            mediterranean=0,
            west_africa=5,               # knows the coast
            east_indies=0,
        ),
        strengths=[
            "25% bonus selling luxury goods (silk, spice, porcelain)",
            "Less provision burn and cargo damage at sea",
            "Extra provisions at start",
            "Thrives on volatile markets and shortages",
        ],
        weaknesses=[
            "50% more inspections, higher fines",
            "7% chance of cargo seizure during inspection",
            "Slightly worse sell prices on staple goods",
            "Starts with customs heat, no commercial trust",
        ],
    ),

    CaptainType.NAVIGATOR: CaptainTemplate(
        id=CaptainType.NAVIGATOR,
        name="The Navigator",
        title="Route Specialist",
        description=(
            "You read the winds better than anyone and your crew trusts your charts. "
            "Long hauls that break other captains are your bread run. "
            "Distant markets open to you before anyone else can reach them."
        ),
        home_region="Mediterranean",
        home_port_id="silva_bay",        # shipyard port, timber-rich
        starting_silver=450,
        starting_ship_id="coastal_sloop",
        starting_provisions=30,
        pricing=PricingModifiers(
            buy_price_mult=1.05,         # 5% more expensive buys (not a negotiator)
            sell_price_mult=1.0,         # normal sell prices
            luxury_sell_bonus=0.0,
            port_fee_mult=1.0,
        ),
        voyage=VoyageModifiers(
            provision_burn=0.7,          # 30% less provision use (efficient routing)
            speed_bonus=1.5,             # +1.5 flat speed (reads the winds)
            storm_resist_bonus=0.15,     # 15% extra storm resistance
            cargo_damage_mult=0.7,       # 30% less cargo damage (good stowage)
        ),
        inspection=InspectionProfile(
            inspection_chance_mult=1.0,
            seizure_risk=0.0,
            fine_mult=1.0,
        ),
        reputation_seed=ReputationSeed(
            commercial_trust=5,
            customs_heat=0,
            mediterranean=5,
            west_africa=0,
            east_indies=5,              # has sailed there before
        ),
        strengths=[
            "30% less provision consumption at sea",
            "+1.5 speed bonus (faster voyages)",
            "Extra storm resistance and less cargo damage",
            "Starting familiarity with East Indies",
        ],
        weaknesses=[
            "5% more expensive buys (worse negotiator)",
            "No special sell price advantages",
            "Slower commercial reputation growth in settled markets",
        ],
    ),
}


def get_captain_template(captain_type: CaptainType) -> CaptainTemplate:
    """Get template for a captain type. Raises KeyError if unknown."""
    return CAPTAIN_TEMPLATES[captain_type]


# ---------------------------------------------------------------------------
# Authoritative effects reference — all captain identity modifiers in one place
# ---------------------------------------------------------------------------
# Scattered across: economy.py (pricing), voyage.py (voyage mods),
# reputation.py (inspection/trust), captain_identity.py (templates).
# This index exists so there's ONE place to audit what each type does.

CAPTAIN_EFFECTS_REFERENCE: dict[str, dict[str, str]] = {
    "merchant": {
        "buy_price_mult": "0.92 (8% cheaper buys)",
        "sell_price_mult": "1.05 (5% better sells)",
        "port_fee_mult": "0.7 (30% cheaper port fees)",
        "inspection_chance_mult": "0.5 (50% fewer inspections)",
        "fine_mult": "0.6 (lower fines)",
        "trust_bonus": "+1 extra trust on clean profitable trades (reputation.py:191)",
        "starting_trust": "15",
        "starting_med_standing": "10",
    },
    "smuggler": {
        "luxury_sell_bonus": "0.25 (25% bonus on luxury goods)",
        "sell_price_mult": "0.97 (3% worse on staples)",
        "provision_burn": "0.9 (10% less provisions)",
        "cargo_damage_mult": "0.8 (20% less cargo damage)",
        "inspection_chance_mult": "1.5 (50% more inspections)",
        "seizure_risk": "0.07 (7% cargo seizure chance per inspection)",
        "fine_mult": "1.3 (higher fines)",
        "contraband_detect_bonus": "-0.15 detection chance (voyage.py:208)",
        "suspicion_bonus": "+1 suspicion on sells (reputation.py:127)",
        "starting_heat": "10",
    },
    "navigator": {
        "buy_price_mult": "1.05 (5% more expensive buys)",
        "provision_burn": "0.7 (30% less provision use)",
        "speed_bonus": "+1.5 flat speed",
        "storm_resist_bonus": "+0.15 storm resistance",
        "cargo_damage_mult": "0.7 (30% less cargo damage)",
        "starting_ei_standing": "5 (East Indies familiarity)",
    },
}
