"""Main PDF generator for the Portlight Print-and-Play kit.

Orchestrates all components: cover, rulebook, board, cards, tracks.
Pulls content from Portlight's structured dataclasses.
"""

from __future__ import annotations

from pathlib import Path

from portlight.printandplay.assets import (
    CARD_GAP,
    CARD_H,
    CARD_W,
    CARDS_PER_ROW,
    COMPACT_CARD_H,
    FONT_HEADING,
    INK,
    MARGIN,
    SHIP_TABLETOP,
    CAPTAIN_TABLETOP,
    tabletop_price,
)


def generate(output: Path | None = None) -> Path:
    """Generate the complete Print-and-Play PDF kit.

    Returns the path to the generated PDF.
    """
    try:
        from fpdf import FPDF
    except ImportError:
        raise RuntimeError(
            "fpdf2 is required for PDF generation. "
            "Install it with: pip install portlight[printandplay]"
        )

    from portlight.content.goods import GOODS
    from portlight.content.ports import PORTS
    from portlight.content.routes import ROUTES
    from portlight.content.ships import SHIPS
    from portlight.content.contracts import TEMPLATES

    from portlight.printandplay.board import draw_board
    from portlight.printandplay.cards import (
        draw_captain_card,
        draw_contract_card,
        draw_event_card,
        draw_goods_card,
        draw_port_card,
        draw_season_card,
        draw_ship_card,
    )
    from portlight.printandplay.rules import (
        render_cover,
        render_player_aid,
        render_rules,
        render_score_tracks,
    )

    pdf = FPDF(unit="mm", format="Letter")
    # Flow pages (cover/rules) may auto-break; card sheets use absolute placement.
    pdf.set_auto_page_break(auto=True, margin=MARGIN)

    # --- Cover ---
    render_cover(pdf)

    # --- Rulebook ---
    render_rules(pdf)

    # --- Game Board (landscape) ---
    draw_board(pdf, PORTS, ROUTES)

    # Restore portrait and disable auto-break: cards are placed at absolute (x, y)
    # against the *current* page height. Leaving landscape + auto-break True
    # explodes the kit into dozens of near-blank sheets.
    pdf.set_auto_page_break(auto=False)
    pdf.add_page(orientation="P")

    # --- Captain Cards ---
    _add_section_header(pdf, "CAPTAIN CARDS", row_h=CARD_H)
    col = 0
    row_y = _ensure_card_row(pdf, pdf.get_y(), CARD_H)
    for cap_id, cap in CAPTAIN_TABLETOP.items():
        col, row_y = _next_card_cell(pdf, col, row_y, CARD_H)
        x = MARGIN + col * (CARD_W + CARD_GAP)
        draw_captain_card(
            pdf, x, row_y,
            name=cap["name"],
            home_port=cap["home_port"],
            silver=cap["silver"],
            provisions=cap["provisions"],
            heat=cap["heat"],
            ability=cap["ability"],
            weakness=cap["weakness"],
        )
        col += 1
    pdf.set_y(row_y + CARD_H + CARD_GAP)

    # --- Ship Cards ---
    _add_section_header(pdf, "SHIP CARDS", row_h=CARD_H)
    col = 0
    row_y = _ensure_card_row(pdf, pdf.get_y(), CARD_H)
    for ship_id, ship in SHIPS.items():
        col, row_y = _next_card_cell(pdf, col, row_y, CARD_H)
        x = MARGIN + col * (CARD_W + CARD_GAP)
        stats = SHIP_TABLETOP.get(ship_id, {
            "cargo": 5, "speed": 4, "hull": 6, "crew_cost": 0, "price": 0, "cannons": 0,
        })
        draw_ship_card(pdf, x, row_y, ship.name, ship.ship_class.value, stats)
        col += 1
    pdf.set_y(row_y + CARD_H + CARD_GAP)

    # --- Goods Cards (3 copies each) ---
    _add_section_header(pdf, "GOODS CARDS", row_h=CARD_H)
    col = 0
    row_y = _ensure_card_row(pdf, pdf.get_y(), CARD_H)
    for good_id, good in GOODS.items():
        if good_id == "pelts":
            continue  # Skip pelts (hunted, not traded as card)
        for _copy in range(3):
            col, row_y = _next_card_cell(pdf, col, row_y, CARD_H)
            x = MARGIN + col * (CARD_W + CARD_GAP)
            draw_goods_card(
                pdf, x, row_y,
                name=good.name,
                category=good.category.value,
                base_price=good.base_price,
                tabletop_price=tabletop_price(good.base_price),
            )
            col += 1
    pdf.set_y(row_y + CARD_H + CARD_GAP)

    # --- Contract Cards ---
    _add_section_header(pdf, "CONTRACT CARDS", row_h=CARD_H)
    col = 0
    row_y = _ensure_card_row(pdf, pdf.get_y(), CARD_H)
    for tmpl in TEMPLATES[:24]:  # Cap at 24 contracts
        col, row_y = _next_card_cell(pdf, col, row_y, CARD_H)
        x = MARGIN + col * (CARD_W + CARD_GAP)
        goods_name = tmpl.goods_pool[0].title() if tmpl.goods_pool else "Mixed"
        qty = f"{tmpl.quantity_min}-{tmpl.quantity_max}"
        reward = str(round(tmpl.reward_per_unit * (tmpl.quantity_min + tmpl.quantity_max) / 2 / 5))
        deadline = str(max(2, round(tmpl.deadline_days / 8)))
        flavor = getattr(tmpl, "cultural_flavor", "") or ""
        draw_contract_card(
            pdf, x, row_y,
            title=tmpl.title_pattern.replace("{destination}", "Dest"),
            goods=goods_name,
            qty_range=qty,
            reward=reward,
            deadline=deadline,
            trust=tmpl.trust_requirement,
            flavor=flavor,
        )
        col += 1
    pdf.set_y(row_y + CARD_H + CARD_GAP)

    # --- Event Cards ---
    _add_section_header(pdf, "EVENT CARDS", row_h=CARD_H)
    events = _build_event_deck()
    col = 0
    row_y = _ensure_card_row(pdf, pdf.get_y(), CARD_H)
    for evt in events:
        col, row_y = _next_card_cell(pdf, col, row_y, CARD_H)
        x = MARGIN + col * (CARD_W + CARD_GAP)
        draw_event_card(pdf, x, row_y, **evt)
        col += 1
    pdf.set_y(row_y + CARD_H + CARD_GAP)

    # --- Season Cards ---
    _add_section_header(pdf, "SEASON CARDS", row_h=CARD_H)
    seasons = [
        {"season": "Spring", "rounds": "1-3",
         "effects": ["Mediterranean routes -1 cost (min 1)", "Grain demand +2 silver", "Calm seas: fewer storm events"]},
        {"season": "Summer", "rounds": "4-6",
         "effects": ["East Indies routes +1 cost (monsoon)", "Spice demand +2 silver", "Pirate activity peaks"]},
        {"season": "Autumn", "rounds": "7-9",
         "effects": ["West Africa routes stable", "Cotton & Dyes demand +2 silver", "Harvest trade bonuses"]},
        {"season": "Winter", "rounds": "10-12",
         "effects": ["North Atlantic routes +1 cost (storms)", "Medicines demand +2 silver", "Storm events more frequent"]},
    ]
    col = 0
    row_y = _ensure_card_row(pdf, pdf.get_y(), CARD_H)
    for s in seasons:
        col, row_y = _next_card_cell(pdf, col, row_y, CARD_H)
        x = MARGIN + col * (CARD_W + CARD_GAP)
        draw_season_card(pdf, x, row_y, **s)
        col += 1
    pdf.set_y(row_y + CARD_H + CARD_GAP)

    # --- Port Reference Cards (compact) ---
    _add_section_header(pdf, "PORT REFERENCE CARDS", row_h=COMPACT_CARD_H)
    col = 0
    row_y = _ensure_card_row(pdf, pdf.get_y(), COMPACT_CARD_H)
    for pid, port in PORTS.items():
        col, row_y = _next_card_cell(pdf, col, row_y, COMPACT_CARD_H)
        x = MARGIN + col * (CARD_W + CARD_GAP)

        # Determine exports (high affinity) and imports (low affinity)
        exports = []
        imports = []
        for slot in port.market:
            if slot.local_affinity >= 1.3:
                exports.append(slot.good_id.title())
            elif slot.local_affinity <= 0.65:
                imports.append(slot.good_id.title())

        features = [f.value for f in port.features]
        draw_port_card(
            pdf, x, row_y,
            name=port.name,
            region=port.region,
            features=features,
            exports=exports,
            imports=imports,
            port_fee=port.port_fee,
        )
        col += 1
    pdf.set_y(row_y + COMPACT_CARD_H + CARD_GAP)

    # Flow pages again for the player aid and score tracks.
    pdf.set_auto_page_break(auto=True, margin=MARGIN)

    # --- Player Aid ---
    render_player_aid(pdf)

    # --- Score Tracks ---
    render_score_tracks(pdf)

    # --- Output ---
    if output is None:
        output = Path("portlight-print-and-play.pdf")
    pdf.output(str(output))
    return output


def _ensure_card_row(pdf, row_y: float, card_h: float) -> float:
    """Return a y that can hold one card row on the current (portrait) page."""
    if row_y + card_h > pdf.h - MARGIN:
        pdf.add_page(orientation="P")
        return MARGIN + 2
    return row_y


def _next_card_cell(pdf, col: int, row_y: float, card_h: float) -> tuple[int, float]:
    """Advance to the next grid cell, wrapping onto a new portrait page if needed."""
    if col < CARDS_PER_ROW:
        return col, row_y
    return 0, _ensure_card_row(pdf, row_y + card_h + CARD_GAP, card_h)


def _add_section_header(pdf, title: str, row_h: float = 0) -> None:
    """Add a section header, starting a new portrait page if needed.

    `row_h` reserves room so the header is not orphaned above a card row
    that would immediately wrap to the next sheet.
    """
    if pdf.get_y() > pdf.h - MARGIN - 30 - row_h:
        pdf.add_page(orientation="P")
    else:
        pdf.ln(4)
    pdf.set_font("Helvetica", "B", FONT_HEADING)
    pdf.set_text_color(*INK)
    pdf.cell(0, 8, title, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)


def _build_event_deck() -> list[dict]:
    """Build the ~40 card event deck."""
    events = []

    # Weather (10)
    weather = [
        ("Calm Seas", "+1 movement point this round."),
        ("Calm Seas", "+1 movement point this round."),
        ("Favorable Winds", "+2 movement points this round."),
        ("Favorable Winds", "+2 movement points this round."),
        ("Squall", "Lose 1 hull point. If hull at 0, ship wrecked."),
        ("Squall", "Lose 1 hull point. If hull at 0, ship wrecked."),
        ("Storm", "Lose 1 cargo card (your choice) OR 2 hull points."),
        ("Storm", "Lose 1 cargo card (your choice) OR 2 hull points."),
        ("Monsoon", "Your current route is blocked. Return to origin port. No movement cost refund."),
        ("Fog Bank", "No encounter this round. Skip to Resolution."),
    ]
    for title, effect in weather:
        events.append({"title": title, "category": "Weather", "effect": effect})

    # Pirates (8)
    pirates = [
        ("Pirate Attack!", "Pirate strength: 8. Fight (2d6 + cannons >= 8), Pay Tribute (5 silver), or Flee (2d6 >= 12 - speed)."),
        ("Pirate Attack!", "Pirate strength: 10. Fight (2d6 + cannons >= 10), Pay Tribute (8 silver), or Flee (2d6 >= 12 - speed)."),
        ("Pirate Attack!", "Pirate strength: 6. Fight (2d6 + cannons >= 6), Pay Tribute (3 silver), or Flee (2d6 >= 12 - speed)."),
        ("Pirate Blockade", "Pay 4 silver toll or reroute: add +1 to this route's movement cost."),
        ("Pirate Blockade", "Pay 6 silver toll or reroute: add +1 to this route's movement cost."),
        ("Black Market Offer", "A smuggler offers contraband at half price. Buy 1 contraband card for half its base price. Heat +1."),
        ("Pirate Parley", "A pirate captain offers a deal: deliver 1 good from your cargo to their port. If you accept, Heat -2 and gain 5 silver."),
        ("Pirate Raid", "Pirate strength: 12. Fight (2d6 + cannons >= 12), Pay Tribute (10 silver), or Flee (2d6 >= 12 - speed). Reward if won: 8 silver."),
    ]
    for title, effect in pirates:
        events.append({"title": title, "category": "Pirates", "effect": effect})

    # Inspections (6)
    inspections = [
        ("Customs Check", "Roll 2d6 - Heat (min 2). 7+ = passed. Below 7 = lose all contraband, Heat +2."),
        ("Customs Check", "Roll 2d6 - Heat (min 2). 7+ = passed. Below 7 = lose all contraband, Heat +2."),
        ("Customs Check", "Roll 2d6 - Heat (min 2). 7+ = passed. Below 7 = lose all contraband, Heat +2."),
        ("Harbor Patrol", "Heat +1. No other effect."),
        ("Diplomatic Immunity", "Heat -2 (min 0). A local official vouches for your cargo."),
        ("Strict Inspection", "Roll 2d6 - Heat - 1 (min 2). 7+ = passed. Below 7 = lose all contraband AND 1 luxury good, Heat +3."),
    ]
    for title, effect in inspections:
        events.append({"title": title, "category": "Inspection", "effect": effect})

    # Trade (8)
    trade = [
        ("Merchant Fleet", "Buy any 1 good from the nearest port's market at -2 silver discount (min 1)."),
        ("Merchant Fleet", "Buy any 1 good from the nearest port's market at -2 silver discount (min 1)."),
        ("Market Rumor", "Peek at the top 2 cards of the goods deck. Place one on any port's market display."),
        ("Market Rumor", "Peek at the top 2 cards of the goods deck. Place one on any port's market display."),
        ("Shortage Alert", "The next good you sell at your destination earns +3 silver bonus."),
        ("Shortage Alert", "The next good you sell at your destination earns +3 silver bonus."),
        ("Trade Wind Bonus", "If you complete a contract this round, earn +2 silver bonus on top of the reward."),
        ("Cargo Salvage", "Draw 1 card from the goods deck. Add it to your cargo for free (if you have space)."),
    ]
    for title, effect in trade:
        events.append({"title": title, "category": "Trade", "effect": effect})

    # Culture (8)
    culture = [
        ("Festival Season", "If you are in the Mediterranean, +3 silver bonus on your next sell."),
        ("Festival Season", "If you are in the East Indies, +3 silver bonus on your next sell."),
        ("Superstition", "Local sailors refuse to board. Skip 1 crew hire this round. No other penalty."),
        ("NPC Encounter", "A local merchant offers to buy 1 good from you at +2 silver above market price."),
        ("NPC Encounter", "A retired captain shares route knowledge. Peek at the top 3 event cards, put them back in any order."),
        ("Port Celebration", "Port fee waived this round. Reputation +1 in this region."),
        ("Storm Warning", "Sailors warn of danger ahead. You may cancel your voyage and return to port for free."),
        ("Sea Legend", "An old sailor tells a tale. No mechanical effect, but you feel the weight of the sea."),
    ]
    for title, effect in culture:
        events.append({"title": title, "category": "Culture", "effect": effect})

    return events
