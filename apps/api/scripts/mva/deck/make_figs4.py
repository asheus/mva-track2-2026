#!/usr/bin/env python3
"""Two figures adapted from CC BY 4.0 reviews, redrawn rather than copied.

  fig_attach.png   adapted from McVey, Cosby & Nannas, Int J Mol Sci 2021,
                   PMID 34445523, CC BY 4.0
  fig_domains2.png adapted from Bloom & North, Cell Biosci 2021,
                   PMID 33892776, CC BY 4.0
Both redrawn in our own palette; variant sets merged with our atlas.
"""
import sys, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Ellipse, FancyArrowPatch

OUT = sys.argv[1] if len(sys.argv) > 1 else "img"
plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 13,
                     "savefig.facecolor": "white", "figure.facecolor": "white"})
BLUE, ORANGE, GREEN, NAVY, GREY = "#4F81BD", "#F79646", "#00B050", "#1F497D", "#5C5C5C"
RED, MAG = "#C0392B", "#B5379B"


def chromo(ax, cx, cy, poles, kt_left, kt_right, sc=1.0):
    """One chromosome: two sister chromatids, cohesin, two kinetochores.
    poles: list of x for spindle poles. kt_left/right: list of pole indices
    that attach to that kinetochore."""
    w, h = 0.17 * sc, 0.62 * sc
    for dx in (-w * 1.15, w * 1.15):
        ax.add_patch(FancyBboxPatch((cx + dx - w / 2, cy - h / 2), w, h,
            boxstyle="round,pad=0,rounding_size=0.07", fc="#9FB6CE", ec="none"))
    ax.add_patch(Rectangle((cx - w * 1.9, cy - 0.055 * sc), w * 3.8, 0.11 * sc,
                           fc=ORANGE, ec="none"))
    for dx, atts in ((-w * 1.15, kt_left), (w * 1.15, kt_right)):
        kx = cx + dx
        ax.add_patch(Circle((kx, cy), 0.072 * sc, fc="#F2C230", ec="white", lw=1.2,
                            zorder=4))
        for pi in atts:
            ax.plot([poles[pi], kx], [cy, cy], color="#3A3A3A", lw=1.5, zorder=2)


def attach():
    fig, ax = plt.subplots(figsize=(12.4, 3.9), dpi=200)
    ax.set_xlim(0, 12.4); ax.set_ylim(0, 3.9); ax.axis("off")

    cases = [("Amphitelic", "correct", [0], [1], GREEN),
             ("Syntelic", "both to one pole", [0], [0], RED),
             ("Monotelic", "one unattached", [], [1], RED),
             ("Merotelic", "one kinetochore, both poles", [0], [0, 1], RED)]
    bw = 2.98
    x = 0.14
    for name, sub, kl, kr, col in cases:
        ax.add_patch(FancyBboxPatch((x, 0.42), bw, 3.10,
            boxstyle="round,pad=0,rounding_size=0.10",
            fc="#F7FBF8" if col == GREEN else "#FDF6F5", ec=col, lw=1.8))
        cx = x + bw / 2
        poles = [x + 0.34, x + bw - 0.34]
        for px in poles:
            ax.add_patch(Circle((px, 2.05), 0.085, fc="#3A3A3A", ec="none", zorder=5))
        # merotelic: second line from the other pole to the same kinetochore
        chromo(ax, cx, 2.05, poles, kl, kr, sc=1.35)
        if name == "Merotelic":
            ax.plot([poles[1], cx + 0.265], [2.05, 2.20], color="#3A3A3A", lw=1.5)
        ax.text(cx, 3.18, name, ha="center", fontsize=13.5, fontweight="bold",
                color=col)
        ax.text(cx, 2.90, sub, ha="center", fontsize=10.5, color=GREY, style="italic")
        ax.text(cx, 0.62, "✓ segregates correctly" if col == GREEN
                else "corrected by Aurora B", ha="center", fontsize=11,
                color=col, fontweight="bold")
        x += bw + 0.08
    fig.savefig(f"{OUT}/fig_attach.png", bbox_inches="tight", pad_inches=0.07)
    plt.close(fig)


def domains2():
    fig, ax = plt.subplots(figsize=(12.4, 3.75), dpi=200)
    ax.set_xlim(-30, 1090); ax.set_ylim(-1.55, 1.85); ax.axis("off")

    ax.add_patch(Rectangle((1, -0.20), 1049, 0.40, fc="#E4E8ED", ec="none"))
    doms = [("KEN1", 26, 34, RED), ("TPR", 62, 226, BLUE), ("D1", 235, 272, "#E8C23A"),
            ("ABBA", 276, 290, ORANGE), ("KEN2", 300, 308, RED),
            ("ABBA", 338, 352, ORANGE), ("GLEBS", 410, 445, "#8E6BBF"),
            ("ABBA", 518, 532, ORANGE), ("D2", 560, 620, "#E8C23A"),
            ("KARD", 667, 681, GREEN), ("Pseudokinase", 766, 1050, NAVY)]
    for name, a, b, c in doms:
        ax.add_patch(Rectangle((a, -0.20), b - a, 0.40, fc=c, ec="white", lw=0.8))
        if b - a > 90:
            ax.text((a + b) / 2, 0.0, name, ha="center", va="center", color="white",
                    fontsize=11.5, fontweight="bold")
        else:
            lvl = {"KEN1": 0.26, "D1": 0.26, "ABBA": 0.44, "KEN2": 0.62,
                   "GLEBS": 0.26, "D2": 0.26, "KARD": 0.26}.get(name, 0.26)
            if name == "ABBA" and a > 500: lvl = 0.26
            ax.text((a + b) / 2, lvl, name, ha="center", va="bottom", fontsize=8.5,
                    color=c, fontweight="bold")
    for t in (1, 200, 400, 600, 800, 1050):
        ax.text(t, -0.28, str(t), ha="center", va="top", fontsize=9, color=GREY)

    # function callouts, as the source figure does
    ax.annotate("binds kinetochores\nand the APC/C", xy=(144, -0.22), xytext=(144, -0.92),
                ha="center", fontsize=10, color=BLUE,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=1.1))
    ax.annotate("error correction,\ncongression", xy=(674, -0.22), xytext=(640, -1.18),
                ha="center", fontsize=10, color=GREEN, fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=GREEN, lw=1.4))
    ax.annotate("protein stability", xy=(908, -0.22), xytext=(908, -0.92),
                ha="center", fontsize=10, color=NAVY, fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=NAVY, lw=1.1))

    mva = [(40, "M40T"), (155, "Y155C"), (166, "E166D"), (349, "R349Q"),
           (363, "Q363R"), (390, "E390D"), (618, "V618A"), (727, "R727"),
           (909, "I909T"), (921, "Q921H")]
    can = [(550, "R550Q"), (814, "R814H"), (844, "L844F"), (1012, "L1012P")]
    for i, (pos, lab) in enumerate(mva):
        h = 0.52 + 0.30 * (i % 3)
        ax.plot([pos, pos], [0.20, h], color=MAG, lw=1.1, zorder=2)
        ax.plot([pos], [h], "o", ms=7, color=MAG, mec="white", mew=1.1, zorder=3)
        ax.text(pos, h + 0.08, lab, ha="center", va="bottom", fontsize=8.5, color=MAG)
    for i, (pos, lab) in enumerate(can):
        h = 1.46 if i % 2 == 0 else 1.22
        ax.plot([pos, pos], [0.20, h], color="#B07A2A", lw=1.0, ls=":", zorder=2)
        ax.plot([pos], [h], "s", ms=6, color="#B07A2A", mec="white", mew=1.0, zorder=3)
        ax.text(pos, h + 0.07, lab, ha="center", va="bottom", fontsize=8.5,
                color="#B07A2A")

    for pos, lab in ((737, "p.Leu737Ter"), (1002, "p.Asn1002Lys")):
        ax.plot([pos, pos], [-0.22, -1.34], color=RED, lw=2.4, zorder=5)
        ax.plot([pos], [-1.34], "o", ms=12, color=RED, mec="white", mew=1.5, zorder=6)
        ax.text(pos, -1.47, lab, ha="center", va="top", fontsize=10.5,
                fontweight="bold", color=RED)

    ax.text(-25, 1.74, "MVA variants", fontsize=10.5, color=MAG, fontweight="bold")
    ax.text(150, 1.74, "cancer variants", fontsize=10.5, color="#B07A2A",
            fontweight="bold")
    ax.text(330, 1.74, "this child", fontsize=10.5, color=RED, fontweight="bold")
    fig.savefig(f"{OUT}/fig_domains2.png", bbox_inches="tight", pad_inches=0.07)
    plt.close(fig)


for f in (attach, domains2):
    f(); print("ok", f.__name__)
