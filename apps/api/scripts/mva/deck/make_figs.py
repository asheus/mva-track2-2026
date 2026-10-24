#!/usr/bin/env python3
"""Original figures for the MVA Track 2 deck. All data from our own documents;
sources named in each figure's caption on the slide."""
import sys, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch

OUT = sys.argv[1] if len(sys.argv) > 1 else "img"
plt.rcParams.update({
    "font.family": "Liberation Sans",   # metric-compatible with Arial
    "font.size": 13, "axes.linewidth": 0.9,
    "savefig.facecolor": "white", "figure.facecolor": "white",
})
BLUE, ORANGE, GREEN, NAVY, GREY = "#4F81BD", "#F79646", "#00B050", "#1F497D", "#5C5C5C"
PALE = "#E8EFF7"


# ---------------------------------------------------------------- 1 domains
def domains():
    fig, (ax, bx) = plt.subplots(
        2, 1, figsize=(12.4, 3.6), dpi=200,
        gridspec_kw=dict(height_ratios=[1.6, 1], hspace=0.30))

    doms = [("TPR", 1, 204, BLUE, 13), ("KEN / ABBA", 205, 340, "#7FA6CE", 10),
            ("GLEBS", 341, 477, BLUE, 13), ("", 478, 765, "#C9D6E6", 14),
            ("Pseudokinase", 766, 1050, NAVY, 19)]
    ax.add_patch(Rectangle((1, 0.30), 1049, 0.40, fc="#E9EDF2", ec="none"))
    for name, a, b, c, _ in doms:
        ax.add_patch(Rectangle((a, 0.30), b - a, 0.40, fc=c, ec="none"))
        if name:
            ax.text((a + b) / 2, 0.50, name, ha="center", va="center",
                    color="white", fontsize=12.5, fontweight="bold")
    # KARD, the motif that recruits PP2A-B56
    ax.add_patch(Rectangle((667, 0.26), 14, 0.48, fc=ORANGE, ec="white", lw=1.0))
    ax.annotate("KARD 667-681\nrecruits PP2A-B56", xy=(674, 0.26), xytext=(610, -0.30),
                fontsize=11.5, color=ORANGE, fontweight="bold", ha="center",
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=1.4))

    for pos, lab in ((737, "Allele 1\np.Leu737Ter"), (1002, "Allele 2\np.Asn1002Lys")):
        ax.plot([pos, pos], [0.24, 0.94], color="#C0392B", lw=2.6, zorder=5)
        ax.plot([pos], [0.94], marker="v", ms=11, color="#C0392B", zorder=6)
        ax.text(pos, 1.04, lab, ha="center", va="bottom", fontsize=12,
                fontweight="bold", color="#C0392B")

    ax.set_xlim(-18, 1078); ax.set_ylim(-0.52, 1.72); ax.axis("off")
    for t in (1, 200, 400, 800, 1050):
        ax.text(t, 0.22, str(t), ha="center", va="top", fontsize=9.5, color=GREY)

    xs = [(a + b) / 2 for _, a, b, _, _ in doms]
    ws = [(b - a) * 0.88 for _, a, b, _, _ in doms]
    ns = [n for *_, n in doms]
    bx.bar(xs, ns, width=ws, color=[c for _, _, _, c, _ in doms], edgecolor="white")
    for x, n in zip(xs, ns):
        bx.text(x, n + 0.8, str(n), ha="center", fontsize=11.5, fontweight="bold",
                color=NAVY)
    bx.set_xlim(-18, 1078); bx.set_ylim(0, 27)
    bx.text(-10, 24.5, "pathogenic variants", fontsize=10.5, color=GREY, ha="left")
    bx.tick_params(labelbottom=False, left=False, labelleft=False, bottom=False)
    for sp in ("top", "right", "left"): bx.spines[sp].set_visible(False)
    bx.spines["bottom"].set_color(GREY)
    fig.savefig(f"{OUT}/fig_domains.png", bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)


# --------------------------------------------------------------- 2 exposure
def exposure():
    fig, ax = plt.subplots(figsize=(12.4, 4.25), dpi=200)
    rows = [
        ("Perphenazine\nPP2A activation",      0.0024, 0.0024, 0.024),
        ("Amlexanox\nNMD inhibition",          0.0011, 0.0044, 0.0116),
        ("Ataluren\nreadthrough",              0.006,  0.012,  0.02),
        ("Momelotinib\nAurora B off-target",   0.10,   0.19,   0.35),
        ("Barasertib-hQPA\nAurora B",            12,     24,   1208),
    ]
    ys = np.arange(len(rows))[::-1]
    for y, (lab, lo, mid, hi) in zip(ys, rows):
        win = mid >= 1
        c = GREEN if win else ORANGE
        if hi > lo:
            ax.plot([lo, hi], [y, y], color=c, lw=7, solid_capstyle="round",
                    alpha=0.85, zorder=2)
        ax.plot([mid], [y], "o", ms=13, color=c, zorder=3,
                markeredgecolor="white", markeredgewidth=1.6)
        ax.text((lo if win else mid) * (2.6 if win else 1), y + 0.30,
                f"{lo:,.0f}-{hi:,.0f}x" if win else f"{1/mid:,.0f}x short",
                fontsize=12, fontweight="bold", color=c,
                ha="left" if win else "center", va="bottom")

    ax.axvline(1, color=NAVY, lw=2, ls="--", zorder=1)
    ax.text(1.25, len(rows) - 0.42, "target reached", fontsize=12,
            color=NAVY, fontweight="bold")
    ax.set_xscale("log"); ax.set_xlim(5e-4, 1e4)
    ax.set_yticks(ys); ax.set_yticklabels([r[0] for r in rows], fontsize=12.5)
    ax.set_xlabel("achievable plasma concentration  /  concentration the effect needs\nclosed arms: free. Barasertib bar spans free at 99% bound (12x) to TOTAL (1,208x); its free fraction is unpublished.",
                  fontsize=10.5, color=GREY, labelpad=9)
    ax.set_ylim(-0.75, len(rows) - 0.25)
    for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GREY); ax.tick_params(left=False)
    ax.grid(axis="x", color="#E6E6E6", lw=0.8, zorder=0)
    fig.savefig(f"{OUT}/fig_exposure.png", bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


# ----------------------------------------------------------------- 3 funnel
def funnel():
    W, H = 12.4, 5.4
    fig, ax = plt.subplots(figsize=(W, H), dpi=200)
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

    engines = [("Kosmos",        "3 runs, ~40 hypotheses"),
               ("Paperclip",     "3.4M full texts"),
               ("Gero mining",   "107,407 drug-target pairs"),
               ("Our own atlas", "2,536 alleles scored")]
    bh, gap, y0 = 0.82, 0.20, 0.78
    hub = (4.30, 2.72)
    for i, (name, sub) in enumerate(reversed(engines)):
        y = y0 + i * (bh + gap)
        ax.add_patch(FancyBboxPatch((0.18, y), 2.80, bh,
            boxstyle="round,pad=0,rounding_size=0.08", fc=PALE, ec=BLUE, lw=1.6))
        ax.text(1.58, y + 0.54, name, ha="center", fontsize=13, fontweight="bold",
                color=BLUE)
        ax.text(1.58, y + 0.19, sub, ha="center", fontsize=10, color="#333")
        ax.add_patch(FancyArrowPatch((3.06, y + bh / 2), hub, arrowstyle="-|>",
            mutation_scale=13, color="#A9BFD4", lw=1.4,
            connectionstyle="arc3,rad=0.10"))
    ax.text(1.58, y0 + 4 * bh + 3 * gap + 0.16, "HYPOTHESIS ENGINES", ha="center",
            fontsize=11.5, fontweight="bold", color=GREY)

    ax.add_patch(FancyBboxPatch((4.36, 1.92), 2.52, 1.60,
        boxstyle="round,pad=0,rounding_size=0.08", fc="#FDF3E9", ec=ORANGE, lw=1.8))
    ax.text(5.62, 3.22, "FILTERS", ha="center", fontsize=11.5, fontweight="bold",
            color=ORANGE)
    ax.text(5.62, 2.38, "exposure gate\nReview Room, 7 seats\nconfound control",
            ha="center", va="bottom", fontsize=10.5, color="#333", linespacing=1.5)
    ax.add_patch(FancyArrowPatch((6.96, 2.72), (7.78, 2.72), arrowstyle="-|>",
        mutation_scale=16, color="#A9BFD4", lw=1.8))

    ax.add_patch(FancyBboxPatch((7.88, 2.08), 1.94, 1.28,
        boxstyle="round,pad=0,rounding_size=0.08", fc=NAVY, ec=NAVY))
    ax.text(8.85, 2.88, "Maaz", ha="center", fontsize=15, fontweight="bold",
            color="white")
    ax.text(8.85, 2.34, "decides what\nis worth testing", ha="center", fontsize=10.5,
            color="#D6E2F0", linespacing=1.4)
    ax.add_patch(FancyArrowPatch((9.90, 2.72), (10.72, 2.72), arrowstyle="-|>",
        mutation_scale=16, color="#A9BFD4", lw=1.8))

    ax.add_patch(FancyBboxPatch((10.82, 1.92), 1.42, 1.60,
        boxstyle="round,pad=0,rounding_size=0.08", fc="#ECF7EE", ec=GREEN, lw=1.8))
    ax.text(11.53, 2.82, "1", ha="center", fontsize=30, fontweight="bold", color=GREEN)
    ax.text(11.53, 2.18, "falsifiable\nprediction", ha="center", fontsize=10.5,
            color="#333", linespacing=1.4)

    ax.text(W / 2, 0.20, "~40 hypotheses   \u2192   10 arms survived scrutiny   "
            "\u2192   1 committed prediction", ha="center", fontsize=13.5,
            fontweight="bold", color=NAVY)
    fig.savefig(f"{OUT}/fig_funnel.png", bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)


# ----------------------------------------------------------------- 4 window
def window():
    fig, ax = plt.subplots(figsize=(7.6, 4.3), dpi=200)
    x = np.logspace(-0.5, 3.5, 500)                    # multiples of Aurora B IC50

    congression = 100 * np.exp(-((np.log10(x) - 1.0) ** 2) / (2 * 0.60 ** 2))
    sac_normal  = 100 / (1 + (x / 260.0) ** 2.4)       # Santaguida: tolerates partial
    sac_patient = 100 / (1 + (x / 18.0) ** 1.9)        # synergy in a weakened checkpoint

    ax.axvspan(3, 26, color=GREEN, alpha=0.10, zorder=0)
    ax.plot(x, congression, color=GREEN, lw=3.2, label="congression rescue", zorder=3)
    ax.plot(x, sac_normal, color=ORANGE, lw=2.6, ls="--", zorder=3,
            label="checkpoint, normal cell")
    ax.plot(x, sac_patient, color="#C0392B", lw=2.6, ls=":", zorder=3,
            label="checkpoint, this child")

    for xv, lab, col in ((1208, "adult oncology, TOTAL drug", "#7B241C"),):
        ax.axvline(xv, color=col, lw=1.3, ls="-", alpha=0.55, zorder=1)
        ax.text(xv, 123, lab, rotation=0, fontsize=10, color=col, ha="center")

    ax.text(8.8, 112, "the window", ha="center", fontsize=12, color=GREEN,
            fontweight="bold")
    ax.set_xscale("log"); ax.set_xlim(0.35, 3000); ax.set_ylim(0, 132)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_xlabel("free drug, multiples of the BIOCHEMICAL Aurora B IC50\ncurves are PREDICTED, not measured; cellular potency is not the enzyme IC50", fontsize=10.5, color=GREY)
    ax.set_ylabel("% of normal function", fontsize=12, color=GREY)
    ax.legend(frameon=False, fontsize=10.5, loc="lower left", bbox_to_anchor=(0.005, 0.02))
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    for sp in ("bottom", "left"): ax.spines[sp].set_color(GREY)
    ax.text(0.99, -0.215, "PREDICTED, not measured \u2014 this is the experiment",
            transform=ax.transAxes, ha="right", fontsize=10, color=GREY, style="italic")
    fig.savefig(f"{OUT}/fig_window.png", bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)


for f in (domains, exposure, funnel, window):
    f(); print("ok", f.__name__)
