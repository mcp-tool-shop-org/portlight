"""Combat screen — interactive duel and naval combat."""

from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Static, RichLog

if TYPE_CHECKING:
    from portlight.app.session import GameSession


class CombatScreen(Screen):
    """Interactive combat screen with action keybindings."""

    BINDINGS = [
        Binding("t", "combat_action('thrust')", "Thrust", priority=True),
        Binding("z", "combat_action('slash')", "Slash", priority=True),
        Binding("x", "combat_action('parry')", "Parry", priority=True),
        Binding("e", "combat_action('dodge')", "Dodge", priority=True),
        Binding("o", "combat_action('shoot')", "Shoot", priority=True),
        Binding("escape", "end_combat", "Leave", priority=True),
    ]

    def __init__(
        self,
        session: "GameSession",
        player_combatant,
        opponent_combatant,
        encounter,
    ) -> None:
        super().__init__()
        self.session = session
        self.player = player_combatant
        self.opponent = opponent_combatant
        self.encounter = encounter
        self._turn = 0
        self._finished = False

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal():
                yield Static(self._player_panel(), id="combat-you")
                yield Static(self._opponent_panel(), id="combat-enemy")
            yield RichLog(id="combat-log", wrap=True, highlight=True)
            yield Static(
                "[T]hrust [Z]Slash [X]Parry [E]Dodge [O]Shoot [Esc]Leave",
                id="footer-bar",
            )

    def _player_panel(self) -> str:
        p = self.player
        lines = [
            f"[bold green]{self.session.world.captain.name}[/bold green]",
            f"HP:      {p.hp}/{p.hp_max}",
            f"Stamina: {p.stamina}/{p.stamina_max}",
        ]
        if hasattr(p, "ammo"):
            lines.append(f"Ammo:    {p.ammo}")
        if hasattr(p, "style_name") and p.style_name:
            lines.append(f"Style:   {p.style_name}")
        return "\n".join(lines)

    def _opponent_panel(self) -> str:
        o = self.opponent
        name = getattr(o, "name", "Opponent")
        lines = [
            f"[bold red]{name}[/bold red]",
            f"HP:      {o.hp}/{o.hp_max}",
            f"Stamina: {o.stamina}/{o.stamina_max}",
        ]
        if hasattr(o, "style_name") and o.style_name:
            lines.append(f"Style:   {o.style_name}")
        return "\n".join(lines)

    def _refresh_panels(self) -> None:
        self.query_one("#combat-you", Static).update(self._player_panel())
        self.query_one("#combat-enemy", Static).update(self._opponent_panel())

    def action_combat_action(self, action: str) -> None:
        if self._finished:
            return

        self._turn += 1
        log = self.query_one("#combat-log", RichLog)

        # Execute combat round via engine
        try:
            from portlight.engine.combat import resolve_combat_round
            round_data = resolve_combat_round(
                self.player, self.opponent, action, self._turn
            )

            # Log the round
            for msg in round_data.get("messages", []):
                log.write(f"  {msg}")
            log.write("")

            self._refresh_panels()

            # Check victory/defeat
            if self.opponent.hp <= 0:
                self._finished = True
                log.write("[bold green]Victory![/bold green]")
                self.app.notify("You won the duel!", severity="information")
            elif self.player.hp <= 0:
                self._finished = True
                log.write("[bold red]Defeated![/bold red]")
                self.app.notify("You were defeated.", severity="error")

        except Exception as e:
            log.write(f"[red]Combat error: {e}[/red]")

    def action_end_combat(self) -> None:
        self.app.pop_screen()
        self.app.refresh_views()
