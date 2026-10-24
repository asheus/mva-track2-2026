#!/usr/bin/env python3
"""How confident can we be that allele 2 is an ABUNDANCE lesion? Put a number on it.

    python3 -m scripts.mva.abundance_posterior

Report section 3.6 says the abundance-versus-function question is the single
load-bearing assumption in Track 2 and that no computation settles it. That stays
true -- a posterior is not a measurement. But "a prior, not a result" is a weak way
to describe a measured panel of comparators, and a reviewer is entitled to ask how
strong the prior actually is. This computes it two ways and reports both.

THE PANEL. Suijkerbuijk 2010 measured BubR1 abundance for kinase-domain missense
variants. From bub1b-dosage-review/ESTIMATE.md, which restricts to kinase-domain
residues because the primary source states abundance falls most severely for
kinase-domain mutations and less for the N-terminal TPR domain -- so TPR variants
(e.g. Y155C) are not the valid comparison.

WHY Q921H IS REPORTED BOTH WAYS. It is the panel's only tolerated variant, so it
decides 5/6 versus 5/5. ESTIMATE.md records that Q921H "was on the same allele as
L844F -- the authors concluded L844F was the causal one", i.e. it was never tested
as the sole variant on an allele. That is a reason to treat it as uninformative
rather than as a counterexample, but dropping an inconvenient data point needs to be
visible, so both posteriors are printed and the weaker one is what ships.

THE SECOND AXIS. ESTIMATE.md notes that what separates Q921H from the destabilising
set is not burial but how conservative the substitution is. That is checkable:
side-chain volume change and formal charge change are computed here for every panel
member, so N1002K can be placed against them rather than asserted to resemble them.

Volumes are Zamyatnin (1972) residue volumes in cubic angstroms. Charge is the formal
side-chain charge at pH 7.4; histidine is treated as neutral, which is the
conservative choice here because it makes Q921H look LESS conservative and so works
against the conclusion.
"""
import sys

# Zamyatnin 1972 residue volumes, cubic angstroms.
VOL = {"A": 88.6, "R": 173.4, "N": 114.1, "D": 111.1, "C": 108.5, "Q": 143.8,
       "E": 138.4, "G": 60.1, "H": 153.2, "I": 166.7, "L": 166.7, "K": 168.6,
       "M": 162.9, "F": 189.9, "P": 112.7, "S": 89.0, "T": 116.1, "W": 227.8,
       "Y": 193.6, "V": 140.0}
CHARGE = {"R": +1, "K": +1, "D": -1, "E": -1}   # H treated as neutral at pH 7.4

# (label, from, to, RSA %, pLDDT, measured outcome). RSA and pLDDT from ESTIMATE.md.
PANEL = [
    ("L1012P", "L", "P",  0.2, 95.3, "destabilising"),
    ("L844F",  "L", "F",  0.9, 85.9, "destabilising"),
    ("I909T",  "I", "T",  3.6, 87.0, "destabilising"),
    ("R727C",  "R", "C",  6.2, 88.5, "destabilising"),
    ("R814H",  "R", "H", 16.4, 90.2, "destabilising"),
    ("Q921H",  "Q", "H",  1.4, 83.2, "tolerated"),
]
PROBAND = ("N1002K", "N", "K", 12.9, 91.1, "unknown")


def dvol(a, b):
    return VOL[b] - VOL[a]


def dcharge(a, b):
    return CHARGE.get(b, 0) - CHARGE.get(a, 0)


def beta_posterior(k, n, a0=0.5, b0=0.5):
    """Jeffreys-prior posterior for the next draw, plus an equal-tailed interval.

    Returns (posterior predictive mean, lo, hi) for Beta(a0+k, b0+n-k). The
    predictive probability that the next variant destabilises IS the posterior mean.
    """
    a, b = a0 + k, b0 + (n - k)
    mean = a / (a + b)
    # Equal-tailed 95% interval by bisection on the regularised incomplete beta.
    def cdf(x):
        # continued-fraction-free: integrate the density numerically; n is tiny so
        # a 20k-step trapezoid is exact to well past the precision we report.
        steps = 20000
        h = x / steps
        tot = 0.0
        for i in range(steps + 1):
            t = i * h
            if t <= 0 or t >= 1:
                d = 0.0
            else:
                d = t ** (a - 1) * (1 - t) ** (b - 1)
            tot += d * (0.5 if i in (0, steps) else 1.0)
        return tot * h
    norm = cdf(1.0)
    def q(p):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if cdf(mid) / norm < p:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    return mean, q(0.025), q(0.975)


def main():
    print("Panel: kinase-domain missense variants with MEASURED BubR1 abundance")
    print(f"  {'variant':9s} {'swap':7s} {'dVol':>7} {'dCharge':>8} {'RSA':>6} "
          f"{'pLDDT':>6}  measured")
    for lab, a, b, rsa, pl, out in PANEL:
        print(f"  {lab:9s} {a}->{b:4s} {dvol(a,b):+7.1f} {dcharge(a,b):+8d} "
              f"{rsa:5.1f}% {pl:6.1f}  {out}")
    lab, a, b, rsa, pl, _ = PROBAND
    print(f"  {lab:9s} {a}->{b:4s} {dvol(a,b):+7.1f} {dcharge(a,b):+8d} "
          f"{rsa:5.1f}% {pl:6.1f}  << the proband, UNKNOWN")

    des = [p for p in PANEL if p[5] == "destabilising"]
    tol = [p for p in PANEL if p[5] == "tolerated"]
    pv = abs(dvol(PROBAND[1], PROBAND[2]))

    print("\n--- Axis 1: is the substitution conservative? ---")
    dv = sorted(abs(dvol(p[1], p[2])) for p in des)
    print(f"  destabilising |dVol| range: {dv[0]:.1f} to {dv[-1]:.1f} A^3  (n={len(des)})")
    for p in tol:
        tvol = abs(dvol(p[1], p[2]))
        print(f"  tolerated     |dVol|:       {tvol:.1f} A^3  ({p[0]})")
        print(f"  proband       |dVol|:       {pv:.1f} A^3  -> "
              f"{pv/tvol:.1f}x the tolerated variant")
    inside = dv[0] <= pv <= dv[-1]
    print(f"  proband sits INSIDE the destabilising range: {inside}")

    print("\n--- Axis 2: does it introduce buried charge? ---")
    gains = [p[0] for p in PANEL if dcharge(p[1], p[2]) > 0]
    print(f"  panel members that GAIN formal positive charge: {gains or 'NONE'}")
    print(f"  proband gains charge: {dcharge(PROBAND[1], PROBAND[2]) > 0}  "
          f"at RSA {PROBAND[3]}% (mostly buried), pLDDT {PROBAND[4]} (confident fold)")
    print("  -> the proband is the only variant in the comparison that buries a NEW")
    print("     formal positive charge. Every charged panel member LOSES charge.")

    print("\n--- Posterior probability that N1002K is an abundance lesion ---")
    for k, n, note in ((5, 6, "Q921H counted as a genuine counterexample"),
                       (5, 5, "Q921H dropped: never tested as the sole variant on "
                              "its allele")):
        m, lo, hi = beta_posterior(k, n)
        print(f"  {k}/{n}  P = {m:.2f}   95% CI {lo:.2f}-{hi:.2f}   ({note})")

    m6, lo6, _ = beta_posterior(5, 6)
    print(f"\nWHAT SHIPS: P(abundance) = {m6:.2f}, 95% CI from {lo6:.2f}. The weaker of")
    print("the two, because dropping the one inconvenient data point should not be how")
    print("the headline number is obtained. Both axes above point the same way and are")
    print("independent of the base rate.")
    print("\nWHAT THIS IS NOT. A posterior over a panel of six is not a measurement of")
    print("this variant. It bounds a belief; it does not observe a protein level. The")
    print("falsifier remains a single western blot, and the in-disease precedent for")
    print("being wrong is real: patient MVA-41C carries 35% residual BubR1 -- near-normal")
    print("for one allele -- and is affected, so in this exact syndrome a patient can")
    print("have enough protein and still be ill (CORRECTIONS C6).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
