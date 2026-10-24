#!/usr/bin/env python3
"""Does stability-style prediction really work better on buried residues? Tested against
MEASURED protein abundance, at a sample size our own finding does not have.

    python3 -m scripts.mva.burial_dependence_test

WHY THIS EXISTS. The claim that carries our entire allele-2 argument is the two-class
finding: stability prediction separates pathogenic from benign at AUC 0.952 inside the
folded pseudokinase core and 0.364 -- worse than chance -- across the binding interfaces.
p.Asn1002Lys sits at RSA 14%, inside the folding class, which is why we are willing to
say anything about its abundance at all.

That AUC rests on **5 pathogenic variants against 25 benign** (VUS-NOMINATION.md). It
carries a burial-matched permutation null, which is more than most small results get, but
five positives is five positives, and the number appears in the report, the methods
description and the video script as one of four on-screen figures. Nothing has ever tested
the underlying mechanism -- that destabilisation prediction tracks reality where a residue
is buried and fails where it is exposed -- on data where the answer was MEASURED.

It can be tested, on thousands of variants, in proteins that are not BUB1B. MaveDB holds
multiplexed assays that measure **steady-state protein abundance**: PTEN and TPMT by
VAMP-seq, NUDT15 stability, CYP2C9 and CYP2C19 abundance. Abundance is exactly the
quantity our thesis is about -- not function, not fitness -- so these are the right assays
rather than the convenient ones.

BUB1B ITSELF HAS NONE. MaveDB's 2,898 target genes contain no BUB1B, no BubR1, no BUB1,
and nothing else in the spindle checkpoint (no MAD2L1, MAD1L1, CENP*, CDC20, AURK*, PLK1).
Enumerated, not inferred from a failed search. So allele 2 cannot be scored against
measured data directly, and there is no near homolog to borrow from either. Calibrating
the mechanism on other proteins is the only route available.

WHAT IS TESTED. Two axes, and they are the two that C27 found survive where burial alone
does not:
  * |delta volume| -- the residue volume change (Zamyatnin 1972), the classic driver of
    core packing defects;
  * buried charge introduction -- a charged side chain placed in a hydrophobic interior.
Each is correlated against measured abundance separately inside buried positions
(RSA < 20%) and exposed ones (RSA > 50%), with the difference bootstrapped.

PASS / FAIL, fixed before looking:
  PASS  |rho| is higher at buried than exposed positions by >= 0.15, with the bootstrap
        95% CI of the difference excluding zero, in a majority of the assays.
  FAIL  the difference is < 0.05, or its CI includes zero, in a majority of assays.
Between those is INCONCLUSIVE and is reported as such.

A FAIL IS THE OUTCOME WORTH MOST, and that is recorded here before any result exists. If
measured abundance shows no burial-dependent accuracy, then the two-class finding was an
artefact of comparing predictions against predictions, our stated confidence about
N1002K's abundance loses its foundation, and the report has to say so. That would be a
more valuable contribution than another favourable number, because every other team's
structural argument rests on the same unexamined assumption.

LIMIT, stated in advance. These are five proteins, none of them a pseudokinase and none a
spindle-checkpoint protein, assayed in cell lines by fluorescence or mass spectrometry.
Burial-dependence replicating here supports the MECHANISM; it does not transfer the AUC to
BUB1B, and nothing downstream may read it as though it had.
"""
import json
import math
import random
import sys
import urllib.request

import numpy as np

sys.path.insert(0, __import__("pathlib").Path(__file__).resolve().parent.as_posix())
from neighbourhood_structure import MAXASA, THREE, VDW          # noqa: E402

API = "https://api.mavedb.org/api/v1"
# The model URL is RESOLVED through the API, never built by hand. The first version of
# this file hardcoded "-model_v4.pdb"; AlphaFold is on v6, so every fetch 404'd and the
# test reported "skipped, not assumed" for every assay -- a silent total failure that
# looked like orderly handling of missing data.
AF_API = "https://alphafold.ebi.ac.uk/api/prediction/{acc}"
OUT = __import__("pathlib").Path(__file__).resolve().parents[4].joinpath(
    "docs/mva/data/burial_dependence_test.json").as_posix()
BURIED, EXPOSED = 20.0, 50.0
MIN_N = 30               # per stratum, per assay; below this the assay is skipped
PASS_DIFF, FAIL_DIFF = 0.15, 0.05
BOOT = 2000
SEED = 20261016

# Zamyatnin 1972 residue volumes (A^3), the same table used by abundance_posterior.py.
VOL = {"A": 88.6, "R": 173.4, "N": 114.1, "D": 111.1, "C": 108.5, "Q": 143.8,
       "E": 138.4, "G": 60.1, "H": 153.2, "I": 166.7, "L": 166.7, "K": 168.6,
       "M": 162.9, "F": 189.9, "P": 112.7, "S": 89.0, "T": 116.1, "W": 227.8,
       "Y": 193.6, "V": 140.0}
CHARGED = set("DEKRH")

# MaveDB score sets measuring steady-state ABUNDANCE (not activity, not fitness).
ASSAYS = [
    ("PTEN VAMP-seq", "urn:mavedb:00000013-a-1"),
    ("TPMT VAMP-seq", "urn:mavedb:00000013-b-1"),
    ("NUDT15 stability", "urn:mavedb:00000055-a-1"),
    ("CYP2C9 abundance", "urn:mavedb:00000062-a-1"),
    ("CYP2C19 abundance", "urn:mavedb:00000062-b-1"),
]


def get_json(url):
    r = urllib.request.Request(url, headers={"Accept": "application/json",
                                             "User-Agent": "research/1.0"})
    return json.loads(urllib.request.urlopen(r, timeout=180).read())


def get_text(url):
    r = urllib.request.Request(url, headers={"User-Agent": "research/1.0"})
    return urllib.request.urlopen(url=r, timeout=300).read().decode(errors="replace")


def uniprot_of(score_set):
    for tg in score_set.get("targetGenes", []):
        for xid in tg.get("externalIdentifiers", []):
            ident = xid.get("identifier", {})
            if ident.get("dbName") == "UniProt":
                return ident.get("identifier")
    return None


def parse_scores(csv_text):
    """(pos, ref_aa, alt_aa, score) from hgvs_pro, single substitutions only."""
    import csv as _csv
    import io
    import re
    three_to_one = {v: k for k, v in
                    {"A": "Ala", "R": "Arg", "N": "Asn", "D": "Asp", "C": "Cys",
                     "Q": "Gln", "E": "Glu", "G": "Gly", "H": "His", "I": "Ile",
                     "L": "Leu", "K": "Lys", "M": "Met", "F": "Phe", "P": "Pro",
                     "S": "Ser", "T": "Thr", "W": "Trp", "Y": "Tyr",
                     "V": "Val"}.items()}
    pat = re.compile(r"^p\.([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2})$")
    out = []
    for row in _csv.DictReader(io.StringIO(csv_text)):
        h = (row.get("hgvs_pro") or "").strip()
        s = (row.get("score") or "").strip()
        if not h or not s:
            continue
        m = pat.match(h)
        if not m:
            continue                      # synonymous, nonsense, multi-mutant
        ref, pos, alt = three_to_one.get(m.group(1)), int(m.group(2)), \
            three_to_one.get(m.group(3))
        if not ref or not alt or ref == alt:
            continue
        try:
            out.append((pos, ref, alt, float(s)))
        except ValueError:
            continue
    return out


def rsa_from_pdb(pdb_text, n=480):
    """Shrake-Rupley RSA per residue, the same method as burial_vs_constraint.py."""
    atoms = []
    for line in pdb_text.split("\n"):
        if not line.startswith("ATOM"):
            continue
        el = line[76:78].strip() or line[12:16].strip()[0]
        atoms.append({"x": float(line[30:38]), "y": float(line[38:46]),
                      "z": float(line[46:54]), "el": el,
                      "seq": int(line[22:26]), "res": line[17:20].strip()})
    if not atoms:
        return {}, {}
    seqres = {}
    for a in atoms:
        seqres.setdefault(a["seq"], THREE.get(a["res"], "X"))
    xyz = np.array([[a["x"], a["y"], a["z"]] for a in atoms])
    rad = np.array([VDW.get(a["el"], 1.7) for a in atoms]) + 1.4
    seq = np.array([a["seq"] for a in atoms])
    k = np.arange(n)
    off = 2.0 / n
    inc = math.pi * (3 - math.sqrt(5))
    y = k * off - 1 + off / 2
    r = np.sqrt(np.maximum(0, 1 - y * y))
    phi = k * inc
    S = np.stack([np.cos(phi) * r, y, np.sin(phi) * r], axis=1)
    area = {}
    rmax = rad.max()
    for i in range(len(atoms)):
        d = np.linalg.norm(xyz - xyz[i], axis=1)
        nb = np.where((d < rad[i] + rmax) & (d > 0))[0]
        pts = xyz[i] + rad[i] * S
        dd = np.linalg.norm(pts[:, None, :] - xyz[nb][None, :, :], axis=2)
        acc = int(np.sum(~np.any(dd < rad[nb][None, :], axis=1)))
        area[seq[i]] = area.get(seq[i], 0.0) + 4 * math.pi * rad[i] ** 2 * acc / n
    rsa = {p: 100 * a / MAXASA.get(seqres[p], 200) for p, a in area.items()}
    return rsa, seqres


def spearman(a, b):
    n = len(a)
    if n < 3:
        return float("nan")

    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        rk = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for t in range(i, j + 1):
                rk[order[t]] = avg
            i = j + 1
        return rk
    ra, rb = rank(list(a)), rank(list(b))
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    da = math.sqrt(sum((x - ma) ** 2 for x in ra))
    db = math.sqrt(sum((y - mb) ** 2 for y in rb))
    return num / (da * db) if da and db else float("nan")


def boot_diff(xb, yb, xe, ye, rng):
    """Bootstrap the difference |rho_buried| - |rho_exposed|."""
    diffs = []
    for _ in range(BOOT):
        ib = [rng.randrange(len(xb)) for _ in range(len(xb))]
        ie = [rng.randrange(len(xe)) for _ in range(len(xe))]
        rb = spearman([xb[i] for i in ib], [yb[i] for i in ib])
        re_ = spearman([xe[i] for i in ie], [ye[i] for i in ie])
        if not (math.isnan(rb) or math.isnan(re_)):
            diffs.append(abs(rb) - abs(re_))
    diffs.sort()
    if not diffs:
        return float("nan"), float("nan"), float("nan")
    lo = diffs[int(0.025 * len(diffs))]
    hi = diffs[int(0.975 * len(diffs)) - 1]
    return sum(diffs) / len(diffs), lo, hi


def main():
    rng = random.Random(SEED)
    print(__doc__.split("LIMIT, stated in advance.")[0].strip()[-0:] or "", end="")
    print(f"PASS >= {PASS_DIFF} with CI excluding 0;  FAIL < {FAIL_DIFF} or CI "
          f"includes 0\n")
    results, verdicts = [], []
    for name, urn in ASSAYS:
        print("=" * 72)
        print(name, f"({urn})")
        try:
            ss = get_json(f"{API}/score-sets/{urn}")
            acc = uniprot_of(ss)
            if not acc:
                print("  no UniProt accession -- skipped")
                continue
            scores = parse_scores(get_text(f"{API}/score-sets/{urn}/scores"))
            meta = get_json(AF_API.format(acc=acc))
            entry = meta[0] if isinstance(meta, list) else meta
            pdb_url = entry.get("pdbUrl")
            if not pdb_url:
                print("  AlphaFold has no model for this accession -- skipped")
                continue
            pdb = get_text(pdb_url)
        except Exception as e:
            print(f"  fetch failed ({type(e).__name__}: {str(e)[:70]}) -- skipped")
            continue
        rsa, seqres = rsa_from_pdb(pdb)
        print(f"  UniProt {acc}   {len(scores)} single substitutions   "
              f"{len(rsa)} residues with RSA")
        # keep only variants whose reference residue matches the structure
        kept = [(p, r, a, s) for p, r, a, s in scores
                if p in rsa and seqres.get(p) == r]
        print(f"  reference-consistent with the AlphaFold model: {len(kept)}"
              f" ({len(kept) / max(1, len(scores)):.0%})")
        strata = {"buried": [v for v in kept if rsa[v[0]] < BURIED],
                  "exposed": [v for v in kept if rsa[v[0]] > EXPOSED]}
        print(f"  buried (RSA<{BURIED:.0f}%): {len(strata['buried']):5d}   "
              f"exposed (RSA>{EXPOSED:.0f}%): {len(strata['exposed']):5d}")
        if min(len(strata["buried"]), len(strata["exposed"])) < MIN_N:
            print(f"  a stratum is below {MIN_N} -- skipped rather than reported")
            continue
        row = {"assay": name, "urn": urn, "uniprot": acc,
               "n_buried": len(strata["buried"]),
               "n_exposed": len(strata["exposed"]), "axes": {}}
        for axis, fn in (("abs_delta_volume",
                          lambda p, r, a: abs(VOL.get(a, 0) - VOL.get(r, 0))),
                         ("buried_charge_introduced",
                          lambda p, r, a: 1.0 if (a in CHARGED and r not in CHARGED)
                          else 0.0)):
            xb = [fn(*v[:3]) for v in strata["buried"]]
            yb = [v[3] for v in strata["buried"]]
            xe = [fn(*v[:3]) for v in strata["exposed"]]
            ye = [v[3] for v in strata["exposed"]]
            rb, re_ = spearman(xb, yb), spearman(xe, ye)
            d, lo, hi = boot_diff(xb, yb, xe, ye, rng)
            v = ("PASS" if (d >= PASS_DIFF and lo > 0) else
                 "FAIL" if (d < FAIL_DIFF or lo <= 0 <= hi) else "INCONCLUSIVE")
            print(f"    {axis:26s} rho buried {rb:+.3f}   exposed {re_:+.3f}   "
                  f"diff {d:+.3f} [{lo:+.3f},{hi:+.3f}]  {v}")
            row["axes"][axis] = {"rho_buried": rb, "rho_exposed": re_,
                                 "diff": d, "ci": [lo, hi], "verdict": v}
            verdicts.append((name, axis, v))
        results.append(row)

    print("\n" + "=" * 72)
    print("OVERALL")
    print("=" * 72)
    if not results:
        print("  no assay produced a testable pair of strata. Nothing is claimed.")
        return 1
    for axis in ("abs_delta_volume", "buried_charge_introduced"):
        vs = [v for _n, a, v in verdicts if a == axis]
        p, f = vs.count("PASS"), vs.count("FAIL")
        call = ("PASS" if p > len(vs) / 2 else "FAIL" if f > len(vs) / 2
                else "INCONCLUSIVE")
        print(f"  {axis:26s} {p} pass / {f} fail of {len(vs)} assays -> {call}")
    print("\n  Burial-dependence replicating here supports the MECHANISM behind the")
    print("  two-class finding. It does NOT transfer the 0.952 AUC to BUB1B: five")
    print("  proteins, none a pseudokinase, none in the spindle checkpoint.")
    with open(OUT, "w") as fh:
        json.dump({"criteria": {"pass_diff": PASS_DIFF, "fail_diff": FAIL_DIFF,
                                "buried_rsa": BURIED, "exposed_rsa": EXPOSED,
                                "min_n": MIN_N, "bootstrap": BOOT, "seed": SEED},
                   "mavedb_has_bub1b": False,
                   "mavedb_target_genes_searched": 2898,
                   "results": results}, fh, indent=2)
    print(f"\nwrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
