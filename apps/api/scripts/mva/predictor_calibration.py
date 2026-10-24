"""Three-predictor calibration against the MEASURED BUB1B variants.

Rather than asking three predictors what they think of the proband's alleles, this
asks the prior question: do they get the variants whose answer we ALREADY KNOW right?

Ground truth: docs/mva/bub1b-dosage-review/extracted_units.json units D05/D06,
tracing to Suijkerbuijk 2010 (PMC2887387).
  D05 -- I909T, R814H, L1012P, L844F, R727C: 5-10 fold LOWER protein, fail to
         restore checkpoint or alignment.  Destabilised.
  D06 -- Y155C (pathogenic but protein levels UNCHANGED, separation-of-function),
         R550Q (fully functional), Q921H (in the kinase domain, indistinguishable
         from wild-type).

Two different axes are scored separately, because they are not the same question:
  (a) PATHOGENIC vs benign        -- Y155C counts as pathogenic
  (b) DESTABILISED vs stable      -- Y155C counts as stable; this is the axis the
                                     child's case actually turns on
"""
import csv, json, statistics, sys, urllib.request

AM_URL = "https://alphafold.ebi.ac.uk/files/AF-O60566-F1-aa-substitutions.csv"
GPN_MODELS = ("m447", "p243", "v100")

# protein change -> (hg38 pos, ref, alt).  Resolved via Ensembl variant_recoder
# against ENSP00000287598; see docs/mva/PREDICTOR-CALIBRATION.md for the
# internal consistency checks.
COORD = {
    "I909T": (40217543, "T", "C"), "R814H": (40212554, "G", "A"),
    "L1012P": (40220641, "T", "C"), "L844F": (40212643, "C", "T"),
    "R727C": (40209670, "C", "T"), "Y155C": (40176556, "A", "G"),
    "R550Q": (40202609, "G", "A"), "Q921H": (40217580, "G", "C"),
    "A739S": (40209706, "G", "T"), "W722R": (40209655, "T", "C"),
    "N1002K": (40220612, "T", "G"), "L737*": (40209701, "T", "G"),
}
DESTAB = ["I909T", "R814H", "L1012P", "L844F", "R727C"]
STABLE_NORMAL = ["R550Q", "Q921H"]
PATHO_STABLE = ["Y155C"]
QUERY = ["N1002K", "L737*"]
OTHER = ["A739S", "W722R"]

NOTE = {
    "I909T": "MVA allele, 5-10x reduced", "R814H": "MVA allele, 5-10x reduced",
    "L1012P": "MVA allele, 5-10x reduced", "L844F": "MVA allele, 5-10x reduced",
    "R727C": "MVA allele, 5-10x reduced",
    "Y155C": "MVA allele, levels UNCHANGED (separation-of-function)",
    "R550Q": "fully functional", "Q921H": "kinase domain, WT-like",
    "N1002K": "proband allele 2 (unmeasured)", "L737*": "proband allele 1, nonsense",
    "A739S": "monoallelic, recurrent pregnancy loss", "W722R": "monoallelic, RPL",
}


def load_am():
    lines = urllib.request.urlopen(AM_URL).read().decode().splitlines()
    return {r["protein_variant"]: float(r["am_pathogenicity"])
            for r in csv.DictReader(lines)}


def load_gpn(model):
    rows = json.load(open(f"/tmp/gpn_{model}.json"))
    return {(p, r, a): l for p, r, a, l in rows}, [l for _, _, _, l in rows]


def pctile(v, pool):
    return 100.0 * sum(1 for x in pool if x < v) / len(pool)


def auc(pos, neg):
    return sum((1 if a > b else 0.5 if a == b else 0)
               for a in pos for b in neg) / (len(pos) * len(neg))


def main():
    am = load_am()
    gpn = {m: load_gpn(m) for m in GPN_MODELS}

    # Direction check: GPN LLR is alt-vs-ref log-likelihood, so MORE NEGATIVE =
    # more constrained. Verify against the null before trusting any ranking.
    print("=" * 78)
    print("DIRECTION AND NULL (all %d SNVs across the BUB1B span)" %
          len(gpn["m447"][1]))
    print("=" * 78)
    for m in GPN_MODELS:
        pool = gpn[m][1]
        print(f"  GPN-Star {m}: mean {statistics.mean(pool):+.3f}  "
              f"median {statistics.median(pool):+.3f}  "
              f"1st pctile {sorted(pool)[len(pool)//100]:+.3f}")

    print()
    print("=" * 78)
    print("SCORES  (GPN shown as percentile: LOW percentile = more constrained)")
    print("=" * 78)
    hdr = f"  {'variant':8s} {'AM':>6s} {'AMpct':>6s}"
    for m in GPN_MODELS:
        hdr += f" {m+'_llr':>9s} {m+'%':>6s}"
    print(hdr + "   ground truth")
    print("  " + "-" * 118)

    S = {}
    for title, grp in (("MEASURED: DESTABILISED", DESTAB),
                       ("MEASURED: PATHOGENIC BUT STABLE", PATHO_STABLE),
                       ("MEASURED: NORMAL", STABLE_NORMAL),
                       ("PROBAND", QUERY),
                       ("OTHER", OTHER)):
        print(f"\n  -- {title}")
        for v in grp:
            pos, ref, alt = COORD[v]
            rec = {"am": am.get(v)}
            line = f"  {v:8s} "
            line += f"{rec['am']:6.3f} {pctile(rec['am'], list(am.values())):5.1f}%" \
                if rec["am"] is not None else f"{'n/a':>6s} {'n/a':>6s}"
            for m in GPN_MODELS:
                tbl, pool = gpn[m]
                l = tbl.get((pos, ref, alt))
                rec[m] = l
                line += f" {l:+9.3f} {pctile(l, pool):5.1f}%" if l is not None \
                    else f" {'MISSING':>9s} {'':>6s}"
            S[v] = rec
            print(line + f"   {NOTE[v]}")

    print()
    print("=" * 78)
    print("DISCRIMINATION  (AUC; 0.5 = coin flip, 1.0 = perfect)")
    print("=" * 78)
    print(f"  {'predictor':12s} {'(a) pathogenic vs normal':>26s} "
          f"{'(b) destabilised vs stable':>28s}")
    print("  " + "-" * 70)
    for name, key, flip in [("AlphaMissense", "am", False)] + \
                           [(f"GPN-Star {m}", m, True) for m in GPN_MODELS]:
        sgn = -1 if flip else 1     # GPN: more negative = more deleterious
        a = auc([sgn * S[v][key] for v in DESTAB + PATHO_STABLE],
                [sgn * S[v][key] for v in STABLE_NORMAL])
        b = auc([sgn * S[v][key] for v in DESTAB],
                [sgn * S[v][key] for v in STABLE_NORMAL + PATHO_STABLE])
        print(f"  {name:12s} {a:26.2f} {b:28.2f}")
    print("\n  n is 6 vs 2 (a) and 5 vs 3 (b). These AUCs cannot be significant in")
    print("  either direction -- they are descriptive, and read as such below.")

    print()
    print("=" * 78)
    print("PER-VARIANT MISSES  (true MVA alleles a predictor ranks as tolerable)")
    print("=" * 78)
    for name, key, flip in [("AlphaMissense", "am", False)] + \
                           [(f"GPN-Star {m}", m, True) for m in GPN_MODELS]:
        if key == "am":
            missed = [v for v in DESTAB + PATHO_STABLE if S[v]["am"] < 0.34]
            ctrl = f"Q921H={S['Q921H']['am']:.3f}"
        else:
            pool = gpn[key][1]
            missed = [v for v in DESTAB + PATHO_STABLE
                      if pctile(S[v][key], pool) > 25]
            ctrl = f"Q921H={pctile(S['Q921H'][key], pool):.1f}%ile"
        print(f"  {name:14s} misses {len(missed)}/6: {missed or '-'}   [control {ctrl}]")


if __name__ == "__main__":
    main()
