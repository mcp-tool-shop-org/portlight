"""Session manager — load/save active run, command context.

The session is the bridge between CLI commands and engine state.
Every command goes through the session to ensure state is consistent
and saved after mutations.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

from portlight.content.contracts import TEMPLATES as CONTRACT_TEMPLATES
from portlight.content.goods import GOODS
from portlight.content.ships import SHIPS, create_ship_from_template
from portlight.content.world import new_game
from portlight.engine.captain_identity import CAPTAIN_TEMPLATES, CaptainType
from portlight.engine.economy import execute_buy, execute_sell, recalculate_prices, tick_markets
from portlight.engine.models import VoyageStatus, WorldState
from portlight.engine.reputation import (
    get_service_modifier,
    record_inspection_outcome,
    record_port_arrival,
    record_trade_outcome,
    tick_reputation,
)
from portlight.engine.contracts import (
    ContractBoard,
    abandon_contract,
    accept_offer,
    check_delivery,
    generate_offers,
    resolve_completed,
    tick_contracts,
)
from portlight.engine.infrastructure import (
    InfrastructureState,
    compute_board_effects,
    deposit_cargo,
    draw_credit,
    expire_voyage_policies,
    lease_warehouse,
    open_broker_office,
    open_credit_line,
    purchase_license,
    purchase_policy,
    repay_credit,
    resolve_claim,
    tick_credit,
    tick_infrastructure,
    withdraw_cargo,
)
from portlight.engine.campaign import CampaignState, SessionSnapshot, evaluate_milestones
from portlight.engine.narrative import NarrativeState, evaluate_narrative
from portlight.engine.save import load_game, save_game
from portlight.engine.voyage import EventType, VoyageEvent, advance_day, arrive, depart
from portlight.receipts.models import ReceiptLedger, TradeReceipt


def _trim_cargo_to_capacity(cargo: list, capacity: int) -> list[tuple[str, int]]:
    """Reduce quantity on trailing stacks until used <= capacity.

    Pops a CargoItem only when its remainder is 0. Returns (good_id, qty)
    pairs that were jettisoned, last-stack-first.
    """
    jettisoned: list[tuple[str, int]] = []
    if capacity < 0:
        capacity = 0
    while cargo and sum(c.quantity for c in cargo) > capacity:
        last = cargo[-1]
        if last.quantity <= 0:
            cargo.pop()
            continue
        overflow = sum(c.quantity for c in cargo) - capacity
        drop = min(last.quantity, overflow)
        if drop <= 0:
            break
        original_qty = last.quantity
        last.quantity -= drop
        if original_qty > 0 and getattr(last, "cost_basis", 0):
            last.cost_basis = int(last.cost_basis * last.quantity / original_qty)
        jettisoned.append((last.good_id, drop))
        if last.quantity <= 0:
            cargo.pop()
    return jettisoned


def apply_crew_casualties(ship, lost: int, *, keep_at_least: int = 0) -> int:
    """Remove crew losses from the roster (sailors first), then officers, then sync.

    Ship.crew is derived from CrewRoster; mutating crew alone is resurrected on
    the next hire/fire sync_crew(). Returns the number actually removed.
    """
    if ship is None or lost <= 0:
        return 0
    roster = getattr(ship, "roster", None)
    if roster is None or getattr(roster, "total", 0) <= 0:
        floor = max(0, keep_at_least)
        applied = min(lost, max(0, ship.crew - floor))
        ship.crew = max(floor, ship.crew - lost)
        return applied

    current = roster.total
    floor = max(0, keep_at_least)
    lost = min(lost, max(0, current - floor))
    if lost <= 0:
        ship.sync_crew()
        return 0

    remaining = lost
    # Sailors absorb casualties first; specialists and named officers follow.
    take = min(getattr(roster, "sailors", 0), remaining)
    roster.sailors -= take
    remaining -= take

    from portlight.engine.models import CrewRole
    specialist_order = (
        ("gunners", CrewRole.GUNNER),
        ("navigators", CrewRole.NAVIGATOR),
        ("surgeons", CrewRole.SURGEON),
        ("marines", CrewRole.MARINE),
        ("quartermasters", CrewRole.QUARTERMASTER),
    )
    for attr, role in specialist_order:
        if remaining <= 0:
            break
        cur = getattr(roster, attr, 0)
        take = min(cur, remaining)
        if take <= 0:
            continue
        setattr(roster, attr, cur - take)
        remaining -= take
        officers = getattr(ship, "officers", None)
        if officers and take > 0:
            to_drop = take
            kept = []
            for officer in reversed(officers):
                o_role = officer.role
                match = o_role == role or getattr(o_role, "value", o_role) == role.value
                if match and to_drop > 0:
                    to_drop -= 1
                else:
                    kept.append(officer)
            ship.officers = list(reversed(kept))

    ship.sync_crew()
    return lost - remaining


def injury_ids_from(injuries) -> list[str]:
    """Return hashable injury id strings. ActiveInjury objects are not dict keys."""
    ids: list[str] = []
    for inj in injuries or []:
        if isinstance(inj, str):
            ids.append(inj)
            continue
        iid = getattr(inj, "injury_id", None)
        if isinstance(iid, str):
            ids.append(iid)
    return ids


def naval_capture_gate(captain, encounter) -> tuple[bool, str]:
    """Whether a naval sink may become a prize. Same gate as CLI naval."""
    from portlight.engine.encounter import can_capture_prize
    from portlight.engine.models import max_fleet_size
    trust = 0
    standing = getattr(captain, "standing", None)
    if standing is not None:
        trust = getattr(standing, "commercial_trust", 0) or 0
    return can_capture_prize(captain, encounter, max_fleet_size(trust))


def prize_crew_limits(captain, encounter) -> tuple[int, int]:
    """Minimum crew for the prize and the flagship after a split."""
    from portlight.engine.encounter import prize_template_id
    prize_tid = prize_template_id(encounter.enemy_strength)
    prize_tmpl = SHIPS.get(prize_tid)
    prize_min = prize_tmpl.crew_min if prize_tmpl else 3
    current_tmpl = SHIPS.get(captain.ship.template_id)
    current_min = current_tmpl.crew_min if current_tmpl else 3
    return prize_min, current_min


def assign_prize_ship(session: "GameSession", encounter, crew_to_assign: int):
    """Validate crew, capture the prize, append to fleet.

    Returns (OwnedShip, None) on success or (None, error) matching CLI capture.
    """
    from portlight.engine.encounter import capture_prize

    captain = session.captain
    can_cap, reason = naval_capture_gate(captain, encounter)
    if not can_cap:
        return None, f"Cannot capture: {reason}"

    prize_min, current_min = prize_crew_limits(captain, encounter)
    if crew_to_assign < prize_min:
        return None, f"Need at least {prize_min} crew for the prize ship."
    leftover = captain.ship.crew - crew_to_assign
    if leftover < current_min:
        return None, (
            f"Would leave your flagship with {leftover} crew (need {current_min})."
        )

    owned = capture_prize(captain, encounter, crew_to_assign)
    if session.world and session.world.voyage:
        owned.docked_port_id = session.world.voyage.destination_id
    else:
        owned.docked_port_id = session.current_port_id or "porto_novo"
    captain.fleet.append(owned)
    return owned, None


_ENCOUNTER_RESUME_PHASES = frozenset({
    "approach", "naval", "boarding", "duel",
    "capture_available", "resolved", "victory", "defeat",
})


def encounter_persist_blob(enc, *, pending_victory: bool = False, player=None, opponent=None) -> dict:
    """Serialize EncounterState into the free-form pirates.encounter_state blob."""
    blob = {
        "enemy_captain_id": enc.enemy_captain_id,
        "enemy_captain_name": enc.enemy_captain_name,
        "enemy_faction_id": enc.enemy_faction_id,
        "enemy_personality": enc.enemy_personality,
        "enemy_strength": enc.enemy_strength,
        "enemy_region": enc.enemy_region,
        "enemy_ship_hull": enc.enemy_ship_hull,
        "enemy_ship_hull_max": enc.enemy_ship_hull_max,
        "enemy_ship_cannons": enc.enemy_ship_cannons,
        "enemy_ship_maneuver": enc.enemy_ship_maneuver,
        "enemy_ship_speed": enc.enemy_ship_speed,
        "enemy_ship_crew": enc.enemy_ship_crew,
        "enemy_ship_crew_max": enc.enemy_ship_crew_max,
        "boarding_progress": enc.boarding_progress,
        "boarding_threshold": enc.boarding_threshold,
        "naval_turns": enc.naval_turns,
        "duel_turns": enc.duel_turns,
        "pending_victory": pending_victory,
    }
    if player is not None:
        blob["player_hp"] = player.hp
        blob["player_stamina"] = player.stamina
    if opponent is not None:
        blob["opponent_hp"] = opponent.hp
        blob["opponent_stamina"] = opponent.stamina
    return blob


def persist_encounter(
    session: "GameSession",
    enc,
    *,
    pending_victory: bool = False,
    player=None,
    opponent=None,
    phase: str | None = None,
) -> None:
    """Write phase + full ship stats onto pirates.encounter_state (engine round-trips the dict)."""
    if not session or not session.world:
        return
    pirates = session.world.pirates
    pirates.encounter_phase = phase if phase is not None else (enc.phase or "approach")
    pirates.encounter_state = encounter_persist_blob(
        enc, pending_victory=pending_victory, player=player, opponent=opponent,
    )


def reconstruct_encounter(session: "GameSession", *, victory_phase: str = "victory"):
    """Rebuild EncounterState from pending_duel + persisted blob.

    Does not call create_encounter (that re-rolls cannons/speed/hull_max).
    Identity comes from pending_duel; ship stats come from encounter_state.
    ``victory_phase`` is 'victory' for TUI and 'resolved' for CLI spare/take-all.
    """
    from portlight.engine.models import EncounterState

    if not session or not session.world or session.world.pirates.pending_duel is None:
        return None
    pd = session.world.pirates.pending_duel
    estate = session.world.pirates.encounter_state or {}
    hull = int(estate.get("enemy_ship_hull", 0) or 0)
    crew = int(estate.get("enemy_ship_crew", 0) or 0)
    enc = EncounterState(
        enemy_captain_id=estate.get("enemy_captain_id") or pd.captain_id,
        enemy_captain_name=estate.get("enemy_captain_name") or pd.captain_name,
        enemy_faction_id=estate.get("enemy_faction_id") or pd.faction_id,
        enemy_personality=estate.get("enemy_personality") or pd.personality,
        enemy_strength=int(estate.get("enemy_strength", pd.strength) or pd.strength),
        enemy_region=estate.get("enemy_region") or pd.region or "",
        enemy_ship_hull=hull,
        enemy_ship_hull_max=int(estate.get("enemy_ship_hull_max", hull) or hull),
        enemy_ship_cannons=int(estate.get("enemy_ship_cannons", 0) or 0),
        enemy_ship_maneuver=float(estate.get("enemy_ship_maneuver", 0.5)),
        enemy_ship_speed=float(estate.get("enemy_ship_speed", 6.0)),
        enemy_ship_crew=crew,
        enemy_ship_crew_max=int(estate.get("enemy_ship_crew_max", crew) or crew),
        phase="approach",
        boarding_progress=int(estate.get("boarding_progress", 0) or 0),
        boarding_threshold=int(estate.get("boarding_threshold", 3) or 3),
        naval_turns=int(estate.get("naval_turns", 0) or 0),
        duel_turns=int(estate.get("duel_turns", 0) or 0),
    )
    phase = session.world.pirates.encounter_phase
    if phase and phase in _ENCOUNTER_RESUME_PHASES:
        enc.phase = phase
    if estate.get("pending_victory") and enc.phase != "capture_available":
        enc.phase = victory_phase
    return enc


def inventory_gear_data(captain) -> dict:
    """Map captain combat_gear, injuries, and upgrades into inventory_view keys."""
    gear = captain.combat_gear
    from portlight.content.armor import ARMOR
    from portlight.content.melee_weapons import MELEE_WEAPONS
    from portlight.content.ranged_weapons import RANGED_WEAPONS
    from portlight.content.fighting_styles import FIGHTING_STYLES
    from portlight.content.injuries import INJURIES

    armor_def = ARMOR.get(gear.armor) if gear.armor else None
    melee_def = MELEE_WEAPONS.get(gear.melee_weapon) if gear.melee_weapon else None
    firearm_def = RANGED_WEAPONS.get(gear.firearm) if gear.firearm else None
    mechanical_def = RANGED_WEAPONS.get(gear.mechanical_weapon) if gear.mechanical_weapon else None
    style_def = FIGHTING_STYLES.get(captain.active_style) if captain.active_style else None

    throwing_summary = []
    for wid, count in (gear.throwing_weapons or {}).items():
        w = RANGED_WEAPONS.get(wid)
        throwing_summary.append({"name": w.name if w else wid, "count": count})

    injuries_data = []
    for inj in captain.injuries or []:
        if isinstance(inj, str):
            iid = inj
        else:
            iid = getattr(inj, "injury_id", None)
        if not isinstance(iid, str):
            continue
        idef = INJURIES.get(iid)
        heal_remaining = getattr(inj, "heal_remaining", None)
        if idef:
            if heal_remaining is None and getattr(idef, "heal_days", None) is None:
                healing = "Permanent"
            elif heal_remaining is None:
                healing = "Permanent"
            elif heal_remaining <= 0:
                healing = "Healed"
            else:
                healing = f"{heal_remaining} days"
            injuries_data.append({
                "name": idef.name,
                "severity": idef.severity,
                "healing": healing,
            })
        elif iid:
            injuries_data.append({
                "name": str(iid).replace("_", " ").title(),
                "severity": str(getattr(inj, "severity", "minor")),
                "healing": f"{heal_remaining} days" if heal_remaining else "",
            })

    ship_upgrades = []
    ship = getattr(captain, "ship", None)
    if ship and getattr(ship, "upgrades", None):
        from portlight.content.upgrades import UPGRADES
        for u in ship.upgrades:
            uid = u.upgrade_id if hasattr(u, "upgrade_id") else u
            udef = UPGRADES.get(uid)
            ship_upgrades.append(udef.name if udef else uid)

    cargo = getattr(captain, "cargo", None) or []
    cargo_used = sum(c.quantity for c in cargo)
    cargo_cap = ship.cargo_capacity if ship else 0

    return {
        "armor_name": armor_def.name if armor_def else "None",
        "armor_dr": armor_def.damage_reduction if armor_def else 0,
        "armor_type": armor_def.armor_type if armor_def else "",
        "melee_name": melee_def.name if melee_def else "Fists",
        "melee_bonus": f"+{melee_def.damage_bonus} dmg" if melee_def else "",
        "active_style": style_def.name if style_def else "None",
        "style_special": style_def.special_action.name if style_def and style_def.special_action else "",
        "firearm_name": firearm_def.name if firearm_def else "None",
        "firearm_ammo": gear.firearm_ammo,
        "mechanical_name": mechanical_def.name if mechanical_def else "None",
        "mechanical_ammo": gear.mechanical_ammo,
        "throwing_summary": throwing_summary,
        "injuries": injuries_data,
        "ship_upgrades": ship_upgrades,
        "cargo_used": cargo_used,
        "cargo_capacity": cargo_cap,
        "silver": captain.silver,
    }


def list_save_slots(base_path: Path | None = None) -> list[dict]:
    """Peek saves/*.json for (slot, captain, day). Skips unreadable files."""
    from portlight.engine.save import SAVE_DIR, SAVE_FILE

    base = base_path or Path(".")
    save_dir = base / SAVE_DIR
    if not save_dir.is_dir():
        return []
    default_path = save_dir / "default.json"
    rows: list[dict] = []
    seen: set[str] = set()
    for path in sorted(save_dir.glob("*.json")):
        stem = path.stem
        if path.name == SAVE_FILE:
            if default_path.exists():
                continue
            stem = "default"
        if stem in seen:
            continue
        captain = ""
        day = 0
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        if not isinstance(data, dict):
            continue
        cap = data.get("captain") or {}
        if isinstance(cap, dict):
            captain = str(cap.get("name") or "")
            if not day:
                day = int(cap.get("day") or 0)
        day = int(data.get("day") or day or 0)
        seen.add(stem)
        rows.append({"slot": stem, "captain": captain, "day": day})
    return rows


class GameSession:
    """Holds active game state and mediates all player actions."""

    def __init__(self, base_path: Path | None = None, slot: str = "default") -> None:
        self.base_path = base_path or Path(".")
        self.slot = slot
        self.world: WorldState | None = None
        self.ledger: ReceiptLedger = ReceiptLedger()
        self.board: ContractBoard = ContractBoard()
        self.infra: InfrastructureState = InfrastructureState()
        self.campaign: CampaignState = CampaignState()
        self.narrative: NarrativeState = NarrativeState()
        self._trade_seq: int = 0
        self._rng: random.Random = random.Random()
        self.auto_resolve_duels: bool = False
        self.last_provision_cost: int = 0
        self.last_jettison: list[tuple[str, int]] = []
        self.last_milestone_ids: list[str] = []
        self.last_path_ids: list[str] = []

    @property
    def active(self) -> bool:
        return self.world is not None

    @property
    def captain(self):
        return self.world.captain if self.world else None

    @property
    def current_port_id(self) -> str | None:
        if not self.world or not self.world.voyage:
            return None
        if self.world.voyage.status == VoyageStatus.IN_PORT:
            return self.world.voyage.destination_id
        return None

    @property
    def current_port(self):
        pid = self.current_port_id
        if pid and self.world:
            return self.world.ports.get(pid)
        return None

    @property
    def at_sea(self) -> bool:
        return (self.world is not None and
                self.world.voyage is not None and
                self.world.voyage.status == VoyageStatus.AT_SEA)

    @property
    def captain_template(self):
        """Get the active captain's archetype template."""
        if not self.world:
            return None
        try:
            ct = CaptainType(self.world.captain.captain_type)
            return CAPTAIN_TEMPLATES[ct]
        except (ValueError, KeyError):
            return CAPTAIN_TEMPLATES[CaptainType.MERCHANT]

    def new(
        self,
        captain_name: str = "Captain",
        starting_port: str | None = None,
        captain_type: str = "merchant",
        seed: int | None = None,
    ) -> None:
        """Start a fresh game. captain_type: 'merchant', 'smuggler', or 'navigator'."""
        ct = CaptainType(captain_type)
        self.world = new_game(captain_name, starting_port, ct, seed=seed)
        self._rng = random.Random(self.world.seed)
        self.ledger = ReceiptLedger(run_id=f"run-{self.world.seed}")
        self.board = ContractBoard()
        self.infra = InfrastructureState()
        self.campaign = CampaignState()
        self.narrative = NarrativeState()
        self._trade_seq = 0
        self._save()
        # Populate contract board at starting port using a deterministic
        # RNG derived from world.seed to avoid perturbing the main sequence.
        port = self.current_port
        if port:
            saved_rng = self._rng
            self._rng = random.Random(self.world.seed + 7919)
            self._refresh_board(port)
            self._rng = saved_rng
            self._save()

    def load(self) -> bool:
        """Load saved game. Returns True if loaded."""
        result = load_game(self.base_path, slot=self.slot)
        if result is None:
            return False
        self.world, self.ledger, self.board, self.infra, self.campaign, self.narrative = result
        self._rng = random.Random(self.world.seed + self.world.day)
        self._trade_seq = len(self.ledger.receipts)
        # Recalculate prices for all ports (handles migrated slots with price=0)
        for port in self.world.ports.values():
            self._recalc(port)
        return True

    @property
    def _pricing(self):
        """Captain's pricing modifiers for economy calls."""
        t = self.captain_template
        return t.pricing if t else None

    def _save(self) -> None:
        """Auto-save after every mutation."""
        if self.world:
            # Clamp silver to non-negative (infrastructure/wage deductions can overshoot)
            self.world.captain.silver = max(0, self.world.captain.silver)
            save_game(self.world, self.ledger, self.board, self.infra, self.campaign, self.narrative, self.base_path, slot=self.slot)

    def _recalc(self, port) -> None:
        """Recalculate prices at a port with captain modifiers."""
        recalculate_prices(port, GOODS, self._pricing)

    def _resolve_pending_duel(self) -> None:
        """Auto-resolve a pending pirate duel (for bots/tests)."""
        from portlight.engine.duel import resolve_duel
        from portlight.engine.models import PirateEncounterRecord
        pd = self.world.pirates.pending_duel
        stances = [self._rng.choice(["thrust", "slash", "parry"]) for _ in range(5)]
        result = resolve_duel(
            player_stances=stances,
            opponent_id=pd.captain_id, opponent_name=pd.captain_name,
            opponent_personality=pd.personality, opponent_strength=pd.strength,
            rng=self._rng,
            player_crew=self.captain.ship.crew if self.captain.ship else 5,
        )
        self.captain.silver = max(0, self.captain.silver + result.silver_delta)
        outcome_str = "duel_win" if result.player_won else ("duel_draw" if result.draw else "duel_loss")
        self.world.pirates.encounters.append(PirateEncounterRecord(
            captain_id=pd.captain_id, faction_id=pd.faction_id,
            day=self.world.day, outcome=outcome_str, region=pd.region,
        ))
        if result.player_won:
            self.world.pirates.duels_won += 1
        elif not result.draw:
            self.world.pirates.duels_lost += 1
        self.world.pirates.pending_duel = None

    # --- Trading ---

    def buy(self, good_id: str, qty: int) -> TradeReceipt | str:
        """Buy goods at current port."""
        port = self.current_port
        if not port:
            return "Not docked at a port"
        result = execute_buy(self.world.captain, port, good_id, qty, GOODS, self._trade_seq)
        if isinstance(result, TradeReceipt):
            self.ledger.append(result)
            self._trade_seq += 1
            self._recalc(port)
            self._save()
        return result

    def sell(self, good_id: str, qty: int) -> TradeReceipt | str:
        """Sell goods at current port. Mutates reputation based on suspicion."""
        port = self.current_port
        if not port:
            return "Not docked at a port"

        # Snapshot slot before sell for margin computation
        slot = next((s for s in port.market if s.good_id == good_id), None)
        flood_before = slot.flood_penalty if slot else 0.0
        stock_target = slot.stock_target if slot else 50

        # Snapshot cargo provenance before sell (sell may remove the item)
        # Note: if cargo_item is None, execute_sell will return an error string
        # so the provenance defaults below are never reached by check_delivery.
        cargo_item = next((c for c in self.world.captain.cargo if c.good_id == good_id), None)
        cargo_source_port = cargo_item.acquired_port if cargo_item else ""
        cargo_source_region = cargo_item.acquired_region if cargo_item else ""

        result = execute_sell(self.world.captain, port, good_id, qty, self._trade_seq)
        if isinstance(result, TradeReceipt):
            self.ledger.append(result)
            self._trade_seq += 1

            # Compute margin for reputation
            cost_basis = self._estimate_cost_basis(good_id, result.quantity)
            revenue = result.total_price
            margin_pct = ((revenue - cost_basis) / max(cost_basis, 1)) * 100 if cost_basis > 0 else 50.0

            good = GOODS.get(good_id)
            good_category = good.category if good else None
            from portlight.engine.models import GoodCategory
            category = good_category if good_category else GoodCategory.COMMODITY

            record_trade_outcome(
                self.world.captain.standing,
                self.world.captain.captain_type,
                self.world.day,
                port.id,
                port.region,
                good_id,
                category,
                result.quantity,
                margin_pct,
                stock_target,
                flood_before,
                is_sell=True,
            )

            # Check contract delivery (uses pre-sell provenance snapshot)
            credited = check_delivery(
                self.board, port.id, good_id, result.quantity,
                cargo_source_port, cargo_source_region,
            )
            # Resolve any completed contracts
            if credited:
                outcomes = resolve_completed(self.board, self.world.day)
                for outcome in outcomes:
                    self.world.captain.silver += outcome.silver_delta

            self._recalc(port)
            self._evaluate_narrative()
            self._save()
        return result

    def _estimate_cost_basis(self, good_id: str, qty: int) -> int:
        """Estimate cost basis for sold goods from cargo records."""
        for item in self.world.captain.cargo:
            if item.good_id == good_id and item.quantity > 0:
                avg = item.cost_basis / item.quantity if item.quantity > 0 else 0
                return int(avg * qty)
        # Fallback: use base price
        good = GOODS.get(good_id)
        return good.base_price * qty if good else qty * 10

    # --- Voyage ---

    def sail(self, destination_id: str, defer_fee: bool = False) -> str | None:
        """Depart for destination. Returns error string or None on success.

        Accepts port IDs (jade_port) or display names (Jade Port, "jade port").
        """
        if not self.world:
            return "No active game"
        def _normalize(s: str) -> str:
            return s.lower().replace("_", " ").replace("-", " ").replace("'", "").strip()

        # Try exact ID first
        resolved = destination_id
        if resolved not in self.world.ports:
            # Try matching by display name (case-insensitive, punctuation-tolerant)
            needle = _normalize(destination_id)
            for pid, port in self.world.ports.items():
                if _normalize(port.name) == needle:
                    resolved = pid
                    break
            else:
                # Try partial match (e.g. "monsoon" matches "Monsoon Reach")
                matches = [
                    pid for pid, port in self.world.ports.items()
                    if needle in _normalize(port.name)
                ]
                if len(matches) == 1:
                    resolved = matches[0]

        result = depart(self.world, resolved, defer_fee=defer_fee)
        if isinstance(result, str):
            return result
        self._save()
        return None

    def advance(self) -> list:
        """Advance one day. Returns voyage events."""
        if not self.world:
            return []

        # Daily reputation tick (heat decay)
        tick_reputation(self.world.captain.standing)

        # Daily contract tick (expiry, stale offers)
        contract_outcomes = tick_contracts(self.board, self.world.day)
        for outcome in contract_outcomes:
            self.world.captain.silver += outcome.silver_delta
            # Resolve contract guarantee insurance on failure/expiry
            if outcome.outcome_type in ("expired", "abandoned"):
                # Loss value = the reward that was missed + reputation damage cost
                loss_value = abs(outcome.trust_delta) * 50 + abs(outcome.standing_delta) * 30
                resolve_claim(
                    self.infra, self.world.captain,
                    "contract_failure", loss_value, self.world.day,
                    contract_id=outcome.contract_id,
                )

        # Daily infrastructure upkeep
        infra_msgs = tick_infrastructure(self.infra, self.world.captain, self.world.day)
        # File insurance claims for warehouse seizures
        for msg in infra_msgs:
            if "seized" in msg.lower():
                # Estimate lost cargo value from message for insurance claim
                resolve_claim(
                    self.infra, self.world.captain,
                    "cargo_damage", 100, self.world.day,  # base estimate
                )

        # Daily credit tick (interest, due dates, defaults)
        credit_msgs = tick_credit(self.infra, self.world.captain, self.world.day)
        # Credit default damages trust
        for msg in credit_msgs:
            if "DEFAULT" in msg:
                self.world.captain.standing.commercial_trust = max(
                    0, self.world.captain.standing.commercial_trust - 15,
                )

        # Heal injuries daily (in port always, at sea only with surgeon's bay)
        if self.world.captain.injuries:
            from portlight.engine.injuries import heal_injury_tick
            in_port = not self.at_sea
            has_surgeons_bay = False
            if self.world.captain.ship and hasattr(self.world.captain.ship, 'upgrades'):
                has_surgeons_bay = any(
                    getattr(u, 'upgrade_id', '') == 'surgeons_bay'
                    for u in self.world.captain.ship.upgrades
                )
            # Heal at sea only if surgeon's bay installed
            if in_port or has_surgeons_bay:
                has_medicines = any(c.good_id == "medicines" for c in self.world.captain.cargo)
                self.world.captain.injuries = heal_injury_tick(
                    self.world.captain.injuries,
                    days=1,
                    in_port=True,  # surgeon's bay counts as "in port" for healing
                    has_medicines=has_medicines,
                )

        if not self.at_sea:
            # In port: tick markets forward
            tick_markets(self.world.ports, days=1, rng=self._rng)
            self.world.day += 1
            self.world.captain.day += 1

            # Consume provisions (1 per day in port)
            captain = self.world.captain
            if captain.provisions > 0:
                captain.provisions -= 1

            # Pay crew wages while docked (same formula as at sea)
            if captain.ship:
                from portlight.content.ships import SHIPS as _SHIPS
                from portlight.engine.ship_stats import compute_daily_wages as _cdw
                from portlight.engine.fleet import fleet_daily_wages as _fdw
                _tmpl = _SHIPS.get(captain.ship.template_id)
                _dw = _tmpl.daily_wage if _tmpl else 1
                _wage = _cdw(captain.ship.roster, _dw) if captain.ship.roster.total > 0 else _dw * captain.ship.crew
                _wage += _fdw(captain)
                if _wage > 0 and captain.silver >= _wage:
                    captain.silver -= _wage

            for port in self.world.ports.values():
                self._recalc(port)
            self._evaluate_campaign()
            self._save()
            return []

        # Auto-resolve pending pirate duels (for bots/tests that can't respond)
        if self.auto_resolve_duels and self.world.pirates.pending_duel is not None:
            self._resolve_pending_duel()

        events = advance_day(self.world, self._rng)

        # Enrich with sea culture — route encounters, NPC sightings, weather, crew mood
        from portlight.engine.sea_culture_engine import enrich_voyage_day
        from portlight.engine.voyage import find_route as _find_route
        _voyage = self.world.voyage
        _route = _find_route(self.world, _voyage.origin_id, _voyage.destination_id) if _voyage else None
        events = enrich_voyage_day(
            self.world, _route, events, self._rng,
            ledger=self.ledger, board=self.board,
        )

        # Note: markets don't tick while at sea — prices only change when
        # you're in port to observe them. This is intentional: it preserves
        # the arbitrage window you planned for during departure.

        # Record inspection events for reputation + resolve insurance claims
        voyage = self.world.voyage
        dest = voyage.destination_id if voyage else ""
        for event in events:
            if event.event_type == EventType.INSPECTION:
                region = self._voyage_region()
                port_id = voyage.origin_id if voyage else ""
                cargo_seized = event.cargo_lost is not None and len(event.cargo_lost) > 0
                record_inspection_outcome(
                    self.world.captain.standing,
                    self.world.day, port_id, region,
                    abs(event.silver_delta), cargo_seized,
                )

            # Resolve insurance claims for damaging events
            self._resolve_event_insurance(event, dest)

        # Check arrival
        if self.world.voyage and self.world.voyage.status == VoyageStatus.ARRIVED:
            arrive(self.world)
            # Expire voyage-scoped policies on arrival
            expire_voyage_policies(self.infra)
            port = self.current_port
            if port:
                record_port_arrival(
                    self.world.captain.standing,
                    self.world.day, port.id, port.region,
                )
                # Track cultural state on arrival
                from portlight.engine.culture_engine import record_port_visit
                record_port_visit(port.id, port.region, self.world.culture)
                # Track festival arrival for narrative beat
                if any(af.port_id == port.id for af in self.world.culture.active_festivals):
                    self.world.culture.festivals_visited += 1
                # Generate arrival experience with NPC greetings
                from portlight.engine.port_arrival_engine import generate_arrival, format_arrival_text
                arrival_exp = generate_arrival(self.world, port.id)
                arrival_lines = format_arrival_text(arrival_exp)
                # Inject arrival text as a VoyageEvent so it flows through the event display
                if arrival_lines:
                    arrival_text = "\n".join(arrival_lines)
                    events.append(VoyageEvent(
                        event_type=EventType.NOTHING,
                        message=arrival_text,
                        flavor="[arrival]",
                    ))
                # Check for port consequences (history-based encounters)
                from portlight.engine.consequences import apply_consequence, check_port_consequences
                port_consequences = check_port_consequences(
                    self.world, port.id, self.ledger, self.board, self._rng,
                )
                for consequence in port_consequences:
                    apply_consequence(self.world, consequence)
                    effect_note = ""
                    if consequence.silver_delta > 0:
                        effect_note = f" (+{consequence.silver_delta} silver)"
                    elif consequence.silver_delta < 0:
                        effect_note = f" ({consequence.silver_delta} silver)"
                    events.append(VoyageEvent(
                        event_type=EventType.NOTHING,
                        message=f"{consequence.text}{effect_note}",
                        flavor=f"[consequence:{consequence.effect_type}]",
                    ))
                self._recalc(port)
                self._refresh_board(port)

        # Recalculate all markets (time passes)
        for port in self.world.ports.values():
            self._recalc(port)

        # Evaluate campaign milestones
        self._evaluate_campaign()

        # Evaluate narrative beats
        self._evaluate_narrative(events_this_turn=events)

        self._save()
        return events

    def _voyage_region(self) -> str:
        """Best guess of the current voyage's region (use destination port)."""
        if self.world and self.world.voyage:
            dest = self.world.ports.get(self.world.voyage.destination_id)
            if dest:
                return dest.region
        return "Mediterranean"

    def tick_sea_captain_agency(self):
        """Tick NPC captain agency while at sea (shared CLI + TUI advance path).

        Silver gifts are applied immediately. An ambush/challenge creates an
        EncounterState, writes pending_duel + full ship stats onto
        encounter_state, and returns it so the frontend can present the fight.

        Returns (encounter_or_none, is_ambush, notices) where notices is a list
        of (effect_type, message) tuples.
        """
        if not self.world or not self.at_sea:
            return None, False, []
        from portlight.content.factions import PIRATE_CAPTAINS
        from portlight.engine.captain_memory import tick_captain_agency
        from portlight.engine.encounter import create_encounter
        from portlight.engine.models import PendingDuel

        region = self._voyage_region()
        actions = tick_captain_agency(
            self.world.pirates.captain_memories, region,
            self.captain.silver, self.world.day, self._rng,
        )
        notices: list[tuple[str, str]] = []
        encounter = None
        ambush = False
        for ca in actions:
            notices.append((ca.effect_type, ca.message))
            if ca.effect_type == "silver":
                self.captain.silver += ca.effect_value
            elif ca.effect_type == "encounter" and encounter is None:
                dest = self.world.voyage.destination_id if self.world.voyage else "porto_novo"
                enc = create_encounter(self.world.ports, dest, self._rng)
                if enc:
                    cap = PIRATE_CAPTAINS.get(ca.captain_id)
                    enc.enemy_captain_id = ca.captain_id
                    enc.enemy_captain_name = ca.captain_name
                    if cap:
                        enc.enemy_faction_id = cap.faction_id
                        enc.enemy_personality = cap.personality
                        enc.enemy_strength = cap.strength
                    enc.enemy_region = region
                    if ca.verb == "ambush":
                        enc.phase = "naval"
                        ambush = True
                    self.world.pirates.pending_duel = PendingDuel(
                        captain_id=enc.enemy_captain_id,
                        captain_name=enc.enemy_captain_name,
                        faction_id=enc.enemy_faction_id,
                        personality=enc.enemy_personality,
                        strength=enc.enemy_strength,
                        region=enc.enemy_region,
                    )
                    persist_encounter(self, enc)
                    encounter = enc
                    break
        if notices or encounter:
            self._save()
        return encounter, ambush, notices

    # --- Provisioning & Repair ---

    def _service_mult(self) -> float:
        """Get service cost multiplier from port standing reputation."""
        port = self.current_port
        if not port or not self.world:
            return 1.0
        return get_service_modifier(self.world.captain.standing, port.id)

    def provision(self, days: int) -> str | None:
        """Buy provisions at port-specific cost. Returns error or None.

        On success the amount charged is stored in ``last_provision_cost``
        (port.provision_cost * service modifier, minimum 1/day).
        """
        if not self.world:
            return "No active game"
        if days <= 0:
            return "Quantity must be a positive number."
        port = self.current_port
        if not port:
            return "Must be docked to provision"
        svc_mult = self._service_mult()
        cost_per_day = max(1, int(port.provision_cost * svc_mult))
        cost = days * cost_per_day
        if cost > self.world.captain.silver:
            return f"Need {cost} silver for {days} days of provisions ({cost_per_day}/day here), have {self.world.captain.silver}"
        self.world.captain.silver -= cost
        self.world.captain.provisions += days
        self.last_provision_cost = cost
        self._save()
        return None

    def repair(self, amount: int | None = None) -> tuple[int, int] | str:
        """Repair hull at port-specific cost. Returns (repaired, cost) or error."""
        if not self.world:
            return "No active game"
        port = self.current_port
        if not port:
            return "Must be docked to repair"
        ship = self.world.captain.ship
        if not ship:
            return "No ship"
        damage = ship.hull_max - ship.hull
        if damage == 0:
            return "Ship is already in perfect condition"
        if amount is not None and amount <= 0:
            return "Quantity must be a positive number."
        if amount is None:
            amount = damage
        amount = min(amount, damage)
        svc_mult = self._service_mult()
        cost_per_hp = max(1, int(port.repair_cost * svc_mult))
        cost = amount * cost_per_hp
        if cost > self.world.captain.silver:
            affordable = self.world.captain.silver // cost_per_hp if cost_per_hp > 0 else 0
            if affordable == 0:
                return "Can't afford any repairs"
            amount = affordable
            cost = amount * cost_per_hp
        self.world.captain.silver -= cost
        ship.hull += amount
        self._save()
        return (amount, cost)

    def dry_dock(self, ship_name: str | None = None) -> tuple[int, int] | str:
        """Fully restore hull_max at a shipyard. Costs 5x repair rate per point.

        Returns (points_restored, cost) or error string.
        """
        if not self.world:
            return "No active game"
        port = self.current_port
        if not port:
            return "Must be docked"
        from portlight.engine.models import PortFeature
        if PortFeature.SHIPYARD not in port.features:
            return f"{port.name} has no shipyard"

        if ship_name:
            # Dry dock a fleet ship
            for owned in self.world.captain.fleet:
                if owned.docked_port_id == port.id and (
                    owned.ship.name.lower() == ship_name.lower()
                    or owned.ship.template_id.lower() == ship_name.lower()
                ):
                    return self._do_dry_dock(owned.ship, port)
            return f"No ship named '{ship_name}' docked at this port"
        else:
            ship = self.world.captain.ship
            if not ship:
                return "No ship"
            return self._do_dry_dock(ship, port)

    def _do_dry_dock(self, ship, port) -> tuple[int, int] | str:
        """Internal: restore hull_max and hull to template values."""
        from portlight.content.ships import SHIPS
        template = SHIPS.get(ship.template_id)
        if not template:
            return "Unknown ship template"
        degradation = template.hull_max - ship.hull_max
        if degradation <= 0:
            return "Ship hull is not degraded"
        svc_mult = self._service_mult()
        cost_per = max(1, int(port.repair_cost * svc_mult * 5))  # 5x normal repair
        cost = degradation * cost_per
        if cost > self.world.captain.silver:
            return f"Need {cost} silver for dry dock ({degradation} points at {cost_per}/point), have {self.world.captain.silver}"
        self.world.captain.silver -= cost
        ship.hull_max = template.hull_max
        ship.hull = min(ship.hull + degradation, ship.hull_max)
        self._save()
        return (degradation, cost)

    # --- Shipyard ---

    def buy_ship(self, ship_id: str) -> str | None:
        """Buy a new ship at a shipyard port. Returns error or None."""
        if not self.world:
            return "No active game"
        port = self.current_port
        if not port:
            return "Must be docked"
        from portlight.engine.models import PortFeature
        if PortFeature.SHIPYARD not in port.features:
            return f"{port.name} has no shipyard"
        template = SHIPS.get(ship_id)
        if not template:
            return f"Unknown ship: {ship_id}"
        if template.id == self.world.captain.ship.template_id:
            return "You already have this ship"
        if template.price > self.world.captain.silver:
            return f"Need {template.price} silver, have {self.world.captain.silver}"

        # Fleet: try to dock old ship instead of selling
        from portlight.engine.models import OwnedShip, max_fleet_size
        old_ship = self.world.captain.ship
        trust = self.world.captain.standing.commercial_trust
        fleet_limit = max_fleet_size(trust)
        fleet_count = len(self.world.captain.fleet) + 1  # +1 for current flagship

        if fleet_count < fleet_limit:
            # Add old ship to fleet (docked at this port, empty cargo)
            # Cargo stays with the captain for the new ship
            self.world.captain.fleet.append(OwnedShip(
                ship=old_ship,
                docked_port_id=port.id,
            ))
        else:
            # Fleet full — sell old ship for 40% of its template price
            old_template = SHIPS.get(old_ship.template_id)
            if old_template:
                self.world.captain.silver += int(old_template.price * 0.4)

        self.world.captain.silver -= template.price
        self.world.captain.ship = create_ship_from_template(template)

        # Transfer cargo: trim overflow quantity from the last stack(s), never
        # pop a whole stack that still has units that fit.
        self.last_jettison = _trim_cargo_to_capacity(
            self.world.captain.cargo, template.cargo_capacity,
        )

        self._save()
        return None

    def install_upgrade(self, upgrade_id: str) -> str | None:
        """Install a ship upgrade at a shipyard port. Returns error or None."""
        if not self.world:
            return "No active game"
        port = self.current_port
        if not port:
            return "Must be docked"
        from portlight.engine.models import InstalledUpgrade, PortFeature
        if PortFeature.SHIPYARD not in port.features:
            return f"{port.name} has no shipyard"
        from portlight.content.upgrades import UPGRADES
        template = UPGRADES.get(upgrade_id)
        if not template:
            return f"Unknown upgrade: {upgrade_id}"
        ship = self.world.captain.ship
        if not ship:
            return "No ship"
        if len(ship.upgrades) >= ship.upgrade_slots:
            return f"No upgrade slots remaining ({ship.upgrade_slots}/{ship.upgrade_slots} used)"
        if template.price > self.world.captain.silver:
            return f"Need {template.price} silver, have {self.world.captain.silver}"

        self.world.captain.silver -= template.price
        ship.upgrades.append(InstalledUpgrade(
            upgrade_id=upgrade_id,
            installed_day=self.world.day,
        ))
        self._save()
        return None

    def remove_upgrade(self, upgrade_id: str) -> str | None:
        """Remove an installed upgrade. No refund. Returns error or None."""
        if not self.world:
            return "No active game"
        port = self.current_port
        if not port:
            return "Must be docked"
        from portlight.engine.models import PortFeature
        if PortFeature.SHIPYARD not in port.features:
            return f"{port.name} has no shipyard"
        ship = self.world.captain.ship
        if not ship:
            return "No ship"
        for i, inst in enumerate(ship.upgrades):
            if inst.upgrade_id == upgrade_id:
                ship.upgrades.pop(i)
                self._save()
                return None
        return f"Upgrade not installed: {upgrade_id}"

    def rename_ship(self, new_name: str, ship_name: str | None = None) -> str | None:
        """Rename a ship. Renames flagship by default, or a fleet ship by name."""
        if not self.world:
            return "No active game"
        if not new_name.strip():
            return "Name cannot be empty"
        new_name = new_name.strip()[:30]  # cap at 30 chars

        if ship_name is None:
            # Rename flagship
            if not self.world.captain.ship:
                return "No ship"
            self.world.captain.ship.name = new_name
        else:
            # Rename a fleet ship
            for owned in self.world.captain.fleet:
                if (owned.ship.name.lower() == ship_name.lower()
                        or owned.ship.template_id.lower() == ship_name.lower()):
                    owned.ship.name = new_name
                    self._save()
                    return None
            return f"No ship named '{ship_name}' in fleet"

        self._save()
        return None

    # --- Fleet ---

    def dock_current_ship(self) -> str | None:
        """Dock the flagship and switch to another ship at this port."""
        if not self.world:
            return "No active game"
        port = self.current_port
        if not port:
            return "Must be docked"
        from portlight.engine.fleet import dock_ship
        err = dock_ship(self.world.captain, port.id)
        if err:
            return err
        self._save()
        return None

    def board_fleet_ship(self, ship_name: str) -> str | None:
        """Switch to a docked ship by name."""
        if not self.world:
            return "No active game"
        port = self.current_port
        if not port:
            return "Must be docked"
        from portlight.engine.fleet import board_ship
        err = board_ship(self.world.captain, ship_name, port.id)
        if err:
            return err
        self._save()
        return None

    def transfer_fleet_cargo(self, good_id: str, qty: int, from_ship: str, to_ship: str) -> str | None:
        """Move cargo between ships at the same port."""
        if not self.world:
            return "No active game"
        port = self.current_port
        if not port:
            return "Must be docked"
        from portlight.engine.fleet import transfer_cargo
        err = transfer_cargo(self.world.captain, good_id, qty, from_ship, to_ship, port.id)
        if err:
            return err
        self._save()
        return None

    def sell_fleet_ship(self, ship_name: str) -> tuple[int, str] | str:
        """Sell a docked fleet ship at a shipyard."""
        if not self.world:
            return "No active game"
        port = self.current_port
        if not port:
            return "Must be docked"
        from portlight.engine.models import PortFeature
        if PortFeature.SHIPYARD not in port.features:
            return f"{port.name} has no shipyard"
        from portlight.engine.fleet import sell_docked_ship
        result = sell_docked_ship(self.world.captain, ship_name, port.id)
        if isinstance(result, str):
            return result
        self._save()
        return result

    # --- Hire crew ---

    def hire_crew(self, count: int, role: str = "sailor") -> str | None:
        """Hire crew at port. Specify role (default: sailor). Returns error or None."""
        if not self.world:
            return "No active game"
        port = self.current_port
        if not port:
            return "Must be docked to hire crew"
        ship = self.world.captain.ship
        if not ship:
            return "No ship"
        from portlight.content.upgrades import UPGRADES as _UPG
        from portlight.engine.ship_stats import resolve_crew_max
        eff_crew_max = resolve_crew_max(ship, _UPG)
        space = eff_crew_max - ship.crew
        if space <= 0:
            return "Crew is already full"

        from portlight.engine.models import CrewRole
        try:
            crew_role = CrewRole(role.lower())
        except ValueError:
            return f"Unknown role: {role}. Valid: {', '.join(r.value for r in CrewRole)}"

        from portlight.content.crew_roles import ROLE_SPECS, get_role_count, set_role_count
        spec = ROLE_SPECS[crew_role]

        # Check role limit
        if spec.max_per_ship is not None:
            current = get_role_count(ship.roster, crew_role)
            avail = spec.max_per_ship - current
            if avail <= 0:
                return f"Already at maximum {spec.name}s ({spec.max_per_ship})"
            count = min(count, avail)

        count = min(count, space)
        # Sailors use port crew_cost, specialists cost wage * 10
        if crew_role == CrewRole.SAILOR:
            cost_per = port.crew_cost
        else:
            cost_per = spec.wage * 10
        cost = count * cost_per
        if cost > self.world.captain.silver:
            return f"Need {cost} silver for {count} {spec.name}(s) ({cost_per}/each), have {self.world.captain.silver}"

        self.world.captain.silver -= cost
        current = get_role_count(ship.roster, crew_role)
        set_role_count(ship.roster, crew_role, current + count)
        ship.sync_crew()

        # Generate named officers for specialist roles
        if crew_role != CrewRole.SAILOR:
            from portlight.engine.models import Officer
            from portlight.content.officer_names import generate_officer_name, generate_officer_trait
            region = port.region if port else "Mediterranean"
            for _ in range(count):
                name = generate_officer_name(region, self._rng)
                trait = generate_officer_trait(self._rng)
                ship.officers.append(Officer(
                    name=name,
                    role=crew_role,
                    origin_port=port.id if port else "",
                    trait=trait,
                ))

        self._save()
        return None

    def hunt(self):
        """Hunt/forage at port or sea. Applies yields and dangers, then saves.

        Same apply/save path as CLI ``portlight hunt``. Returns HuntResult on
        success or an error string.
        """
        if not self.world:
            return "No active game"
        from portlight.engine.hunting import hunt as do_hunt
        from portlight.engine.models import CargoItem, VoyageStatus

        location = "port"
        if self.world.voyage and self.world.voyage.status == VoyageStatus.AT_SEA:
            location = "sea"

        if location == "sea" and self.captain.ship and self.captain.ship.morale < 20:
            return "Crew morale too low for hunting at sea (need 20+)."

        crew_count = self.captain.ship.crew if self.captain.ship else 1
        result = do_hunt(self.captain, location, crew_count, self._rng)
        # hunt() advances captain.day but not world.day -- keep them in sync
        self.world.day = self.captain.day

        if result.success:
            if result.provisions_gained > 0:
                self.captain.provisions += result.provisions_gained
            if result.pelts_gained > 0:
                existing = next((c for c in self.captain.cargo if c.good_id == "pelts"), None)
                if existing:
                    existing.quantity += result.pelts_gained
                else:
                    acquired_port = self.current_port.id if self.current_port else ""
                    self.captain.cargo.append(CargoItem(
                        good_id="pelts", quantity=result.pelts_gained,
                        cost_basis=0, acquired_port=acquired_port,
                        acquired_region="", acquired_day=self.captain.day,
                    ))
            if result.silver_gained > 0:
                self.captain.silver += result.silver_gained

        if result.crew_lost > 0 and self.captain.ship:
            apply_crew_casualties(self.captain.ship, result.crew_lost, keep_at_least=1)
        if result.hull_damage > 0 and self.captain.ship:
            self.captain.ship.hull = max(1, self.captain.ship.hull - result.hull_damage)
        if result.morale_cost > 0 and self.captain.ship:
            self.captain.ship.morale = max(0, self.captain.ship.morale - result.morale_cost)

        self._save()
        return result

    def work(self) -> int | str:
        """Work the docks for a day. Returns silver earned or an error string.

        Same apply/save path as CLI ``portlight work``.
        """
        if not self.world:
            return "No active game"
        if not self.current_port:
            return "Must be docked to work the docks."
        from portlight.engine.economy import work_docks

        earned = work_docks(self.captain, self._rng)
        # work_docks() advances captain.day but not world.day -- keep them in sync
        self.world.day = self.captain.day
        self._save()
        return earned

    def snapshot(self) -> dict:
        """Stable JSON-safe dict for CLI --json (status/market/cargo/routes/contracts)."""
        if not self.world or not self.captain:
            return {
                "slot": self.slot,
                "day": 0,
                "at_sea": False,
                "captain": None,
                "port": None,
                "voyage": None,
                "cargo": [],
                "market": [],
                "routes": [],
                "board": {"offers": [], "active": []},
            }
        cap = self.captain
        port = self.current_port
        voyage = self.world.voyage
        cargo = [
            {
                "good_id": c.good_id,
                "quantity": c.quantity,
                "cost_basis": c.cost_basis,
                "acquired_port": c.acquired_port,
                "acquired_region": c.acquired_region,
                "acquired_day": c.acquired_day,
            }
            for c in (cap.cargo or [])
        ]
        market = []
        if port:
            for slot in port.market:
                market.append({
                    "good_id": slot.good_id,
                    "buy_price": slot.buy_price,
                    "sell_price": slot.sell_price,
                    "stock_current": slot.stock_current,
                    "stock_target": slot.stock_target,
                    "flood_penalty": slot.flood_penalty,
                })
        routes = []
        if port:
            for route in self.world.routes:
                dest_id = None
                if route.port_a == port.id:
                    dest_id = route.port_b
                elif route.port_b == port.id:
                    dest_id = route.port_a
                if dest_id is None:
                    continue
                dest = self.world.ports.get(dest_id)
                routes.append({
                    "port_a": route.port_a,
                    "port_b": route.port_b,
                    "destination_id": dest_id,
                    "destination_name": dest.name if dest else dest_id,
                    "distance": route.distance,
                    "danger": route.danger,
                })
        offers = []
        for o in self.board.offers:
            family = o.family.value if hasattr(o.family, "value") else o.family
            offers.append({
                "id": o.id,
                "title": o.title,
                "good_id": o.good_id,
                "quantity": o.quantity,
                "reward_silver": o.reward_silver,
                "bonus_reward": o.bonus_reward,
                "deadline_day": o.deadline_day,
                "destination_port_id": o.destination_port_id,
                "family": family,
            })
        active = []
        for c in self.board.active:
            family = c.family.value if hasattr(c.family, "value") else c.family
            status = c.status.value if hasattr(c.status, "value") else c.status
            active.append({
                "offer_id": c.offer_id,
                "title": c.title,
                "good_id": c.good_id,
                "required_quantity": c.required_quantity,
                "delivered_quantity": c.delivered_quantity,
                "reward_silver": c.reward_silver,
                "deadline_day": c.deadline_day,
                "destination_port_id": c.destination_port_id,
                "status": status,
                "family": family,
            })
        voyage_dict = None
        if voyage:
            status = voyage.status.value if hasattr(voyage.status, "value") else voyage.status
            voyage_dict = {
                "origin_id": voyage.origin_id,
                "destination_id": voyage.destination_id,
                "distance": voyage.distance,
                "progress": voyage.progress,
                "days_elapsed": voyage.days_elapsed,
                "status": status,
            }
        port_dict = None
        if port:
            port_dict = {"id": port.id, "name": port.name, "region": port.region}
        return {
            "slot": self.slot,
            "day": self.world.day,
            "at_sea": self.at_sea,
            "captain": {
                "name": cap.name,
                "captain_type": cap.captain_type,
                "silver": cap.silver,
                "provisions": cap.provisions,
                "day": cap.day,
                "reputation": cap.reputation,
            },
            "port": port_dict,
            "voyage": voyage_dict,
            "cargo": cargo,
            "market": market,
            "routes": routes,
            "board": {"offers": offers, "active": active},
        }

    def fire_crew(self, count: int = 1, role: str = "sailor") -> str | None:
        """Fire crew of a specific role. Returns error or None."""
        if not self.world:
            return "No active game"
        port = self.current_port
        if not port:
            return "Must be docked to fire crew"
        ship = self.world.captain.ship
        if not ship:
            return "No ship"

        from portlight.engine.models import CrewRole
        try:
            crew_role = CrewRole(role.lower())
        except ValueError:
            return f"Unknown role: {role}"

        from portlight.content.crew_roles import get_role_count, set_role_count
        current = get_role_count(ship.roster, crew_role)
        if current <= 0:
            return f"No {role}s to fire"
        fired = min(count, current)
        set_role_count(ship.roster, crew_role, current - fired)
        ship.sync_crew()

        # Remove named officers for specialist roles (remove from end)
        if crew_role != CrewRole.SAILOR:
            to_remove = fired
            new_officers = []
            for o in reversed(ship.officers):
                if o.role == crew_role and to_remove > 0:
                    to_remove -= 1
                else:
                    new_officers.append(o)
            ship.officers = list(reversed(new_officers))

        self._save()
        return None

    # --- Contracts ---

    def _refresh_board(self, port) -> None:
        """Generate fresh contract offers at the current port."""
        if not self.world:
            return
        if self.board.last_refresh_day == self.world.day:
            return  # already refreshed today
        # Compute infrastructure effects on contract board
        from portlight.content.infrastructure import LICENSE_CATALOG
        from portlight.engine.voyage import ship_class_rank
        effects = compute_board_effects(self.infra, port.region, LICENSE_CATALOG)
        ship = self.world.captain.ship
        ship_rank = ship_class_rank(ship.template_id) if ship else 0
        offers = generate_offers(
            CONTRACT_TEMPLATES,
            self.world,
            port,
            self.world.captain.standing,
            self.world.captain.captain_type,
            self._rng,
            player_ship_rank=ship_rank,
            max_offers=self.board.max_offers,
            board_effects=effects,
        )
        self.board.offers = offers
        self.board.last_refresh_day = self.world.day
        self._save()

    def accept_contract(self, offer_id: str) -> str | None:
        """Accept a contract offer. Returns error string or None on success."""
        if not self.world:
            return "No active game"
        result = accept_offer(self.board, offer_id, self.world.day)
        if isinstance(result, str):
            return result
        self._save()
        return None

    def abandon_contract_cmd(self, offer_id: str) -> str | None:
        """Abandon an active contract. Returns error string or None on success."""
        if not self.world:
            return "No active game"
        result = abandon_contract(self.board, offer_id, self.world.day)
        if isinstance(result, str):
            return result
        self._save()
        return None

    # --- Warehouses ---

    def lease_warehouse_cmd(self, tier_spec) -> str | None:
        """Lease a warehouse at current port. Returns error or None."""
        if not self.world:
            return "No active game"
        port = self.current_port
        if not port:
            return "Must be docked to lease a warehouse"
        result = lease_warehouse(
            self.infra, self.world.captain, port.id, tier_spec, self.world.day,
        )
        if isinstance(result, str):
            return result
        self._save()
        return None

    def deposit_cmd(self, good_id: str, qty: int) -> int | str:
        """Deposit cargo into warehouse. Returns qty deposited or error."""
        if not self.world:
            return "No active game"
        port = self.current_port
        if not port:
            return "Must be docked to deposit"
        result = deposit_cargo(
            self.infra, port.id, self.world.captain, good_id, qty, self.world.day,
        )
        if isinstance(result, str):
            return result
        self._save()
        return result

    def withdraw_cmd(self, good_id: str, qty: int, source_port: str | None = None) -> int | str:
        """Withdraw cargo from warehouse. Returns qty withdrawn or error."""
        if not self.world:
            return "No active game"
        port = self.current_port
        if not port:
            return "Must be docked to withdraw"
        result = withdraw_cargo(
            self.infra, port.id, self.world.captain, good_id, qty, source_port,
        )
        if isinstance(result, str):
            return result
        self._save()
        return result

    # --- Broker offices ---

    def open_broker_cmd(self, region: str, spec) -> str | None:
        """Open or upgrade a broker office. Returns error or None."""
        if not self.world:
            return "No active game"
        result = open_broker_office(
            self.infra, self.world.captain, region, spec, self.world.day,
        )
        if isinstance(result, str):
            return result
        self._save()
        return None

    # --- Licenses ---

    def purchase_license_cmd(self, spec) -> str | None:
        """Purchase a license. Returns error or None."""
        if not self.world:
            return "No active game"
        result = purchase_license(
            self.infra, self.world.captain, spec,
            self.world.captain.standing, self.world.day,
        )
        if isinstance(result, str):
            return result
        self._save()
        return None

    # --- Insurance ---

    def purchase_policy_cmd(
        self, spec, target_id: str = "", voyage_origin: str = "", voyage_destination: str = "",
    ) -> str | None:
        """Purchase an insurance policy. Returns error or None."""
        if not self.world:
            return "No active game"
        region = self._voyage_region() if self.at_sea else (
            self.current_port.region if self.current_port else "Mediterranean"
        )
        heat = self.world.captain.standing.customs_heat.get(region, 0)
        result = purchase_policy(
            self.infra, self.world.captain, spec, self.world.day,
            heat=heat, target_id=target_id,
            voyage_origin=voyage_origin, voyage_destination=voyage_destination,
        )
        if isinstance(result, str):
            return result
        self._save()
        return None

    def _resolve_event_insurance(self, event, voyage_destination: str = "") -> None:
        """Check active policies against a voyage event and resolve claims."""
        if not self.world:
            return

        incident_type = event.event_type.value if hasattr(event.event_type, 'value') else str(event.event_type)

        # Hull damage claim
        if event.hull_delta < 0:
            # Estimate hull repair value (3 silver per HP is base repair cost)
            hull_loss_value = abs(event.hull_delta) * 3
            resolve_claim(
                self.infra, self.world.captain,
                incident_type, hull_loss_value, self.world.day,
                voyage_destination=voyage_destination,
            )

        # Cargo loss claim
        if event.cargo_lost:
            for good_id, qty in event.cargo_lost.items():
                good = GOODS.get(good_id)
                if not good:
                    continue
                cargo_value = good.base_price * qty
                cargo_category = good.category.value if good.category else ""
                resolve_claim(
                    self.infra, self.world.captain,
                    incident_type, cargo_value, self.world.day,
                    cargo_category=cargo_category,
                    voyage_destination=voyage_destination,
                )

        # Silver loss from fines/fees (not insurable for hull/cargo,
        # but inspection silver loss is effectively a fine — not covered separately)

    # --- Campaign ---

    def _build_snapshot(self) -> SessionSnapshot:
        """Build a read-only snapshot for campaign evaluation."""
        return SessionSnapshot(
            captain=self.world.captain,
            world=self.world,
            board=self.board,
            infra=self.infra,
            ledger=self.ledger,
            campaign=self.campaign,
        )

    def _evaluate_campaign(self) -> list:
        """Evaluate milestones and victory closure. Returns newly completed milestones.

        Newly completed milestone/path ids are stashed on last_milestone_ids /
        last_path_ids so TUI execute_advance can notify without changing
        advance() return type (callers expect voyage events).
        """
        from portlight.content.campaign import MILESTONE_SPECS
        from portlight.engine.campaign import evaluate_victory_closure
        self.last_milestone_ids = []
        self.last_path_ids = []
        snap = self._build_snapshot()
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        if newly:
            self.campaign.completed.extend(newly)
            # Re-snapshot after milestone updates for victory evaluation
            snap = self._build_snapshot()
        # Check for victory path completion
        victory_newly = evaluate_victory_closure(snap)
        if victory_newly:
            self.campaign.completed_paths.extend(victory_newly)
        self.last_milestone_ids = [c.milestone_id for c in newly]
        self.last_path_ids = [p.path_id for p in victory_newly]
        return newly

    # --- Narrative ---

    def _evaluate_narrative(self, events_this_turn: list | None = None) -> list:
        """Evaluate narrative beats based on current game state."""
        if not self.world:
            return []
        return evaluate_narrative(
            self.narrative,
            self.world.captain,
            self.world,
            self.board,
            self.infra,
            self.ledger,
            current_port_id=self.current_port_id,
            events_this_turn=events_this_turn,
        )

    # --- Credit ---

    def open_credit_cmd(self, spec) -> str | None:
        """Open or upgrade a credit line. Returns error or None."""
        if not self.world:
            return "No active game"
        result = open_credit_line(
            self.infra, spec, self.world.captain.standing, self.world.day,
        )
        if isinstance(result, str):
            return result
        self._save()
        return None

    def draw_credit_cmd(self, amount: int) -> str | None:
        """Borrow from credit line. Returns error or None."""
        if not self.world:
            return "No active game"
        result = draw_credit(self.infra, self.world.captain, amount)
        if isinstance(result, str):
            return result
        self._save()
        return None

    def repay_credit_cmd(self, amount: int) -> str | None:
        """Repay credit debt. Returns error or None."""
        if not self.world:
            return "No active game"
        result = repay_credit(self.infra, self.world.captain, amount)
        if isinstance(result, str):
            return result
        self._save()
        return None
