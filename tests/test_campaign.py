"""Tests for Phase 3D-4A — Campaign milestone engine, career profiles, victory paths.

Coverage:
  - Content laws: all 27 milestones exist, families correct, evaluators registered
  - Milestone evaluation: each family fires from real state
  - No-fire: milestones don't trigger from unrelated state
  - Already-completed: milestones don't re-fire
  - Career profile: different captains produce different top profiles
  - Victory paths: requirements check real state
  - Save/load: campaign state round-trips
  - Session integration: advance() triggers milestones
"""

import pytest
from dataclasses import field

from portlight.engine.campaign import (
    CampaignState,
    MilestoneCompletion,
    MilestoneFamily,
    MilestoneSpec,
    ProfileScore,
    SessionSnapshot,
    VictoryPathProgress,
    compute_career_profile,
    compute_victory_progress,
    evaluate_milestones,
)
from portlight.content.campaign import MILESTONE_SPECS, MILESTONE_BY_ID
from portlight.engine.models import (
    Captain,
    CargoItem,
    Port,
    ReputationState,
    Route,
    Ship,
    VoyageState,
    VoyageStatus,
    WorldState,
)
from portlight.engine.contracts import (
    ContractBoard,
    ContractOutcome,
)
from portlight.engine.infrastructure import (
    BrokerOffice,
    BrokerTier,
    CreditState,
    CreditTier,
    InfrastructureState,
    OwnedLicense,
    WarehouseLease,
    WarehouseTier,
)
from portlight.receipts.models import ReceiptLedger, TradeReceipt, TradeAction


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _base_world(captain_type: str = "merchant") -> WorldState:
    """Minimal world for campaign tests."""
    return WorldState(
        captain=Captain(
            name="Trader",
            captain_type=captain_type,
            silver=1000,
            ship=Ship(
                template_id="coastal_sloop",
                name="Test Sloop",
                hull=60, hull_max=60,
                cargo_capacity=30, speed=8,
                crew=5, crew_max=8,
            ),
            standing=ReputationState(
                regional_standing={"Mediterranean": 0, "West Africa": 0, "East Indies": 0},
                customs_heat={"Mediterranean": 0, "West Africa": 0, "East Indies": 0},
                commercial_trust=0,
            ),
        ),
        ports={
            "porto_novo": Port(id="porto_novo", name="Porto Novo", description="", region="Mediterranean"),
            "sun_harbor": Port(id="sun_harbor", name="Sun Harbor", description="", region="West Africa"),
            "jade_port": Port(id="jade_port", name="Jade Port", description="", region="East Indies"),
        },
        routes=[Route("porto_novo", "sun_harbor", distance=40)],
        voyage=VoyageState(
            origin_id="porto_novo",
            destination_id="porto_novo",
            distance=0,
            status=VoyageStatus.IN_PORT,
        ),
        day=10,
        seed=42,
    )


def _base_snap(**overrides) -> SessionSnapshot:
    """Build a session snapshot with optional overrides."""
    world = overrides.get("world", _base_world())
    return SessionSnapshot(
        captain=world.captain,
        world=world,
        board=overrides.get("board", ContractBoard()),
        infra=overrides.get("infra", InfrastructureState()),
        ledger=overrides.get("ledger", ReceiptLedger()),
        campaign=overrides.get("campaign", CampaignState()),
    )


# ---------------------------------------------------------------------------
# Content law tests
# ---------------------------------------------------------------------------

class TestContentLaws:
    def test_27_milestones_defined(self):
        assert len(MILESTONE_SPECS) == 27

    def test_all_families_represented(self):
        families = {s.family for s in MILESTONE_SPECS}
        for f in MilestoneFamily:
            assert f in families, f"Family {f} has no milestones"

    def test_unique_ids(self):
        ids = [s.id for s in MILESTONE_SPECS]
        assert len(ids) == len(set(ids)), "Duplicate milestone IDs"

    def test_all_evaluators_registered(self):
        from portlight.engine.campaign import _EVALUATORS
        for spec in MILESTONE_SPECS:
            assert spec.evaluator in _EVALUATORS, f"Evaluator {spec.evaluator} not registered for {spec.id}"

    def test_milestone_by_id_lookup(self):
        for spec in MILESTONE_SPECS:
            assert MILESTONE_BY_ID[spec.id] is spec

    def test_family_counts_reasonable(self):
        counts = {}
        for s in MILESTONE_SPECS:
            counts[s.family] = counts.get(s.family, 0) + 1
        # Each family should have 4-6 milestones
        for f, c in counts.items():
            assert 4 <= c <= 6, f"Family {f} has {c} milestones (expected 4-6)"


# ---------------------------------------------------------------------------
# Regional foothold milestones
# ---------------------------------------------------------------------------

class TestFootholdMilestones:
    def test_first_warehouse_fires(self):
        infra = InfrastructureState(
            warehouses=[WarehouseLease(
                id="wh1", port_id="porto_novo", tier=WarehouseTier.DEPOT,
                capacity=20, lease_cost=50, upkeep_per_day=1,
                opened_day=5, upkeep_paid_through=10, active=True,
            )],
        )
        snap = _base_snap(infra=infra)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "foothold_first_warehouse" in ids

    def test_first_broker_fires(self):
        infra = InfrastructureState(
            brokers=[BrokerOffice(region="Mediterranean", tier=BrokerTier.LOCAL, opened_day=5, active=True)],
        )
        snap = _base_snap(infra=infra)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "foothold_first_broker" in ids

    def test_standing_fires_at_10(self):
        world = _base_world()
        world.captain.standing.regional_standing["Mediterranean"] = 10
        snap = _base_snap(world=world)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "foothold_standing_established" in ids

    def test_two_regions_fires(self):
        world = _base_world()
        world.captain.standing.regional_standing["Mediterranean"] = 5
        world.captain.standing.regional_standing["West Africa"] = 5
        snap = _base_snap(world=world)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "foothold_two_regions" in ids

    def test_no_fire_with_zero_standing(self):
        snap = _base_snap()
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "foothold_standing_established" not in ids
        assert "foothold_two_regions" not in ids


# ---------------------------------------------------------------------------
# Lawful house milestones
# ---------------------------------------------------------------------------

class TestLawfulHouseMilestones:
    def test_credible_trust_fires(self):
        world = _base_world()
        world.captain.standing.commercial_trust = 10
        snap = _base_snap(world=world)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "lawful_credible_trust" in ids

    def test_reliable_trust_fires(self):
        world = _base_world()
        world.captain.standing.commercial_trust = 25
        snap = _base_snap(world=world)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "lawful_reliable_trust" in ids

    def test_charter_fires_with_license(self):
        infra = InfrastructureState(
            licenses=[OwnedLicense(license_id="med_trade_charter", purchased_day=5, active=True)],
        )
        snap = _base_snap(infra=infra)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "lawful_first_charter" in ids

    def test_high_rep_charter_fires(self):
        infra = InfrastructureState(
            licenses=[OwnedLicense(license_id="high_rep_charter", purchased_day=5, active=True)],
        )
        snap = _base_snap(infra=infra)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "lawful_high_rep_charter" in ids

    def test_contract_record_fires_at_5(self):
        board = ContractBoard(
            completed=[
                ContractOutcome(
                    contract_id=f"c{i}", outcome_type="completed",
                    silver_delta=100, trust_delta=1, standing_delta=1,
                    heat_delta=0, completion_day=i + 1, summary=f"Delivered grain",
                )
                for i in range(5)
            ],
        )
        snap = _base_snap(board=board)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "lawful_contract_record" in ids

    def test_low_heat_scaling_requires_both(self):
        world = _base_world()
        world.captain.standing.commercial_trust = 25  # reliable
        world.captain.standing.customs_heat["Mediterranean"] = 10  # too much heat
        snap = _base_snap(world=world)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "lawful_low_heat_scaling" not in ids

        # Now with low heat
        world.captain.standing.customs_heat = {"Mediterranean": 3, "West Africa": 2, "East Indies": 0}
        snap = _base_snap(world=world)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "lawful_low_heat_scaling" in ids


# ---------------------------------------------------------------------------
# Shadow network milestones
# ---------------------------------------------------------------------------

class TestShadowMilestones:
    def test_elevated_heat_fires(self):
        world = _base_world()
        world.captain.standing.customs_heat["Mediterranean"] = 15
        world.captain.silver = 500
        snap = _base_snap(world=world)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "shadow_elevated_heat" in ids

    def test_shadow_profitability_fires(self):
        world = _base_world()
        world.captain.standing.customs_heat["West Africa"] = 10
        ledger = ReceiptLedger(net_profit=2500)
        snap = _base_snap(world=world, ledger=ledger)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "shadow_profitability" in ids

    def test_seizure_recovery_fires(self):
        from portlight.engine.models import ReputationIncident
        world = _base_world()
        world.captain.silver = 500
        world.captain.standing.recent_incidents = [
            ReputationIncident(day=5, port_id="porto_novo", region="Mediterranean",
                             incident_type="inspection", description="Cargo seized during inspection",
                             heat_delta=5, standing_delta=-3),
        ]
        snap = _base_snap(world=world)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "shadow_seizure_recovery" in ids


# ---------------------------------------------------------------------------
# Oceanic reach milestones
# ---------------------------------------------------------------------------

class TestOceanicMilestones:
    def test_ei_access_fires(self):
        infra = InfrastructureState(
            licenses=[OwnedLicense(license_id="ei_access_charter", purchased_day=5, active=True)],
        )
        snap = _base_snap(infra=infra)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "oceanic_ei_access" in ids

    def test_galleon_fires(self):
        world = _base_world()
        world.captain.ship = Ship(
            template_id="merchant_galleon", name="Galleon",
            hull=160, hull_max=160, cargo_capacity=150,
            speed=4, crew=20, crew_max=40,
        )
        snap = _base_snap(world=world)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "oceanic_galleon" in ids

    def test_ei_standing_fires(self):
        world = _base_world()
        world.captain.standing.regional_standing["East Indies"] = 15
        snap = _base_snap(world=world)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "oceanic_ei_standing" in ids


# ---------------------------------------------------------------------------
# Commercial finance milestones
# ---------------------------------------------------------------------------

class TestFinanceMilestones:
    def test_credit_opened_fires(self):
        from portlight.engine.infrastructure import InsuranceClaim
        infra = InfrastructureState(
            credit=CreditState(
                tier=CreditTier.MERCHANT_LINE,
                credit_limit=300, outstanding=100,
                total_borrowed=100, active=True,
            ),
        )
        snap = _base_snap(infra=infra)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "finance_credit_opened" in ids

    def test_credit_clean_requires_200_borrowed(self):
        infra = InfrastructureState(
            credit=CreditState(
                tier=CreditTier.MERCHANT_LINE,
                credit_limit=300, outstanding=50,
                total_borrowed=50, defaults=0, active=True,
            ),
        )
        snap = _base_snap(infra=infra)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "finance_credit_clean" not in ids

        # Now with 200+
        infra.credit.total_borrowed = 200
        snap = _base_snap(infra=infra)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "finance_credit_clean" in ids

    def test_insurance_payout_fires(self):
        from portlight.engine.infrastructure import InsuranceClaim
        infra = InfrastructureState(
            claims=[InsuranceClaim(
                policy_id="p1", day=5, incident_type="storm",
                loss_value=100, payout=50,
            )],
        )
        snap = _base_snap(infra=infra)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "finance_first_insurance" in ids


# ---------------------------------------------------------------------------
# Integrated house milestones
# ---------------------------------------------------------------------------

class TestIntegratedMilestones:
    def test_multi_region_infra_fires(self):
        infra = InfrastructureState(
            warehouses=[
                WarehouseLease(id="wh1", port_id="porto_novo", tier=WarehouseTier.DEPOT,
                             capacity=20, lease_cost=50, upkeep_per_day=1, active=True),
            ],
            brokers=[
                BrokerOffice(region="West Africa", tier=BrokerTier.LOCAL, active=True),
            ],
        )
        snap = _base_snap(infra=infra)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "integrated_multi_region" in ids

    def test_brigantine_fires(self):
        world = _base_world()
        world.captain.ship = Ship(
            template_id="trade_brigantine", name="Brig",
            hull=100, hull_max=100, cargo_capacity=80,
            speed=6, crew=10, crew_max=20,
        )
        snap = _base_snap(world=world)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "integrated_brigantine" in ids


# ---------------------------------------------------------------------------
# Already-completed milestones don't re-fire
# ---------------------------------------------------------------------------

class TestNoRefire:
    def test_completed_milestone_does_not_refire(self):
        infra = InfrastructureState(
            warehouses=[WarehouseLease(
                id="wh1", port_id="porto_novo", tier=WarehouseTier.DEPOT,
                capacity=20, lease_cost=50, upkeep_per_day=1, active=True,
            )],
        )
        campaign = CampaignState(
            completed=[MilestoneCompletion(milestone_id="foothold_first_warehouse", completed_day=5)],
        )
        snap = _base_snap(infra=infra, campaign=campaign)
        newly = evaluate_milestones(MILESTONE_SPECS, snap)
        ids = {c.milestone_id for c in newly}
        assert "foothold_first_warehouse" not in ids


# ---------------------------------------------------------------------------
# Career profile scoring
# ---------------------------------------------------------------------------

class TestCareerProfile:
    def test_merchant_lawful_profile(self):
        """Merchant with high trust, charters, low heat → Lawful House on top."""
        world = _base_world("merchant")
        world.captain.standing.commercial_trust = 40
        world.captain.standing.customs_heat = {"Mediterranean": 1, "West Africa": 2, "East Indies": 0}
        infra = InfrastructureState(
            licenses=[
                OwnedLicense(license_id="med_trade_charter", purchased_day=5, active=True),
                OwnedLicense(license_id="high_rep_charter", purchased_day=10, active=True),
            ],
        )
        board = ContractBoard(
            completed=[
                ContractOutcome(
                    contract_id=f"c{i}", outcome_type="completed",
                    silver_delta=100, trust_delta=1, standing_delta=1,
                    heat_delta=0, completion_day=i + 1, summary="Delivered grain",
                )
                for i in range(8)
            ],
        )
        snap = _base_snap(world=world, infra=infra, board=board)
        profile = compute_career_profile(snap)
        assert profile[0].tag == "Lawful House"
        assert profile[0].score > 0

    def test_smuggler_shadow_profile(self):
        """Smuggler with high heat, seizure survival → Shadow Operator rises."""
        from portlight.engine.models import ReputationIncident
        world = _base_world("smuggler")
        world.captain.standing.customs_heat = {"Mediterranean": 5, "West Africa": 20, "East Indies": 0}
        world.captain.silver = 800
        world.captain.standing.recent_incidents = [
            ReputationIncident(day=5, port_id="palm_cove", region="West Africa",
                             incident_type="inspection", description="Cargo seized",
                             heat_delta=5),
        ]
        ledger = ReceiptLedger(net_profit=2000)
        snap = _base_snap(world=world, ledger=ledger)
        profile = compute_career_profile(snap)
        shadow = next(p for p in profile if p.tag == "Shadow Operator")
        assert shadow.score > 0
        # Shadow should be competitive
        assert shadow.score >= profile[1].score or shadow == profile[0]

    def test_navigator_oceanic_profile(self):
        """Navigator with galleon and EI presence → Oceanic Carrier rises."""
        world = _base_world("navigator")
        world.captain.standing.regional_standing["East Indies"] = 20
        world.captain.ship = Ship(
            template_id="merchant_galleon", name="Galleon",
            hull=160, hull_max=160, cargo_capacity=150,
            speed=4, crew=20, crew_max=40,
        )
        infra = InfrastructureState(
            licenses=[OwnedLicense(license_id="ei_access_charter", purchased_day=5, active=True)],
            brokers=[BrokerOffice(region="East Indies", tier=BrokerTier.ESTABLISHED, active=True)],
        )
        snap = _base_snap(world=world, infra=infra)
        profile = compute_career_profile(snap)
        oceanic = next(p for p in profile if p.tag == "Oceanic Carrier")
        assert oceanic.score >= 60  # strong signal

    def test_profile_ranking_changes(self):
        """An empty run should have low scores everywhere."""
        snap = _base_snap()
        profile = compute_career_profile(snap)
        assert all(p.score < 20 for p in profile)


# ---------------------------------------------------------------------------
# Victory path evaluation
# ---------------------------------------------------------------------------

class TestVictoryPaths:
    def test_lawful_victory_incomplete_initially(self):
        snap = _base_snap()
        paths = compute_victory_progress(snap)
        lawful = next(p for p in paths if p.path_id == "lawful_house")
        assert not lawful.is_complete
        # A fresh captain meets "max heat ≤ 5" trivially, so 1 requirement met
        assert lawful.met_count <= 2

    def test_lawful_victory_complete(self):
        world = _base_world()
        world.captain.standing.commercial_trust = 40
        world.captain.standing.regional_standing = {"Mediterranean": 20, "West Africa": 15, "East Indies": 5}
        world.captain.standing.customs_heat = {"Mediterranean": 2, "West Africa": 3, "East Indies": 1}
        world.captain.silver = 3000
        infra = InfrastructureState(
            licenses=[OwnedLicense(license_id="high_rep_charter", purchased_day=5, active=True)],
        )
        board = ContractBoard(
            completed=[
                ContractOutcome(
                    contract_id=f"c{i}", outcome_type="completed",
                    silver_delta=100, trust_delta=1, standing_delta=1,
                    heat_delta=0, completion_day=i + 1, summary="Delivered grain",
                )
                for i in range(8)
            ],
        )
        snap = _base_snap(world=world, infra=infra, board=board)
        paths = compute_victory_progress(snap)
        lawful = next(p for p in paths if p.path_id == "lawful_house")
        assert lawful.is_complete

    def test_shadow_victory_requires_heat(self):
        snap = _base_snap()
        paths = compute_victory_progress(snap)
        shadow = next(p for p in paths if p.path_id == "shadow_network")
        assert not shadow.is_complete

    def test_four_victory_paths_exist(self):
        snap = _base_snap()
        paths = compute_victory_progress(snap)
        assert len(paths) == 4
        ids = {p.path_id for p in paths}
        assert "lawful_house" in ids
        assert "shadow_network" in ids
        assert "oceanic_reach" in ids
        assert "commercial_empire" in ids

    def test_missing_requirements_reported(self):
        snap = _base_snap()
        paths = compute_victory_progress(snap)
        for path in paths:
            for req in path.requirements:
                # All should have a description
                assert req.description


# ---------------------------------------------------------------------------
# Save/load round-trip
# ---------------------------------------------------------------------------

class TestCampaignSaveLoad:
    def test_campaign_round_trip(self, tmp_path):
        from portlight.engine.save import save_game, load_game
        from portlight.content.world import new_game
        from portlight.engine.captain_identity import CaptainType

        world = new_game("Trader", captain_type=CaptainType.MERCHANT)
        ledger = ReceiptLedger(run_id="test-run")
        board = ContractBoard()
        infra = InfrastructureState()
        campaign = CampaignState(
            completed=[
                MilestoneCompletion(milestone_id="foothold_first_warehouse", completed_day=5, evidence="Warehouse at porto_novo"),
                MilestoneCompletion(milestone_id="lawful_credible_trust", completed_day=12, evidence="Trust tier: credible"),
            ],
        )

        save_game(world, ledger, board, infra, campaign, tmp_path)
        result = load_game(tmp_path)
        assert result is not None
        _, _, _, _, loaded_campaign = result
        assert len(loaded_campaign.completed) == 2
        assert loaded_campaign.completed[0].milestone_id == "foothold_first_warehouse"
        assert loaded_campaign.completed[0].completed_day == 5
        assert loaded_campaign.completed[0].evidence == "Warehouse at porto_novo"
        assert loaded_campaign.completed[1].milestone_id == "lawful_credible_trust"

    def test_backward_compat_no_campaign(self, tmp_path):
        """Old saves without campaign key should load with empty CampaignState."""
        import json
        from portlight.engine.save import SAVE_DIR, SAVE_FILE
        from portlight.content.world import new_game
        from portlight.engine.save import world_to_dict, load_game
        from portlight.engine.captain_identity import CaptainType

        world = new_game("Trader", captain_type=CaptainType.MERCHANT)
        # Serialize without campaign key
        data = world_to_dict(world)
        # Remove campaign if present
        data.pop("campaign", None)

        save_dir = tmp_path / SAVE_DIR
        save_dir.mkdir()
        save_path = save_dir / SAVE_FILE
        save_path.write_text(json.dumps(data), encoding="utf-8")

        result = load_game(tmp_path)
        assert result is not None
        _, _, _, _, campaign = result
        assert len(campaign.completed) == 0


# ---------------------------------------------------------------------------
# Session integration
# ---------------------------------------------------------------------------

class TestSessionIntegration:
    def test_session_holds_campaign_state(self, tmp_path):
        from portlight.app.session import GameSession
        s = GameSession(base_path=tmp_path)
        s.new("Tester", captain_type="merchant")
        assert isinstance(s.campaign, CampaignState)
        assert len(s.campaign.completed) == 0

    def test_advance_evaluates_milestones(self, tmp_path):
        """Warehouse milestone should fire after setup + advance."""
        from portlight.app.session import GameSession
        from portlight.engine.infrastructure import WarehouseLease, WarehouseTier
        s = GameSession(base_path=tmp_path)
        s.new("Tester", captain_type="merchant")

        # Manually add a warehouse
        s.infra.warehouses.append(WarehouseLease(
            id="wh1", port_id=s.current_port_id, tier=WarehouseTier.DEPOT,
            capacity=20, lease_cost=50, upkeep_per_day=1,
            opened_day=1, upkeep_paid_through=100, active=True,
        ))

        # Advance one day in port
        s.advance()

        ids = {c.milestone_id for c in s.campaign.completed}
        assert "foothold_first_warehouse" in ids

    def test_milestone_persists_across_save_load(self, tmp_path):
        """Milestones should survive save/load cycle."""
        from portlight.app.session import GameSession
        from portlight.engine.infrastructure import WarehouseLease, WarehouseTier
        s = GameSession(base_path=tmp_path)
        s.new("Tester", captain_type="merchant")

        s.infra.warehouses.append(WarehouseLease(
            id="wh1", port_id=s.current_port_id, tier=WarehouseTier.DEPOT,
            capacity=20, lease_cost=50, upkeep_per_day=1,
            opened_day=1, upkeep_paid_through=100, active=True,
        ))
        s.advance()

        # Reload
        s2 = GameSession(base_path=tmp_path)
        assert s2.load()
        ids = {c.milestone_id for c in s2.campaign.completed}
        assert "foothold_first_warehouse" in ids

    def test_build_snapshot(self, tmp_path):
        from portlight.app.session import GameSession
        s = GameSession(base_path=tmp_path)
        s.new("Tester", captain_type="merchant")
        snap = s._build_snapshot()
        assert snap.captain is s.captain
        assert snap.world is s.world
        assert snap.campaign is s.campaign
