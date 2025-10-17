import math

def estimate_cognitive_load(num_clusters: int) -> float:
    return math.sqrt(max(0, num_clusters)) / 10.0

def compute_option_entropy(k_distinct_actions: int, lambda_penalty: float = 0.0) -> float:
    k = max(1, int(k_distinct_actions))
    omega = math.log(k)
    if lambda_penalty and lambda_penalty > 0:
        load = estimate_cognitive_load(k)
        omega = max(0.0, omega - lambda_penalty * load)
    return omega