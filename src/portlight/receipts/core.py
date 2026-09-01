"""Receipt hashing and export.

Contract:
  - hash_receipt(receipt) -> deterministic SHA-256 hex digest
  - export_ledger(ledger) -> JSON string (human-readable)
  - verify_receipt(receipt) -> bool (receipt_id matches recomputed hash)
"""

from __future__ import annotations

import json
from dataclasses import asdict

from portlight.receipts.models import ReceiptLedger, TradeReceipt, compute_receipt_hash

_HEX = frozenset("0123456789abcdef")


def hash_receipt(receipt: TradeReceipt) -> str:
    """Deterministic hash of a receipt's core trade data (excludes timestamp)."""
    return compute_receipt_hash(receipt)


def _is_economy_receipt_id(value: str) -> bool:
    """Live engine ids are a 16-char sha256 prefix (captain:port:good:day:seq)."""
    return len(value) == 16 and all(c in _HEX for c in value)


def verify_receipt(receipt: TradeReceipt) -> bool:
    """Return whether the stored hash matches a recomputation of the payload.

    Accepts either receipt_id == hash_receipt(receipt) (64-char content hash)
    or a live 16-char economy id whose content_hash matches. Empty or
    tampered ids fail. A len()>0 check is not verification.
    """
    if not receipt.receipt_id:
        return False
    expected = hash_receipt(receipt)
    if not expected:
        return False
    if receipt.receipt_id == expected:
        return True
    stored = receipt.content_hash
    return stored == expected and _is_economy_receipt_id(receipt.receipt_id)


def export_ledger(ledger: ReceiptLedger) -> str:
    """Export full ledger as pretty-printed JSON."""
    data = asdict(ledger)
    return json.dumps(data, indent=2, ensure_ascii=False)


def export_ledger_to_file(ledger: ReceiptLedger, path: str) -> None:
    """Write ledger JSON to a file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(export_ledger(ledger))
