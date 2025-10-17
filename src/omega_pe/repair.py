from typing import List
from .models import Cohort

def suggest_repairs(cohort: Cohort) -> List[str]:
    fixes = []
    if cohort.available_time() < 3:
        fixes.append("Time credit: shift schedules or reduce mandatory hours")
    if cohort.transport_level < 1:
        fixes.append("Transport voucher or shuttle access key")
    if cohort.literacy_level < 1:
        fixes.append("Plain-language support or micro-tutorials")
    if not cohort.permissions:
        fixes.append("Grant necessary permissions/appeal channel")
    if "mentor" not in [s.lower() for s in cohort.supports]:
        fixes.append("Assign mentor/peer group for 30 days")
    return fixes