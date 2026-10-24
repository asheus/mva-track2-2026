#!/usr/bin/env python3
"""Order-of-magnitude exposure bound for oral amlexanox vs its NMD-effective range.

WHY THIS EXISTS: the decisive parameter for the allele-1 NMD route is whether oral
amlexanox reaches the 25-100 uM at which NMD inhibition / readthrough is reported in
cells. A literature search (23 Oct 2026) did NOT find a published human Cmax:

  - Oral et al. 2017 Cell Metab (PMID 28683283) dosed 50 mg PO TID for 12 weeks and
    states only that amlexanox and metabolites were "identifiable in the serum" with no
    responder/non-responder difference. No numeric concentration appears in the
    retrievable full text; the only concentration units in the paper are a 20 mM buffer.
  - DailyMed returns NO amlexanox label (the US topical product is delisted), so there
    is no US pharmacokinetics section to read.
  - The Japanese oral product (asthma/allergic rhinitis) is the likely home of the
    number and was not reachable from here.

So this computes a GENEROUS UPPER BOUND from dose and molecular weight alone. It is an
estimate, not a measurement, and it is deliberately biased in the drug's favour:
complete absorption, no first-pass loss, no elimination during absorption, instantaneous
distribution. A real Cmax must be lower than every figure printed here.
"""
MW = 298.29          # g/mol, amlexanox
DOSE_MG = 50.0       # the dose used in Oral 2017: 50 mg PO three times daily
VD_L = [10.0, 20.0, 50.0]   # plausible apparent Vd/F for a small carboxylic acid
EFFECTIVE_UM = (25.0, 100.0)  # Carrard screen 25 uM; Benslimane 2023 100 uM / 20 h

def main():
    umol = DOSE_MG * 1000.0 / MW      # ug / (ug/umol) = umol
    print(__doc__.split("WHY")[0].strip())
    print("dose %.0f mg  =  %.1f umol  (MW %.2f)" % (DOSE_MG, umol, MW))
    print()
    print("GENEROUS upper-bound plasma concentration, assuming F=1 and no elimination:")
    print("  %-10s %-14s %s" % ("Vd/F (L)", "C_max (uM)", "fold short of 25-100 uM"))
    for vd in VD_L:
        c = umol / vd                 # umol/L = uM
        lo = EFFECTIVE_UM[0] / c
        hi = EFFECTIVE_UM[1] / c
        print("  %-10.0f %-14.1f %.1f - %.0f x" % (vd, c, lo, hi))
    print()
    print("READ THIS BEFORE QUOTING ANY NUMBER ABOVE:")
    print("  1. These are TOTAL drug. Amlexanox is a carboxylic acid, so plasma protein")
    print("     binding is likely high and FREE concentration lower still. Binding was")
    print("     not found in an accessible source; it is unknown, not assumed.")
    print("  2. The 25-100 uM figures are in vitro, in serum-containing medium. In-vitro")
    print("     potency does not transfer 1:1, and for an albumin binder it usually")
    print("     transfers UNFAVOURABLY.")
    print("  3. Vd/F is UNKNOWN for amlexanox here. The three values are illustrative.")
    print("     If Vd/F is much smaller than 10 L the gap narrows; nothing rules that out.")
    print("  4. Therefore this does NOT establish the route fails. It establishes that a")
    print("     gap is likely and that the published human Cmax is the thing to find.")
    print()
    print("WHERE THE REAL NUMBER PROBABLY IS, in order of expected yield:")
    print("  a. The Japanese oral product's PMDA interview form (asthma / allergic")
    print("     rhinitis indication) - interview forms routinely carry Cmax, Tmax, AUC.")
    print("  b. The supplementary figure of Oral 2017 that the main text cites for drug")
    print("     metabolism; serum values are plotted there but not in the prose.")
    print("  c. Any Phase 1 of the obesity programme, if one was published separately.")

if __name__ == "__main__":
    main()
