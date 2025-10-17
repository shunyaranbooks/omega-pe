from typing import List, Set
from .models import Action

def jaccard(a: Set[str], b: Set[str]) -> float:
    if not a and not b:
        return 1.0
    inter = len(a.intersection(b))
    union = len(a.union(b))
    return 0.0 if union == 0 else inter / union

def cluster_actions(actions: List[Action], theta: float) -> List[list]:
    """Greedy clustering by Jaccard similarity on outcome_signature."""
    remaining = actions[:]
    clusters = []
    while remaining:
        seed = remaining.pop(0)
        cluster = [seed]
        keep = []
        for a in remaining:
            sim = jaccard(seed.outcome_signature, a.outcome_signature)
            if sim >= theta:
                cluster.append(a)
            else:
                keep.append(a)
        clusters.append(cluster)
        remaining = keep
    return clusters