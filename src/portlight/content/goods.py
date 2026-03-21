"""Expanded goods catalog — 14 tradeable goods across 6 categories.

Phase 1: 8 goods (grain, timber, iron, cotton, spice, silk, rum, porcelain)
Phase 2: +6 goods (tea, tobacco, dyes, pearls, weapons, medicines)

New goods create deeper trade triangles:
  - Tea/tobacco: mid-tier luxuries, more accessible than silk/spice
  - Dyes: commodity that bridges West Africa → Mediterranean textile trade
  - Pearls: ultra-luxury, rare, high-risk high-reward
  - Weapons: military category, restricted at some ports, high margins
  - Medicines: medicine category, universally needed, moderate margins
"""

from portlight.engine.models import Good, GoodCategory

GOODS: dict[str, Good] = {g.id: g for g in [
    # === Commodities ===
    Good("grain",     "Grain",         GoodCategory.COMMODITY,  base_price=12),
    Good("timber",    "Timber",        GoodCategory.COMMODITY,  base_price=18),
    Good("iron",      "Iron Ore",      GoodCategory.COMMODITY,  base_price=25),
    Good("cotton",    "Cotton",        GoodCategory.COMMODITY,  base_price=15),
    Good("dyes",      "Dyes",          GoodCategory.COMMODITY,  base_price=22),

    # === Luxuries ===
    Good("spice",     "Spice",         GoodCategory.LUXURY,     base_price=55),
    Good("silk",      "Silk",          GoodCategory.LUXURY,     base_price=70),
    Good("porcelain", "Porcelain",     GoodCategory.LUXURY,     base_price=60),
    Good("tea",       "Tea",           GoodCategory.LUXURY,     base_price=40),
    Good("pearls",    "Pearls",        GoodCategory.LUXURY,     base_price=95),

    # === Provisions ===
    Good("rum",       "Rum",           GoodCategory.PROVISION,  base_price=20),
    Good("tobacco",   "Tobacco",       GoodCategory.PROVISION,  base_price=28),

    # === Military ===
    Good("weapons",   "Weapons",       GoodCategory.MILITARY,   base_price=45),

    # === Medicine ===
    Good("medicines", "Medicines",     GoodCategory.MEDICINE,   base_price=35),
]}
