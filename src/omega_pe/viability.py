from typing import Dict
from .models import Action, Cohort

def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))

def viability_score(cohort: Cohort, action: Action, weights: Dict[str, float]) -> float:
    """Compute f_i(a; C_i) in [0,1] combining affordability, time fit, skills, perms, support."""
    eps = 1e-6
    afford = 1.0 - (action.cost / (cohort.money_per_week + eps))
    afford = clamp01(afford)

    avail = cohort.available_time()
    if avail <= 0:
        timefit = 0.0
    else:
        ratio = action.time_hours / (avail + 1e-6)
        timefit = clamp01(1.0 - ratio)

    skills = clamp01(1.0 - max(0.0, (action.skill_level_required - cohort.literacy_level) / 2.0))

    if not action.perms_required:
        perms = 1.0
    else:
        have = set([p.lower() for p in cohort.permissions])
        need = set([p.lower() for p in action.perms_required])
        perms = len(need.intersection(have)) / len(need) if len(need) > 0 else 1.0

    support = 1.0
    tags = set([t.lower() for t in action.support_tags])
    if "transport" in tags:
        support *= (cohort.transport_level / 2.0)
    if "mentor" in tags or "peer" in tags:
        support *= (1.0 if ("mentor" in [s.lower() for s in cohort.supports] or "peer" in [s.lower() for s in cohort.supports]) else 0.5)

    w = {
        "afford": 0.25, "time": 0.25, "skills": 0.2, "perms": 0.15, "support": 0.15
    }
    if weights:
        w.update(weights)
    score = (
        w["afford"] * afford +
        w["time"] * timefit +
        w["skills"] * skills +
        w["perms"] * perms +
        w["support"] * clamp01(support)
    )
    return clamp01(score)