#!/usr/bin/env python3
"""Render the two structures from coordinates, so every chain is labelled.

5JJA  chain A = PP2A-B56gamma (333 res) ; chain C = BubR1 KARD peptide (8 res resolved)
4AF3  chain A = Aurora B kinase (253 res) ; chain D = INCENP (43 res) ; VX6 = inhibitor
"""
import sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PDBDIR = sys.argv[1]
OUT = sys.argv[2]
plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 13,
                     "savefig.facecolor": "white", "figure.facecolor": "white"})
NAVY, ORANGE, GREY, RED, BLUE = "#1F497D", "#F79646", "#5C5C5C", "#C0392B", "#4F81BD"


def load(pid):
    ca, lig = {}, []
    for L in open(f"{PDBDIR}/{pid}.pdb"):
        if L.startswith("ATOM") and L[12:16].strip() == "CA":
            ch = L[21]
            ca.setdefault(ch, []).append([float(L[30:38]), float(L[38:46]),
                                          float(L[46:54])])
        elif L.startswith("HETATM") and L[17:20].strip() == "VX6":
            lig.append([float(L[30:38]), float(L[38:46]), float(L[46:54])])
    return {k: np.array(v) for k, v in ca.items()}, np.array(lig) if lig else None


def project(points_list, roll=0.0):
    """PCA onto the two widest axes, shared across all point sets."""
    allp = np.vstack(points_list)
    c = allp.mean(0)
    u, s, vt = np.linalg.svd(allp - c, full_matrices=False)
    basis = vt[:2]
    th = np.deg2rad(roll)
    R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    return lambda p: ((p - c) @ basis.T) @ R.T


def panel(ax, pid, keep, colors, labels, widths, ligand_label=None, roll=0.0):
    ca, lig = load(pid)
    sets = [ca[k] for k in keep] + ([lig] if lig is not None else [])
    pr = project(sets, roll)
    for k, col, lw in zip(keep, colors, widths):
        xy = pr(ca[k])
        ax.plot(xy[:, 0], xy[:, 1], color=col, lw=lw, solid_capstyle="round",
                solid_joinstyle="round", zorder=3 if lw > 2.2 else 2, alpha=0.95)
    if lig is not None:
        xy = pr(lig)
        ax.scatter(xy[:, 0], xy[:, 1], s=120, c=RED, edgecolors="white",
                   linewidths=0.7, zorder=6)
        cx, cy = xy.mean(0)
        ax.annotate(ligand_label, xy=(cx, cy), xytext=(cx + 26, cy - 20),
                    fontsize=12, color=RED, fontweight="bold", ha="left",
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8,
                                    mutation_scale=14))
    ax.set_aspect("equal"); ax.axis("off")
    return pr, ca


fig, (axl, axr) = plt.subplots(1, 2, figsize=(12.4, 4.6), dpi=200,
                               gridspec_kw=dict(wspace=0.04))

# ---- left: the interaction that fails
pr, ca = panel(axl, "5jja", ["A", "C"], ["#AEB9C4", ORANGE],
               None, [1.6, 6.0], roll=0)
xy = pr(ca["C"])
cx, cy = xy.mean(0)
axl.annotate("BubR1 KARD\n8 residues resolved", xy=(cx, cy),
             xytext=(cx - 20, cy - 46), fontsize=12.5, color=ORANGE,
             fontweight="bold", ha="center",
             arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2.0,
                             mutation_scale=15))
xa = pr(ca["A"])
axl.text(xa[:, 0].mean() + 6, xa[:, 1].min() - 8, "PP2A-B56γ", fontsize=12.5,
         color=GREY, fontweight="bold", ha="center")


# ---- right: where the drug acts
pr2, ca2 = panel(axr, "4af3", ["A", "D"], ["#AEB9C4", BLUE],
                 None, [1.6, 2.8], ligand_label="inhibitor in\nthe ATP pocket", roll=0)
xa2 = pr2(ca2["A"]); xd2 = pr2(ca2["D"])
axr.text(xa2[:, 0].mean(), xa2[:, 1].max() + 7, "Aurora B kinase", fontsize=12.5,
         color=GREY, fontweight="bold", ha="center")
axr.text(xd2[:, 0].mean(), xd2[:, 1].min() - 11, "INCENP", fontsize=12.5,
         color=BLUE, fontweight="bold", ha="center")


fig.text(0.27, 0.985, "The interaction that FAILS", ha="center", va="top",
         fontsize=15, color=RED, fontweight="bold")
fig.text(0.75, 0.985, "Where the DRUG acts", ha="center", va="top",
         fontsize=15, color="#00802E", fontweight="bold")
fig.subplots_adjust(top=0.90)
fig.savefig(f"{OUT}/fig_structures.png", bbox_inches="tight", pad_inches=0.10)
plt.close(fig)
print("ok fig_structures")
