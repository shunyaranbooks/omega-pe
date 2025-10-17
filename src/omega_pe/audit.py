from typing import Dict, List, Tuple
import pandas as pd
from .models import Action, Cohort
from .viability import viability_score
from .harm import passes_guardrail
from .clustering import cluster_actions
from .entropy import compute_option_entropy

def omega_by_cohort(cohorts: List[Cohort], actions: List[Action], params: Dict) -> Dict[str, float]:
    tau = float(params.get('tau', 0.6))
    gamma = float(params.get('gamma', 0.2))
    theta = float(params.get('theta', 0.8))
    lam = float(params.get('lambda_penalty', 0.0))
    weights = params.get('weights', {})

    omegas = {}
    for c in cohorts:
        viable = []
        for a in actions:
            v = viability_score(c, a, weights)
            if v < tau:
                continue
            if not passes_guardrail(a, gamma):
                continue
            viable.append(a)
        clusters = cluster_actions(viable, theta) if viable else []
        k = len(clusters)
        omega = compute_option_entropy(k, lambda_penalty=lam)
        omegas[c.id] = omega
    return omegas

def vulnerability_weights(cohorts: List[Cohort], baseline_omega: Dict[str, float], alpha: float = 1.0) -> Dict[str, float]:
    v = {}
    for c in cohorts:
        base = baseline_omega.get(c.id, 0.0)
        v[c.id] = 1.0 / (alpha + base)
    return v

def run_audit(cohorts: List[Cohort], actions: List[Action], baseline_params: Dict, variant_params_list: List[Tuple[str, Dict]]):
    base = omega_by_cohort(cohorts, actions, baseline_params)
    weights = vulnerability_weights(cohorts, base, alpha=float(baseline_params.get('vulnerability_alpha', 1.0)))

    rows = []
    for variant_name, params in variant_params_list:
        var = omega_by_cohort(cohorts, actions, params)
        for c in cohorts:
            rows.append({
                "cohort_id": c.id,
                "cohort_name": c.name,
                "omega_baseline": base.get(c.id, 0.0),
                "omega_variant": var.get(c.id, 0.0),
                "delta_omega": var.get(c.id, 0.0) - base.get(c.id, 0.0),
                "v_weight": weights.get(c.id, 1.0),
                "v_weighted_delta": weights.get(c.id, 1.0) * (var.get(c.id, 0.0) - base.get(c.id, 0.0)),
                "variant": variant_name
            })
    df = pd.DataFrame(rows)
    return base, weights, df

def aggregate_objective(df: pd.DataFrame):
    aggs = df.groupby('variant').agg(
        total_weighted_delta=('v_weighted_delta', 'sum'),
        mean_delta=('delta_omega','mean')
    ).reset_index()
    return aggs