"""Market screen — interactive buy/sell with live price table."""

from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Input, Label, Static

if TYPE_CHECKING:
    from portlight.app.session import GameSession


class TradeDialog(ModalScreen[str | None]):
    """Modal dialog for buy/sell input."""

    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    def __init__(self, action: str, good_id: str, good_name: str, max_qty: int) -> None:
        super().__init__()
        self.action = action
        self.good_id = good_id
        self.good_name = good_name
        self.max_qty = max_qty

    def compose(self) -> ComposeResult:
        with Vertical(id="input-area"):
            yield Label(f"{self.action.title()} {self.good_name} (max {self.max_qty}):")
            yield Input(placeholder=f"Quantity (1-{self.max_qty})", id="qty-input")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value.strip()
        if text.isdigit() and 0 < int(text) <= self.max_qty:
            self.dismiss(text)
        else:
            self.notify(f"Enter a number between 1 and {self.max_qty}", severity="warning")

    def action_cancel(self) -> None:
        self.dismiss(None)


class GoodSelectDialog(ModalScreen[str | None]):
    """Modal dialog to select a good for buy/sell."""

    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    def __init__(self, action: str, goods: list[tuple[str, str]]) -> None:
        super().__init__()
        self.action = action
        self.goods = goods  # list of (good_id, display_name)

    def compose(self) -> ComposeResult:
        with Vertical(id="input-area"):
            lines = [f"[bold]{self.action.title()} which good?[/bold]", ""]
            for i, (gid, name) in enumerate(self.goods, 1):
                lines.append(f"  {i}. {name} ({gid})")
            lines.append("")
            yield Static("\n".join(lines))
            yield Input(placeholder="Enter good name or number", id="good-input")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value.strip().lower()
        # Try as number
        if text.isdigit():
            idx = int(text) - 1
            if 0 <= idx < len(self.goods):
                self.dismiss(self.goods[idx][0])
                return
        # Try as good_id match
        for gid, name in self.goods:
            if text == gid or text == name.lower():
                self.dismiss(gid)
                return
        # Try as prefix
        for gid, name in self.goods:
            if gid.startswith(text) or name.lower().startswith(text):
                self.dismiss(gid)
                return
        self.notify(f"Unknown good: {text}", severity="warning")

    def action_cancel(self) -> None:
        self.dismiss(None)


def execute_buy_flow(app, session: "GameSession") -> None:
    """Launch the buy flow: select good -> enter quantity -> execute."""
    port = session.current_port
    if not port:
        app.notify("Not docked at a port.", severity="warning")
        return

    from portlight.content.goods import GOODS
    available = []
    for slot in port.market:
        good = GOODS.get(slot.good_id)
        if good and slot.buy_price > 0 and slot.stock_current > 0:
            max_afford = session.world.captain.silver // slot.buy_price if slot.buy_price > 0 else 0
            if max_afford > 0:
                available.append((slot.good_id, good.name))

    if not available:
        app.notify("Nothing affordable to buy.", severity="warning")
        return

    def on_good_selected(good_id: str | None) -> None:
        if good_id is None:
            return
        slot = next((s for s in port.market if s.good_id == good_id), None)
        if not slot:
            return
        good = GOODS.get(good_id)
        max_afford = session.world.captain.silver // slot.buy_price if slot.buy_price > 0 else 0
        max_qty = min(max_afford, slot.stock_current)

        def on_qty(qty_str: str | None) -> None:
            if qty_str is None:
                return
            result = session.buy(good_id, int(qty_str))
            if isinstance(result, str):
                app.notify(result, severity="error")
            else:
                app.notify(
                    f"Bought {result.quantity} {good.name} for {result.total_cost} silver",
                    severity="information",
                )
                app.refresh_views()

        app.push_screen(TradeDialog("buy", good_id, good.name, max_qty), on_qty)

    app.push_screen(GoodSelectDialog("buy", available), on_good_selected)


def execute_sell_flow(app, session: "GameSession") -> None:
    """Launch the sell flow: select cargo -> enter quantity -> execute."""
    port = session.current_port
    if not port:
        app.notify("Not docked at a port.", severity="warning")
        return

    cap = session.world.captain
    from portlight.content.goods import GOODS
    available = []
    for cargo in cap.cargo:
        good = GOODS.get(cargo.good_id)
        if good and cargo.quantity > 0:
            available.append((cargo.good_id, good.name))

    if not available:
        app.notify("No cargo to sell.", severity="warning")
        return

    def on_good_selected(good_id: str | None) -> None:
        if good_id is None:
            return
        cargo_item = next((c for c in cap.cargo if c.good_id == good_id), None)
        if not cargo_item:
            return
        good = GOODS.get(good_id)

        def on_qty(qty_str: str | None) -> None:
            if qty_str is None:
                return
            result = session.sell(good_id, int(qty_str))
            if isinstance(result, str):
                app.notify(result, severity="error")
            else:
                app.notify(
                    f"Sold {result.quantity} {good.name} for {result.total_revenue} silver",
                    severity="information",
                )
                app.refresh_views()

        app.push_screen(TradeDialog("sell", good_id, good.name, cargo_item.quantity), on_qty)

    app.push_screen(GoodSelectDialog("sell", available), on_good_selected)
