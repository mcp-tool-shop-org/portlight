"""Routes and voyage screens — navigation + day advance."""

from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.containers import Vertical
from textual.widgets import Input, Static

if TYPE_CHECKING:
    from portlight.app.session import GameSession


class SailDialog(ModalScreen[str | None]):
    """Modal dialog to select a destination and sail."""

    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    def __init__(self, destinations: list[tuple[str, str, int, float]]) -> None:
        super().__init__()
        self.destinations = destinations  # (port_id, port_name, distance, danger)

    def compose(self) -> ComposeResult:
        with Vertical(id="input-area"):
            lines = ["[bold]Sail to which port?[/bold]", ""]
            for i, (pid, name, dist, danger) in enumerate(self.destinations, 1):
                lines.append(f"  {i}. {name} ({dist} leagues, danger {danger:.0%})")
            lines.append("")
            yield Static("\n".join(lines))
            yield Input(placeholder="Enter port name or number", id="dest-input")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value.strip().lower()
        if text.isdigit():
            idx = int(text) - 1
            if 0 <= idx < len(self.destinations):
                self.dismiss(self.destinations[idx][0])
                return
        for pid, name, _, _ in self.destinations:
            if text == pid or text == name.lower():
                self.dismiss(pid)
                return
        for pid, name, _, _ in self.destinations:
            if name.lower().startswith(text):
                self.dismiss(pid)
                return
        self.notify(f"Unknown destination: {text}", severity="warning")

    def action_cancel(self) -> None:
        self.dismiss(None)


def execute_sail_flow(app, session: "GameSession") -> None:
    """Launch the sail flow: select destination -> depart."""
    if session.at_sea:
        app.notify("Already at sea.", severity="warning")
        return
    port = session.current_port
    if not port:
        app.notify("Not docked at a port.", severity="warning")
        return

    w = session.world
    destinations = []
    for route in w.routes:
        if route.port_a == port.id:
            dest_port = w.ports.get(route.port_b)
            if dest_port:
                destinations.append((dest_port.id, dest_port.name, route.distance, route.danger))
        elif route.port_b == port.id:
            dest_port = w.ports.get(route.port_a)
            if dest_port:
                destinations.append((dest_port.id, dest_port.name, route.distance, route.danger))

    if not destinations:
        app.notify("No routes from this port.", severity="warning")
        return

    destinations.sort(key=lambda d: d[2])

    def on_dest(dest_id: str | None) -> None:
        if dest_id is None:
            return
        err = session.sail(dest_id)
        if err:
            app.notify(err, severity="error")
        else:
            dest_name = w.ports.get(dest_id)
            app.notify(
                f"Set sail for {dest_name.name if dest_name else dest_id}!",
                severity="information",
            )
            app.refresh_views()

    app.push_screen(SailDialog(destinations), on_dest)


def execute_advance(app, session: "GameSession") -> None:
    """Advance one day and show events."""
    if not session.active:
        app.notify("No active game.", severity="warning")
        return

    events = session.advance()
    if events:
        for ev in events:
            severity = "information"
            if hasattr(ev, "event_type"):
                from portlight.engine.voyage import EventType
                if ev.event_type in (EventType.PIRATE, EventType.STORM):
                    severity = "warning"
                elif ev.event_type == EventType.ARRIVAL:
                    severity = "information"
            app.notify(str(ev.description) if hasattr(ev, "description") else str(ev), severity=severity, timeout=5)
    else:
        app.notify(f"Day {session.world.day} — nothing eventful.", timeout=3)

    app.refresh_views()
