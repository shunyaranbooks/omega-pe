from .models import Action

def passes_guardrail(action: Action, gamma: float) -> bool:
    return action.risk <= gamma