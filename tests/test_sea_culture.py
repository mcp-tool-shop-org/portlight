"""Tests for sea culture — route encounters, region defaults."""

from portlight.content.routes import ROUTES
from portlight.content.sea_culture import (
    REGION_ENCOUNTERS,
    ROUTE_ENCOUNTERS,
    get_region_encounters,
    get_route_encounters,
)


class TestRouteEncounters:
    """All named routes must have encounter tables."""

    def test_all_named_routes_have_encounters(self):
        named = [r for r in ROUTES if r.lore_name]
        for route in named:
            table = get_route_encounters(route.lore_name)
            assert table is not None, f"Missing encounters for '{route.lore_name}'"

    def test_encounter_tables_not_empty(self):
        for name, table in ROUTE_ENCOUNTERS.items():
            assert len(table.encounters) >= 3, f"'{name}' needs >= 3 encounters, has {len(table.encounters)}"

    def test_encounters_have_text(self):
        for name, table in ROUTE_ENCOUNTERS.items():
            for enc in table.encounters:
                assert enc.text, f"Empty text in '{name}'"
                assert enc.category, f"Empty category in '{name}'"

    def test_encounter_categories_valid(self):
        valid = {"sighting", "lore", "weather", "crew", "encounter"}
        for name, table in ROUTE_ENCOUNTERS.items():
            for enc in table.encounters:
                assert enc.category in valid, f"Invalid category '{enc.category}' in '{name}'"

    def test_fifteen_named_routes(self):
        assert len(ROUTE_ENCOUNTERS) == 15


class TestRegionEncounters:
    """All 5 regions must have default encounters."""

    REGIONS = ["Mediterranean", "North Atlantic", "West Africa", "East Indies", "South Seas"]

    def test_all_regions_have_encounters(self):
        for region in self.REGIONS:
            table = get_region_encounters(region)
            assert table is not None, f"Missing region encounters for '{region}'"

    def test_region_tables_not_empty(self):
        for name, table in REGION_ENCOUNTERS.items():
            assert len(table.encounters) >= 3, f"'{name}' needs >= 3 encounters"

    def test_five_regions(self):
        assert len(REGION_ENCOUNTERS) == 5


class TestEncounterVariety:
    """Each route should have multiple encounter categories."""

    def test_long_routes_have_mixed_categories(self):
        """Routes with 5+ encounters should span multiple categories."""
        for name, table in ROUTE_ENCOUNTERS.items():
            if len(table.encounters) >= 5:
                cats = {e.category for e in table.encounters}
                assert len(cats) >= 3, f"'{name}' has {len(table.encounters)} encounters but only {len(cats)} categories"
