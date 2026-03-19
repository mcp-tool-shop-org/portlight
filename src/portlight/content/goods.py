"""Phase 1 goods catalog — 8 tradeable goods."""

from portlight.engine.models import Good, GoodCategory

GOODS: dict[str, Good] = {g.id: g for g in [
    Good("grain",     "Grain",         GoodCategory.COMMODITY,  base_price=12),
    Good("timber",    "Timber",        GoodCategory.COMMODITY,  base_price=18),
    Good("iron",      "Iron Ore",      GoodCategory.COMMODITY,  base_price=25),
    Good("cotton",    "Cotton",        GoodCategory.COMMODITY,  base_price=15),
    Good("spice",     "Spice",         GoodCategory.LUXURY,     base_price=55),
    Good("silk",      "Silk",          GoodCategory.LUXURY,     base_price=70),
    Good("rum",       "Rum",           GoodCategory.PROVISION,  base_price=20),
    Good("porcelain", "Porcelain",     GoodCategory.LUXURY,     base_price=60),
]}
