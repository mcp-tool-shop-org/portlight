"""Campaign engine — milestones, career profile, and victory truth.

This is the interpretive layer: it reads session truth and derives what kind
of trade house the player actually built. No fiction, no flavor toggles.
Everything here is mechanically grounded in ledger, contracts, reputation,
infrastructure, and ship history.

Core functions:
  - evaluate_milestones(session_snapshot) → newly completed milestones
  - compute_career_profile(session_snapshot) → ranked profile tags
  - compute_victory_progress(session_snapshot) → per-path progress

Design law:
  - Milestones derive from actual business history, not flags or counters.
  - Profile tags are weighted evidence, not arbitrary labels.
  - Victory paths represent commercial identities, not checklists.
  - Two runs that end rich in different ways must be distinguishable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from portlight.engine.contracts import ContractBoard
    from portlight.engine.infrastructure import InfrastructureState
    from portlight.engine.models import Captain, ReputationState, WorldState
    from portlight.receipts.models import ReceiptLedger


# ---------------------------------------------------------------------------
# Milestone families
# ---------------------------------------------------------------------------

class MilestoneFamily(str, Enum):
    REGIONAL_FOOTHOLD = "regional_foothold"
    LAWFUL_HOUSE = "lawful_house"
    SHADOW_NETWORK = "shadow_network"
    OCEANIC_REACH = "oceanic_reach"
    COMMERCIAL_FINANCE = "commercial_finance"
    INTEGRATED_HOUSE = "integrated_house"


# ---------------------------------------------------------------------------
# Milestone spec (content-driven definition)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class MilestoneSpec:
    """Static definition of a milestone. Content data, not runtime state."""
    id: str
    name: str
    family: MilestoneFamily
    description: str
    evaluator: str               # function name in _EVALUATORS registry


# ---------------------------------------------------------------------------
# Milestone completion (runtime state)
# ---------------------------------------------------------------------------

@dataclass
class MilestoneCompletion:
    """Record of a completed milestone."""
    milestone_id: str
    completed_day: int
    evidence: str = ""           # human-readable summary of what triggered it


# ---------------------------------------------------------------------------
# Campaign state (persisted)
# ---------------------------------------------------------------------------

@dataclass
class CampaignState:
    """All campaign progress. Persisted in save file."""
    completed: list[MilestoneCompletion] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Session snapshot — read-only view for evaluation
# ---------------------------------------------------------------------------

@dataclass
class SessionSnapshot:
    """Immutable snapshot of session state for milestone evaluation.

    This decouples the campaign engine from the session's mutable internals.
    Built by session.py before evaluation.
    """
    captain: "Captain"
    world: "WorldState"
    board: "ContractBoard"
    infra: "InfrastructureState"
    ledger: "ReceiptLedger"
    campaign: CampaignState


# ---------------------------------------------------------------------------
# Career profile
# ---------------------------------------------------------------------------

@dataclass
class ProfileScore:
    """A weighted profile tag with evidence."""
    tag: str
    score: float
    evidence: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Victory path
# ---------------------------------------------------------------------------

@dataclass
class VictoryRequirement:
    """One requirement within a victory path."""
    description: str
    met: bool
    detail: str = ""


@dataclass
class VictoryPathProgress:
    """Progress toward one victory condition."""
    path_id: str
    name: str
    requirements: list[VictoryRequirement] = field(default_factory=list)

    @property
    def met_count(self) -> int:
        return sum(1 for r in self.requirements if r.met)

    @property
    def total_count(self) -> int:
        return len(self.requirements)

    @property
    def is_complete(self) -> bool:
        return all(r.met for r in self.requirements)

    @property
    def is_active_candidate(self) -> bool:
        """At least half the requirements are met — this path is live."""
        return self.total_count > 0 and self.met_count >= self.total_count // 2


# ---------------------------------------------------------------------------
# Evaluator helpers — read session truth
# ---------------------------------------------------------------------------

def _completed_ids(snap: SessionSnapshot) -> set[str]:
    return {c.milestone_id for c in snap.campaign.completed}


def _active_warehouses(snap: SessionSnapshot) -> list:
    return [w for w in snap.infra.warehouses if w.active]


def _active_brokers(snap: SessionSnapshot) -> list:
    from portlight.engine.infrastructure import BrokerTier
    return [b for b in snap.infra.brokers if b.active and b.tier != BrokerTier.NONE]


def _active_licenses(snap: SessionSnapshot) -> list:
    return [lic for lic in snap.infra.licenses if lic.active]


def _has_license(snap: SessionSnapshot, license_id: str) -> bool:
    return any(lic.license_id == license_id and lic.active for lic in snap.infra.licenses)


def _trust_tier(snap: SessionSnapshot) -> str:
    from portlight.engine.reputation import get_trust_tier
    return get_trust_tier(snap.captain.standing)


def _trust_rank(tier: str) -> int:
    return {"unproven": 0, "new": 1, "credible": 2, "reliable": 3, "trusted": 4}.get(tier, 0)


def _regions_with_standing(snap: SessionSnapshot, min_standing: int) -> list[str]:
    return [r for r, s in snap.captain.standing.regional_standing.items() if s >= min_standing]


def _max_heat(snap: SessionSnapshot) -> int:
    return max(snap.captain.standing.customs_heat.values()) if snap.captain.standing.customs_heat else 0


def _min_heat(snap: SessionSnapshot) -> int:
    return min(snap.captain.standing.customs_heat.values()) if snap.captain.standing.customs_heat else 0


def _completed_contracts(snap: SessionSnapshot) -> list:
    return [o for o in snap.board.completed if o.outcome_type in ("completed", "completed_bonus")]


def _completed_contract_families(snap: SessionSnapshot) -> dict[str, int]:
    """Count completed contracts by template family."""
    from portlight.engine.contracts import ContractFamily
    counts: dict[str, int] = {}
    for c in snap.board.completed:
        if c.outcome_type in ("completed", "completed_bonus"):
            # We don't store family on outcome, but we can infer from template
            # For now count by outcome_type
            counts[c.outcome_type] = counts.get(c.outcome_type, 0) + 1
    return counts


def _total_completed_contracts(snap: SessionSnapshot) -> int:
    return len(_completed_contracts(snap))


def _total_trades(snap: SessionSnapshot) -> int:
    return len(snap.ledger.receipts)


def _ship_class(snap: SessionSnapshot) -> str:
    if not snap.captain.ship:
        return "sloop"
    from portlight.content.ships import SHIPS
    template = SHIPS.get(snap.captain.ship.template_id)
    return template.ship_class.value if template else "sloop"


def _regions_with_broker(snap: SessionSnapshot) -> set[str]:
    from portlight.engine.infrastructure import BrokerTier
    return {b.region for b in snap.infra.brokers if b.active and b.tier != BrokerTier.NONE}


def _regions_with_warehouse(snap: SessionSnapshot) -> set[str]:
    """Regions that have an active warehouse (need port→region mapping)."""
    regions = set()
    for w in snap.infra.warehouses:
        if not w.active:
            continue
        port = snap.world.ports.get(w.port_id)
        if port:
            regions.add(port.region)
    return regions


def _credit_active_no_defaults(snap: SessionSnapshot) -> bool:
    credit = snap.infra.credit
    if credit is None:
        return False
    return credit.active and credit.defaults == 0


def _insurance_claims_paid(snap: SessionSnapshot) -> int:
    return sum(1 for c in snap.infra.claims if not c.denied and c.payout > 0)


def _policies_purchased(snap: SessionSnapshot) -> int:
    return len(snap.infra.policies)


# ---------------------------------------------------------------------------
# Milestone evaluators — each returns (met, evidence_string)
# ---------------------------------------------------------------------------

def _eval_first_warehouse(snap: SessionSnapshot) -> tuple[bool, str]:
    wh = _active_warehouses(snap)
    if wh:
        return True, f"Warehouse at {wh[0].port_id}"
    return False, ""


def _eval_first_broker(snap: SessionSnapshot) -> tuple[bool, str]:
    brokers = _active_brokers(snap)
    if brokers:
        return True, f"Broker in {brokers[0].region}"
    return False, ""


def _eval_standing_one_region(snap: SessionSnapshot) -> tuple[bool, str]:
    regions = _regions_with_standing(snap, 10)
    if regions:
        return True, f"Standing 10+ in {regions[0]}"
    return False, ""


def _eval_strong_standing_one_region(snap: SessionSnapshot) -> tuple[bool, str]:
    regions = _regions_with_standing(snap, 25)
    if regions:
        return True, f"Standing 25+ in {regions[0]}"
    return False, ""


def _eval_presence_two_regions(snap: SessionSnapshot) -> tuple[bool, str]:
    regions = _regions_with_standing(snap, 5)
    if len(regions) >= 2:
        return True, f"Established in {', '.join(regions[:2])}"
    return False, ""


def _eval_sustained_three_regions(snap: SessionSnapshot) -> tuple[bool, str]:
    regions = _regions_with_standing(snap, 10)
    if len(regions) >= 3:
        return True, f"Standing 10+ in all three regions"
    return False, ""


# --- Lawful house ---

def _eval_credible_trust(snap: SessionSnapshot) -> tuple[bool, str]:
    tier = _trust_tier(snap)
    if _trust_rank(tier) >= 2:
        return True, f"Trust tier: {tier}"
    return False, ""


def _eval_reliable_trust(snap: SessionSnapshot) -> tuple[bool, str]:
    tier = _trust_tier(snap)
    if _trust_rank(tier) >= 3:
        return True, f"Trust tier: {tier}"
    return False, ""


def _eval_regional_charter(snap: SessionSnapshot) -> tuple[bool, str]:
    for lic_id in ("med_trade_charter", "wa_commerce_permit", "ei_access_charter"):
        if _has_license(snap, lic_id):
            return True, f"License: {lic_id}"
    return False, ""


def _eval_high_rep_charter(snap: SessionSnapshot) -> tuple[bool, str]:
    if _has_license(snap, "high_rep_charter"):
        return True, "High Reputation Commercial Charter acquired"
    return False, ""


def _eval_lawful_contracts_completed(snap: SessionSnapshot) -> tuple[bool, str]:
    count = _total_completed_contracts(snap)
    if count >= 5:
        return True, f"{count} contracts completed successfully"
    return False, ""


def _eval_low_heat_scaling(snap: SessionSnapshot) -> tuple[bool, str]:
    """Achieved reliable trust while keeping max heat <= 5."""
    tier = _trust_tier(snap)
    max_h = _max_heat(snap)
    if _trust_rank(tier) >= 3 and max_h <= 5:
        return True, f"Reliable trust with max heat {max_h}"
    return False, ""


# --- Shadow network ---

def _eval_first_discreet_success(snap: SessionSnapshot) -> tuple[bool, str]:
    # luxury_discreet contracts show in completed outcomes
    # We check for any completed contract where the summary contains "discreet" or template family
    for o in snap.board.completed:
        if o.outcome_type in ("completed", "completed_bonus"):
            # Best heuristic: check if any active/completed contract had luxury_discreet family
            # Since outcome doesn't store family, check for keyword in summary
            if "luxury" in o.summary.lower() or "discreet" in o.summary.lower():
                return True, "First discreet luxury delivery"
    # Fallback: check for elevated heat + profitability
    return False, ""


def _eval_elevated_heat_sustained(snap: SessionSnapshot) -> tuple[bool, str]:
    """Sustained heat >= 15 in any region while staying profitable."""
    max_h = _max_heat(snap)
    if max_h >= 15 and snap.captain.silver >= 500:
        return True, f"Operating at heat {max_h} with {snap.captain.silver} silver"
    return False, ""


def _eval_shadow_profitability(snap: SessionSnapshot) -> tuple[bool, str]:
    """Net profit > 2000 while having sustained heat."""
    profit = snap.ledger.net_profit
    max_h = _max_heat(snap)
    if profit > 2000 and max_h >= 10:
        return True, f"Profit {profit} with heat {max_h}"
    return False, ""


def _eval_seizure_recovery(snap: SessionSnapshot) -> tuple[bool, str]:
    """Survived a cargo seizure and still operating profitably."""
    had_seizure = any(
        i.incident_type == "inspection" and "seized" in i.description.lower()
        for i in snap.captain.standing.recent_incidents
    )
    if had_seizure and snap.captain.silver >= 300:
        return True, "Recovered from cargo seizure"
    return False, ""


# --- Oceanic reach ---

def _eval_ei_access(snap: SessionSnapshot) -> tuple[bool, str]:
    if _has_license(snap, "ei_access_charter"):
        return True, "East Indies Access Charter acquired"
    return False, ""


def _eval_ei_broker(snap: SessionSnapshot) -> tuple[bool, str]:
    if "East Indies" in _regions_with_broker(snap):
        return True, "Broker office in East Indies"
    return False, ""


def _eval_galleon_deployed(snap: SessionSnapshot) -> tuple[bool, str]:
    if _ship_class(snap) == "galleon":
        return True, "Operating a Merchant Galleon"
    return False, ""


def _eval_ei_standing(snap: SessionSnapshot) -> tuple[bool, str]:
    standing = snap.captain.standing.regional_standing.get("East Indies", 0)
    if standing >= 15:
        return True, f"East Indies standing: {standing}"
    return False, ""


# --- Commercial finance ---

def _eval_first_insurance_success(snap: SessionSnapshot) -> tuple[bool, str]:
    paid = _insurance_claims_paid(snap)
    if paid >= 1:
        return True, f"{paid} insurance claims paid"
    return False, ""


def _eval_credit_opened(snap: SessionSnapshot) -> tuple[bool, str]:
    credit = snap.infra.credit
    if credit and credit.total_borrowed > 0:
        return True, f"Credit used, {credit.total_borrowed} total borrowed"
    return False, ""


def _eval_credit_clean(snap: SessionSnapshot) -> tuple[bool, str]:
    if _credit_active_no_defaults(snap) and snap.infra.credit.total_borrowed >= 200:
        return True, f"Borrowed {snap.infra.credit.total_borrowed} with no defaults"
    return False, ""


def _eval_leveraged_expansion(snap: SessionSnapshot) -> tuple[bool, str]:
    """Used credit + has multiple infrastructure assets."""
    credit = snap.infra.credit
    wh = len(_active_warehouses(snap))
    brokers = len(_active_brokers(snap))
    if credit and credit.total_borrowed >= 300 and credit.defaults == 0 and (wh + brokers) >= 3:
        return True, f"Borrowed {credit.total_borrowed}, {wh} warehouses + {brokers} brokers"
    return False, ""


# --- Integrated house ---

def _eval_multi_region_infra(snap: SessionSnapshot) -> tuple[bool, str]:
    wh_regions = _regions_with_warehouse(snap)
    bk_regions = _regions_with_broker(snap)
    infra_regions = wh_regions | bk_regions
    if len(infra_regions) >= 2:
        return True, f"Infrastructure in {', '.join(sorted(infra_regions))}"
    return False, ""


def _eval_full_spectrum(snap: SessionSnapshot) -> tuple[bool, str]:
    """Has warehouse + broker + license + insurance used + credit used."""
    wh = len(_active_warehouses(snap)) >= 1
    brokers = len(_active_brokers(snap)) >= 1
    licenses = len(_active_licenses(snap)) >= 1
    insured = _policies_purchased(snap) >= 1
    credit = snap.infra.credit is not None and snap.infra.credit.total_borrowed > 0
    met = sum([wh, brokers, licenses, insured, credit])
    if met >= 4:
        parts = []
        if wh: parts.append("warehouse")
        if brokers: parts.append("broker")
        if licenses: parts.append("license")
        if insured: parts.append("insurance")
        if credit: parts.append("credit")
        return True, f"Using {', '.join(parts)}"
    return False, ""


def _eval_major_contracts_multi_region(snap: SessionSnapshot) -> tuple[bool, str]:
    """5+ completed contracts and standing 10+ in 2+ regions."""
    contracts = _total_completed_contracts(snap)
    regions = _regions_with_standing(snap, 10)
    if contracts >= 5 and len(regions) >= 2:
        return True, f"{contracts} contracts, standing in {', '.join(regions)}"
    return False, ""


def _eval_brigantine_acquired(snap: SessionSnapshot) -> tuple[bool, str]:
    sc = _ship_class(snap)
    if sc in ("brigantine", "galleon"):
        return True, f"Operating a {sc}"
    return False, ""


# ---------------------------------------------------------------------------
# Evaluator registry
# ---------------------------------------------------------------------------

_EVALUATORS: dict[str, callable] = {
    "first_warehouse": _eval_first_warehouse,
    "first_broker": _eval_first_broker,
    "standing_one_region": _eval_standing_one_region,
    "strong_standing_one_region": _eval_strong_standing_one_region,
    "presence_two_regions": _eval_presence_two_regions,
    "sustained_three_regions": _eval_sustained_three_regions,
    "credible_trust": _eval_credible_trust,
    "reliable_trust": _eval_reliable_trust,
    "regional_charter": _eval_regional_charter,
    "high_rep_charter": _eval_high_rep_charter,
    "lawful_contracts_completed": _eval_lawful_contracts_completed,
    "low_heat_scaling": _eval_low_heat_scaling,
    "first_discreet_success": _eval_first_discreet_success,
    "elevated_heat_sustained": _eval_elevated_heat_sustained,
    "shadow_profitability": _eval_shadow_profitability,
    "seizure_recovery": _eval_seizure_recovery,
    "ei_access": _eval_ei_access,
    "ei_broker": _eval_ei_broker,
    "galleon_deployed": _eval_galleon_deployed,
    "ei_standing": _eval_ei_standing,
    "first_insurance_success": _eval_first_insurance_success,
    "credit_opened": _eval_credit_opened,
    "credit_clean": _eval_credit_clean,
    "leveraged_expansion": _eval_leveraged_expansion,
    "multi_region_infra": _eval_multi_region_infra,
    "full_spectrum": _eval_full_spectrum,
    "major_contracts_multi_region": _eval_major_contracts_multi_region,
    "brigantine_acquired": _eval_brigantine_acquired,
}


# ---------------------------------------------------------------------------
# Evaluate milestones
# ---------------------------------------------------------------------------

def evaluate_milestones(
    specs: list[MilestoneSpec],
    snap: SessionSnapshot,
) -> list[MilestoneCompletion]:
    """Check all milestones against current session state.

    Returns only newly completed milestones (not already in snap.campaign.completed).
    """
    already = _completed_ids(snap)
    newly: list[MilestoneCompletion] = []

    for spec in specs:
        if spec.id in already:
            continue
        evaluator = _EVALUATORS.get(spec.evaluator)
        if evaluator is None:
            continue
        met, evidence = evaluator(snap)
        if met:
            completion = MilestoneCompletion(
                milestone_id=spec.id,
                completed_day=snap.world.day,
                evidence=evidence,
            )
            newly.append(completion)
            already.add(spec.id)  # prevent double-fire in same pass

    return newly


# ---------------------------------------------------------------------------
# Career profile scoring
# ---------------------------------------------------------------------------

def compute_career_profile(snap: SessionSnapshot) -> list[ProfileScore]:
    """Derive ranked profile tags from session truth.

    Returns list sorted by score descending. Top tag = primary identity.
    """
    rep = snap.captain.standing
    scores: list[ProfileScore] = []

    # --- Lawful House ---
    lawful = 0.0
    lawful_ev = []
    tier = _trust_tier(snap)
    rank = _trust_rank(tier)
    lawful += rank * 10
    if rank >= 3:
        lawful_ev.append(f"trust: {tier}")
    if _min_heat(snap) <= 3:
        lawful += 15
        lawful_ev.append("low heat")
    for lic_id in ("med_trade_charter", "wa_commerce_permit", "ei_access_charter", "high_rep_charter"):
        if _has_license(snap, lic_id):
            lawful += 10
            lawful_ev.append(lic_id)
    completed = _total_completed_contracts(snap)
    lawful += min(completed * 3, 30)
    if completed >= 3:
        lawful_ev.append(f"{completed} contracts completed")
    scores.append(ProfileScore("Lawful House", lawful, lawful_ev))

    # --- Shadow Operator ---
    shadow = 0.0
    shadow_ev = []
    max_h = _max_heat(snap)
    if max_h >= 10:
        shadow += min(max_h * 2, 40)
        shadow_ev.append(f"max heat: {max_h}")
    if snap.captain.captain_type == "smuggler":
        shadow += 15
        shadow_ev.append("smuggler captain")
    # Seizure survival
    seizures = sum(
        1 for i in rep.recent_incidents
        if "seized" in i.description.lower()
    )
    if seizures > 0 and snap.captain.silver >= 200:
        shadow += seizures * 10
        shadow_ev.append(f"survived {seizures} seizures")
    if snap.ledger.net_profit > 1500 and max_h >= 10:
        shadow += 20
        shadow_ev.append("profitable under heat")
    scores.append(ProfileScore("Shadow Operator", shadow, shadow_ev))

    # --- Oceanic Carrier ---
    oceanic = 0.0
    oceanic_ev = []
    ei_standing = rep.regional_standing.get("East Indies", 0)
    if ei_standing >= 5:
        oceanic += ei_standing * 2
        oceanic_ev.append(f"East Indies standing: {ei_standing}")
    if _has_license(snap, "ei_access_charter"):
        oceanic += 20
        oceanic_ev.append("EI access charter")
    if "East Indies" in _regions_with_broker(snap):
        oceanic += 15
        oceanic_ev.append("EI broker")
    if _ship_class(snap) == "galleon":
        oceanic += 25
        oceanic_ev.append("galleon operator")
    elif _ship_class(snap) == "brigantine":
        oceanic += 10
        oceanic_ev.append("brigantine capable")
    scores.append(ProfileScore("Oceanic Carrier", oceanic, oceanic_ev))

    # --- Contract Specialist ---
    contract = 0.0
    contract_ev = []
    contract += min(completed * 5, 50)
    if completed >= 3:
        contract_ev.append(f"{completed} contracts delivered")
    bonus_count = sum(1 for o in snap.board.completed if o.outcome_type == "completed_bonus")
    if bonus_count > 0:
        contract += bonus_count * 8
        contract_ev.append(f"{bonus_count} early bonuses")
    scores.append(ProfileScore("Contract Specialist", contract, contract_ev))

    # --- Infrastructure Builder ---
    infra = 0.0
    infra_ev = []
    wh = len(_active_warehouses(snap))
    bk = len(_active_brokers(snap))
    lics = len(_active_licenses(snap))
    infra += wh * 10 + bk * 12 + lics * 15
    if wh >= 2:
        infra_ev.append(f"{wh} warehouses")
    if bk >= 2:
        infra_ev.append(f"{bk} broker offices")
    if lics >= 2:
        infra_ev.append(f"{lics} licenses")
    regions = _regions_with_warehouse(snap) | _regions_with_broker(snap)
    if len(regions) >= 2:
        infra += 15
        infra_ev.append(f"presence in {len(regions)} regions")
    scores.append(ProfileScore("Infrastructure Builder", infra, infra_ev))

    # --- Leveraged Trader ---
    leverage = 0.0
    leverage_ev = []
    credit = snap.infra.credit
    if credit and credit.total_borrowed > 0:
        leverage += min(credit.total_borrowed // 10, 30)
        leverage_ev.append(f"borrowed {credit.total_borrowed}")
        if credit.defaults == 0:
            leverage += 20
            leverage_ev.append("no defaults")
        if credit.total_repaid > credit.total_borrowed * 0.5:
            leverage += 15
            leverage_ev.append("repaying responsibly")
    scores.append(ProfileScore("Leveraged Trader", leverage, leverage_ev))

    # --- Risk-Managed Merchant ---
    risk = 0.0
    risk_ev = []
    policies = _policies_purchased(snap)
    claims_paid = _insurance_claims_paid(snap)
    if policies > 0:
        risk += policies * 8
        risk_ev.append(f"{policies} policies purchased")
    if claims_paid > 0:
        risk += claims_paid * 12
        risk_ev.append(f"{claims_paid} claims paid")
    if policies >= 3 and _trust_rank(_trust_tier(snap)) >= 2:
        risk += 15
        risk_ev.append("systematic insurance user")
    scores.append(ProfileScore("Risk-Managed Merchant", risk, risk_ev))

    # Sort by score descending
    scores.sort(key=lambda s: s.score, reverse=True)
    return scores


# ---------------------------------------------------------------------------
# Victory path evaluation
# ---------------------------------------------------------------------------

def compute_victory_progress(snap: SessionSnapshot) -> list[VictoryPathProgress]:
    """Evaluate all victory paths against current session state."""
    paths: list[VictoryPathProgress] = []

    # --- Lawful Trade House ---
    lawful = VictoryPathProgress(path_id="lawful_house", name="Lawful Trade House")
    tier = _trust_tier(snap)
    lawful.requirements = [
        VictoryRequirement(
            "Trusted commercial standing",
            _trust_rank(tier) >= 4,
            f"Currently: {tier}",
        ),
        VictoryRequirement(
            "High Reputation Commercial Charter",
            _has_license(snap, "high_rep_charter"),
        ),
        VictoryRequirement(
            "Standing 15+ in 2 regions",
            len(_regions_with_standing(snap, 15)) >= 2,
            f"Regions at 15+: {', '.join(_regions_with_standing(snap, 15)) or 'none'}",
        ),
        VictoryRequirement(
            "8+ contracts completed",
            _total_completed_contracts(snap) >= 8,
            f"Completed: {_total_completed_contracts(snap)}",
        ),
        VictoryRequirement(
            "Max heat ≤ 5",
            _max_heat(snap) <= 5,
            f"Max heat: {_max_heat(snap)}",
        ),
        VictoryRequirement(
            "2000+ silver",
            snap.captain.silver >= 2000,
            f"Silver: {snap.captain.silver}",
        ),
    ]
    paths.append(lawful)

    # --- Shadow Network ---
    shadow = VictoryPathProgress(path_id="shadow_network", name="Shadow Network")
    shadow.requirements = [
        VictoryRequirement(
            "Net profit > 3000",
            snap.ledger.net_profit > 3000,
            f"Profit: {snap.ledger.net_profit}",
        ),
        VictoryRequirement(
            "Sustained heat ≥ 15 in any region",
            _max_heat(snap) >= 15,
            f"Max heat: {_max_heat(snap)}",
        ),
        VictoryRequirement(
            "2000+ silver on hand",
            snap.captain.silver >= 2000,
            f"Silver: {snap.captain.silver}",
        ),
        VictoryRequirement(
            "5+ successful trades under heat",
            _total_trades(snap) >= 10 and _max_heat(snap) >= 10,
            f"Trades: {_total_trades(snap)}, max heat: {_max_heat(snap)}",
        ),
        VictoryRequirement(
            "Operational resilience (survived seizure or maintained profitability)",
            snap.ledger.net_profit > 2000 and _max_heat(snap) >= 10,
            f"Profit: {snap.ledger.net_profit}",
        ),
    ]
    paths.append(shadow)

    # --- Oceanic Reach ---
    oceanic = VictoryPathProgress(path_id="oceanic_reach", name="Oceanic Reach")
    oceanic.requirements = [
        VictoryRequirement(
            "East Indies Access Charter",
            _has_license(snap, "ei_access_charter"),
        ),
        VictoryRequirement(
            "East Indies broker office",
            "East Indies" in _regions_with_broker(snap),
        ),
        VictoryRequirement(
            "Galleon or Brigantine",
            _ship_class(snap) in ("galleon", "brigantine"),
            f"Ship: {_ship_class(snap)}",
        ),
        VictoryRequirement(
            "East Indies standing ≥ 15",
            snap.captain.standing.regional_standing.get("East Indies", 0) >= 15,
            f"EI standing: {snap.captain.standing.regional_standing.get('East Indies', 0)}",
        ),
        VictoryRequirement(
            "5+ contracts completed",
            _total_completed_contracts(snap) >= 5,
            f"Completed: {_total_completed_contracts(snap)}",
        ),
        VictoryRequirement(
            "2000+ silver",
            snap.captain.silver >= 2000,
            f"Silver: {snap.captain.silver}",
        ),
    ]
    paths.append(oceanic)

    # --- Commercial Empire ---
    empire = VictoryPathProgress(path_id="commercial_empire", name="Commercial Empire")
    infra_regions = _regions_with_warehouse(snap) | _regions_with_broker(snap)
    empire.requirements = [
        VictoryRequirement(
            "Infrastructure in 3 regions",
            len(infra_regions) >= 3,
            f"Regions: {', '.join(sorted(infra_regions)) or 'none'}",
        ),
        VictoryRequirement(
            "Reliable+ trust",
            _trust_rank(_trust_tier(snap)) >= 3,
            f"Trust: {_trust_tier(snap)}",
        ),
        VictoryRequirement(
            "Insurance and credit used",
            _policies_purchased(snap) >= 1 and snap.infra.credit is not None and snap.infra.credit.total_borrowed > 0,
        ),
        VictoryRequirement(
            "10+ contracts completed",
            _total_completed_contracts(snap) >= 10,
            f"Completed: {_total_completed_contracts(snap)}",
        ),
        VictoryRequirement(
            "3000+ silver",
            snap.captain.silver >= 3000,
            f"Silver: {snap.captain.silver}",
        ),
        VictoryRequirement(
            "3+ active licenses",
            len(_active_licenses(snap)) >= 3,
            f"Active: {len(_active_licenses(snap))}",
        ),
    ]
    paths.append(empire)

    return paths
