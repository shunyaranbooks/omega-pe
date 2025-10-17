import os, json
import pandas as pd
from typing import Dict, List
from .models import Cohort
from .repair import suggest_repairs

def save_report(outdir: str, base_omega: Dict[str, float], weights: Dict[str, float], df_results: pd.DataFrame, cohorts: List[Cohort]):
    os.makedirs(outdir, exist_ok=True)
    df_results.to_csv(os.path.join(outdir, "omega_by_cohort.csv"), index=False)
    agg = df_results.groupby('variant').agg(
        total_weighted_delta=('v_weighted_delta','sum'),
        mean_delta=('delta_omega','mean')
    ).reset_index()
    agg.to_csv(os.path.join(outdir, "aggregate.csv"), index=False)

    repairs = []
    for c in cohorts:
        subset = df_results[df_results['cohort_id']==c.id]
        if (subset['delta_omega'] < 0).any():
            repairs.append({
                "cohort_id": c.id,
                "cohort_name": c.name,
                "repairs": suggest_repairs(c)
            })
    with open(os.path.join(outdir, "repair_queue.json"), "w") as f:
        json.dump(repairs, f, indent=2)