#!/usr/bin/env python3
"""Lollipop map of literature BUB1B variants, and the cell-cycle dosage waveform."""
import sys, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle

OUT = sys.argv[1] if len(sys.argv) > 1 else "img"
plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 13,
                     "savefig.facecolor": "white", "figure.facecolor": "white"})
BLUE, ORANGE, GREEN, NAVY, GREY = "#4F81BD", "#F79646", "#00B050", "#1F497D", "#5C5C5C"
RED, PALE = "#C0392B", "#E8EFF7"

DOMS = [("TPR", 1, 204, BLUE), ("KEN / ABBA", 205, 340, "#7FA6CE"),
        ("GLEBS", 341, 477, BLUE), ("", 478, 765, "#C9D6E6"),
        ("Pseudokinase", 766, 1050, NAVY)]

# Patient-derived variants recovered from the atlas and the literature.
# (position, label, kind)  kind: m = missense, t = truncating
VARIANTS = [(147, "I147T", "m"), (155, "Y155C", "m"), (175, "F175L", "m"),
            (349, "R349Q", "m"), (386, "Q386X", "t"), (416, "R416Q", "m"),
            (550, "R550Q", "m"), (727, "R727C", "m"), (753, "L753X", "t"),
            (814, "R814H", "m"), (844, "L844F", "m"), (893, "R893S", "m"),
            (909, "I909T", "m"), (921, "Q921H", "m"), (941, "I941T", "m"),
            (1004, "N1004S", "m"), (1012, "L1012P", "m")]
PROBAND = [(737, "p.Leu737Ter", "t"), (1002, "p.Asn1002Lys", "m")]


def lollipop():
    fig, ax = plt.subplots(figsize=(12.4, 4.0), dpi=200)
    ax.set_xlim(-25, 1085); ax.set_ylim(-1.35, 2.35); ax.axis("off")

    ax.add_patch(Rectangle((1, -0.22), 1049, 0.44, fc="#E9EDF2", ec="none"))
    for name, a, b, c in DOMS:
        ax.add_patch(Rectangle((a, -0.22), b - a, 0.44, fc=c, ec="none"))
        if name:
            ax.text((a + b) / 2, 0.0, name, ha="center", va="center", color="white",
                    fontsize=11.5, fontweight="bold")
    ax.add_patch(Rectangle((667, -0.27), 14, 0.54, fc=ORANGE, ec="white", lw=0.9))
    ax.text(674, -0.46, "KARD", ha="center", va="top", fontsize=10,
            color=ORANGE, fontweight="bold")
    for t in (1, 200, 400, 600, 800, 1050):
        ax.text(t, -0.30, str(t), ha="center", va="top", fontsize=9, color=GREY)

    # literature variants above the bar, alternating stem heights to avoid collision
    for i, (pos, lab, kind) in enumerate(VARIANTS):
        hgt = 0.95 + 0.42 * (i % 3)
        col = BLUE if kind == "m" else "#8899AA"
        ax.plot([pos, pos], [0.24, hgt], color=col, lw=1.2, zorder=2)
        ax.plot([pos], [hgt], "o", ms=8.5, color=col, mec="white", mew=1.4, zorder=4)
        ax.text(pos, hgt + 0.11, lab, ha="center", va="bottom", fontsize=9,
                color=col)

    # the proband's two alleles below the bar, in red
    for pos, lab, kind in PROBAND:
        ax.plot([pos, pos], [-0.24, -0.86], color=RED, lw=2.4, zorder=5)
        ax.plot([pos], [-0.86], "o", ms=12, color=RED, mec="white", mew=1.6, zorder=6)
        ax.text(pos, -1.02, lab, ha="center", va="top", fontsize=11,
                fontweight="bold", color=RED)

    ax.text(-20, 2.12, "17 patient variants recovered from the literature",
            fontsize=11.5, color=BLUE, fontweight="bold", ha="left")
    ax.text(-20, -1.26, "this child", fontsize=11.5, color=RED,
            fontweight="bold", ha="left")
    ax.plot([930, 960], [2.12, 2.12], color="#8899AA", lw=1.3)
    ax.text(968, 2.12, "truncating", fontsize=10, color=GREY, va="center")
    fig.savefig(f"{OUT}/fig_lollipop.png", bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


def cellcycle():
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(12.4, 3.5), dpi=200,
                                 gridspec_kw=dict(width_ratios=[1.15, 1], wspace=0.26))

    # left: the waveform
    phases = ["G1", "S", "G2 / M"]
    tpm = [22.06, 32.66, 47.91]
    cols = ["#C9D6E6", "#7FA6CE", NAVY]
    ax.bar(phases, tpm, color=cols, width=0.62, edgecolor="white")
    for i, v in enumerate(tpm):
        ax.text(i, v + 1.4, f"{v}", ha="center", fontsize=13, fontweight="bold",
                color=NAVY)
    ax.annotate("", xy=(2, 55.0), xytext=(0, 55.0),
                arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=2))
    ax.text(1, 56.6, "2.2x across the cycle", ha="center", fontsize=12,
            color=ORANGE, fontweight="bold")
    ax.set_ylim(0, 64); ax.set_ylabel("BUB1B median TPM", fontsize=11.5, color=GREY)
    ax.tick_params(labelsize=12, left=False)
    for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GREY)
    ax.set_title("BubR1 is made when it is needed", fontsize=13, color=NAVY,
                 fontweight="bold", pad=12)

    # right: why that matters
    bx.set_xlim(0, 10); bx.set_ylim(0, 10); bx.axis("off")
    bx.text(0.2, 9.3, "Why this number governs everything",
            fontsize=13, color=NAVY, fontweight="bold")
    rows = [("Bulk assays cannot separate", "pharmacology from cycling fraction", ORANGE),
            ("A drug that slows the cycle", "lowers BUB1B and looks like a hit", ORANGE),
            ("So every readout is phase-matched", "or it is not evidence", GREEN)]
    y = 7.3
    for a, b, c in rows:
        bx.add_patch(FancyBboxPatch((0.2, y - 1.5), 9.6, 1.72,
            boxstyle="round,pad=0,rounding_size=0.18",
            fc="#FDF3E9" if c == ORANGE else "#ECF7EE", ec=c, lw=1.5))
        bx.text(0.55, y - 0.28, a, fontsize=11.5, fontweight="bold", color="#222")
        bx.text(0.55, y - 1.02, b, fontsize=11.5, color="#444")
        y -= 2.05
    fig.savefig(f"{OUT}/fig_cellcycle.png", bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


for f in (lollipop, cellcycle):
    f(); print("ok", f.__name__)
