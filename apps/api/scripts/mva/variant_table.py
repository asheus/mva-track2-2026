"""Every BUB1B variant in our literature corpus, by domain, with predictor scores.

Scores:
  AlphaMissense   -- missense only. NOTE: shown for completeness, but this predictor
                     FAILS calibration on BUB1B (PREDICTOR-CALIBRATION.md): it calls
                     3 of 6 proven MVA alleles likely-benign and scores below chance
                     on the destabilisation axis. Do not reason from this column.
  GPN-Star        -- m447 / p243 / v100, three evolutionary timescales. Percentiles
                     are against a MATCHED null: coding variants vs all 9,459 coding
                     SNVs, intronic variants vs all intronic SNVs in the gene span.
                     Mixing the two inflates coding variants by ~10x.
"""
import csv, json, re, statistics, urllib.request

AM_URL = "https://alphafold.ebi.ac.uk/files/AF-O60566-F1-aa-substitutions.csv"

DOMAINS = [  # Zhang 2026 map
    (26, 28, "KEN1"), (59, 219, "TPR"), (224, 232, "D-box 1"),
    (272, 277, "ABBA1"), (304, 306, "KEN2"), (340, 345, "ABBA2"),
    (408, 418, "GLEBS"), (440, 460, "Bub1-binding"), (528, 533, "ABBA3"),
    (555, 563, "D-box 2"), (668, 675, "KARD / LxxIxE"), (766, 1050, "pseudokinase"),
]

def domain(pos):
    for a, b, n in DOMAINS:
        if a <= pos <= b: return n
    return "linker / unassigned"

# label -> (protein pos or None, note, source)
META = {
 "R120Q":(120,"prostate cancer predisposition, monoallelic","PMC11251299"),
 "I147T":(147,"prostate ca; in-silico 'greatly destabilising'","PMC11251299"),
 "Y155C":(155,"MVA-41C w/ 731X. PATHOGENIC, protein levels UNCHANGED","PMC2887387"),
 "F175L":(175,"reference point: stable","PMC11251299"),
 "F175G":(175,"reference point: unstable","PMC11251299"),
 "R244C":(244,"prostate ca; little effect in silico","PMC11251299"),
 "K250R":(250,"PCAF acetylation site. Mouse K243R homozygote EMBRYONIC LETHAL","PMC3718975"),
 "E413K":(413,"reference point: unstable","PMC11251299"),
 "R416Q":(416,"prostate ca; little effect in silico","PMC11251299"),
 "R550Q":(550,"MEASURED: fully functional","PMC2887387"),
 "W722R":(722,"recurrent pregnancy loss, PCS 13.79%","PMC13349884"),
 "R727C":(727,"MVA w/ 386X. MEASURED: 5-10x reduced","PMC2887387"),
 "A739S":(739,"recurrent pregnancy loss; 2 residues from proband stop","PMC13349884"),
 "R770Q":(770,"biallelic w/ R194*; died 6mo. ARCHITECTURAL MATCH to proband","PMC11306263"),
 "R814H":(814,"MVA-12C w/ 753X. MEASURED: 5-10x reduced","PMC2887387"),
 "L844F":(844,"MVA. MEASURED: 5-10x reduced","PMC2887387"),
 "R893S":(893,"MVA1 monoallelic, also in unaffected father","PMC9616775"),
 "I909T":(909,"MVA w/ null allele. MEASURED: 5-10x reduced","PMC2887387"),
 "Q921H":(921,"MEASURED: indistinguishable from wild-type","PMC2887387"),
 "R999Q":(999,"annotated neighbour of the proband's residue","dbSNP"),
 "N1002K":(1002,"*** PROBAND ALLELE 2 ***","this case"),
 "N1004S":(1004,"annotated neighbour","dbSNP"),
 "D1005E":(1005,"annotated neighbour","dbSNP"),
 "L1012P":(1012,"MVA. MEASURED: 5-10x reduced. Closest structural analogue","PMC2887387"),
 "R194*":(194,"nonsense, biallelic w/ R770Q","PMC11306263"),
 "L737*":(737,"*** PROBAND ALLELE 1 *** NMD-competent","this case"),
 "c.1288+5G>A":(None,"splice, biallelic; MDS w/ monosomy 7 at 9y","PMC6500003"),
 "c.1402-5A>G":(None,"splice, biallelic; neuroblastoma 8mo, survived to adulthood","PMC7455400"),
 "c.2386-11A>G":(None,"splice, biallelic, same individual","PMC7455400"),
 "c.2577+5G>A":(None,"splice, biallelic; embryonal rhabdomyosarcoma","PMC10545765"),
}
# in the corpus but not scoreable by either predictor
UNSCOREABLE = [
 ("Q386X",386,"truncating; MVA w/ R727C. Exact cDNA not in our corpus","PMC2887387"),
 ("L731X",731,"truncating; MVA w/ Y155C. Reported to RESCUE when re-expressed","PMC2887387"),
 ("L753X",753,"truncating; MVA w/ R814H. Reported to FAIL. 22 residues from 731X","PMC2887387"),
 ("p.Glu391del",391,"in-frame deletion; prostate ca; reduces stability","PMC11251299"),
 ("c.498_505del",None,"8 bp deletion, biallelic; MDS","PMC6500003"),
 ("c.2405_2406del",802,"p.Ser802Cysfs*29; embryonal rhabdomyosarcoma","PMC10545765"),
 ("Alu ins intron 8",None,"structural variant - missed by exome SNV calling","PMC5462940"),
]


def load():
    lines = urllib.request.urlopen(AM_URL).read().decode().splitlines()
    am = {r["protein_variant"]: float(r["am_pathogenicity"]) for r in csv.DictReader(lines)}
    amc = {r["protein_variant"]: r["am_class"] for r in csv.DictReader(
        urllib.request.urlopen(AM_URL).read().decode().splitlines())}
    cds = json.load(open("/tmp/cds_exons.json"))
    coding = lambda p: any(a <= p <= b for a, b in cds)
    gpn = {}
    for m in ("m447", "p243", "v100"):
        rows = json.load(open(f"/tmp/gpn_{m}.json"))
        gpn[m] = ({(p, r, a): l for p, r, a, l in rows},
                  [l for p, r, a, l in rows if coding(p)],
                  [l for p, r, a, l in rows if not coding(p)])
    return am, amc, gpn, coding


def pct(v, pool):
    return 100.0 * sum(1 for x in pool if x < v) / len(pool)


def main():
    am, amc, gpn, coding = load()
    coords = json.load(open("/tmp/allcoords.json"))
    rows = []
    for label, (ppos, note, src) in META.items():
        hg = coords.get(label) or []
        rec = {"label": label, "pos": ppos, "note": note, "src": src,
               "domain": domain(ppos) if ppos else "intronic",
               "am": am.get(label), "amc": amc.get(label), "gpn": {}, "ambig": len(hg) > 1}
        snvs = [g for g in hg if re.fullmatch(r"NC_000015\.10:g\.\d+[ACGT]>[ACGT]", g)]
        rec["ambig"] = len(snvs) > 1
        rec["nonsnv"] = bool(hg) and not snvs
        for g in snvs:
            m = re.fullmatch(r"NC_000015\.10:g\.(\d+)([ACGT])>([ACGT])", g)
            pos_g, ref, alt = int(m.group(1)), m.group(2), m.group(3)
            isc = coding(pos_g)
            rec["coding"] = isc
            for mm, (tbl, cpool, ipool) in gpn.items():
                l = tbl.get((pos_g, ref, alt))
                if l is None: continue
                rec["gpn"].setdefault(mm, []).append((l, pct(l, cpool if isc else ipool)))
        rows.append(rec)
    rows.sort(key=lambda r: (r["pos"] is None, r["pos"] or 0))

    print("# Every BUB1B variant in the corpus, by domain, with predictor scores\n")
    print("GPN-Star percentile is against a MATCHED null (coding vs coding, intronic vs")
    print("intronic). LOWER percentile = more evolutionarily constrained.\n")
    print("| variant | pos | domain | AlphaMissense | m447 | p243 | v100 | what is known |")
    print("|---|---|---|---|---|---|---|---|")
    for r in rows:
        a = f"{r['am']:.3f} {r['amc']}" if r["am"] is not None else "n/a"
        gs = []
        for m in ("m447", "p243", "v100"):
            g = r["gpn"].get(m)
            gs.append("/".join(f"{x[1]:.0f}%" for x in g) if g else "—")
        star = "**" if "PROBAND" in r["note"] else ""
        if r.get("ambig"): r["label"] += " †"
        if r.get("nonsnv"): r["note"] += " [not a single-nucleotide change - GPN-Star n/a]"
        print(f"| {star}{r['label']}{star} | {r['pos'] or '—'} | {r['domain']} | {a} | "
              f"{gs[0]} | {gs[1]} | {gs[2]} | {r['note']} |")
    print("\n### In the corpus, scoreable by neither predictor\n")
    print("| variant | pos | domain | why not | what is known |")
    print("|---|---|---|---|---|")
    for lab, p, note, src in UNSCOREABLE:
        why = "indel / structural" if ("del" in lab or "ins" in lab) else "exact cDNA unknown"
        print(f"| {lab} | {p or '—'} | {domain(p) if p else '—'} | {why} | {note} |")
    json.dump(rows, open("/tmp/variant_table.json", "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
