"""Encounter screen -- continuous multi-phase combat experience.

Flows through: approach -> naval -> boarding -> duel -> victory/defeat,
or naval sink -> capture_available (prize crew split, not duel payout).
A single RichLog persists across all phases as a scrollable encounter journal.
Panel visibility toggles per phase. Action keys change per phase.
"""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Static, RichLog

if TYPE_CHECKING:
    from portlight.app.session import GameSession
    from portlight.engine.models import EncounterState


# Phase-specific action bar text
_APPROACH_ACTIONS = (
    "  [bold #2a9d8f]N[/bold #2a9d8f].Negotiate  "
    "[bold #e76f51]F[/bold #e76f51].Flee  "
    "[bold #e9c46a]G[/bold #e9c46a].Fight"
)
_NAVAL_ACTION_KEYS = {
    "broadside": ("B", "Broadside", "#2a9d8f"),
    "close": ("C", "Close", "#2a9d8f"),
    "evade": ("E", "Evade", "#2a9d8f"),
    "rake": ("R", "Rake", "#2a9d8f"),
    "flee": ("F", "Flee", "#e76f51"),
}
_DUEL_CORE = ("thrust", "slash", "parry", "dodge", "shoot", "throw")
_DUEL_ACTIONS = (
    "  [bold #2a9d8f]T[/bold #2a9d8f].Thrust  "
    "[bold #2a9d8f]Z[/bold #2a9d8f].Slash  "
    "[bold #2a9d8f]X[/bold #2a9d8f].Parry  "
    "[bold #2a9d8f]E[/bold #2a9d8f].Dodge  "
    "[bold #2a9d8f]O[/bold #2a9d8f].Shoot  "
    "[bold #2a9d8f]W[/bold #2a9d8f].Throw"
)
_VICTORY_ACTIONS = (
    "  [bold #2a9d8f]S[/bold #2a9d8f].Spare  "
    "[bold #e76f51]A[/bold #e76f51].Take All"
)
_CAPTURE_ACTIONS = (
    "  [bold #2a9d8f]C[/bold #2a9d8f].Capture  "
    "[bold #e9c46a]+/-[/bold #e9c46a].Crew  "
    "[bold #e76f51]F[/bold #e76f51].Let sink"
)
_DEFEAT_ACTIONS = "  [dim]Esc.Leave[/dim]"


def reconstruct_encounter(session: "GameSession"):
    """Rebuild EncounterState from pending_duel + persisted blob (no re-roll)."""
    from portlight.app.session import reconstruct_encounter as _reconstruct
    return _reconstruct(session, victory_phase="victory")


class EncounterScreen(Screen):
    """Multi-phase pirate encounter -- approach, naval, boarding, duel, resolution."""

    BINDINGS = [
        # Keys not bound by the App — handled directly by the Screen.
        # Keys that conflict with App bindings (g/f/b/c/r/s/a/e) are
        # intercepted by App.action_* methods which delegate to this screen
        # via action_encounter_key() when an EncounterScreen is active.
        Binding("n", "encounter_key('negotiate')", "Negotiate", priority=True),
        Binding("t", "encounter_key('thrust')", "Thrust", priority=True),
        Binding("z", "encounter_key('slash')", "Slash", priority=True),
        Binding("x", "encounter_key('parry')", "Parry", priority=True),
        Binding("o", "encounter_key('shoot')", "Shoot", priority=True),
        Binding("w", "encounter_key('throw')", "Throw", priority=True),
        Binding("y", "encounter_key('special')", "Style", priority=True),
        Binding("minus", "encounter_key('crew_down')", show=False, priority=True),
        Binding("plus", "encounter_key('crew_up')", show=False, priority=True),
        Binding("equals", "encounter_key('crew_up')", show=False, priority=True),
        Binding("enter", "encounter_key('capture')", show=False, priority=True),
        Binding("escape", "encounter_escape", "Leave", priority=True),
    ]

    def __init__(self, session: "GameSession", encounter: "EncounterState") -> None:
        super().__init__()
        self.session = session
        self.encounter = encounter
        self._phase = encounter.phase  # approach | naval | boarding | duel | victory | defeat | capture_available
        self._player_combatant = None
        self._opponent_combatant = None
        self._transitioning = False
        self._crew_to_assign = 0
        self._prize_min = 0
        self._flagship_min = 0

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("", id="encounter-header")
            with Horizontal(id="ship-panels", classes="hidden"):
                yield Static("", id="ship-player")
                yield Static("", id="ship-enemy")
            with Horizontal(id="combatant-panels", classes="hidden"):
                yield Static("", id="combatant-player")
                yield Static("", id="combatant-enemy")
            yield RichLog(id="encounter-log", wrap=True, highlight=True)
            yield Static(_APPROACH_ACTIONS, id="encounter-actions")

    def on_mount(self) -> None:
        phase = self.encounter.phase or "approach"
        if phase == "naval":
            self._resume_naval()
        elif phase in ("duel", "boarding"):
            # Boarding is a one-shot transition; persist as duel so we don't re-apply losses.
            self._write_header()
            self._begin_duel()
        elif phase == "victory":
            self._write_header()
            self._enter_victory()
        elif phase == "capture_available":
            self._write_header()
            self._enter_capture()
        elif phase in ("resolved", "defeat"):
            self._write_header()
            self._phase = phase
            self._update_actions(_DEFEAT_ACTIONS)
        else:
            self._enter_approach()

    # ------------------------------------------------------------------
    # Key dispatcher
    # ------------------------------------------------------------------

    def action_encounter_escape(self) -> None:
        """Handle Escape key — exit only if encounter is resolved."""
        if self._phase == "victory":
            self.app.notify("Spare (S) or take all (A) first!", severity="warning")
        elif self._phase in ("defeat", "resolved"):
            self._exit_encounter()
        elif self._phase == "capture_available":
            self.app.notify("Capture the prize (C) or let it sink (F) first!", severity="warning")
        else:
            self.app.notify("Resolve the encounter first!", severity="warning")

    def action_encounter_key(self, key: str) -> None:
        if self._transitioning:
            return

        phase = self._phase

        if phase == "approach":
            if key == "negotiate":
                self._handle_negotiate()
            elif key == "flee":
                self._handle_flee()
            elif key == "fight":
                self._handle_fight()
            return

        if phase == "naval":
            if key == "flee":
                self._handle_naval_flee()
            elif key in ("broadside", "close", "evade", "rake"):
                self._handle_naval_action(key)
            return

        if phase == "duel":
            if key in ("thrust", "slash", "parry", "evade", "shoot", "throw"):
                action = "dodge" if key == "evade" else key
                self._handle_duel_action(action)
            elif key == "special":
                self._handle_duel_special()
            return

        if phase == "victory":
            if key == "spare":
                self._handle_spare()
            elif key == "take_all":
                self._handle_take_all()
            return

        if phase == "capture_available":
            if key in ("capture", "close"):
                self._confirm_capture()
            elif key == "flee":
                self._decline_capture()
            elif key == "crew_up":
                self._adjust_crew(1)
            elif key == "crew_down":
                self._adjust_crew(-1)
            return

    # ------------------------------------------------------------------
    # Approach phase
    # ------------------------------------------------------------------

    def _write_header(self) -> None:
        from portlight.app.combat_views import _strength_indicator
        from portlight.content.factions import FACTIONS

        enc = self.encounter
        faction = FACTIONS.get(enc.enemy_faction_id)
        faction_name = faction.name if faction else enc.enemy_faction_id
        header_text = (
            f"[bold red]Sails on the horizon![/bold red]\n\n"
            f"  Captain:  [bold]{enc.enemy_captain_name}[/bold]\n"
            f"  Faction:  {faction_name}\n"
            f"  Demeanor: [italic]{enc.enemy_personality}[/italic]\n"
            f"  Strength: {_strength_indicator(enc.enemy_strength)}"
        )
        self.query_one("#encounter-header", Static).update(header_text)

    def _enter_approach(self) -> None:
        from portlight.content.factions import PIRATE_CAPTAINS

        self._write_header()
        captain_data = PIRATE_CAPTAINS.get(self.encounter.enemy_captain_id)

        # Log
        log = self.query_one("#encounter-log", RichLog)
        if captain_data:
            log.write(f"[italic]{captain_data.duel_opening}[/italic]")
        log.write("")
        log.write("[bold]What will you do?[/bold]  Negotiate, Flee, or Fight?")
        log.write("")

        # Weapon recognition
        self._check_weapon_recognition(log)
        self._persist_encounter()

    def _resume_naval(self) -> None:
        self._write_header()
        self._phase = "naval"
        self.encounter.phase = "naval"
        log = self.query_one("#encounter-log", RichLog)
        log.write("[bold red]NAVAL COMBAT[/bold red]  [dim](resumed)[/dim]")
        log.write("")
        self.query_one("#ship-panels").remove_class("hidden")
        self._refresh_ship_panels()
        self._update_actions(self._naval_actions_bar())

    def _check_weapon_recognition(self, log: RichLog) -> None:
        gear = self.session.captain.combat_gear
        if not gear.melee_weapon:
            return
        try:
            from portlight.engine.weapon_provenance import WeaponProvenance, check_recognition
            prov = gear.weapon_provenance.get(gear.melee_weapon)
            if not isinstance(prov, WeaponProvenance):
                return
            enc = self.encounter
            memories = self.session.world.pirates.captain_memories
            familiarity = 0
            mem = memories.get(enc.enemy_captain_id)
            if mem and hasattr(mem, "familiarity"):
                familiarity = mem.familiarity
            from portlight.content.weapons import MELEE_WEAPONS
            weapon_def = MELEE_WEAPONS.get(gear.melee_weapon)
            weapon_name = weapon_def.name if weapon_def else gear.melee_weapon
            result = check_recognition(prov, weapon_name, enc.enemy_captain_id, familiarity, self._rng())
            if result.recognized:
                log.write(f"[bold magenta]{enc.enemy_captain_name} eyes your {weapon_name} -- {result.flavor}[/bold magenta]")
                log.write("")
        except (ImportError, AttributeError, Exception):
            pass

    # ------------------------------------------------------------------
    # Approach handlers
    # ------------------------------------------------------------------

    def _handle_negotiate(self) -> None:
        from portlight.engine.encounter import resolve_negotiate
        enc = self.encounter
        log = self.query_one("#encounter-log", RichLog)

        standing = {}
        if hasattr(self.session.captain, "standing"):
            standing = self.session.captain.standing.underworld_standing
        captain_type = self.session.captain.captain_type

        success, msg = resolve_negotiate(enc, standing, captain_type, self._rng())
        log.write(f"[bold]Negotiate:[/bold] {msg}")
        log.write("")

        if success:
            self._phase = "resolved"
            log.write("[green]The encounter ends peacefully.[/green]")
            self.app.notify("Encounter resolved -- safe passage.", severity="information", timeout=4)
            self._clear_pending()
            self.session._save()
            self._update_actions(_DEFEAT_ACTIONS)  # just Esc
        else:
            log.write("[yellow]Negotiation failed -- battle is joined![/yellow]")
            self._handle_fight()

    def _handle_flee(self) -> None:
        if self._phase == "naval":
            self._handle_naval_flee()
            return

        from portlight.engine.encounter import resolve_flee
        enc = self.encounter
        log = self.query_one("#encounter-log", RichLog)
        ship = self.session.captain.ship

        escaped, damage, msg = resolve_flee(enc, self._combat_ship(), self._rng())
        log.write(f"[bold]Flee:[/bold] {msg}")

        if damage > 0:
            ship.hull = max(0, ship.hull - damage)

        if escaped:
            self._phase = "resolved"
            log.write("[green]You escape into open water.[/green]")
            self.app.notify("Escaped!", severity="information", timeout=4)
            self._clear_pending()
            self.session._save()
            self._update_actions(_DEFEAT_ACTIONS)
        else:
            log.write("[yellow]Can't escape -- fight![/yellow]")
            self._handle_fight()

    def _handle_fight(self) -> None:
        from portlight.engine.encounter import begin_fight
        enc = self.encounter
        log = self.query_one("#encounter-log", RichLog)

        msg = begin_fight(enc, self._combat_ship())
        self._phase = "naval"
        enc.phase = "naval"

        log.write("")
        log.write(f"[bold #264653]{'=' * 40}[/bold #264653]")
        log.write("[bold red]NAVAL COMBAT[/bold red]")
        log.write(f"[bold #264653]{'=' * 40}[/bold #264653]")
        log.write(f"  {msg}")
        log.write("")

        # Show ship panels
        self.query_one("#ship-panels").remove_class("hidden")
        self._refresh_ship_panels()
        self._update_actions(self._naval_actions_bar())
        self._persist_encounter()

    # ------------------------------------------------------------------
    # Naval phase
    # ------------------------------------------------------------------

    def _combat_ship(self):
        from portlight.content.upgrades import UPGRADES
        from portlight.engine.ship_stats import resolved_ship
        return resolved_ship(self.session.captain.ship, UPGRADES)

    def _handle_naval_flee(self) -> None:
        """Disengage via attempt_flee. Never pass 'flee' to resolve_naval_turn."""
        from portlight.engine.models import EnemyShip
        from portlight.engine.naval import attempt_flee

        enc = self.encounter
        log = self.query_one("#encounter-log", RichLog)
        ship = self.session.captain.ship
        enemy_ship = EnemyShip(
            name=f"{enc.enemy_captain_name}'s Ship",
            hull=enc.enemy_ship_hull, hull_max=enc.enemy_ship_hull_max,
            cannons=enc.enemy_ship_cannons, maneuver=enc.enemy_ship_maneuver,
            speed=enc.enemy_ship_speed, crew=enc.enemy_ship_crew,
            crew_max=enc.enemy_ship_crew_max,
        )
        flee_rng = random.Random(
            self.session.world.seed + self.session.world.day * 1000 + enc.naval_turns + 8888
        )
        escaped, damage = attempt_flee(self._combat_ship(), enemy_ship, flee_rng)
        ship.hull = max(0, ship.hull - damage)
        enc.naval_turns += 1

        log.write(f"[bold #264653]-- Naval Turn {enc.naval_turns} --[/bold #264653]")
        log.write("  You: [cyan]flee[/cyan]")
        if damage > 0:
            log.write(f"  Your hull: [red]-{damage}[/red]")

        if escaped:
            msg = "You break away!"
            if damage > 0:
                msg += f" A parting shot catches your hull for {damage} damage."
            log.write(f"[bold green]{msg}[/bold green]")
            log.write("")
            self._refresh_ship_panels()
            self._resolve_without_prize()
            self.app.notify("Escaped!", severity="information", timeout=4)
            return

        log.write(
            f"[bold red]Flee failed! Their broadside rakes you for {damage} hull damage.[/bold red]"
        )
        log.write("")
        self._refresh_ship_panels()
        if ship.hull <= 0 or ship.crew <= 0:
            self._enter_defeat("Your ship is lost!")
            return
        self._persist_encounter()

    def _handle_naval_action(self, action: str) -> None:
        from portlight.content.upgrades import UPGRADES
        from portlight.engine.encounter import get_encounter_naval_actions, resolve_naval_turn
        from portlight.engine.ship_stats import resolve_cannons
        enc = self.encounter
        log = self.query_one("#encounter-log", RichLog)
        ship = self.session.captain.ship

        if action == "flee":
            self._handle_naval_flee()
            return

        valid = get_encounter_naval_actions(resolve_cannons(ship, UPGRADES))
        if action not in valid:
            self.app.notify(f"Invalid action. Available: {', '.join(valid)}", severity="warning")
            return

        result = resolve_naval_turn(enc, action, self._combat_ship(), self._rng())

        # Apply damage to player ship (roster is source of truth)
        from portlight.app.session import apply_crew_casualties
        ship.hull = max(0, ship.hull + result["player_hull_delta"])
        crew_lost = max(0, -int(result.get("player_crew_delta", 0) or 0))
        apply_crew_casualties(ship, crew_lost)

        # Log the round
        log.write(f"[bold #264653]-- Naval Turn {result['turn']} --[/bold #264653]")
        log.write(f"  You: [cyan]{action}[/cyan]  Enemy: [red]{result['enemy_action']}[/red]")
        if result["player_hull_delta"] != 0:
            log.write(f"  Your hull: [red]{result['player_hull_delta']}[/red]")
        if result["enemy_hull_delta"] != 0:
            log.write(f"  Enemy hull: [green]{result['enemy_hull_delta']}[/green]")
        if result["player_crew_delta"] != 0:
            log.write(f"  Crew lost: [red]{result['player_crew_delta']}[/red]")
        if result.get("flavor"):
            log.write(f"  [italic]{result['flavor']}[/italic]")
        log.write("")

        self._refresh_ship_panels()
        self._persist_encounter()

        # Check player defeat
        if ship.hull <= 0 or ship.crew <= 0:
            self._enter_defeat("Your ship is lost!")
            return

        # Check transitions. Naval sink is prize-capture, never duel victory.
        if result["enemy_sunk"]:
            log.write("[bold green]Enemy ship destroyed![/bold green]")
            self.session.world.pirates.naval_victories += 1
            self._offer_prize_or_clear()
        elif result["boarding_triggered"]:
            log.write("[bold yellow]Boarding threshold reached![/bold yellow]")
            self._auto_boarding()

    def _refresh_ship_panels(self) -> None:
        from portlight.app.tui.theme import render_bar
        from portlight.content.upgrades import UPGRADES
        from portlight.engine.ship_stats import resolve_cannons
        enc = self.encounter
        ship = self.session.captain.ship
        guns = resolve_cannons(ship, UPGRADES)

        player_text = (
            f"[bold #2a9d8f]Your Ship[/bold #2a9d8f]\n\n"
            f"  Hull  {render_bar(ship.hull, ship.hull_max, 10)} {ship.hull}/{ship.hull_max}\n"
            f"  Crew  [bold]{ship.crew}[/bold]\n"
            f"  Guns  [bold]{guns}[/bold]"
        )
        enemy_text = (
            f"[bold #e76f51]{enc.enemy_captain_name}'s Ship[/bold #e76f51]\n\n"
            f"  Hull  {render_bar(enc.enemy_ship_hull, enc.enemy_ship_hull_max, 10)} {enc.enemy_ship_hull}/{enc.enemy_ship_hull_max}\n"
            f"  Crew  [bold]{enc.enemy_ship_crew}[/bold]\n"
            f"  Guns  [bold]{enc.enemy_ship_cannons}[/bold]\n\n"
            f"  Board {render_bar(enc.boarding_progress, enc.boarding_threshold, 8)} {enc.boarding_progress}/{enc.boarding_threshold}"
        )

        self.query_one("#ship-player", Static).update(player_text)
        self.query_one("#ship-enemy", Static).update(enemy_text)

    # ------------------------------------------------------------------
    # Boarding (auto-resolve with brief pause)
    # ------------------------------------------------------------------

    def _auto_boarding(self) -> None:
        from portlight.engine.encounter import resolve_boarding_phase
        enc = self.encounter
        log = self.query_one("#encounter-log", RichLog)
        ship = self.session.captain.ship

        self._transitioning = True

        result = resolve_boarding_phase(enc, ship.crew, self._rng())
        from portlight.app.session import apply_crew_casualties
        apply_crew_casualties(ship, result["player_crew_lost"], keep_at_least=1)

        log.write("")
        log.write(f"[bold #264653]{'=' * 40}[/bold #264653]")
        log.write("[bold yellow]BOARDING![/bold yellow]")
        log.write(f"[bold #264653]{'=' * 40}[/bold #264653]")
        log.write(f"  {result['flavor']}")
        log.write("")

        # Persist as duel so a quit during the pause does not re-run boarding
        self._phase = "duel"
        enc.phase = "duel"
        self._persist_encounter()

        # Brief pause then transition to duel
        self.set_timer(1.0, self._begin_duel)

    def _begin_duel(self) -> None:
        from portlight.app.session import injury_ids_from
        from portlight.engine.encounter import create_duel_combatants
        enc = self.encounter
        log = self.query_one("#encounter-log", RichLog)
        captain = self.session.captain
        gear = captain.combat_gear

        # Create combatants
        throwing_count = sum(gear.throwing_weapons.values()) if isinstance(gear.throwing_weapons, dict) else 0
        self._player_combatant, self._opponent_combatant = create_duel_combatants(
            enc,
            player_crew=captain.ship.crew,
            player_style=captain.active_style,
            player_injury_ids=injury_ids_from(getattr(captain, "injuries", None)),
            player_firearm=gear.firearm,
            player_ammo=gear.firearm_ammo,
            player_throwing=throwing_count,
            player_mechanical=gear.mechanical_weapon,
            player_mechanical_ammo=gear.mechanical_ammo,
        )

        # Apply armor/melee weapon to combatant
        if gear.armor:
            try:
                from portlight.content.weapons import ARMOR
                armor_def = ARMOR.get(gear.armor)
                if armor_def:
                    self._player_combatant.armor_dr = armor_def.damage_reduction
                    self._player_combatant.dodge_stamina_penalty = armor_def.dodge_penalty
            except ImportError:
                pass

        if gear.melee_weapon:
            self._player_combatant.melee_weapon_id = gear.melee_weapon

        # Set opponent name for display
        self._opponent_combatant.name = enc.enemy_captain_name
        self._player_combatant.name = captain.name

        self._phase = "duel"
        enc.phase = "duel"
        self._transitioning = False

        # Swap panels
        self.query_one("#ship-panels").add_class("hidden")
        self.query_one("#combatant-panels").remove_class("hidden")

        log.write(f"[bold #264653]{'=' * 40}[/bold #264653]")
        log.write(f"[bold red]DUEL: {captain.name} vs {enc.enemy_captain_name}[/bold red]")
        log.write(f"[bold #264653]{'=' * 40}[/bold #264653]")
        log.write("")

        self._restore_combatant_hp()
        self._refresh_combatant_panels()
        self._update_actions(self._duel_actions_bar())
        self._persist_encounter()

    # ------------------------------------------------------------------
    # Duel phase
    # ------------------------------------------------------------------

    def _handle_duel_action(self, action: str) -> None:
        from portlight.engine.encounter import resolve_duel_turn
        enc = self.encounter
        log = self.query_one("#encounter-log", RichLog)
        p = self._player_combatant
        o = self._opponent_combatant

        if p is None or o is None:
            return

        # Stamina check
        if p.stamina <= 0 and action not in ("parry",):
            self.app.notify("No stamina! Parry to recover.", severity="warning")
            return

        result = resolve_duel_turn(enc, action, p, o, self._rng())

        log.write(f"[bold #264653]-- Round {result.turn} --[/bold #264653]")
        log.write(f"  You: [cyan]{result.player_action}[/cyan]  Enemy: [red]{result.opponent_action}[/red]")
        if result.damage_to_opponent > 0:
            log.write(f"  You deal [green]{result.damage_to_opponent}[/green] damage!")
        if result.damage_to_player > 0:
            log.write(f"  You take [red]{result.damage_to_player}[/red] damage!")
        if result.injury_inflicted:
            log.write(f"  [bold red]Injury: {result.injury_inflicted}![/bold red]")
        if result.opponent_injury:
            log.write(f"  [bold green]Enemy injured: {result.opponent_injury}![/bold green]")
        if result.style_effect:
            log.write(f"  [italic cyan]{result.style_effect}[/italic cyan]")
        if result.flavor:
            log.write(f"  [italic]{result.flavor}[/italic]")
        log.write("")

        self._refresh_combatant_panels()

        # Fight-over: write injuries + remaining ammo onto the captain before
        # persist/_clear_pending/_save. Mutual-defeat must be checked before
        # the lone player-hp<=0 branch or it is unreachable.
        player_won = o.hp <= 0 and p.hp > 0
        draw = p.hp <= 0 and o.hp <= 0
        player_lost = p.hp <= 0 and o.hp > 0
        if player_won or draw or player_lost:
            self._apply_duel_fight_over_effects(result.injury_inflicted)
            self._persist_encounter()
            if player_won:
                log.write("[bold green]Victory! The captain falls![/bold green]")
                self._enter_victory()
            elif draw:
                log.write("[bold yellow]Mutual defeat -- both fall.[/bold yellow]")
                self._enter_defeat("A draw. Both combatants collapse.")
            else:
                self._enter_defeat(f"{enc.enemy_captain_name} defeats you.")
        else:
            self._update_actions(self._duel_actions_bar())
            self._persist_encounter()

    def _refresh_combatant_panels(self) -> None:
        from portlight.app.tui.theme import render_bar
        p = self._player_combatant
        o = self._opponent_combatant
        if p is None or o is None:
            return

        p_name = getattr(p, "name", "You")
        o_name = getattr(o, "name", "Enemy")

        player_text = (
            f"[bold #2a9d8f]{p_name}[/bold #2a9d8f]\n\n"
            f"  HP  {render_bar(p.hp, p.hp_max, 10)} {p.hp}/{p.hp_max}\n"
            f"  STA {render_bar(p.stamina, p.stamina_max, 10)} {p.stamina}/{p.stamina_max}"
        )
        if p.ammo > 0:
            player_text += f"\n  Ammo: {p.ammo}"
        if p.throwing_weapons > 0:
            player_text += f"\n  Throw: {p.throwing_weapons}"

        enemy_text = (
            f"[bold #e76f51]{o_name}[/bold #e76f51]\n\n"
            f"  HP  {render_bar(o.hp, o.hp_max, 10)} {o.hp}/{o.hp_max}\n"
            f"  STA {render_bar(o.stamina, o.stamina_max, 10)} {o.stamina}/{o.stamina_max}"
        )

        self.query_one("#combatant-player", Static).update(player_text)
        self.query_one("#combatant-enemy", Static).update(enemy_text)

    # ------------------------------------------------------------------
    # Naval prize capture (not duel spare/take-all)
    # ------------------------------------------------------------------

    def is_capturing_prize(self) -> bool:
        return self._phase == "capture_available"

    def _offer_prize_or_clear(self) -> None:
        """Match CLI naval sink: persist capture_available, or clear. No duel payout."""
        from portlight.app.session import naval_capture_gate
        log = self.query_one("#encounter-log", RichLog)
        can_cap, reason = naval_capture_gate(self.session.captain, self.encounter)
        if can_cap:
            self._enter_capture()
            return
        log.write(f"[dim]Cannot capture: {reason}[/dim]")
        log.write("[green]The wreck slips under. Encounter over.[/green]")
        self._resolve_without_prize()
        self.app.notify("Naval victory — no prize.", severity="information", timeout=4)

    def _enter_capture(self) -> None:
        from portlight.app.session import prize_crew_limits
        enc = self.encounter
        self._phase = "capture_available"
        enc.phase = "capture_available"
        prize_min, flagship_min = prize_crew_limits(self.session.captain, enc)
        self._prize_min = prize_min
        self._flagship_min = flagship_min
        lo, hi = self._crew_assign_range()
        self._crew_to_assign = lo
        log = self.query_one("#encounter-log", RichLog)
        log.write("")
        log.write(f"[bold #264653]{'=' * 40}[/bold #264653]")
        log.write("[bold #e9c46a]PRIZE[/bold #e9c46a]")
        log.write(f"[bold #264653]{'=' * 40}[/bold #264653]")
        log.write(f"  You can take {enc.enemy_captain_name}'s vessel as a prize.")
        log.write(f"  Prize needs at least {prize_min} crew; flagship must keep {flagship_min}.")
        log.write(f"  Crew aboard: {self.session.captain.ship.crew}  (assign {lo}–{hi})")
        log.write("  [green]C - Capture[/green] with assigned crew   [red]F - Let it sink[/red]")
        log.write("")
        self.query_one("#ship-panels").remove_class("hidden")
        self.query_one("#combatant-panels").add_class("hidden")
        self._refresh_ship_panels()
        self._update_actions(_CAPTURE_ACTIONS)
        self._refresh_capture_actions()
        self._persist_encounter()

    def _crew_assign_range(self) -> tuple[int, int]:
        crew = self.session.captain.ship.crew
        lo = self._prize_min
        hi = max(lo, crew - self._flagship_min)
        return lo, hi

    def _adjust_crew(self, delta: int) -> None:
        lo, hi = self._crew_assign_range()
        self._crew_to_assign = min(hi, max(lo, self._crew_to_assign + delta))
        self._refresh_capture_actions()

    def _refresh_capture_actions(self) -> None:
        n = self._crew_to_assign
        leftover = self.session.captain.ship.crew - n
        self._update_actions(
            f"  [bold #2a9d8f]C[/bold #2a9d8f].Capture ({n} crew, {leftover} remain)  "
            f"[bold #e9c46a]+/-[/bold #e9c46a].Crew  "
            f"[bold #e76f51]F[/bold #e76f51].Let sink"
        )

    def _confirm_capture(self) -> None:
        from portlight.app.session import assign_prize_ship
        owned, err = assign_prize_ship(self.session, self.encounter, self._crew_to_assign)
        log = self.query_one("#encounter-log", RichLog)
        if err:
            self.app.notify(err, severity="warning")
            log.write(f"[red]{err}[/red]")
            return
        log.write(f"[bold green]Prize captured![/bold green] {owned.ship.name} added to your fleet.")
        log.write(
            f"  Crew split: {self.session.captain.ship.crew} on flagship, "
            f"{owned.ship.crew} on prize"
        )
        self._resolve_without_prize()
        self.app.notify(f"Prize taken: {owned.ship.name}", severity="information", timeout=4)

    def _decline_capture(self) -> None:
        log = self.query_one("#encounter-log", RichLog)
        log.write("[dim]You let the prize go under.[/dim]")
        self._resolve_without_prize()
        self.app.notify("Prize declined.", severity="information", timeout=4)

    def _resolve_without_prize(self) -> None:
        self._phase = "resolved"
        self.encounter.phase = "resolved"
        self._clear_pending()
        self.session._save()
        self._update_actions(_DEFEAT_ACTIONS)

    # ------------------------------------------------------------------
    # Victory
    # ------------------------------------------------------------------

    def _enter_victory(self) -> None:
        # Snapshot remaining ammo before pending-victory persist (CLI fight-over).
        self._sync_combatant_ammo_to_gear()
        self._phase = "victory"
        self.encounter.phase = "resolved"
        self._persist_encounter(pending_victory=True)
        log = self.query_one("#encounter-log", RichLog)
        log.write("")
        log.write(f"[bold #264653]{'=' * 40}[/bold #264653]")
        log.write("[bold #e9c46a]VICTORY[/bold #e9c46a]")
        log.write(f"[bold #264653]{'=' * 40}[/bold #264653]")
        log.write("")
        log.write("[bold]Show mercy or take everything?[/bold]")
        log.write("  [green]S - Spare[/green]: +respect, -grudge, less silver, no loot")
        log.write("  [red]A - Take All[/red]: +fear, +grudge, more silver, full loot")
        log.write("")
        self._update_actions(_VICTORY_ACTIONS)

    def _handle_spare(self) -> None:
        self._finalize_victory(spared=True)

    def _handle_take_all(self) -> None:
        self._finalize_victory(spared=False)

    def _finalize_victory(self, spared: bool) -> None:
        """Apply all victory consequences -- ported from CLI _finalize_victory."""
        enc = self.encounter
        log = self.query_one("#encounter-log", RichLog)
        captain = self.session.captain
        gear = captain.combat_gear

        # Silver reward
        if spared:
            silver_gain = 20 + enc.enemy_strength * 3
        else:
            silver_gain = 20 + enc.enemy_strength * 7
        captain.silver += silver_gain
        self.session.world.pirates.duels_won += 1

        log.write(f"[green]+{silver_gain} silver[/green]")

        # Captain memory
        try:
            from portlight.engine.captain_memory import get_or_create_memory, record_encounter
            memory = get_or_create_memory(self.session.world.pirates.captain_memories, enc.enemy_captain_id)
            record_encounter(
                memory, self.session.world.day, enc.enemy_region, "player_won",
                player_spared=spared, player_used_firearm=False,
                crew_killed=max(0, enc.enemy_ship_crew_max - enc.enemy_ship_crew),
            )
        except (ImportError, Exception):
            pass

        # Underworld standing
        try:
            from portlight.engine.underworld import record_duel_outcome
            uw_standing = captain.standing.underworld_standing
            standing_delta = record_duel_outcome(uw_standing, enc.enemy_faction_id, player_won=True, spared=spared)
            if standing_delta > 0:
                log.write(f"[green]+{standing_delta} underworld standing ({enc.enemy_faction_id})[/green]")
            elif standing_delta < 0:
                log.write(f"[red]{standing_delta} underworld standing ({enc.enemy_faction_id})[/red]")
        except (ImportError, Exception):
            pass

        # Weapon provenance
        if gear.melee_weapon:
            try:
                from portlight.engine.weapon_provenance import (
                    RELIC_COLORS, RELIC_LABELS, WeaponProvenance,
                    create_provenance, record_kill,
                )
                prov = gear.weapon_provenance.get(gear.melee_weapon)
                if not isinstance(prov, WeaponProvenance):
                    prov = create_provenance(gear.melee_weapon)
                    gear.weapon_provenance[gear.melee_weapon] = prov
                tier_change, new_epithet = record_kill(prov, enc.enemy_captain_id, enc.enemy_captain_name)
                if new_epithet:
                    log.write(f"[bold magenta]Your weapon is now known as \"{new_epithet}\"![/bold magenta]")
                if tier_change:
                    label = RELIC_LABELS.get(tier_change, tier_change)
                    color = RELIC_COLORS.get(tier_change, "white")
                    log.write(f"[{color}]Weapon reached {label} status -- {prov.kills} kills.[/{color}]")
            except (ImportError, Exception):
                pass

        # Loot
        try:
            from portlight.engine.loot import apply_loot, roll_loot
            loot = roll_loot(enc.enemy_strength, enc.enemy_captain_id, self._rng())
            if loot and not spared:
                messages = apply_loot(captain, loot)
                for msg in messages:
                    log.write(f"  [green]{msg}[/green]")
            elif spared:
                log.write("[dim]You leave their possessions untouched.[/dim]")
        except (ImportError, Exception):
            pass

        # Companion morale
        try:
            from portlight.engine.companion_engine import CompanionState, PartyState, apply_morale_trigger, check_departures
            party_data = captain.party
            if isinstance(party_data, dict) and party_data.get("companions"):
                companions = [
                    CompanionState(
                        companion_id=c["companion_id"], role_id=c["role_id"],
                        morale=c.get("morale", 70), joined_day=c.get("joined_day", 0),
                        personality=c.get("personality", "pragmatic"),
                    ) for c in party_data["companions"]
                ]
                party = PartyState(
                    companions=companions,
                    max_size=party_data.get("max_size", 2),
                    departed=party_data.get("departed", []),
                )
                trigger = "spared_enemy" if spared else "took_all"
                reactions = apply_morale_trigger(party, trigger)
                for _comp_id, _delta, flavor in reactions:
                    log.write(f"  [dim]{flavor}[/dim]")
                departures = check_departures(party)
                for dep in departures:
                    log.write(f"[bold red]{dep.companion_name} leaves: \"{dep.departure_line}\"[/bold red]")
                captain.party = {
                    "companions": [
                        {"companion_id": c.companion_id, "role_id": c.role_id,
                         "morale": c.morale, "joined_day": c.joined_day, "personality": c.personality}
                        for c in party.companions
                    ],
                    "max_size": party.max_size, "departed": party.departed,
                }
        except (ImportError, Exception):
            pass

        # Captain flavor
        try:
            from portlight.content.factions import PIRATE_CAPTAINS
            captain_data = PIRATE_CAPTAINS.get(enc.enemy_captain_id)
            if captain_data:
                flavor = captain_data.duel_defeat if spared else captain_data.duel_victory
                log.write(f"\n[italic]{flavor}[/italic]")
        except (ImportError, Exception):
            pass

        log.write("")
        choice = "showed mercy" if spared else "took everything"
        log.write(f"[dim]You {choice}. The encounter is over.[/dim]")

        # Weapon degradation (firearm tick only when rounds were spent this fight)
        try:
            from portlight.engine.weapon_quality import tick_melee_degradation, tick_firearm_degradation
            if gear.melee_weapon:
                tick_melee_degradation(gear, gear.melee_weapon)
            if gear.firearm and self._player_combatant and self._player_combatant.ammo < gear.firearm_ammo:
                tick_firearm_degradation(gear, gear.firearm)
        except (ImportError, Exception):
            pass
        # Remaining ammo — firearm, mechanical, and throwing (CLI fight-over)
        self._sync_combatant_ammo_to_gear()

        self._phase = "resolved"
        self._clear_pending()
        self.session._save()
        self._update_actions(_DEFEAT_ACTIONS)
        self.app.notify("Encounter resolved.", severity="information", timeout=4)

    # ------------------------------------------------------------------
    # Defeat
    # ------------------------------------------------------------------

    def _enter_defeat(self, message: str) -> None:
        self._phase = "defeat"
        log = self.query_one("#encounter-log", RichLog)
        log.write("")
        log.write(f"[bold #264653]{'=' * 40}[/bold #264653]")
        log.write("[bold red]DEFEAT[/bold red]")
        log.write(f"[bold #264653]{'=' * 40}[/bold #264653]")
        log.write(f"  {message}")
        log.write("")

        # Remaining ammo (no-op if combatants were never created, e.g. naval loss)
        self._sync_combatant_ammo_to_gear()

        # Duel-loss silver penalty — CLI fight() uses 15 + strength*3.
        # Skip when there is no player combatant (naval ship-loss).
        if self._player_combatant is not None:
            silver_loss = 15 + self.encounter.enemy_strength * 3
            self.session.captain.silver = max(0, self.session.captain.silver - silver_loss)
            log.write(f"[red]-{silver_loss} silver.[/red]")
            log.write("")

        # Record defeat
        self.session.world.pirates.duels_lost += 1
        try:
            from portlight.engine.captain_memory import get_or_create_memory, record_encounter
            enc = self.encounter
            memory = get_or_create_memory(self.session.world.pirates.captain_memories, enc.enemy_captain_id)
            record_encounter(memory, self.session.world.day, enc.enemy_region, "player_lost")
        except (ImportError, Exception):
            pass

        self._clear_pending()
        self.session._save()
        self._update_actions(_DEFEAT_ACTIONS)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _apply_duel_fight_over_effects(self, injury_id: str | None = None) -> None:
        """Port CLI fight-over: persist injury and remaining ammo onto the captain."""
        captain = self.session.captain
        if injury_id:
            from portlight.app.session import injury_ids_from
            from portlight.engine.injuries import create_injury
            if injury_id not in injury_ids_from(captain.injuries):
                captain.injuries.append(create_injury(injury_id, self.session.world.day))
        self._sync_combatant_ammo_to_gear()

    def _sync_combatant_ammo_to_gear(self) -> None:
        """Copy firearm/mechanical ammo and prune spent throwing weapons from gear."""
        p = self._player_combatant
        if p is None:
            return
        gear = self.session.captain.combat_gear
        if gear.firearm and p.ammo < gear.firearm_ammo:
            try:
                from portlight.engine.weapon_quality import tick_firearm_degradation
                tick_firearm_degradation(gear, gear.firearm)
            except (ImportError, Exception):
                pass
        gear.firearm_ammo = p.ammo
        gear.mechanical_ammo = getattr(p, "mechanical_ammo", 0)
        throwing = getattr(gear, "throwing_weapons", None)
        if throwing:
            total_before = sum(throwing.values())
            spent = total_before - p.throwing_weapons
            for wid in list(throwing):
                if spent <= 0:
                    break
                can_take = min(spent, throwing[wid])
                throwing[wid] -= can_take
                spent -= can_take
            gear.throwing_weapons = {k: v for k, v in throwing.items() if v > 0}

    def _rng(self) -> random.Random:
        seed = self.session.world.seed + self.session.world.day * 1000
        seed += self.encounter.naval_turns + self.encounter.duel_turns
        return random.Random(seed)

    def _update_actions(self, text: str) -> None:
        self.query_one("#encounter-actions", Static).update(text)

    def _naval_actions_bar(self) -> str:
        """Live naval verbs from get_encounter_naval_actions (drops broadside at 0 guns)."""
        from portlight.content.upgrades import UPGRADES
        from portlight.engine.encounter import get_encounter_naval_actions
        from portlight.engine.ship_stats import resolve_cannons
        ship = self.session.captain.ship
        guns = resolve_cannons(ship, UPGRADES) if ship else 0
        parts = []
        for action in get_encounter_naval_actions(guns):
            spec = _NAVAL_ACTION_KEYS.get(action)
            if spec is None:
                continue
            key, name, color = spec
            parts.append(f"[bold {color}]{key}[/bold {color}].{name}")
        return "  " + "  ".join(parts) if parts else "  [dim]No actions[/dim]"

    def _live_duel_special_id(self) -> str | None:
        """Style special_action.id when get_encounter_combat_actions includes it."""
        from portlight.engine.encounter import get_encounter_combat_actions
        p = self._player_combatant
        if p is None:
            return None
        for action in get_encounter_combat_actions(p):
            if action not in _DUEL_CORE:
                return action
        return None

    def _duel_actions_bar(self) -> str:
        text = _DUEL_ACTIONS
        sid = self._live_duel_special_id()
        if not sid:
            return text
        from portlight.content.fighting_styles import FIGHTING_STYLES
        label = sid.replace("_", " ").title()
        p = self._player_combatant
        style_id = getattr(p, "active_style", "") if p is not None else ""
        style = FIGHTING_STYLES.get(style_id or "")
        if style and style.special_action and style.special_action.id == sid:
            label = style.special_action.name
        return text + f"  [bold #e9c46a]Y[/bold #e9c46a].{label}"

    def _handle_duel_special(self) -> None:
        sid = self._live_duel_special_id()
        if not sid:
            self.app.notify("Style special not ready.", severity="warning")
            return
        self._handle_duel_action(sid)

    def _restore_combatant_hp(self) -> None:
        """Reapply persisted duel HP/stamina after creating combatants."""
        estate = self.session.world.pirates.encounter_state or {}
        p, o = self._player_combatant, self._opponent_combatant
        if p is not None:
            if "player_hp" in estate:
                p.hp = estate["player_hp"]
            if "player_stamina" in estate:
                p.stamina = estate["player_stamina"]
        if o is not None:
            if "opponent_hp" in estate:
                o.hp = estate["opponent_hp"]
            if "opponent_stamina" in estate:
                o.stamina = estate["opponent_stamina"]

    def _persist_encounter(self, pending_victory: bool = False) -> None:
        """Write phase, full ship stats, HP, and boarding so a mid-fight quit can resume."""
        if not self.session.world:
            return
        enc = self.encounter
        phase = self._phase
        if phase == "victory":
            phase = "resolved"
            pending_victory = True
        elif phase in ("defeat", "resolved"):
            return
        else:
            phase = phase or enc.phase or "approach"
        from portlight.app.session import persist_encounter
        persist_encounter(
            self.session, enc,
            pending_victory=pending_victory,
            player=self._player_combatant,
            opponent=self._opponent_combatant,
            phase=phase,
        )
        self.session._save()

    def _clear_pending(self) -> None:
        """Clear encounter from world state so voyage can resume."""
        self.session.world.pirates.pending_duel = None
        self.session.world.pirates.encounter_phase = ""
        self.session.world.pirates.encounter_state = {}

    def _exit_encounter(self) -> None:
        self.session._save()
        self.app.pop_screen()
        self.app.refresh_views()
