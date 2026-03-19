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
    ReputationState,
    Route,
    Ship,
    VoyageState,
    VoyageStatus,
    WorldState,
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


def _reputation_to_dict(rep: ReputationState) -> dict:
    return {
        "regional_standing": rep.regional_standing,
        "port_standing": rep.port_standing,
        "customs_heat": rep.customs_heat,
        "commercial_trust": rep.commercial_trust,
    }


def _reputation_from_dict(d: dict) -> ReputationState:
    return ReputationState(
        regional_standing=d.get("regional_standing", {"Mediterranean": 0, "West Africa": 0, "East Indies": 0}),
        port_standing=d.get("port_standing", {}),
        customs_heat=d.get("customs_heat", {"Mediterranean": 0, "West Africa": 0, "East Indies": 0}),
        commercial_trust=d.get("commercial_trust", 0),
    )


def _captain_to_dict(captain: Captain) -> dict:
    return {
        "name": captain.name,
        "captain_type": captain.captain_type,
        "silver": captain.silver,
        "reputation": captain.reputation,
        "ship": _ship_to_dict(captain.ship) if captain.ship else None,
        "cargo": [{"good_id": c.good_id, "quantity": c.quantity, "cost_basis": c.cost_basis} for c in captain.cargo],
        "provisions": captain.provisions,
        "day": captain.day,
        "standing": _reputation_to_dict(captain.standing),
    }


def _captain_from_dict(d: dict) -> Captain:
    standing = _reputation_from_dict(d["standing"]) if "standing" in d else ReputationState()
    return Captain(
        name=d["name"],
        captain_type=d.get("captain_type", "merchant"),
        silver=d["silver"],
        reputation=d.get("reputation", 0),
        ship=_ship_from_dict(d["ship"]) if d.get("ship") else None,
        cargo=[CargoItem(**c) for c in d.get("cargo", [])],
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


def world_to_dict(world: WorldState, ledger: ReceiptLedger | None = None) -> dict:
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
    }


def world_from_dict(d: dict) -> tuple[WorldState, ReceiptLedger]:
    """Deserialize game state from dict. Returns (world, ledger)."""
    world = WorldState(
        captain=_captain_from_dict(d["captain"]),
        ports={pid: _port_from_dict(p) for pid, p in d["ports"].items()},
        routes=[Route(**r) for r in d["routes"]],
        voyage=_voyage_from_dict(d["voyage"]) if d.get("voyage") else None,
        day=d["day"],
        seed=d.get("seed", 0),
    )
    ledger = _ledger_from_dict(d["ledger"]) if d.get("ledger") else ReceiptLedger()
    return world, ledger


def save_game(world: WorldState, ledger: ReceiptLedger | None = None, base_path: Path | None = None) -> Path:
    """Save game state to JSON file. Returns path written."""
    base = base_path or Path(".")
    save_dir = base / SAVE_DIR
    save_dir.mkdir(parents=True, exist_ok=True)
    save_path = save_dir / SAVE_FILE
    data = world_to_dict(world, ledger)
    save_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return save_path


def load_game(base_path: Path | None = None) -> tuple[WorldState, ReceiptLedger] | None:
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
