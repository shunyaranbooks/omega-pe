
from omega_pe.entropy import compute_option_entropy

def test_entropy_monotonic():
    assert compute_option_entropy(1) <= compute_option_entropy(2)
    assert compute_option_entropy(2) <= compute_option_entropy(3)
