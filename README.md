# Omega-PE — Possibility Ethics Toolkit (v0.1.0)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17380933.svg)](https://doi.org/10.5281/zenodo.17380933)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Omega-PE** computes **Option Entropy (Ω)** and runs an **Option Audit** to measure whether a policy, product, or schedule expands people’s **safe, fair future options**. It operationalizes the normative objective:

> Maximize **Σ V·ΔΩ** (vulnerability-weighted increase in options) subject to a harm guardrail (Γ) and equity floors.

- 🔢 **Ω (Option Entropy):** `Ω = log(K)` where `K` = number of distinct, **viable** action classes a cohort can actually take within a horizon.  
- 🛡 **Γ (Guardrail):** excludes actions with high externalized harm.  
- ⚖️ **V (Weights):** prioritizes cohorts with fewer baseline options.  
- 🧰 **Option Repair:** suggests fixes if any cohort’s options shrink.

---

## Table of contents
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Input formats](#input-formats)
- [Outputs & interpretation](#outputs--interpretation)
- [Configuration (YAML params)](#configuration-yaml-params)
- [Method sketch](#method-sketch)
- [Reproducibility](#reproducibility)
- [Cite this work](#cite-this-work)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Installation

> Requires Python **3.9+**

```bash
# clone your repo first, then:
pip install -e .
(When published to PyPI, this will become pip install omega-pe.)

Quickstart
Run the included demo audit comparing two design variants to a baseline:

bash
Copy code
omega-audit audit \
  --cohorts examples/cohorts.csv \
  --actions examples/actions.csv \
  --params  examples/params_baseline.yaml \
  --variant examples/params_variant_A.yaml \
  --variant examples/params_variant_B.yaml \
  --out out_demo
You’ll get:

out_demo/omega_by_cohort.csv — per-cohort Ω, ΔΩ, V-weighted ΔΩ

out_demo/aggregate.csv — Σ V·ΔΩ and mean ΔΩ per variant

out_demo/repair_queue.json — cohorts flagged for Option Repair

Input formats
cohorts.csv
Each row is a cohort (persona or subgroup).

column	meaning
id, name	cohort id & label
money_per_week	usable budget (₹/week or your unit)
free_time_hours	free hours/week (before caregiving)
device_bandwidth_level	0=none, 1=limited, 2=good
transport_level	0=none, 1=some, 2=good
literacy_level	0=low, 1=basic, 2=high (skills/comprehension proxy)
caregiving_load_hours	hours/week that subtract from free time
permissions	keys/rights already held, pipe-sep (e.g., `library
supports	social/help resources, pipe-sep (e.g., `mentor

actions.csv
Each row is a candidate action the cohort might take.

column	meaning
id, name	action id & label
cost	cost in the same unit as money_per_week
time_hours	time required
skill_level_required	0=none, 1=basic, 2=high
perms_required	required permissions, pipe-sep
support_tags	needs like transport, mentor, peer (pipe-sep)
outcome_signature	keywords describing outcomes (for de-dup)
risk	expected externalized harm [0..1] (used by Γ)

Example files live in examples/.

Outputs & interpretation
omega_by_cohort.csv
column	meaning
cohort_id, cohort_name	cohort identifiers
omega_baseline	Ω under baseline params
omega_variant	Ω under the given variant
delta_omega	Ω_variant − Ω_baseline
v_weight	vulnerability weight V for this cohort
v_weighted_delta	V · ΔΩ
variant	variant file name

Interpretation: higher ΔΩ and V·ΔΩ = more real, safe future moves enabled.

aggregate.csv
total_weighted_delta — Σ V·ΔΩ across cohorts (primary objective)

mean_delta — average ΔΩ (sanity check)

repair_queue.json
Cohorts that lost options under any variant, with Option Repair suggestions (time credits, transport vouchers, permissions, mentoring, plain-language support, etc.).

Configuration (YAML params)
Parameters file (params_*.yaml) controls thresholds and weights.

yaml
Copy code
horizon_days: 7
tau: 0.6          # viability threshold for f_i(a;C_i)
gamma: 0.2        # harm guardrail Γ (exclude risk > γ)
theta: 0.85       # de-dup similarity (Jaccard) for outcome_signature
lambda_penalty: 0.0  # optional cognitive load penalty
vulnerability_alpha: 1.0  # smoothing for V-weights

weights:          # for viability scoring
  afford: 0.25
  time: 0.25
  skills: 0.20
  perms: 0.15
  support: 0.15
Tuning tips:

Lower tau → more actions count as viable (use sparingly).

Lower gamma → stricter harm guardrail.

Lower theta → merges more similar actions (stops menu inflation).

Method sketch
Viability 
𝑓
𝑖
(
𝑎
;
𝐶
𝑖
)
f 
i
​
 (a;C 
i
​
 ): combines affordability, time-fit, skills/permissions, supports.

Harm guardrail Γ: excludes actions with risk > γ.

De-dup: clusters actions by outcome_signature using Jaccard ≥ θ; count clusters K.

Entropy: Ωᵢ = log(K) (optional presentation-load penalty).

Aggregate: compute ΔΩ vs. baseline; sum Σ V·ΔΩ with vulnerability weights; apply equity floors; trigger Option Repair if any cohort loses options.

See Appendix A in the paper for pseudo-code and a one-page worksheet.

Reproducibility
Release DOI: 10.5281/zenodo.17380933 (versioned v0.1.0).

Git commit (example): b3e0d3e

Environment capture:

bash
Copy code
git rev-parse HEAD
python -m pip freeze | head -n 25
Cite this work
Software (APA):
Akhtar, M. A. K. (2025). Omega-PE: Possibility Ethics Option Entropy Toolkit (v0.1.0) [Computer software]. shunyaranbooks. https://doi.org/10.5281/zenodo.17380933

BibTeX:

bibtex
Copy code
@software{Akhtar_OmegaPE_2025,
  author  = {Akhtar, Mohammad Amir Khusru},
  title   = {Omega-PE: Possibility Ethics Option Entropy Toolkit},
  year    = {2025},
  version = {v0.1.0},
  doi     = {10.5281/zenodo.17380933},
  url     = {https://doi.org/10.5281/zenodo.17380933}
}
A CITATION.cff is included so GitHub can generate citations automatically.

Contributing
Issues and PRs are welcome. For new features:

Open an issue describing the use case.

Add tests in tests/ and docs in README/docs/.

Follow MIT license; keep core API stable.

License
MIT © 2025 Mohammad Amir Khusru Akhtar

Contact
Maintainer: Mohammad Amir Khusru Akhtar (Shunya)
Affiliation: Usha Martin University, Ranchi, India
Email: amir@umu.ac.in
