"""Campaign content — milestone definitions across 6 commercial families.

24 milestones that make a run legible. Not badge clutter — each represents
a real commercial achievement derived from actual business history.

Families:
  - Regional Foothold: becoming established somewhere
  - Lawful House: legitimacy and premium lawful commerce
  - Shadow Network: high-risk, high-margin gray commerce
  - Oceanic Reach: long-haul and distance power
  - Commercial Finance: mature capital management
  - Integrated House: fully formed multi-system operation
"""

from portlight.engine.campaign import MilestoneFamily, MilestoneSpec

# ---------------------------------------------------------------------------
# All milestone specs
# ---------------------------------------------------------------------------

MILESTONE_SPECS: list[MilestoneSpec] = [
    # ===== Regional Foothold (5) =====
    MilestoneSpec(
        id="foothold_first_warehouse",
        name="First Warehouse",
        family=MilestoneFamily.REGIONAL_FOOTHOLD,
        description="Leased your first warehouse — cargo can now be staged for timing plays.",
        evaluator="first_warehouse",
    ),
    MilestoneSpec(
        id="foothold_first_broker",
        name="First Broker Office",
        family=MilestoneFamily.REGIONAL_FOOTHOLD,
        description="Opened your first broker office — intelligence shapes the contract board.",
        evaluator="first_broker",
    ),
    MilestoneSpec(
        id="foothold_standing_established",
        name="Regional Standing",
        family=MilestoneFamily.REGIONAL_FOOTHOLD,
        description="Reached meaningful standing in one region through consistent commerce.",
        evaluator="standing_one_region",
    ),
    MilestoneSpec(
        id="foothold_strong_standing",
        name="Strong Regional Presence",
        family=MilestoneFamily.REGIONAL_FOOTHOLD,
        description="Achieved strong standing in one region — a known and respected operator.",
        evaluator="strong_standing_one_region",
    ),
    MilestoneSpec(
        id="foothold_two_regions",
        name="Two-Region Presence",
        family=MilestoneFamily.REGIONAL_FOOTHOLD,
        description="Established operations in two different regions.",
        evaluator="presence_two_regions",
    ),

    # ===== Lawful House (6) =====
    MilestoneSpec(
        id="lawful_credible_trust",
        name="Credible Operator",
        family=MilestoneFamily.LAWFUL_HOUSE,
        description="The market recognizes you as credible — new opportunities open.",
        evaluator="credible_trust",
    ),
    MilestoneSpec(
        id="lawful_reliable_trust",
        name="Reliable Operator",
        family=MilestoneFamily.LAWFUL_HOUSE,
        description="Reliable commercial trust — premium contracts and better credit terms.",
        evaluator="reliable_trust",
    ),
    MilestoneSpec(
        id="lawful_first_charter",
        name="First Regional Charter",
        family=MilestoneFamily.LAWFUL_HOUSE,
        description="Acquired your first regional trade charter — formal commercial standing.",
        evaluator="regional_charter",
    ),
    MilestoneSpec(
        id="lawful_high_rep_charter",
        name="High Reputation Charter",
        family=MilestoneFamily.LAWFUL_HOUSE,
        description="Earned the highest commercial charter — recognized across all regions.",
        evaluator="high_rep_charter",
    ),
    MilestoneSpec(
        id="lawful_contract_record",
        name="Proven Contract Record",
        family=MilestoneFamily.LAWFUL_HOUSE,
        description="Completed 5+ contracts — a track record of reliable delivery.",
        evaluator="lawful_contracts_completed",
    ),
    MilestoneSpec(
        id="lawful_low_heat_scaling",
        name="Clean Growth",
        family=MilestoneFamily.LAWFUL_HOUSE,
        description="Reached reliable trust while keeping heat low — growth without suspicion.",
        evaluator="low_heat_scaling",
    ),

    # ===== Shadow Network (4) =====
    MilestoneSpec(
        id="shadow_first_discreet",
        name="First Discreet Delivery",
        family=MilestoneFamily.SHADOW_NETWORK,
        description="Completed your first discreet luxury delivery — the shadow lane is open.",
        evaluator="first_discreet_success",
    ),
    MilestoneSpec(
        id="shadow_elevated_heat",
        name="Operating Under Scrutiny",
        family=MilestoneFamily.SHADOW_NETWORK,
        description="Sustained high heat while remaining profitable — the authorities watch, but you persist.",
        evaluator="elevated_heat_sustained",
    ),
    MilestoneSpec(
        id="shadow_profitability",
        name="Shadow Profitability",
        family=MilestoneFamily.SHADOW_NETWORK,
        description="Strong net profit despite elevated customs scrutiny.",
        evaluator="shadow_profitability",
    ),
    MilestoneSpec(
        id="shadow_seizure_recovery",
        name="Seizure Recovery",
        family=MilestoneFamily.SHADOW_NETWORK,
        description="Survived a cargo seizure and rebuilt — the business endures.",
        evaluator="seizure_recovery",
    ),

    # ===== Oceanic Reach (4) =====
    MilestoneSpec(
        id="oceanic_ei_access",
        name="East Indies Access",
        family=MilestoneFamily.OCEANIC_REACH,
        description="Acquired the East Indies Access Charter — the far trade routes are open.",
        evaluator="ei_access",
    ),
    MilestoneSpec(
        id="oceanic_ei_broker",
        name="East Indies Presence",
        family=MilestoneFamily.OCEANIC_REACH,
        description="Opened a broker office in the East Indies — local intelligence secured.",
        evaluator="ei_broker",
    ),
    MilestoneSpec(
        id="oceanic_galleon",
        name="Galleon Operator",
        family=MilestoneFamily.OCEANIC_REACH,
        description="Operating a Merchant Galleon — the long-haul workhorse.",
        evaluator="galleon_deployed",
    ),
    MilestoneSpec(
        id="oceanic_ei_standing",
        name="East Indies Reputation",
        family=MilestoneFamily.OCEANIC_REACH,
        description="Strong standing in the East Indies — a known operator in the spice quarter.",
        evaluator="ei_standing",
    ),

    # ===== Commercial Finance (4) =====
    MilestoneSpec(
        id="finance_first_insurance",
        name="First Insurance Payout",
        family=MilestoneFamily.COMMERCIAL_FINANCE,
        description="An insurance claim was paid — risk pricing proves its worth.",
        evaluator="first_insurance_success",
    ),
    MilestoneSpec(
        id="finance_credit_opened",
        name="First Credit Draw",
        family=MilestoneFamily.COMMERCIAL_FINANCE,
        description="Drew on a credit line — leverage is now part of the business.",
        evaluator="credit_opened",
    ),
    MilestoneSpec(
        id="finance_credit_clean",
        name="Clean Credit Record",
        family=MilestoneFamily.COMMERCIAL_FINANCE,
        description="Significant borrowing with no defaults — the market trusts your debt service.",
        evaluator="credit_clean",
    ),
    MilestoneSpec(
        id="finance_leveraged_expansion",
        name="Leveraged Expansion",
        family=MilestoneFamily.COMMERCIAL_FINANCE,
        description="Used credit to fund infrastructure growth — capital working for capital.",
        evaluator="leveraged_expansion",
    ),

    # ===== Integrated House (4) =====  [total: 27 milestones]
    # Actually we have 27, user spec said 20-28, this is in range.
    # But let's target ~25. Remove the "sustained_three_regions" to keep it at 26,
    # or add one more integrated house milestone. Let's keep all 27 — it's in range.
    MilestoneSpec(
        id="integrated_multi_region",
        name="Multi-Region Infrastructure",
        family=MilestoneFamily.INTEGRATED_HOUSE,
        description="Infrastructure assets across multiple regions — a commercial network.",
        evaluator="multi_region_infra",
    ),
    MilestoneSpec(
        id="integrated_major_contracts",
        name="Cross-Region Contract House",
        family=MilestoneFamily.INTEGRATED_HOUSE,
        description="5+ contracts completed with standing in 2+ regions.",
        evaluator="major_contracts_multi_region",
    ),
    MilestoneSpec(
        id="integrated_full_spectrum",
        name="Full-Spectrum Operation",
        family=MilestoneFamily.INTEGRATED_HOUSE,
        description="Using warehouses, brokers, licenses, insurance, and credit — a complete commercial toolkit.",
        evaluator="full_spectrum",
    ),
    MilestoneSpec(
        id="integrated_brigantine",
        name="Ship Upgrade",
        family=MilestoneFamily.INTEGRATED_HOUSE,
        description="Upgraded beyond the starting sloop — the business justified the investment.",
        evaluator="brigantine_acquired",
    ),
]


# Convenience: spec lookup by ID
MILESTONE_BY_ID: dict[str, MilestoneSpec] = {s.id: s for s in MILESTONE_SPECS}


def get_milestone_spec(milestone_id: str) -> MilestoneSpec | None:
    """Get a milestone spec by ID."""
    return MILESTONE_BY_ID.get(milestone_id)
