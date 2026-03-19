"""Save/load system — serialize WorldState to/from JSON.

Contract:
  - save_game(world, path) → writes JSON file
  - load_game(path) → WorldState | None
  - WorldState round-trips without data loss
"""

from __future__ import annotations

import json
from pathlib import Path

from portlight.engine.models import (
    Captain,
    CargoItem,
    GoodCategory,
    MarketSlot,
    Port,
    PortFeature,
    ReputationIncident,
    ReputationState,
    Route,
    Ship,
    VoyageState,
    VoyageStatus,
    WorldState,
)
from portlight.engine.contracts import (
    ActiveContract,
    ContractBoard,
    ContractFamily,
    ContractOffer,
    ContractOutcome,
    ContractStatus,
)
from portlight.engine.infrastructure import (
    BrokerOffice,
    BrokerTier,
    InfrastructureState,
    OwnedLicense,
    StoredLot,
    WarehouseLease,
    WarehouseTier,
)
from portlight.receipts.models import ReceiptLedger, TradeAction, TradeReceipt

SAVE_DIR = "saves"
SAVE_FILE = "portlight_save.json"


def _ship_to_dict(ship: Ship) -> dict:
    return {
        "template_id": ship.template_id,
        "name": ship.name,
        "hull": ship.hull,
        "hull_max": ship.hull_max,
        "cargo_capacity": ship.cargo_capacity,
        "speed": ship.speed,
        "crew": ship.crew,
        "crew_max": ship.crew_max,
    }


def _ship_from_dict(d: dict) -> Ship:
    return Ship(**d)


def _incident_to_dict(inc: ReputationIncident) -> dict:
    return {
        "day": inc.day,
        "port_id": inc.port_id,
        "region": inc.region,
        "incident_type": inc.incident_type,
        "description": inc.description,
        "heat_delta": inc.heat_delta,
        "standing_delta": inc.standing_delta,
        "trust_delta": inc.trust_delta,
    }


def _incident_from_dict(d: dict) -> ReputationIncident:
    return ReputationIncident(**d)


def _reputation_to_dict(rep: ReputationState) -> dict:
    return {
        "regional_standing": rep.regional_standing,
        "port_standing": rep.port_standing,
        "customs_heat": rep.customs_heat,
        "commercial_trust": rep.commercial_trust,
        "recent_incidents": [_incident_to_dict(i) for i in rep.recent_incidents],
    }


def _reputation_from_dict(d: dict) -> ReputationState:
    incidents = [_incident_from_dict(i) for i in d.get("recent_incidents", [])]
    return ReputationState(
        regional_standing=d.get("regional_standing", {"Mediterranean": 0, "West Africa": 0, "East Indies": 0}),
        port_standing=d.get("port_standing", {}),
        customs_heat=d.get("customs_heat", {"Mediterranean": 0, "West Africa": 0, "East Indies": 0}),
        commercial_trust=d.get("commercial_trust", 0),
        recent_incidents=incidents,
    )


def _captain_to_dict(captain: Captain) -> dict:
    return {
        "name": captain.name,
        "captain_type": captain.captain_type,
        "silver": captain.silver,
        "reputation": captain.reputation,
        "ship": _ship_to_dict(captain.ship) if captain.ship else None,
        "cargo": [{
            "good_id": c.good_id, "quantity": c.quantity, "cost_basis": c.cost_basis,
            "acquired_port": c.acquired_port, "acquired_region": c.acquired_region,
            "acquired_day": c.acquired_day,
        } for c in captain.cargo],
        "provisions": captain.provisions,
        "day": captain.day,
        "standing": _reputation_to_dict(captain.standing),
    }


def _cargo_from_dict(c: dict) -> CargoItem:
    return CargoItem(
        good_id=c["good_id"], quantity=c["quantity"],
        cost_basis=c.get("cost_basis", 0),
        acquired_port=c.get("acquired_port", ""),
        acquired_region=c.get("acquired_region", ""),
        acquired_day=c.get("acquired_day", 0),
    )


def _captain_from_dict(d: dict) -> Captain:
    standing = _reputation_from_dict(d["standing"]) if "standing" in d else ReputationState()
    return Captain(
        name=d["name"],
        captain_type=d.get("captain_type", "merchant"),
        silver=d["silver"],
        reputation=d.get("reputation", 0),
        ship=_ship_from_dict(d["ship"]) if d.get("ship") else None,
        cargo=[_cargo_from_dict(c) for c in d.get("cargo", [])],
        provisions=d["provisions"],
        day=d["day"],
        standing=standing,
    )


def _slot_to_dict(slot: MarketSlot) -> dict:
    return {
        "good_id": slot.good_id,
        "stock_current": slot.stock_current,
        "stock_target": slot.stock_target,
        "restock_rate": slot.restock_rate,
        "local_affinity": slot.local_affinity,
        "spread": slot.spread,
        "buy_price": slot.buy_price,
        "sell_price": slot.sell_price,
        "flood_penalty": slot.flood_penalty,
    }


def _slot_from_dict(d: dict) -> MarketSlot:
    return MarketSlot(**d)


def _port_to_dict(port: Port) -> dict:
    return {
        "id": port.id,
        "name": port.name,
        "description": port.description,
        "region": port.region,
        "features": [f.value for f in port.features],
        "market": [_slot_to_dict(s) for s in port.market],
        "port_fee": port.port_fee,
        "provision_cost": port.provision_cost,
        "repair_cost": port.repair_cost,
        "crew_cost": port.crew_cost,
    }


def _port_from_dict(d: dict) -> Port:
    return Port(
        id=d["id"],
        name=d["name"],
        description=d["description"],
        region=d["region"],
        features=[PortFeature(f) for f in d.get("features", [])],
        market=[_slot_from_dict(s) for s in d.get("market", [])],
        port_fee=d.get("port_fee", 5),
        provision_cost=d.get("provision_cost", 2),
        repair_cost=d.get("repair_cost", 3),
        crew_cost=d.get("crew_cost", 5),
    )


def _voyage_to_dict(voyage: VoyageState) -> dict:
    return {
        "origin_id": voyage.origin_id,
        "destination_id": voyage.destination_id,
        "distance": voyage.distance,
        "progress": voyage.progress,
        "days_elapsed": voyage.days_elapsed,
        "status": voyage.status.value,
    }


def _voyage_from_dict(d: dict) -> VoyageState:
    return VoyageState(
        origin_id=d["origin_id"],
        destination_id=d["destination_id"],
        distance=d["distance"],
        progress=d.get("progress", 0),
        days_elapsed=d.get("days_elapsed", 0),
        status=VoyageStatus(d["status"]),
    )


def _receipt_to_dict(r: TradeReceipt) -> dict:
    return {
        "receipt_id": r.receipt_id,
        "captain_name": r.captain_name,
        "port_id": r.port_id,
        "good_id": r.good_id,
        "action": r.action.value,
        "quantity": r.quantity,
        "unit_price": r.unit_price,
        "total_price": r.total_price,
        "day": r.day,
        "timestamp": r.timestamp,
        "stock_before": r.stock_before,
        "stock_after": r.stock_after,
    }


def _receipt_from_dict(d: dict) -> TradeReceipt:
    return TradeReceipt(
        receipt_id=d["receipt_id"],
        captain_name=d["captain_name"],
        port_id=d["port_id"],
        good_id=d["good_id"],
        action=TradeAction(d["action"]),
        quantity=d["quantity"],
        unit_price=d["unit_price"],
        total_price=d["total_price"],
        day=d["day"],
        timestamp=d.get("timestamp", ""),
        stock_before=d.get("stock_before", 0),
        stock_after=d.get("stock_after", 0),
    )


def _offer_to_dict(o: ContractOffer) -> dict:
    return {
        "id": o.id,
        "template_id": o.template_id,
        "family": o.family.value,
        "title": o.title,
        "description": o.description,
        "issuer_port_id": o.issuer_port_id,
        "destination_port_id": o.destination_port_id,
        "good_id": o.good_id,
        "quantity": o.quantity,
        "created_day": o.created_day,
        "deadline_day": o.deadline_day,
        "reward_silver": o.reward_silver,
        "bonus_reward": o.bonus_reward,
        "required_trust_tier": o.required_trust_tier,
        "required_standing": o.required_standing,
        "heat_ceiling": o.heat_ceiling,
        "inspection_modifier": o.inspection_modifier,
        "source_region": o.source_region,
        "source_port": o.source_port,
        "offer_reason": o.offer_reason,
        "tags": o.tags,
        "acceptance_window": o.acceptance_window,
    }


def _offer_from_dict(d: dict) -> ContractOffer:
    return ContractOffer(
        id=d["id"],
        template_id=d["template_id"],
        family=ContractFamily(d["family"]),
        title=d["title"],
        description=d["description"],
        issuer_port_id=d["issuer_port_id"],
        destination_port_id=d["destination_port_id"],
        good_id=d["good_id"],
        quantity=d["quantity"],
        created_day=d["created_day"],
        deadline_day=d["deadline_day"],
        reward_silver=d["reward_silver"],
        bonus_reward=d.get("bonus_reward", 0),
        required_trust_tier=d.get("required_trust_tier", "unproven"),
        required_standing=d.get("required_standing", 0),
        heat_ceiling=d.get("heat_ceiling"),
        inspection_modifier=d.get("inspection_modifier", 0.0),
        source_region=d.get("source_region"),
        source_port=d.get("source_port"),
        offer_reason=d.get("offer_reason", ""),
        tags=d.get("tags", []),
        acceptance_window=d.get("acceptance_window", 10),
    )


def _active_contract_to_dict(c: ActiveContract) -> dict:
    return {
        "offer_id": c.offer_id,
        "template_id": c.template_id,
        "family": c.family.value,
        "title": c.title,
        "accepted_day": c.accepted_day,
        "deadline_day": c.deadline_day,
        "destination_port_id": c.destination_port_id,
        "good_id": c.good_id,
        "required_quantity": c.required_quantity,
        "delivered_quantity": c.delivered_quantity,
        "reward_silver": c.reward_silver,
        "bonus_reward": c.bonus_reward,
        "source_region": c.source_region,
        "source_port": c.source_port,
        "inspection_modifier": c.inspection_modifier,
        "status": c.status.value,
    }


def _active_contract_from_dict(d: dict) -> ActiveContract:
    return ActiveContract(
        offer_id=d["offer_id"],
        template_id=d["template_id"],
        family=ContractFamily(d["family"]),
        title=d["title"],
        accepted_day=d["accepted_day"],
        deadline_day=d["deadline_day"],
        destination_port_id=d["destination_port_id"],
        good_id=d["good_id"],
        required_quantity=d["required_quantity"],
        delivered_quantity=d.get("delivered_quantity", 0),
        reward_silver=d.get("reward_silver", 0),
        bonus_reward=d.get("bonus_reward", 0),
        source_region=d.get("source_region"),
        source_port=d.get("source_port"),
        inspection_modifier=d.get("inspection_modifier", 0.0),
        status=ContractStatus(d.get("status", "accepted")),
    )


def _outcome_to_dict(o: ContractOutcome) -> dict:
    return {
        "contract_id": o.contract_id,
        "outcome_type": o.outcome_type,
        "silver_delta": o.silver_delta,
        "trust_delta": o.trust_delta,
        "standing_delta": o.standing_delta,
        "heat_delta": o.heat_delta,
        "completion_day": o.completion_day,
        "summary": o.summary,
    }


def _outcome_from_dict(d: dict) -> ContractOutcome:
    return ContractOutcome(**d)


def _board_to_dict(board: ContractBoard) -> dict:
    return {
        "offers": [_offer_to_dict(o) for o in board.offers],
        "active": [_active_contract_to_dict(c) for c in board.active],
        "completed": [_outcome_to_dict(o) for o in board.completed],
        "last_refresh_day": board.last_refresh_day,
        "max_offers": board.max_offers,
    }


def _board_from_dict(d: dict) -> ContractBoard:
    return ContractBoard(
        offers=[_offer_from_dict(o) for o in d.get("offers", [])],
        active=[_active_contract_from_dict(c) for c in d.get("active", [])],
        completed=[_outcome_from_dict(o) for o in d.get("completed", [])],
        last_refresh_day=d.get("last_refresh_day", 0),
        max_offers=d.get("max_offers", 5),
    )


def _stored_lot_to_dict(lot: StoredLot) -> dict:
    return {
        "good_id": lot.good_id,
        "quantity": lot.quantity,
        "acquired_port": lot.acquired_port,
        "acquired_region": lot.acquired_region,
        "acquired_day": lot.acquired_day,
        "deposited_day": lot.deposited_day,
    }


def _stored_lot_from_dict(d: dict) -> StoredLot:
    return StoredLot(**d)


def _warehouse_to_dict(w: WarehouseLease) -> dict:
    return {
        "id": w.id,
        "port_id": w.port_id,
        "tier": w.tier.value,
        "capacity": w.capacity,
        "lease_cost": w.lease_cost,
        "upkeep_per_day": w.upkeep_per_day,
        "inventory": [_stored_lot_to_dict(lot) for lot in w.inventory],
        "opened_day": w.opened_day,
        "upkeep_paid_through": w.upkeep_paid_through,
        "active": w.active,
    }


def _warehouse_from_dict(d: dict) -> WarehouseLease:
    return WarehouseLease(
        id=d["id"],
        port_id=d["port_id"],
        tier=WarehouseTier(d["tier"]),
        capacity=d["capacity"],
        lease_cost=d.get("lease_cost", 0),
        upkeep_per_day=d.get("upkeep_per_day", 1),
        inventory=[_stored_lot_from_dict(lot) for lot in d.get("inventory", [])],
        opened_day=d.get("opened_day", 0),
        upkeep_paid_through=d.get("upkeep_paid_through", 0),
        active=d.get("active", True),
    )


def _broker_to_dict(b: BrokerOffice) -> dict:
    return {
        "region": b.region,
        "tier": b.tier.value,
        "opened_day": b.opened_day,
        "upkeep_paid_through": b.upkeep_paid_through,
        "active": b.active,
    }


def _broker_from_dict(d: dict) -> BrokerOffice:
    return BrokerOffice(
        region=d["region"],
        tier=BrokerTier(d.get("tier", "none")),
        opened_day=d.get("opened_day", 0),
        upkeep_paid_through=d.get("upkeep_paid_through", 0),
        active=d.get("active", True),
    )


def _license_to_dict(lic: OwnedLicense) -> dict:
    return {
        "license_id": lic.license_id,
        "purchased_day": lic.purchased_day,
        "upkeep_paid_through": lic.upkeep_paid_through,
        "active": lic.active,
    }


def _license_from_dict(d: dict) -> OwnedLicense:
    return OwnedLicense(
        license_id=d["license_id"],
        purchased_day=d.get("purchased_day", 0),
        upkeep_paid_through=d.get("upkeep_paid_through", 0),
        active=d.get("active", True),
    )


def _infra_to_dict(state: InfrastructureState) -> dict:
    return {
        "warehouses": [_warehouse_to_dict(w) for w in state.warehouses],
        "brokers": [_broker_to_dict(b) for b in state.brokers],
        "licenses": [_license_to_dict(lic) for lic in state.licenses],
    }


def _infra_from_dict(d: dict) -> InfrastructureState:
    return InfrastructureState(
        warehouses=[_warehouse_from_dict(w) for w in d.get("warehouses", [])],
        brokers=[_broker_from_dict(b) for b in d.get("brokers", [])],
        licenses=[_license_from_dict(lic) for lic in d.get("licenses", [])],
    )


def _ledger_to_dict(ledger: ReceiptLedger) -> dict:
    return {
        "run_id": ledger.run_id,
        "receipts": [_receipt_to_dict(r) for r in ledger.receipts],
        "total_buys": ledger.total_buys,
        "total_sells": ledger.total_sells,
        "net_profit": ledger.net_profit,
    }


def _ledger_from_dict(d: dict) -> ReceiptLedger:
    ledger = ReceiptLedger(
        run_id=d.get("run_id", ""),
        total_buys=d.get("total_buys", 0),
        total_sells=d.get("total_sells", 0),
        net_profit=d.get("net_profit", 0),
    )
    ledger.receipts = [_receipt_from_dict(r) for r in d.get("receipts", [])]
    return ledger


def world_to_dict(
    world: WorldState,
    ledger: ReceiptLedger | None = None,
    board: ContractBoard | None = None,
    infra: InfrastructureState | None = None,
) -> dict:
    """Serialize full game state to a JSON-safe dict."""
    return {
        "version": 1,
        "captain": _captain_to_dict(world.captain),
        "ports": {pid: _port_to_dict(p) for pid, p in world.ports.items()},
        "routes": [{"port_a": r.port_a, "port_b": r.port_b, "distance": r.distance, "danger": r.danger, "min_ship_class": r.min_ship_class} for r in world.routes],
        "voyage": _voyage_to_dict(world.voyage) if world.voyage else None,
        "day": world.day,
        "seed": world.seed,
        "ledger": _ledger_to_dict(ledger) if ledger else None,
        "contract_board": _board_to_dict(board) if board else None,
        "infrastructure": _infra_to_dict(infra) if infra else None,
    }


def world_from_dict(d: dict) -> tuple[WorldState, ReceiptLedger, ContractBoard, InfrastructureState]:
    """Deserialize game state from dict. Returns (world, ledger, board, infra)."""
    world = WorldState(
        captain=_captain_from_dict(d["captain"]),
        ports={pid: _port_from_dict(p) for pid, p in d["ports"].items()},
        routes=[Route(**r) for r in d["routes"]],
        voyage=_voyage_from_dict(d["voyage"]) if d.get("voyage") else None,
        day=d["day"],
        seed=d.get("seed", 0),
    )
    ledger = _ledger_from_dict(d["ledger"]) if d.get("ledger") else ReceiptLedger()
    board = _board_from_dict(d["contract_board"]) if d.get("contract_board") else ContractBoard()
    infra = _infra_from_dict(d["infrastructure"]) if d.get("infrastructure") else InfrastructureState()
    return world, ledger, board, infra


def save_game(
    world: WorldState,
    ledger: ReceiptLedger | None = None,
    board: ContractBoard | None = None,
    infra: InfrastructureState | None = None,
    base_path: Path | None = None,
) -> Path:
    """Save game state to JSON file. Returns path written."""
    base = base_path or Path(".")
    save_dir = base / SAVE_DIR
    save_dir.mkdir(parents=True, exist_ok=True)
    save_path = save_dir / SAVE_FILE
    data = world_to_dict(world, ledger, board, infra)
    save_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return save_path


def load_game(base_path: Path | None = None) -> tuple[WorldState, ReceiptLedger, ContractBoard, InfrastructureState] | None:
    """Load game state from JSON file. Returns None if no save exists or data is corrupt."""
    base = base_path or Path(".")
    save_path = base / SAVE_DIR / SAVE_FILE
    if not save_path.exists():
        return None
    try:
        data = json.loads(save_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    try:
        return world_from_dict(data)
    except (KeyError, TypeError, ValueError):
        return None
