
import os
import click
from .io import read_cohorts, read_actions, read_params
from .audit import run_audit, aggregate_objective
from .report import save_report

@click.group()
def main():
    """Omega-PE: Option Entropy (Ω) audit CLI."""

@main.command()
@click.option("--cohorts", required=True, type=click.Path(exists=True), help="Path to cohorts.csv")
@click.option("--actions", required=True, type=click.Path(exists=True), help="Path to actions.csv")
@click.option("--params", "baseline_params", required=True, type=click.Path(exists=True), help="Baseline params YAML")
@click.option("--variant", "variant_params", multiple=True, type=click.Path(exists=True), help="Variant params YAML (can pass multiple)")
@click.option("--out", "outdir", required=True, type=click.Path(), help="Output directory")
def audit(cohorts, actions, baseline_params, variant_params, outdir):
    """Run Option Audit comparing baseline vs. one or more variants."""
    cohorts_obj = read_cohorts(cohorts)
    actions_obj = read_actions(actions)
    base_params = read_params(baseline_params)
    variants = []
    if not variant_params:
        variants.append(("variant", base_params))
    else:
        for vp in variant_params:
            variants.append((os.path.splitext(os.path.basename(vp))[0], read_params(vp)))

    base, weights, df = run_audit(cohorts_obj, actions_obj, base_params, variants)
    save_report(outdir, base, weights, df, cohorts_obj)
    agg = aggregate_objective(df)
    click.echo("Wrote per-cohort results and aggregate summary to: %s" % outdir)
    click.echo(agg.to_string(index=False))
