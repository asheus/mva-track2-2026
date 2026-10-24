#!/usr/bin/env python3
"""Moonshot: a trans-acting circular RNA that raises output from a gene's own mRNA."""
import sys, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
OUT = sys.argv[1] if len(sys.argv) > 1 else "img"
plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 13,
                     "savefig.facecolor": "white", "figure.facecolor": "white"})
BLUE, ORANGE, GREEN, NAVY, GREY = "#4F81BD", "#F79646", "#00B050", "#1F497D", "#5C5C5C"
RED = "#C0392B"
fig, ax = plt.subplots(figsize=(12.5, 4.15), dpi=200)
ax.set_xlim(0, 12.5); ax.set_ylim(0, 4.15); ax.axis("off")

for x0, title, col in ((0.10, "TODAY  — gene therapy", GREY),
                       (4.28, "THE MOONSHOT  — trans-acting RNA", GREEN),
                       (8.46, "WHY IT GENERALISES", BLUE)):
    ax.add_patch(FancyBboxPatch((x0, 0.30), 3.94, 3.45,
        boxstyle="round,pad=0,rounding_size=0.10",
        fc="#FBFBFA" if col == GREY else ("#ECF7EE" if col == GREEN else "#EDF2F8"),
        ec=col, lw=2.0))
    ax.text(x0 + 1.97, 3.46, title, ha="center", fontsize=12.5, fontweight="bold", color=col)

# panel 1: replace the gene
ax.add_patch(Rectangle((0.55, 2.35), 2.00, 0.30, fc="#C9D6E6", ec="none"))
ax.text(1.55, 2.78, "deliver a whole new gene", ha="center", fontsize=10.5, color=GREY)
ax.text(1.55, 2.05, "one disease, one payload", ha="center", fontsize=10.5, color=GREY)
ax.text(2.07, 1.50, "size limits, immunogenicity,\nper-disease development",
        ha="center", va="center", fontsize=10.5, color=RED, linespacing=1.4)

# panel 2: circRNA acting on the native message
ax.add_patch(Rectangle((4.70, 2.35), 2.55, 0.26, fc="#9FB6CE", ec="none"))
ax.text(5.97, 2.72, "the patient's OWN mRNA", ha="center", fontsize=10.5, color=NAVY)
ax.plot([6.30, 6.30], [2.33, 2.33], marker="x", ms=11, mew=3, color=RED)
ax.text(6.30, 2.08, "stop", ha="center", fontsize=9.5, color=RED, fontweight="bold")
c = Circle((5.30, 1.42), 0.36, fc="none", ec=GREEN, lw=3.4)
ax.add_patch(c)
ax.text(5.30, 0.88, "circRNA", ha="center", fontsize=10.5, color=GREEN, fontweight="bold")
ax.add_patch(FancyArrowPatch((5.66, 1.55), (6.22, 2.22), arrowstyle="-|>",
                             mutation_scale=14, color=GREEN, lw=2.2))
ax.text(7.05, 1.52, "raises output\nfrom the message\nthat is already there",
        ha="center", va="center", fontsize=10.5, color=GREEN, linespacing=1.4)

# panel 3
for i, (t, col) in enumerate((("one mechanism, many genes", BLUE),
                              ("no genome edit", BLUE),
                              ("dosage diseases are a class", BLUE),
                              ("delivery is the unsolved half", ORANGE))):
    ax.add_patch(FancyBboxPatch((8.72, 2.72 - i * 0.62), 3.42, 0.50,
        boxstyle="round,pad=0,rounding_size=0.06",
        fc="white" if col == BLUE else "#FDF3E9", ec=col, lw=1.4))
    ax.text(10.43, 2.97 - i * 0.62, t, ha="center", va="center", fontsize=10.5,
            color="#222" if col == BLUE else ORANGE,
            fontweight="normal" if col == BLUE else "bold")
fig.savefig(f"{OUT}/fig_trna.png", bbox_inches="tight", pad_inches=0.06)
print("ok fig_trna")
