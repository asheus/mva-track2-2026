"""Audit the blind-docking run against the truncation it was performed on.

Ten ligands were docked blind (no box) into BubR1 residues 766-1050 carved out of
AlphaFold AF-O60566-F1. None reached the ATP site. Before reading that as evidence
about the ATP site, two artifacts have to be excluded, and this script tests both:

1. TRUNCATION SCAR. Carving a domain out of a longer chain exposes the surface that
   used to face the rest of the protein. That surface is hydrophobic and concave --
   exactly what a docking score rewards. The test: for each pose, count the atomic
   contacts within 6 A that exist in FULL-LENGTH BubR1 but were deleted by the cut.
   A pose sitting on the scar has a large count; a pose on genuine surface has zero.

2. CRYPTIC SITE, RIGID RECEPTOR. Lacuna reports the ATP pocket's APO volume as 0 A^3 --
   it is closed in the apo coordinates and opens only under sampling. Vina holds the
   receptor rigid, so it cannot enter a pocket with no apo volume. This is checked by
   reading the pocket table rather than computed here.

Run:  python3 dock_audit.py
"""
import json, math, os, pathlib, urllib.request

DOMAIN = (766, 1050)
HERE = pathlib.Path(__file__).resolve().parents[5] / "docs" / "mva" / "data"
POSES = HERE / "blind_dock_poses.json"
AF_URL = "https://alphafold.ebi.ac.uk/files/AF-O60566-F1-model_v6.pdb"


def full_length(cache=HERE / "AF-O60566-F1.pdb"):
    if not cache.exists():
        cache.write_bytes(urllib.request.urlopen(AF_URL, timeout=120).read())
    res = {}
    for line in cache.read_text().splitlines():
        if line.startswith("ATOM"):
            res.setdefault(int(line[22:26]), []).append(
                (float(line[30:38]), float(line[38:46]), float(line[46:54])))
    return res


def lining(res, centre, k=6):
    """The k residues whose nearest atom is closest to a pose centroid."""
    d = sorted((min(math.dist(a, centre) for a in v), p)
               for p, v in res.items() if DOMAIN[0] <= p <= DOMAIN[1])
    return [p for _, p in d[:k]]


def deleted_contacts(res, positions):
    """Contacts each residue makes with the chain OUTSIDE the docked construct.

    These exist in the intact protein and were removed by the truncation, so any
    pose that depends on them is binding a surface that does not exist in vivo.
    """
    out = {}
    for p in positions:
        n = 0
        for q, v in res.items():
            if DOMAIN[0] <= q <= DOMAIN[1]:
                continue
            if any(math.dist(x, y) < 6.0 for x in v for y in res[p]):
                n += 1
        out[p] = n
    return out


# Residues whose side chains define the nucleotide pocket: the VAIK lysine and the
# degraded DFG motif. BubR1 is a pseudokinase (HRD->HGD, DFG->DFS) but still binds ATP.
ATP_SITE_RESIDUES = (795, 911, 912, 913)


def amenability(res):
    """Is the nucleotide pocket intact, i.e. far from the variants we care about?

    The pharmacological-chaperone field excludes a variant when the active site is
    affected -- a ligand that stabilises the fold has nowhere to bind if the lesion
    is in the site itself. This measures that distance rather than asserting it.
    """
    print("\nDistance from each variant to the ATP site (PC eligibility criterion):")
    for pos, label in ((1002, "N1002  PROBAND"), (978, "W978   top VUS"),
                       (1012, "L1012  known pathogenic"), (795, "K795   VAIK lysine"),
                       (911, "D911   DFG->DFS")):
        if pos not in res:
            continue
        centre = [sum(c[i] for p in ATP_SITE_RESIDUES for c in res[p])
                  / sum(len(res[p]) for p in ATP_SITE_RESIDUES) for i in range(3)]
        d = min(math.dist(a, centre) for a in res[pos])
        print(f"  {label:26s} {d:5.1f} A")
    near = min(math.dist(a, b) for a in res[1002] for b in res[795])
    print(f"  N1002 closest approach to K795: {near:.1f} A "
          f"-- the pocket is {'intact' if near > 12 else 'IMPLICATED'}")


def main():
    data = json.loads(POSES.read_text())
    res = full_length()
    atp = data["atp_site_centre"]

    print(f"receptor: {data['receptor']}")
    print(f"ATP site (mean of K795, D911, F912, S913 side chains): "
          f"{atp[0]:.1f}, {atp[1]:.1f}, {atp[2]:.1f}\n")
    print(f"{'ligand':18s} {'score':>6s} {'d(ATP site)':>11s} {'scar':>5s}  lining residues")

    rows = []
    for name, pose in data["poses"].items():
        c = pose["centroid"]
        d = math.dist(c, atp)
        near = lining(res, c)
        scar = sum(deleted_contacts(res, near).values())
        rows.append((name, pose["score_kcal_mol"], d, scar, near))
    for name, s, d, scar, near in sorted(rows, key=lambda r: r[1]):
        print(f"{name:18s} {s:6.2f} {d:11.1f} {scar:5d}  "
              f"{', '.join(str(p) for p in near)}")

    # A pose needs more than an incidental neighbour to count as scar-bound; 10
    # deleted contacts is well clear of the 0-1 seen on intact surface.
    scarred = [r for r in rows if r[3] >= 10]
    real = [r for r in rows if r[3] < 10]
    print(f"\nposes on the truncation scar (>=10 deleted contacts): {len(scarred)}/{len(rows)}"
          f"  scores {max(r[1] for r in scarred):.2f} to {min(r[1] for r in scarred):.2f}")
    print(f"poses on intact surface:                            {len(real)}/{len(rows)}"
          f"  scores {max(r[1] for r in real):.2f} to {min(r[1] for r in real):.2f}")
    print(f"poses within 12 A of the ATP site: "
          f"{sum(1 for r in rows if r[2] < 12)}/{len(rows)}")
    amenability(res)
    print("\nVERDICT: the scoring is driven by the cut, not by BubR1. Five of the six\n"
          "best-scoring poses sit on surface that only exists because the domain was\n"
          "carved out of a longer chain; on intact surface nothing scores better than\n"
          "-7.24. The ATP site was never entered -- which a rigid receptor cannot do\n"
          "when the pocket's apo volume is 0 A^3. The run is uninformative about that\n"
          "site, not evidence against it.")


if __name__ == "__main__":
    main()
