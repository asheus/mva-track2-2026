#!/usr/bin/env python3
"""Estimate residual BubR1 protein in proband WGS_EX2312012 (BUB1B 737X / N1002K).

No measurement of this child's BubR1 exists. This derives an estimate from published
comparators, and states the reasoning so it can be attacked.

The model is two terms:   total BubR1 = allele_1 + allele_2
and the whole estimate turns on one question -- does the missense allele destabilise?

The literature supplies an internal control for exactly that question. Two published
MVA patient lines share the same architecture as this proband (a null truncating allele
in the 731-753 window plus one missense allele) and differ ONLY in whether the missense
partner destabilises:

    MVA-41C  731X / Y155C   Y155C measured NOT destabilising  -> 35% of control
    MVA-12C  753X / R814H   R814H measured destabilising      -> 17% of control

So the comparator set answers the question directly: a non-destabilising partner lands
near 35%, a destabilising partner near 17%.

Sources: Suijkerbuijk 2010 (PMC2887387) for the mutation classes, protein-turnover
mechanism and the 2-6 fold patient-line range (all text-verified); Xu 2013 (PMC3654266)
Fig 4A for the 35% / 17% values (FIGURE-DERIVED, quarantined per the review protocol,
used here only because the text-verified 2-6 fold range independently brackets them).
"""

# ---------------------------------------------------------------- allele 1: p.Leu737*
# NMD competence, computed from Ensembl ENST00000287598 exon structure.
PTC_TO_LAST_JUNCTION_NT = 747      # c.2210 sits 747 nt upstream of the last exon-exon junction
PTC_EXON, TOTAL_EXONS   = 17, 23
NMD_RULE_NT             = 55

nmd = PTC_TO_LAST_JUNCTION_NT > NMD_RULE_NT

# Empirical bracket: both flanking truncations are confirmed transcript-null in patients.
FLANKING = {"731X": 766, "753X": 700}   # nt upstream of last junction

allele_1 = 0.0    # fraction of one wild-type allele's output

# ------------------------------------------------------- allele 2: p.Asn1002Lys
# Calibration set, all measured in Suijkerbuijk 2010.
KINASE_DOMAIN = range(766, 1051)        # Zhang 2026 boundary
CALIB = {                               # residue: (label, destabilising?, burial RSA%, pLDDT)
    909:  ("I909T",  True,   3.6, 87.0),
    814:  ("R814H",  True,  16.4, 90.2),
    1012: ("L1012P", True,   0.2, 95.3),
    844:  ("L844F",  True,   0.9, 85.9),
    727:  ("R727C",  True,   6.2, 88.5),   # "near" the domain
    921:  ("Q921H",  False,  1.4, 83.2),   # the ONLY tolerated kinase-domain substitution
    550:  ("R550Q",  False, 80.1, 35.3),   # outside: exposed, disordered
    155:  ("Y155C",  False,  1.0, 96.3),   # outside: TPR domain
}
TARGET = (1002, "N1002K", 12.9, 91.1)

in_domain = lambda r: r in KINASE_DOMAIN or r == 727

# Base rate inside the kinase domain, from the calibration set only.
dom = [(l, d) for r, (l, d, _, _) in CALIB.items() if in_domain(r)]
n_destab = sum(1 for _, d in dom if d)
base_rate = n_destab / len(dom)

# ------------------------------------------------------- the estimate
LOW_PARTNER_NONDESTAB = 35.0   # % of control, MVA-41C
LOW_PARTNER_DESTAB    = 17.0   # % of control, MVA-12C
TEXT_VERIFIED_FOLD    = (2, 6) # "decreased 2-6 fold compared to wild-type alleles"

point   = LOW_PARTNER_DESTAB
# uncertainty: span the two comparators at the top, and the deepest text-verified fold at the bottom
# The two measurement systems disagree and the range must span both.
#   patient lines (native, NMD active)     : 2-6 fold  -> 17-50% of diploid
#   ectopic LAP-BUBR1 (equalised, no NMD)  : 5-10 fold -> allele 2 at 10-20% of one normal
#                                            allele -> 5-10% of diploid once allele 1 is null
# Ectopic overexpression probably saturates chaperone/degradation capacity differently, so
# the patient lines are the more physiological anchor -- but the controlled measurement of
# the missense allele in isolation points LOWER, and burying that would be dishonest.
lo      = 10.0                                    # downside scenario, from the ectopic system
hi      = 25.0                                    # partial destabilisation, toward the 35% arm

# threshold ladder, from the review
LADDER = [("gross missegregation, HeLa shRNA titration", 6, 13),
          ("progeroid phenotype, BubR1 hypomorph mouse", None, 10),
          ("MVA: aneuploidy + cancer risk + development", 17, 50)]

if __name__ == "__main__":
    print("ALLELE 1  p.Leu737*")
    print(f"  PTC {PTC_TO_LAST_JUNCTION_NT} nt upstream of last junction (exon {PTC_EXON}/{TOTAL_EXONS})")
    print(f"  50-55 nt NMD rule -> {'TRIGGERS NMD' if nmd else 'escapes NMD'}")
    print(f"  flanking truncations, both confirmed transcript-null: " +
          ", ".join(f"{k} ({v} nt)" for k, v in FLANKING.items()))
    print(f"  => contribution {allele_1:.0f}% of one wild-type allele\n")

    print("ALLELE 2  p.Asn1002Lys")
    print(f"  residue 1002 in kinase domain {KINASE_DOMAIN.start}-{KINASE_DOMAIN.stop-1}: "
          f"{in_domain(TARGET[0])}")
    print(f"  burial RSA {TARGET[2]}%, pLDDT {TARGET[3]} (confidently folded, mostly buried)")
    print(f"  kinase-domain calibration set: {n_destab}/{len(dom)} measured destabilising "
          f"(base rate {base_rate:.0%})")
    print(f"  the single tolerated one (Q921H) is a near-isosteric, uncharged swap (+9 A^3);")
    print(f"  N1002K is +54 A^3 AND introduces a formal positive charge at a buried site\n")

    print("ESTIMATE")
    print(f"  internal control: non-destabilising partner -> {LOW_PARTNER_NONDESTAB}% "
          f"| destabilising partner -> {LOW_PARTNER_DESTAB}%")
    print(f"  text-verified patient range: {TEXT_VERIFIED_FOLD[0]}-{TEXT_VERIFIED_FOLD[1]} fold "
          f"decrease = {100/TEXT_VERIFIED_FOLD[1]:.0f}-{100/TEXT_VERIFIED_FOLD[0]:.0f}% of control")
    print(f"  -> POINT ESTIMATE {point:.0f}% of normal BubR1, plausible range {lo:.0f}-{hi:.0f}%\n")

    print("AGAINST THE THRESHOLD LADDER")
    for name, l, h in LADDER:
        lo_s = "-" if l is None else f"{l}"
        verdict = "INSIDE" if (l is not None and l <= point <= h) else \
                  ("above this floor" if point > (h if l is None else l) else "below")
        print(f"  {name:<45} {lo_s}-{h}%   -> {verdict}")
    print()
    print(f"  Estimated {point:.0f}% sits ABOVE the {LADDER[0][1]}-{LADDER[0][2]}% cellular cliff,")
    print(f"  and AT THE SEVERE END of the {LADDER[2][1]}-{LADDER[2][2]}% band where MVA actually occurs.")
    print()
    fold_needed = LOW_PARTNER_NONDESTAB / point
    print(f"THERAPEUTIC TARGET")
    print(f"  reaching the milder comparator ({LOW_PARTNER_NONDESTAB}%) needs a "
          f"{fold_needed:.1f}-fold increase in BubR1.")
    print(f"  Suijkerbuijk showed forced overexpression of unstable mutants to wild-type levels")
    print(f"  'fully restored' checkpoint function -- so the ceiling is reachable in principle.")
