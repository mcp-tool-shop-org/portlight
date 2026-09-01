"""Tests for the receipt system — hashing, ledger, export."""

import json

from portlight.receipts.core import export_ledger, hash_receipt, verify_receipt
from portlight.receipts.models import ReceiptLedger, TradeAction, TradeReceipt


def _make_receipt(**overrides) -> TradeReceipt:
    defaults = dict(
        receipt_id="abc123",
        captain_name="Tester",
        port_id="porto_novo",
        good_id="grain",
        action=TradeAction.BUY,
        quantity=10,
        unit_price=12,
        total_price=120,
        day=1,
        stock_before=40,
        stock_after=30,
    )
    defaults.update(overrides)
    return TradeReceipt(**defaults)


class TestReceiptHashing:
    def test_deterministic(self):
        r = _make_receipt()
        h1 = hash_receipt(r)
        h2 = hash_receipt(r)
        assert h1 == h2

    def test_different_data_different_hash(self):
        r1 = _make_receipt(quantity=10)
        r2 = _make_receipt(quantity=20)
        assert hash_receipt(r1) != hash_receipt(r2)

    def test_timestamp_ignored(self):
        r1 = _make_receipt(timestamp="2026-01-01T00:00:00Z")
        r2 = _make_receipt(timestamp="2099-12-31T23:59:59Z")
        assert hash_receipt(r1) == hash_receipt(r2)

    def test_hash_is_hex_string(self):
        h = hash_receipt(_make_receipt())
        assert all(c in "0123456789abcdef" for c in h)


class TestVerifyReceipt:
    """Integrity check — must fail if verify_receipt reverts to len(id) > 0."""

    def test_true_when_receipt_id_equals_hash(self):
        r = _make_receipt()
        r.receipt_id = hash_receipt(r)
        assert r.receipt_id == hash_receipt(r)
        assert verify_receipt(r) is True

    def test_true_when_16_char_economy_id_matches_content_hash(self):
        r = _make_receipt(receipt_id="0123456789abcdef")
        assert len(r.receipt_id) == 16
        assert r.content_hash == hash_receipt(r)
        assert verify_receipt(r) is True

    def test_false_for_empty_id(self):
        r = _make_receipt(receipt_id="")
        assert verify_receipt(r) is False

    def test_false_for_tampered_id(self):
        r = _make_receipt(receipt_id="tampered")
        assert verify_receipt(r) is False

    def test_false_for_mutated_qty_with_stale_hash(self):
        r = _make_receipt(quantity=10)
        stale = hash_receipt(r)
        r.receipt_id = stale
        r.content_hash = stale
        r.quantity = 99
        assert r.content_hash != hash_receipt(r)
        assert verify_receipt(r) is False


class TestLedger:
    def test_append_tracks_buys(self):
        ledger = ReceiptLedger(run_id="test-run")
        ledger.append(_make_receipt(action=TradeAction.BUY, total_price=100))
        assert ledger.total_buys == 100
        assert ledger.total_sells == 0
        assert ledger.net_profit == -100

    def test_append_tracks_sells(self):
        ledger = ReceiptLedger(run_id="test-run")
        ledger.append(_make_receipt(action=TradeAction.SELL, total_price=150))
        assert ledger.total_sells == 150
        assert ledger.net_profit == 150

    def test_net_profit_calculation(self):
        ledger = ReceiptLedger(run_id="test-run")
        ledger.append(_make_receipt(action=TradeAction.BUY, total_price=100))
        ledger.append(_make_receipt(action=TradeAction.SELL, total_price=180))
        assert ledger.net_profit == 80

    def test_export_is_valid_json(self):
        ledger = ReceiptLedger(run_id="test-run")
        ledger.append(_make_receipt())
        exported = export_ledger(ledger)
        data = json.loads(exported)
        assert data["run_id"] == "test-run"
        assert len(data["receipts"]) == 1

    def test_export_roundtrip_fields(self):
        ledger = ReceiptLedger(run_id="test-run")
        r = _make_receipt(captain_name="Hawk", port_id="jade_port", good_id="silk")
        ledger.append(r)
        data = json.loads(export_ledger(ledger))
        receipt_data = data["receipts"][0]
        assert receipt_data["captain_name"] == "Hawk"
        assert receipt_data["port_id"] == "jade_port"
        assert receipt_data["good_id"] == "silk"
