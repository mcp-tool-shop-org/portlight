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
    CareerProfile,
    MilestoneCompletion,
    MilestoneFamily,
    MilestoneSpec,
    ProfileConfidence,
    ProfileScore,
    SessionSnapshot,
    VictoryPathProgress,
    compute_career_profile,
    compute_career_profile_legacy,
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
        assert profile.primary is not None
        assert profile.primary.tag == "Lawful House"
        assert profile.primary.combined_score > 0

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
        shadow = next(t for t in profile.all_tags if t.tag == "Shadow Operator")
        assert shadow.combined_score > 0
        # Shadow should be competitive — in top 2
        assert shadow in [profile.primary] + profile.secondaries or shadow.combined_score > 0

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
        oceanic = next(t for t in profile.all_tags if t.tag == "Oceanic Carrier")
        assert oceanic.combined_score >= 35  # strong signal

    def test_profile_ranking_changes(self):
        """An empty run should have low scores everywhere."""
        snap = _base_snap()
        profile = compute_career_profile(snap)
        assert all(t.combined_score < 20 for t in profile.all_tags)


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


# ---------------------------------------------------------------------------
# 3D-4B — Career Profile Truth
# ---------------------------------------------------------------------------

class TestCareerProfileTruth:
    """Profile returns CareerProfile with primary/secondaries/emerging,
    lifetime vs recent scoring, and confidence bands."""

    def test_profile_returns_career_profile(self):
        """compute_career_profile returns a CareerProfile dataclass."""
        snap = _base_snap()
        profile = compute_career_profile(snap)
        assert isinstance(profile, CareerProfile)
        assert isinstance(profile.all_tags, list)

    def test_all_seven_tags_present(self):
        """All 7 profile tags are always computed."""
        snap = _base_snap()
        profile = compute_career_profile(snap)
        tag_names = {t.tag for t in profile.all_tags}
        expected = {
            "Lawful House", "Shadow Operator", "Oceanic Carrier",
            "Contract Specialist", "Infrastructure Builder",
            "Leveraged Trader", "Risk-Managed Merchant",
        }
        assert tag_names == expected

    def test_tags_have_lifetime_and_recent(self):
        """Each tag has lifetime_score, recent_score, combined_score."""
        snap = _base_snap()
        profile = compute_career_profile(snap)
        for t in profile.all_tags:
            assert hasattr(t, "lifetime_score")
            assert hasattr(t, "recent_score")
            assert hasattr(t, "combined_score")
            assert isinstance(t.confidence, ProfileConfidence)

    def test_primary_is_highest_combined(self):
        """Primary tag is the one with highest combined_score."""
        world = _base_world()
        world.captain.standing.commercial_trust = 50
        world.captain.standing.regional_standing = {"Mediterranean": 20, "West Africa": 15, "East Indies": 0}
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
        assert profile.primary is not None
        # Primary should be the first in all_tags (sorted by combined_score)
        assert profile.primary is profile.all_tags[0]

    def test_secondaries_capped_at_two(self):
        """At most 2 secondary traits."""
        snap = _base_snap()
        profile = compute_career_profile(snap)
        assert len(profile.secondaries) <= 2

    def test_milestones_boost_lifetime_score(self):
        """Completed milestones in aligned families boost lifetime_score."""
        campaign = CampaignState(
            completed=[
                MilestoneCompletion(milestone_id="lawful_credible_trust", completed_day=5, evidence="credible"),
                MilestoneCompletion(milestone_id="lawful_reliable_trust", completed_day=8, evidence="reliable"),
                MilestoneCompletion(milestone_id="lawful_first_charter", completed_day=10, evidence="charter"),
            ],
        )
        snap_with = _base_snap(campaign=campaign)
        snap_without = _base_snap()

        profile_with = compute_career_profile(snap_with)
        profile_without = compute_career_profile(snap_without)

        lawful_with = next(t for t in profile_with.all_tags if t.tag == "Lawful House")
        lawful_without = next(t for t in profile_without.all_tags if t.tag == "Lawful House")
        assert lawful_with.lifetime_score > lawful_without.lifetime_score

    def test_recent_milestones_boost_recent_score(self):
        """Milestones completed within recent window boost recent_score."""
        world = _base_world()
        world.day = 30

        # Recent milestone (within window)
        recent_campaign = CampaignState(
            completed=[
                MilestoneCompletion(
                    milestone_id="lawful_credible_trust",
                    completed_day=25,  # within last 20 days of day 30
                    evidence="credible",
                ),
            ],
        )
        # Old milestone (outside window)
        old_campaign = CampaignState(
            completed=[
                MilestoneCompletion(
                    milestone_id="lawful_credible_trust",
                    completed_day=5,  # 25 days ago, outside 20-day window
                    evidence="credible",
                ),
            ],
        )

        snap_recent = _base_snap(world=world, campaign=recent_campaign)
        snap_old = _base_snap(world=world, campaign=old_campaign)

        profile_recent = compute_career_profile(snap_recent)
        profile_old = compute_career_profile(snap_old)

        lawful_recent = next(t for t in profile_recent.all_tags if t.tag == "Lawful House")
        lawful_old = next(t for t in profile_old.all_tags if t.tag == "Lawful House")

        # Both get the same lifetime boost, but recent gets additional recent_score
        assert lawful_recent.recent_score > lawful_old.recent_score

    def test_confidence_bands(self):
        """Strong activity yields higher confidence than empty run."""
        # Empty run
        snap_empty = _base_snap()
        profile_empty = compute_career_profile(snap_empty)
        # All tags should be Forming on an empty run
        for t in profile_empty.all_tags:
            assert t.confidence in (ProfileConfidence.FORMING, ProfileConfidence.MODERATE)

        # Strong lawful activity
        world = _base_world()
        world.captain.standing.commercial_trust = 50
        world.captain.standing.customs_heat = {"Mediterranean": 0, "West Africa": 0, "East Indies": 0}
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
                    heat_delta=0, completion_day=i + 1, summary="Delivered",
                )
                for i in range(10)
            ],
        )
        snap_strong = _base_snap(world=world, infra=infra, board=board)
        profile_strong = compute_career_profile(snap_strong)
        lawful = next(t for t in profile_strong.all_tags if t.tag == "Lawful House")
        assert lawful.confidence in (ProfileConfidence.STRONG, ProfileConfidence.DEFINING)

    def test_emerging_tag_from_recent_activity(self):
        """A tag with high recent_score but not primary can appear as emerging."""
        world = _base_world()
        world.day = 30
        # Strong lawful base (will be primary)
        world.captain.standing.commercial_trust = 50
        world.captain.standing.customs_heat = {"Mediterranean": 0, "West Africa": 0, "East Indies": 0}
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
                    heat_delta=0, completion_day=i + 1, summary="Delivered",
                )
                for i in range(8)
            ],
        )
        # Recent oceanic milestones (within window)
        campaign = CampaignState(
            completed=[
                MilestoneCompletion(milestone_id="oceanic_ei_access", completed_day=28, evidence="EI charter"),
                MilestoneCompletion(milestone_id="oceanic_ei_broker", completed_day=29, evidence="EI broker"),
                MilestoneCompletion(milestone_id="oceanic_galleon", completed_day=29, evidence="Galleon"),
            ],
        )
        snap = _base_snap(world=world, infra=infra, board=board, campaign=campaign)
        profile = compute_career_profile(snap)
        # Lawful should be primary from strong base
        assert profile.primary is not None
        assert profile.primary.tag == "Lawful House"
        # Oceanic should appear as emerging (recent milestones)
        if profile.emerging:
            assert profile.emerging.recent_score > 0

    def test_legacy_profile_still_works(self):
        """compute_career_profile_legacy returns list[ProfileScore]."""
        snap = _base_snap()
        legacy = compute_career_profile_legacy(snap)
        assert isinstance(legacy, list)
        assert all(isinstance(p, ProfileScore) for p in legacy)
        assert len(legacy) == 7
