"""Session manager — load/save active run, command context.

The session is the bridge between CLI commands and engine state.
Every command goes through the session to ensure state is consistent
and saved after mutations.
"""

from __future__ import annotations

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
from portlight.engine.save import load_game, save_game
from portlight.engine.voyage import EventType, advance_day, arrive, depart
from portlight.receipts.models import ReceiptLedger, TradeReceipt


class GameSession:
    """Holds active game state and mediates all player actions."""

    def __init__(self, base_path: Path | None = None) -> None:
        self.base_path = base_path or Path(".")
        self.world: WorldState | None = None
        self.ledger: ReceiptLedger = ReceiptLedger()
        self.board: ContractBoard = ContractBoard()
        self.infra: InfrastructureState = InfrastructureState()
        self.campaign: CampaignState = CampaignState()
        self._trade_seq: int = 0
        self._rng: random.Random = random.Random()

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
    ) -> None:
        """Start a fresh game. captain_type: 'merchant', 'smuggler', or 'navigator'."""
        ct = CaptainType(captain_type)
        self.world = new_game(captain_name, starting_port, ct)
        self._rng = random.Random(self.world.seed)
        self.ledger = ReceiptLedger(run_id=f"run-{self.world.seed}")
        self.board = ContractBoard()
        self.infra = InfrastructureState()
        self.campaign = CampaignState()
        self._trade_seq = 0
        self._save()

    def load(self) -> bool:
        """Load saved game. Returns True if loaded."""
        result = load_game(self.base_path)
        if result is None:
            return False
        self.world, self.ledger, self.board, self.infra, self.campaign = result
        self._rng = random.Random(self.world.seed + self.world.day)
        self._trade_seq = len(self.ledger.receipts)
        return True

    @property
    def _pricing(self):
        """Captain's pricing modifiers for economy calls."""
        t = self.captain_template
        return t.pricing if t else None

    def _save(self) -> None:
        """Auto-save after every mutation."""
        if self.world:
            save_game(self.world, self.ledger, self.board, self.infra, self.campaign, self.base_path)

    def _recalc(self, port) -> None:
        """Recalculate prices at a port with captain modifiers."""
        recalculate_prices(port, GOODS, self._pricing)

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
        cargo_item = next((c for c in self.world.captain.cargo if c.good_id == good_id), None)
        cargo_source_port = cargo_item.acquired_port if cargo_item else port.id
        cargo_source_region = cargo_item.acquired_region if cargo_item else port.region

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

    def sail(self, destination_id: str) -> str | None:
        """Depart for destination. Returns error string or None on success."""
        if not self.world:
            return "No active game"
        result = depart(self.world, destination_id)
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
        tick_infrastructure(self.infra, self.world.captain, self.world.day)

        # Daily credit tick (interest, due dates, defaults)
        credit_msgs = tick_credit(self.infra, self.world.captain, self.world.day)
        # Credit default damages trust
        for msg in credit_msgs:
            if "DEFAULT" in msg:
                self.world.captain.standing.commercial_trust = max(
                    0, self.world.captain.standing.commercial_trust - 15,
                )

        if not self.at_sea:
            # In port: tick markets forward
            tick_markets(self.world.ports, days=1, rng=self._rng)
            self.world.day += 1
            self.world.captain.day += 1
            for port in self.world.ports.values():
                self._recalc(port)
            self._evaluate_campaign()
            self._save()
            return []

        events = advance_day(self.world, self._rng)

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
                self._recalc(port)
                self._refresh_board(port)

        # Recalculate all markets (time passes)
        for port in self.world.ports.values():
            self._recalc(port)

        # Evaluate campaign milestones
        self._evaluate_campaign()

        self._save()
        return events

    def _voyage_region(self) -> str:
        """Best guess of the current voyage's region (use destination port)."""
        if self.world and self.world.voyage:
            dest = self.world.ports.get(self.world.voyage.destination_id)
            if dest:
                return dest.region
        return "Mediterranean"

    # --- Provisioning & Repair ---

    def _service_mult(self) -> float:
        """Get service cost multiplier from port standing reputation."""
        port = self.current_port
        if not port or not self.world:
            return 1.0
        return get_service_modifier(self.world.captain.standing, port.id)

    def provision(self, days: int) -> str | None:
        """Buy provisions at port-specific cost. Returns error or None."""
        if not self.world:
            return "No active game"
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

        # Sell old ship for 40% of its template price
        old_template = SHIPS.get(self.world.captain.ship.template_id)
        if old_template:
            self.world.captain.silver += int(old_template.price * 0.4)

        self.world.captain.silver -= template.price
        self.world.captain.ship = create_ship_from_template(template)

        # Transfer cargo (drop excess if new ship is smaller)
        cargo_used = sum(c.quantity for c in self.world.captain.cargo)
        if cargo_used > template.cargo_capacity:
            # Drop from the end until it fits
            while sum(c.quantity for c in self.world.captain.cargo) > template.cargo_capacity:
                self.world.captain.cargo.pop()

        self._save()
        return None

    # --- Hire crew ---

    def hire_crew(self, count: int) -> str | None:
        """Hire crew at port-specific cost. Returns error or None."""
        if not self.world:
            return "No active game"
        port = self.current_port
        if not port:
            return "Must be docked to hire crew"
        ship = self.world.captain.ship
        if not ship:
            return "No ship"
        space = ship.crew_max - ship.crew
        if space == 0:
            return "Crew is already full"
        count = min(count, space)
        cost_per = port.crew_cost
        cost = count * cost_per
        if cost > self.world.captain.silver:
            return f"Need {cost} silver for {count} crew ({cost_per}/each here), have {self.world.captain.silver}"
        self.world.captain.silver -= cost
        ship.crew += count
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
        effects = compute_board_effects(self.infra, port.region, LICENSE_CATALOG)
        offers = generate_offers(
            CONTRACT_TEMPLATES,
            self.world,
            port,
            self.world.captain.standing,
            self.world.captain.captain_type,
            self._rng,
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
        """Evaluate milestones and victory closure. Returns newly completed milestones."""
        from portlight.content.campaign import MILESTONE_SPECS
        from portlight.engine.campaign import evaluate_victory_closure
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
        return newly

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
