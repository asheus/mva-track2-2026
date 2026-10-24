#!/usr/bin/env python3
"""The allele-scoring pipeline and the expected-output ladder it produces."""
import sys, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

OUT = sys.argv[1] if len(sys.argv) > 1 else "img"
plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 13,
                     "savefig.facecolor": "white", "figure.facecolor": "white"})
BLUE, ORANGE, GREEN, NAVY, GREY = "#4F81BD", "#F79646", "#00B050", "#1F497D", "#5C5C5C"
RED = "#C0392B"

fig, ax = plt.subplots(figsize=(12.6, 4.75), dpi=200)
ax.set_xlim(0, 12.6); ax.set_ylim(0, 4.75); ax.axis("off")

# ---------------- left: the pipeline
steps = [("2,536 alleles", "atlas + 854 full texts", BLUE),
         ("consequence call", "truncating / missense / splice", BLUE),
         ("NMD rule, 55 nt", "does the transcript survive", ORANGE),
         ("AlphaMissense + GPN-Star", "two predictors, one adds splice", BLUE),
         ("literature abundance", "no predictor has this axis", GREEN)]
y = 4.08
for i, (a, b, c) in enumerate(steps):
    ax.add_patch(FancyBboxPatch((0.10, y - 0.62), 4.42, 0.66,
        boxstyle="round,pad=0,rounding_size=0.07",
        fc="#ECF7EE" if c == GREEN else ("#FDF3E9" if c == ORANGE else "#EDF2F8"),
        ec=c, lw=1.6))
    ax.text(0.30, y - 0.16, a, fontsize=12.5, fontweight="bold", color=c)
    ax.text(0.30, y - 0.48, b, fontsize=10.5, color="#555")
    if i < len(steps) - 1:
        ax.add_patch(FancyArrowPatch((2.31, y - 0.64), (2.31, y - 0.78),
            arrowstyle="-|>", mutation_scale=12, color="#9AA6B2", lw=1.6))
    y -= 0.80
ax.text(0.10, 4.42, "Every allele, scored the same way", fontsize=13,
        fontweight="bold", color=NAVY)

ax.add_patch(FancyArrowPatch((4.62, 2.15), (5.28, 2.15), arrowstyle="-|>",
                             mutation_scale=18, color=NAVY, lw=2.6))

# ---------------- right: the expected-output ladder
X0, X1 = 5.55, 12.35
ax.text(X0, 4.42, "Expected BubR1 output, by allele class", fontsize=13,
        fontweight="bold", color=NAVY)
bands = [("none", 0.0, 0.17, "#F3D4D0"), ("trace", 0.17, 0.38, "#F7E2CE"),
         ("partial", 0.38, 0.72, "#E7EEF6"), ("near-full", 0.72, 1.0, "#DCEFE0")]
BY, BH = 0.52, 2.95
for lab, a, b, col in bands:
    ax.add_patch(Rectangle((X0 + (X1 - X0) * a, BY), (X1 - X0) * (b - a), BH,
                           fc=col, ec="white", lw=1.2))
    ax.text(X0 + (X1 - X0) * (a + b) / 2, BY + BH + 0.09, lab, ha="center",
            fontsize=10.5, color=GREY)

rows = [(0.08, "PTC > 55 nt upstream of last junction", "transcript degraded", RED),
        (0.27, "PTC in the last exon", "escapes NMD, protein truncated", ORANGE),
        (0.50, "buried missense, destabilising", "made, then degraded", BLUE),
        (0.86, "surface missense, non-interface", "made and kept", GREEN)]
yy = BY + BH - 0.42
for frac, lab, note, col in rows:
    cx = X0 + (X1 - X0) * frac
    ax.plot([cx], [yy], "o", ms=12, color=col, mec="white", mew=1.6, zorder=5)
    ha = "left" if frac < 0.6 else "right"
    tx = cx + 0.20 if frac < 0.6 else cx - 0.20
    ax.text(tx, yy + 0.07, lab, fontsize=10.5, fontweight="bold", color=col, ha=ha)
    ax.text(tx, yy - 0.21, note, fontsize=10, color="#555", ha=ha)
    yy -= 0.74

# the proband's two alleles, pinned onto the same ladder
for frac, lab in ((0.08, "p.Leu737Ter\n747 nt upstream"), (0.50, "p.Asn1002Lys\n87% buried")):
    cx = X0 + (X1 - X0) * frac
    ax.plot([cx, cx], [BY, BY - 0.30], color=RED, lw=2.4, zorder=6)
    ax.text(cx, BY - 0.38, lab, ha="center", va="top", fontsize=10.5,
            fontweight="bold", color=RED, linespacing=1.3)

fig.savefig(f"{OUT}/fig_scoring.png", bbox_inches="tight", pad_inches=0.07)
plt.close(fig)
print("ok fig_scoring")
