"""Phase 1 route network — connections between ports.

Distance determines travel time (distance / ship.speed = days).
Danger scales hostile event probability.

Route design:
  - Mediterranean ports are well-connected (short, safe)
  - West Africa is reachable from Mediterranean (medium distance)
  - East Indies require longer voyages (high reward, high risk)
  - Crosswind Isle is the hub connecting regions
"""

from portlight.engine.models import Route

ROUTES: list[Route] = [
    # === Mediterranean internal ===
    Route("porto_novo",     "al_manar",        distance=24,  danger=0.08),
    Route("porto_novo",     "silva_bay",       distance=16,  danger=0.05),
    Route("al_manar",       "silva_bay",       distance=20,  danger=0.07),

    # === Mediterranean → West Africa ===
    Route("porto_novo",     "sun_harbor",      distance=40,  danger=0.12),
    Route("al_manar",       "sun_harbor",      distance=48,  danger=0.15),
    Route("silva_bay",      "palm_cove",       distance=44,  danger=0.13),

    # === West Africa internal ===
    Route("sun_harbor",     "palm_cove",       distance=20,  danger=0.10),
    Route("sun_harbor",     "iron_point",      distance=18,  danger=0.09),
    Route("palm_cove",      "iron_point",      distance=22,  danger=0.11),

    # === West Africa → East Indies (long haul) ===
    Route("sun_harbor",     "crosswind_isle",  distance=64,  danger=0.18),
    Route("iron_point",     "crosswind_isle",  distance=60,  danger=0.16),

    # === East Indies internal ===
    Route("crosswind_isle", "jade_port",       distance=28,  danger=0.10),
    Route("crosswind_isle", "monsoon_reach",   distance=24,  danger=0.09),
    Route("crosswind_isle", "silk_haven",      distance=32,  danger=0.12),
    Route("jade_port",      "monsoon_reach",   distance=20,  danger=0.08),
    Route("jade_port",      "silk_haven",      distance=18,  danger=0.07),
    Route("monsoon_reach",  "silk_haven",      distance=22,  danger=0.10),

    # === Mediterranean → East Indies (dangerous shortcuts) ===
    Route("al_manar",       "monsoon_reach",   distance=72,  danger=0.22),
]
