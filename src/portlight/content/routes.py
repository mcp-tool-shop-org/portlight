"""Phase 2 route network - connections between ports with ship class requirements.

Route design creates three archetype tiers:
  Tier 1 (Sloop): Mediterranean internal. Short, safe, low margins.
  Tier 2 (Brigantine): Mediterranean-West Africa and W.Africa internal.
    Medium distance, moderate risk. Bulk commodity routes become viable.
  Tier 3 (Galleon): Long-haul East Indies and cross-region shortcuts.
    High distance, high danger, but luxury margins justify the investment.

min_ship_class gates which routes are available. A sloop CAN attempt
a brigantine route but the voyage engine will warn about unsuitability
and apply a danger penalty. Galleon routes are hard-gated.
"""

from portlight.engine.models import Route

ROUTES: list[Route] = [
    # === Mediterranean internal (Sloop-safe) ===
    Route("porto_novo",     "al_manar",        distance=24,  danger=0.08,  min_ship_class="sloop"),
    Route("porto_novo",     "silva_bay",       distance=16,  danger=0.05,  min_ship_class="sloop"),
    Route("al_manar",       "silva_bay",       distance=20,  danger=0.07,  min_ship_class="sloop"),

    # === Mediterranean to West Africa (Brigantine recommended) ===
    Route("porto_novo",     "sun_harbor",      distance=40,  danger=0.12,  min_ship_class="brigantine"),
    Route("al_manar",       "sun_harbor",      distance=48,  danger=0.15,  min_ship_class="brigantine"),
    Route("silva_bay",      "palm_cove",       distance=44,  danger=0.13,  min_ship_class="brigantine"),

    # === West Africa internal (Brigantine recommended) ===
    Route("sun_harbor",     "palm_cove",       distance=20,  danger=0.10,  min_ship_class="sloop"),
    Route("sun_harbor",     "iron_point",      distance=18,  danger=0.09,  min_ship_class="sloop"),
    Route("palm_cove",      "iron_point",      distance=22,  danger=0.11,  min_ship_class="sloop"),

    # === West Africa to East Indies (Galleon-class voyages) ===
    Route("sun_harbor",     "crosswind_isle",  distance=64,  danger=0.18,  min_ship_class="galleon"),
    Route("iron_point",     "crosswind_isle",  distance=60,  danger=0.16,  min_ship_class="brigantine"),

    # === East Indies internal (Brigantine minimum) ===
    Route("crosswind_isle", "jade_port",       distance=28,  danger=0.10,  min_ship_class="brigantine"),
    Route("crosswind_isle", "monsoon_reach",   distance=24,  danger=0.09,  min_ship_class="brigantine"),
    Route("crosswind_isle", "silk_haven",      distance=32,  danger=0.12,  min_ship_class="brigantine"),
    Route("jade_port",      "monsoon_reach",   distance=20,  danger=0.08,  min_ship_class="brigantine"),
    Route("jade_port",      "silk_haven",      distance=18,  danger=0.07,  min_ship_class="brigantine"),
    Route("monsoon_reach",  "silk_haven",      distance=22,  danger=0.10,  min_ship_class="brigantine"),

    # === Dangerous long-haul shortcuts (Galleon only) ===
    Route("al_manar",       "monsoon_reach",   distance=72,  danger=0.22,  min_ship_class="galleon"),
]
