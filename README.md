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
- [Release notes (v0.1.0)](#release-notes-v010)
- [Cite this work](#cite-this-work)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)
- [Appendix A — Pseudo-code, Worksheet, Delta Table](#appendix-a--pseudo-code-worksheet-delta-table)

---

## Installation

> Requires Python **3.9+**

```bash
# clone your repo first, then:
pip install -e .
```

*(When published to PyPI, this will become `pip install omega-pe`.)*

---

## Quickstart

Run the included demo audit comparing two design variants to a baseline:

```bash
omega-audit audit   --cohorts examples/cohorts.csv   --actions examples/actions.csv   --params  examples/params_baseline.yaml   --variant examples/params_variant_A.yaml   --variant examples/params_variant_B.yaml   --out out_demo
```

You’ll get:
- `out_demo/omega_by_cohort.csv` — per-cohort Ω, ΔΩ, V-weighted ΔΩ  
- `out_demo/aggregate.csv` — Σ V·ΔΩ and mean ΔΩ per variant  
- `out_demo/repair_queue.json` — cohorts flagged for **Option Repair**

---

## Input formats

### `cohorts.csv`
Each row is a cohort (persona or subgroup).

| column | meaning |
|---|---|
| `id`, `name` | cohort id & label |
| `money_per_week` | usable budget (₹/week or your unit) |
| `free_time_hours` | free hours/week (before caregiving) |
| `device_bandwidth_level` | 0=none, 1=limited, 2=good |
| `transport_level` | 0=none, 1=some, 2=good |
| `literacy_level` | 0=low, 1=basic, 2=high (skills/comprehension proxy) |
| `caregiving_load_hours` | hours/week that subtract from free time |
| `permissions` | keys/rights already held, pipe-sep (e.g., `library|export|offline|appeal`) |
| `supports` | social/help resources, pipe-sep (e.g., `mentor|peer`) |

**Example cohorts provided**
```
id,name,money_per_week,free_time_hours,device_bandwidth_level,transport_level,literacy_level,caregiving_load_hours,permissions,supports
C1,Commuter Students,1200,18,1,1,1,6,library|export,mentor|peer
C2,First-Gen Low-Bandwidth,800,22,0,0,1,4,appeal,peer
C3,Working Caregivers,1500,12,2,1,2,8,export|offline,mentor
```

### `actions.csv`
Each row is a candidate action the cohort might take.

| column | meaning |
|---|---|
| `id`, `name` | action id & label |
| `cost` | cost in the same unit as `money_per_week` |
| `time_hours` | time required |
| `skill_level_required` | 0=none, 1=basic, 2=high |
| `perms_required` | required permissions, pipe-sep |
| `support_tags` | needs like `transport`, `mentor`, `peer` (pipe-sep) |
| `outcome_signature` | keywords describing outcomes (for de-dup) |
| `risk` | expected externalized harm [0..1] (used by Γ) |

Example files live in [`examples/`](examples/).

---

## Outputs & interpretation

### `omega_by_cohort.csv`
| column | meaning |
|---|---|
| `cohort_id`, `cohort_name` | cohort identifiers |
| `omega_baseline` | Ω under baseline params |
| `omega_variant` | Ω under the given variant |
| `delta_omega` | Ω_variant − Ω_baseline |
| `v_weight` | vulnerability weight V for this cohort |
| `v_weighted_delta` | V · ΔΩ |
| `variant` | variant file name |

Interpretation: higher **ΔΩ** and **V·ΔΩ** = more real, safe future moves enabled.

### `aggregate.csv`
- `total_weighted_delta` — Σ V·ΔΩ across cohorts (**primary objective**)  
- `mean_delta` — average ΔΩ (sanity check)

### `repair_queue.json`
Cohorts that lost options under any variant, with **Option Repair** suggestions (time credits, transport vouchers, permissions, mentoring, plain-language support, etc.).

---

## Configuration (YAML params)

Parameters file (`params_*.yaml`) controls thresholds and weights.

```yaml
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
```

Tuning tips:
- Lower `tau` → more actions count as viable (use sparingly).  
- Lower `gamma` → stricter harm guardrail.  
- Lower `theta` → merges more similar actions (stops menu inflation).

---

## Method sketch

1. **Viability** \(fᵢ(a;Cᵢ)\): combines affordability, time-fit, skills/permissions, supports.  
2. **Harm guardrail** Γ: excludes actions with `risk > γ`.  
3. **De-dup**: clusters actions by `outcome_signature` using Jaccard ≥ `θ`; count clusters `K`.  
4. **Entropy**: `Ωᵢ = log(K)` (optional presentation-load penalty).  
5. **Aggregate**: compute **ΔΩ** vs. baseline; sum **Σ V·ΔΩ** with vulnerability weights; apply equity floors; trigger **Option Repair** if any cohort loses options.

For formal definitions and practitioner tools, see **Appendix A** below.

---

## Reproducibility

- **Release DOI:** `10.5281/zenodo.17380933` (versioned **v0.1.0**).  
- **Git commit (example):** `b3e0d3e`  
- **Environment capture:**
  ```bash
  git rev-parse HEAD
  python -m pip freeze | head -n 25
  ```

**Suggested citation text for papers** appears in [Cite this work](#cite-this-work).

---

## Release notes (v0.1.0)

**Omega-PE v0.1.0 — Possibility Ethics Toolkit**

**Highlights**
- Viability scoring `f_i(a;C_i)` combining affordability, time-fit, skills/permissions, and supports  
- Harm guardrail **Γ** to exclude options with high externalized risk  
- Outcome de-duplication via Jaccard clustering on `outcome_signature` (prevents menu inflation)  
- Per-cohort **Ω = log(K)**; aggregation as **Σ V·ΔΩ** with built-in vulnerability weights  
- Heuristic **Option Repair** suggestions for cohorts with ΔΩ < 0  
- Example datasets and a one-command audit pipeline

**Install**
```bash
pip install -e .
# (future) pip install omega-pe
```

**Quickstart**
```bash
omega-audit audit   --cohorts examples/cohorts.csv   --actions examples/actions.csv   --params  examples/params_baseline.yaml   --variant examples/params_variant_A.yaml   --variant examples/params_variant_B.yaml   --out out_demo
```

**Artifacts**
- Wheel: `omega_pe-0.1.0-py3-none-any.whl`  
- Source: `omega_pe-0.1.0.tar.gz`  
- Checksums: `SHA256SUMS.txt`  

Verify:
```bash
sha256sum -c SHA256SUMS.txt
```

---

## Cite this work

**Software (APA):**  
Akhtar, M. A. K. (2025). *Omega-PE: Possibility Ethics Option Entropy Toolkit* (v0.1.0) [Computer software]. shunyaranbooks. https://doi.org/10.5281/zenodo.17380933

**BibTeX:**
```bibtex
@software{Akhtar_OmegaPE_2025,
  author  = {Akhtar, Mohammad Amir Khusru},
  title   = {Omega-PE: Possibility Ethics Option Entropy Toolkit},
  year    = {2025},
  version = {v0.1.0},
  doi     = {10.5281/zenodo.17380933},
  url     = {https://doi.org/10.5281/zenodo.17380933}
}
```

---

## License

**MIT © 2025 Mohammad Amir Khusru Akhtar**

<details>
<summary>Click to view full MIT text</summary>

MIT License

Copyright (c) 2025 Mohammad Amir Khusru Akhtar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons **to whom the Software is
furnished** to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
</details>

---

## Contributing

Issues and PRs are welcome. For new features:
1. Open an issue describing the use case.  
2. Add tests in `tests/` and docs in `README`/`docs/`.  
3. Keep core API stable; follow MIT license.

---

## Contact

**Maintainer:** Mohammad Amir Khusru Akhtar (Shunya)  
**Affiliation:** Usha Martin University, Ranchi, India  
**Email:** amir@umu.ac.in

---

## Appendix A — Pseudo-code, Worksheet, Delta Table

### A.1 Ω (Option Entropy) — Pseudo-code (language-agnostic)
```text
INPUTS:
- Cohorts C_i with constraints (money, time, skills/literacy, transport, permissions, supports)
- Actions A with cost/time/skill/perm/support/risk + outcome_signature
- Parameters: τ (viability), γ (harm guardrail), θ (de-dup similarity), λ (load penalty), V (vulnerability weights)

For each cohort i:
  SAFE := {}
  For each action a in A:
    v = f_i(a; C_i)    # combine affordability, time-fit, skills, perms, support ∈ [0,1]
    if v < τ: continue
    if risk(a) > γ: continue
    SAFE.add(a)

  CLUSTERS := cluster_by_similarity(SAFE, using outcome_signature, Jaccard ≥ θ)
  K := |CLUSTERS|
  Ω_i := log(max(K, 1)) - λ * load_penalty(K)   # optional penalty
Return Ω_i for all cohorts; compute ΔΩ vs. baseline; aggregate Σ V·ΔΩ.
```

### A.2 Option Audit — One-page Worksheet (template)

**Decision context:** *(policy/design choice you’re comparing)*  
**Horizon (H):** ☐ 7 ☐ 14 ☐ 30 days | **Population:** *(e.g., commuters, caregivers, low-bandwidth users)*

1) **Baseline constraints** (per cohort): money/wk, free time, device/bandwidth (0–2), transport (0–2), literacy (0–2), caregiving hrs, permissions, supports.  
2) **Candidate actions**: id, name, cost, time, skill level, perms needed, support tags, outcome signature, risk.  
3) **Viability** \(fᵢ(a;Cᵢ)\): weighted sum of affordability, time-fit, skills, perms, support. Choose **τ** ∈ [0,1].  
4) **Harm guardrail** Γ: exclude actions with **risk > γ**.  
5) **De-dup / clustering**: Jaccard ≥ **θ** on outcome_signature; count clusters **K**.  
6) **Compute Ω & ΔΩ**: `Ω_i = log(K)`; record baseline vs. variants.  
7) **Aggregate**: assign **Vᵢ** (higher for fewer baseline options); report **Σ V·ΔΩ**; ensure subgroup floors; plan **Option Repair** for any ΔΩ<0.

### A.3 One-page Delta Table — Where Possibility Ethics Differs

| Criterion | Utilitarianism | Capabilities (Sen/Nussbaum) | Republican Freedom (Pettit) | Relational Theories (Deleuze/Genealogy/ANT) | **Possibility Ethics (this repo)** |
|---|---|---|---|---|---|
| **Moral value** | Aggregate utility | Capabilities/functionings | Non-domination | Relational becoming | **V-weighted Option Entropy (Ω)** |
| **Objective** | Max total/avg utility | Expand central capabilities | Secure non-domination | Diagnose relations/power | **Max Σ V·ΔΩ** with Γ + subgroup floors |
| **Operationalization** | Utilities vague | Qualitative audits | Legal/structural | Descriptive/analytic | **Computable audit**: viability → Γ → de-dup → Ω |
| **Power & agency** | Agent-centric | Person + supports | Arbitrary control focus | Distributed agency | Distributed; **design lifts Ω** via time/access/skills/perm/supports |
| **Tech/policy steer** | Welfare proxies (clicks, QALYs) | Enabling infrastructure | Exits/appeals | Trace networks | **Exits, undo, portability, offline, plain-language** |
| **Auditability** | Weak | Moderate | Legal audits | Ethnographic | **High**: publish Ω calculators/assumptions; pre/post ΔΩ |
| **Equity** | Minority sacrifice risk | Equity ethos | Individual protection | Reveals marginalization | **Built-in**: V-weights + subgroup floors |
| **Time** | Often short-term | Life-course aware | Durable institutions | Becoming/process | **Polytemporal Ω** (keep options alive) |
| **Pathologies** | Wireheading, manipulation | Vagueness, paternalism | Legalism | Under-prescriptive | Junk options → blocked by Γ + de-dup; overload → penalty; error → open audits |

---
