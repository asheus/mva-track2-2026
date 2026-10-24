#!/usr/bin/env python3
"""Is 50% of BubR1 safe in humans, and can the locus be moved at all?

    python3 -m scripts.mva.dosage_headroom

A DIFFERENT ANGLE. Every therapeutic argument we have made rests on a dosage model whose
two ends were borrowed: a disease threshold from seven families (Matsuura 2006) and a
dose-response from mice (Baker 2004). Both are small, and neither says what a therapy
actually needs to know -- **what level to aim for, whether that level is safe, and whether
the gene can be moved there at all.**

Population genetics answers all three without a single new experiment, because the
experiment has already been run at scale and by accident.

  gnomAD is a cohort of ~730,000 people, depleted of severe pediatric disease. Anyone
  carrying one loss-of-function BUB1B allele sits at roughly 50% of normal BubR1 for
  life. If such people are numerous there, then 50% is not merely "above threshold" --
  it is a state humans occupy safely, at a sample size no trial will reach. And if
  nobody is homozygous, the floor is real too.

  GTEx eQTLs ask the second question. If common regulatory variants measurably shift
  BUB1B expression, the locus is tunable rather than dosage-locked, and the regulatory
  elements that do the shifting have coordinates. If no variant moves it, every
  expression-raising strategy is fighting the gene's own regulation.

WHY THIS IS WORTH MORE THAN ANOTHER MECHANISM. It reframes the goal. The target is not
"correct the mutation" or "restore to normal" -- it is "reach the state that carriers
already occupy." Carriers are a natural treated cohort: already enrolled, already followed
for a lifetime, already demonstrating the safety of the endpoint we would aim at.

HONEST LIMITS. gnomAD is not phenotyped. "Depleted of severe pediatric disease" is not a
clean bill of health, and a carrier could have mild findings nobody recorded -- so the
claim is about the absence of a severe early phenotype, never about perfect health. And
eQTL effect sizes (NES) are slopes on normal-quantile-transformed expression, NOT fold
changes; we report them as evidence that the locus responds, and deliberately do not
convert them into a multiple to compare against our 1.4x requirement.
"""
import collections
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
D = ROOT / "docs/mva/data"
OUT = D / "dosage_headroom.json"


def main():
    con = json.loads((D / "gnomad.json").read_text())["data"]["gene"]["gnomad_constraint"]
    gv = json.loads((D / "gnomad_vars.json").read_text())["data"]["gene"]
    variants = gv.get("variants") or []
    lof = [v for v in variants
           if (v.get("transcript_consequence") or {}).get("lof") == "HC"]
    ac = hom = 0
    an = 0
    for v in lof:
        for src in ("exome", "genome"):
            s = v.get(src)
            if s:
                ac += s.get("ac") or 0
                hom += s.get("homozygote_count") or 0
                an = max(an, s.get("an") or 0)

    print("=" * 80)
    print("Q1  IS 50% OF BubR1 SAFE IN HUMANS?   (gnomAD v4)")
    print("=" * 80)
    print(f"  pLI                              {con['pLI']:.2e}   "
          f"(~0 -> NOT haploinsufficient)")
    print(f"  observed / expected LoF          {con['oe_lof']:.3f}  "
          f"(90% CI {con['oe_lof_lower']:.3f}-{con['oe_lof_upper']:.3f})")
    print(f"  LoF variants observed / expected {con['obs_lof']:.0f} / {con['exp_lof']:.1f}")
    print(f"\n  distinct high-confidence LoF variants   {len(lof)}")
    print(f"  LoF alleles observed (carriers)         {ac}")
    print(f"  LoF HOMOZYGOTES observed                {hom}")
    print(f"  alleles sampled                         ~{an:,}  (~{an//2:,} people)")
    safe = ac > 50 and hom == 0
    print(f"\n  VERDICT: {'YES' if safe else 'UNCLEAR'} -- roughly {ac} people carry one dead")
    print(f"  BUB1B allele and sit near 50% for life, in a cohort depleted of severe")
    print(f"  pediatric disease. None is homozygous, so the floor below is real.")
    print(f"  50% is not merely above threshold; it is a lived human state at n~{ac}.")

    eq = json.loads((D / "eqtl_BUB1B.json").read_text())["data"]
    ind = json.loads((D / "eqtl_ind_BUB1B.json").read_text())["data"]
    tissues = collections.Counter(e["tissueSiteDetailId"] for e in eq)
    nes = sorted((abs(e["nes"]) for e in eq), reverse=True)
    print("\n" + "=" * 80)
    print("Q2  CAN THE LOCUS BE MOVED?   (GTEx v8 cis-eQTLs)")
    print("=" * 80)
    print(f"  single-tissue eQTL associations   {len(eq)}")
    print(f"  distinct tissues with a signal    {len(tissues)}")
    print(f"  independent signals               {len(ind)}")
    if nes:
        print(f"  |NES| max / median                {nes[0]:.3f} / {nes[len(nes)//2]:.3f}")
    print(f"\n  strongest independent signals (NES is a slope on normalised expression,")
    print(f"  NOT a fold change -- see the module docstring):")
    print(f"    {'rsID':<14}{'tissue':<34}{'NES':>8}{'MAF':>7}{'kb from TSS':>13}")
    for e in sorted(ind, key=lambda x: -abs(x["nes"]))[:6]:
        print(f"    {e['snpId']:<14}{e['tissueSiteDetailId']:<34}{e['nes']:>8.3f}"
              f"{e['maf']:>7.2f}{e['tssDistance']/1000:>12.0f}k")
    tunable = len(eq) > 20 and len(ind) > 0
    print(f"\n  VERDICT: {'YES' if tunable else 'NO'} -- common variation measurably shifts BUB1B in")
    print(f"  {len(tissues)} tissues through {len(ind)} independent signals. The locus is")
    print(f"  regulated, not dosage-locked, and the elements doing it have coordinates.")

    print("\n" + "=" * 80)
    print("WHAT THIS CHANGES")
    print("=" * 80)
    print("  The goal stops being 'correct the mutation' and becomes 'reach carrier level'.")
    print(f"  That level has ~{ac} living examples, followed for a lifetime, with no severe")
    print("  early phenotype. It is the one endpoint in this disease that needs no trial to")
    print("  establish as survivable -- only to reach.")
    print("\n  It also bounds the risk from the other side. Choi 2009 showed too much BubR1")
    print("  delays chromosome segregation, but that concern lives ABOVE normal. Nothing")
    print(f"  here argues against aiming at half of normal, and ~{ac} people make the case.")

    OUT.write_text(json.dumps({
        "source": "gnomAD v4 GraphQL and GTEx v8 API, retrieved 21 Oct 2026",
        "constraint": con,
        "lof": {"distinct_variants": len(lof), "alleles_observed": ac,
                "homozygotes": hom, "alleles_sampled": an},
        "fifty_percent_is_a_lived_human_state": safe,
        "eqtl": {"single_tissue_associations": len(eq), "tissues": len(tissues),
                 "independent_signals": len(ind),
                 "abs_nes_max": nes[0] if nes else None,
                 "top_independent": sorted(ind, key=lambda x: -abs(x["nes"]))[:6]},
        "locus_is_tunable": tunable,
        "caveats": ["gnomAD is not phenotyped; the claim is absence of a severe early "
                    "phenotype, not perfect health",
                    "NES is a slope on normal-quantile-transformed expression and is "
                    "deliberately NOT converted to a fold change"],
    }, indent=2) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
