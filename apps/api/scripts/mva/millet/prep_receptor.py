"""Convert the BubR1 pseudokinase domain to PDBQT and define the docking box.

Vina needs AutoDock atom types and Gasteiger charges. Meeko's receptor path pulls in a
full polymer/template stack that is overkill for a single rigid chain from AlphaFold,
so this writes the PDBQT directly: the typing rules for a protein with no metals, no
cofactors and no non-standard residues are short and it is better to see them than to
trust a black box.

THE BOX IS THE POINT. The previous campaign used a hosted Vina with no box parameter,
so every dock was blind and the scoring was captured by the truncation scar
(DOCKING-AUDIT.md). A box centred on the chosen allosteric site makes the question
"what binds HERE" instead of "where on this construct is the greasiest patch".
"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
NS = ROOT / "docs/mva/data/neurosnap"
BOX_SIZE = 18.0          # A per side. Generous for a 134 A^3 pocket, and small
                         # enough that the nearest decoy box (20.4 A away) does
                         # not overlap it -- otherwise a decoy scores the target.

# AutoDock types. Protein heavy atoms only; polar H are added implicitly by using the
# united-atom convention Vina expects (NA/OA/SA are H-bond acceptors).
ACCEPTOR_N = {"ASN": {"OD1"}, "GLN": {"OE1"}, "ASP": {"OD1", "OD2"}, "GLU": {"OE1", "OE2"},
              "HIS": {"ND1", "NE2"}, "SER": {"OG"}, "THR": {"OG1"}, "TYR": {"OH"}}


def atom_type(resname, atom, element):
    if element == "C":
        return "A" if resname in ("PHE", "TYR", "TRP", "HIS") and atom not in ("CA", "CB", "C") else "C"
    if element == "N":
        return "NA" if atom in ACCEPTOR_N.get(resname, ()) else "N"
    if element == "O":
        return "OA"                      # backbone and side-chain O are all acceptors
    if element == "S":
        return "SA" if resname == "MET" else "S"
    return element


# Gasteiger-like partial charges by (residue, atom); a coarse table is enough because
# Vina's scoring function is not electrostatic -- charges only gate the H-bond terms.
CHARGE = {"N": -0.35, "NA": -0.35, "OA": -0.40, "SA": -0.10, "S": -0.10, "C": 0.0, "A": 0.0}


def main(pdb=None, out=None):
    pdb = pathlib.Path(pdb or NS / "bubr1_pseudokinase_766_1050.pdb")
    out = pathlib.Path(out or NS / "bubr1_pseudokinase.pdbqt")
    lines, n = [], 0
    for line in open(pdb):
        if not line.startswith("ATOM"):
            continue
        atom, resname = line[12:16].strip(), line[17:20].strip()
        element = (line[76:78].strip() or atom[0]).upper()
        if element == "H":
            continue
        t = atom_type(resname, atom, element)
        n += 1
        lines.append(f"{line[:54]}  1.00  0.00    {CHARGE.get(t, 0.0):6.3f} {t:<2s}\n")
    out.write_text("".join(lines))
    print(f"{n} atoms -> {out}")

    site = (NS / "millet_site.txt").read_text().splitlines()[0]
    cx, cy, cz = (float(v) for v in site.split(","))
    print(f"box centre {cx:.2f}, {cy:.2f}, {cz:.2f}   size {BOX_SIZE} A cubed")
    (NS / "millet_box.txt").write_text(f"{cx},{cy},{cz},{BOX_SIZE}\n")


if __name__ == "__main__":
    main(*sys.argv[1:])
