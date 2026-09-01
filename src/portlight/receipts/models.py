"""Trade receipt schema — the verifiable proof trail.

Receipts are deterministic: same inputs -> same ID and hash.
This module defines the schema only; hashing and export live in receipts.core.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class TradeAction(str, Enum):
    BUY = "buy"
    SELL = "sell"


def compute_receipt_hash(receipt: "TradeReceipt") -> str:
    """SHA-256 of core trade fields (excludes timestamp, receipt_id, content_hash)."""
    payload = (
        f"{receipt.captain_name}:{receipt.port_id}:{receipt.good_id}:"
        f"{receipt.action.value}:{receipt.quantity}:{receipt.unit_price}:"
        f"{receipt.day}:{receipt.stock_before}:{receipt.stock_after}"
    )
    return hashlib.sha256(payload.encode()).hexdigest()


@dataclass
class TradeReceipt:
    """One completed trade transaction."""
    receipt_id: str                  # engine: 16-char id; or full content hash
    captain_name: str
    port_id: str
    good_id: str
    action: TradeAction
    quantity: int
    unit_price: int
    total_price: int
    day: int                         # in-game day
    timestamp: str = ""              # ISO 8601 wall clock (for export)
    stock_before: int = 0            # port stock before trade
    stock_after: int = 0             # port stock after trade
    content_hash: str = ""           # hash_receipt payload; stamped at creation

    def __post_init__(self) -> None:
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()
        if not self.content_hash:
            self.content_hash = compute_receipt_hash(self)


@dataclass
class ReceiptLedger:
    """Ordered collection of all trade receipts for one game run."""
    run_id: str = ""                 # unique per save/run
    receipts: list[TradeReceipt] = field(default_factory=list)
    total_buys: int = 0
    total_sells: int = 0
    net_profit: int = 0

    def append(self, receipt: TradeReceipt) -> None:
        self.receipts.append(receipt)
        if receipt.action == TradeAction.BUY:
            self.total_buys += receipt.total_price
        else:
            self.total_sells += receipt.total_price
        self.net_profit = self.total_sells - self.total_buys
