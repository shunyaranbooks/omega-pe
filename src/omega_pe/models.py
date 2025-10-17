from dataclasses import dataclass, field
from typing import List, Set

@dataclass
class Action:
    id: str
    name: str
    cost: float
    time_hours: float
    skill_level_required: float  # 0=none, 1=basic, 2=high
    perms_required: List[str]
    support_tags: List[str]      # e.g., ["transport", "mentor"]
    outcome_signature: Set[str]  # used for de-dup clustering
    risk: float                  # expected externalized harm in [0,1]

@dataclass
class Cohort:
    id: str
    name: str
    money_per_week: float
    free_time_hours: float
    device_bandwidth_level: int  # 0/1/2
    transport_level: int         # 0/1/2
    literacy_level: int          # 0/1/2  (proxy for skills)
    caregiving_load_hours: float
    permissions: List[str] = field(default_factory=list)
    supports: List[str] = field(default_factory=list)

    def available_time(self) -> float:
        t = self.free_time_hours - self.caregiving_load_hours
        return max(0.0, t)