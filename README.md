# Omega-PE (v0.1.0) — Possibility Ethics Toolkit

**Option Entropy (Ω)** calculator and **Option Audit** CLI for measuring how a policy, product feature, or schedule **expands people’s safe and fair future options**.

> Moral objective: maximize vulnerability-weighted ΔΩ subject to a harm guardrail and equity floors.

## Install (local)
```bash
pip install -e .
```

## Quickstart
```bash
omega-audit audit   --cohorts examples/cohorts.csv   --actions examples/actions.csv   --params examples/params_baseline.yaml   --variant examples/params_variant_A.yaml   --out out_A
```

Outputs:
- `out_A/omega_by_cohort.csv`
- `out_A/aggregate.csv`
- `out_A/repair_queue.json`

## Concepts
- **Ω (Option Entropy):** `Ω = log(K)` where `K` is the number of **distinct viable action classes** reachable for a cohort within horizon `H`, after **harm screening** and **de-duplication by outcome similarity**.
- **Viability:** a weighted score of affordability, time fit, skills/permissions fit, support availability.
- **Γ (Harm guardrail):** excludes actions with expected externalized harm above `γ`.
- **V (Vulnerability weight):** higher for cohorts with fewer baseline options.
- **Option Repair:** if ΔΩ < 0 for a cohort, suggest targeted interventions (time, transport, skills, permissions).

## File formats
- `cohorts.csv` — constraints per cohort
- `actions.csv` — candidate actions with costs, requirements, and outcome signatures
- `params_*.yaml` — thresholds (τ, γ, θ), horizon, weights, and penalties

## License
MIT. See `LICENSE`.

## Citation
Please cite using `CITATION.cff`.