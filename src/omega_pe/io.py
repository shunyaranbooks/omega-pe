import pandas as pd
import yaml
from typing import List
from .models import Action, Cohort

def read_cohorts(path: str) -> List[Cohort]:
    df = pd.read_csv(path)
    cohorts = []
    for _, r in df.iterrows():
        cohorts.append(Cohort(
            id=str(r['id']), name=str(r['name']),
            money_per_week=float(r['money_per_week']),
            free_time_hours=float(r['free_time_hours']),
            device_bandwidth_level=int(r['device_bandwidth_level']),
            transport_level=int(r['transport_level']),
            literacy_level=int(r['literacy_level']),
            caregiving_load_hours=float(r.get('caregiving_load_hours', 0)),
            permissions=[p.strip() for p in str(r.get('permissions','')).split('|') if p.strip()],
            supports=[s.strip() for s in str(r.get('supports','')).split('|') if s.strip()],
        ))
    return cohorts

def parse_sig(x: str):
    return set([t.strip().lower() for t in str(x).split('|') if t.strip()])

def parse_list(x: str):
    return [t.strip() for t in str(x).split('|') if t.strip()]

def read_actions(path: str) -> List[Action]:
    df = pd.read_csv(path)
    actions = []
    for _, r in df.iterrows():
        actions.append(Action(
            id=str(r['id']), name=str(r['name']),
            cost=float(r['cost']), time_hours=float(r['time_hours']),
            skill_level_required=float(r['skill_level_required']),
            perms_required=parse_list(r.get('perms_required','')),
            support_tags=parse_list(r.get('support_tags','')),
            outcome_signature=parse_sig(r.get('outcome_signature','')),
            risk=float(r.get('risk',0.0))
        ))
    return actions

def read_params(path: str):
    import yaml
    with open(path, 'r') as f:
        return yaml.safe_load(f) or {}