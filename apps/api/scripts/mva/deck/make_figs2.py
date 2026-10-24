#!/usr/bin/env python3
"""Three more figures: the mechanism, the themed search space, the evidence base."""
import sys, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch, Ellipse

OUT = sys.argv[1] if len(sys.argv) > 1 else "img"
plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 13,
                     "savefig.facecolor": "white", "figure.facecolor": "white"})
BLUE, ORANGE, GREEN, NAVY, GREY = "#4F81BD", "#F79646", "#00B050", "#1F497D", "#5C5C5C"
RED, PALE = "#C0392B", "#E8EFF7"


# ------------------------------------------------- 1 the mechanism, visually
def mechanism():
    fig, ax = plt.subplots(figsize=(12.4, 4.9), dpi=200)
    ax.set_xlim(0, 12.4); ax.set_ylim(0, 4.9); ax.axis("off")

    for panel, x0, title in ((0, 0.15, "NORMAL"), (1, 6.45, "THIS CHILD")):
        ax.add_patch(FancyBboxPatch((x0, 0.30), 5.80, 4.05,
            boxstyle="round,pad=0,rounding_size=0.10", fc="#FCFCFA",
            ec=BLUE if panel == 0 else RED, lw=2.0))
        ax.text(x0 + 2.90, 4.02, title, ha="center", fontsize=13.5,
                fontweight="bold", color=BLUE if panel == 0 else RED)

        # chromosome arm + centromere
        ax.add_patch(FancyBboxPatch((x0 + 0.30, 1.05), 0.52, 2.35,
            boxstyle="round,pad=0,rounding_size=0.18", fc="#C9D6E6", ec="none"))
        ax.add_patch(Ellipse((x0 + 0.56, 2.22), 0.56, 0.62, fc="#9FB6CE", ec="none"))
        ax.text(x0 + 0.56, 0.72, "chromosome", ha="center", fontsize=10, color=GREY)

        # kinetochore plate
        ax.add_patch(Rectangle((x0 + 0.92, 1.80), 0.30, 0.85, fc=NAVY, ec="none"))
        ax.text(x0 + 1.07, 1.52, "kinetochore", ha="center", fontsize=10, color=GREY)

        # microtubule
        ok = panel == 0
        ax.plot([x0 + 1.22, x0 + 2.55], [2.22, 2.22], color="#6B7A8C",
                lw=7 if ok else 3, solid_capstyle="round",
                ls="-" if ok else (0, (3, 3)))
        ax.text(x0 + 1.95, 2.52 if ok else 2.50, "microtubule" if ok else "unstable",
                ha="center", fontsize=10, color=GREY if ok else RED,
                fontweight="normal" if ok else "bold")

        # Aurora B
        ax.add_patch(Circle((x0 + 1.07, 3.25), 0.33, fc=ORANGE, ec="none"))
        ax.text(x0 + 1.07, 3.25, "Aur\nB", ha="center", va="center", fontsize=9.5,
                color="white", fontweight="bold", linespacing=1.0)
        ax.add_patch(FancyArrowPatch((x0 + 1.07, 2.90), (x0 + 1.07, 2.70),
            arrowstyle="-|>", mutation_scale=13, color=ORANGE, lw=2.2))
        ax.text(x0 + 1.46, 2.80, "P", ha="center", fontsize=11, color=ORANGE,
                fontweight="bold")

        # BubR1 + PP2A-B56
        bx = x0 + 3.05
        ax.add_patch(FancyBboxPatch((bx, 1.92), 1.05, 0.62,
            boxstyle="round,pad=0,rounding_size=0.08",
            fc=BLUE if ok else "#E3E7EB", ec="none"))
        ax.text(bx + 0.52, 2.23, "BubR1", ha="center", va="center", fontsize=11,
                color="white" if ok else "#9AA3AB", fontweight="bold")
        ax.add_patch(FancyBboxPatch((bx + 1.30, 1.92), 1.28, 0.62,
            boxstyle="round,pad=0,rounding_size=0.08",
            fc=GREEN if ok else "#E3E7EB", ec="none"))
        ax.text(bx + 1.94, 2.23, "PP2A-B56", ha="center", va="center", fontsize=11,
                color="white" if ok else "#9AA3AB", fontweight="bold")

        if ok:
            ax.add_patch(FancyArrowPatch((bx + 1.28, 2.23), (bx + 1.32, 2.23),
                arrowstyle="-", color=GREEN, lw=2.0))
            ax.add_patch(FancyArrowPatch((bx - 0.02, 2.23), (x0 + 1.28, 2.23),
                arrowstyle="-|>", mutation_scale=14, color=GREEN, lw=2.4))
            ax.text(x0 + 2.25, 1.96, "removes P", ha="center", fontsize=10,
                    color=GREEN, fontweight="bold")
            ax.text(x0 + 2.90, 0.60, "kinase and phosphatase in balance",
                    ha="center", fontsize=11.5, color=BLUE, fontweight="bold")
        else:
            ax.plot([bx - 0.55, bx - 0.05], [2.48, 1.98], color=RED, lw=3.4)
            ax.plot([bx - 0.55, bx - 0.05], [1.98, 2.48], color=RED, lw=3.4)
            ax.text(bx + 0.52, 1.56, "never arrives", ha="center", fontsize=10,
                    color=RED, fontweight="bold")
            ax.text(x0 + 2.90, 0.60, "Aurora B unopposed, attachments fail",
                    ha="center", fontsize=11.5, color=RED, fontweight="bold")
            for i, (lab, yy) in enumerate((("allele 1 deletes the domain", 3.42),
                                           ("allele 2 breaks its signal", 3.08))):
                ax.text(bx + 1.94, yy, lab, ha="center", fontsize=10, color=RED)
            ax.add_patch(FancyArrowPatch((bx + 1.94, 3.00), (bx + 0.70, 2.60),
                arrowstyle="-|>", mutation_scale=11, color=RED, lw=1.3))
    fig.savefig(f"{OUT}/fig_mechanism.png", bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)


# ------------------------------------------------------ 2 the search, themed
def themes():
    """2x2 block so it sits beside the exposure chart without being crushed."""
    fig, ax = plt.subplots(figsize=(6.5, 5.3), dpi=200)
    ax.set_xlim(0, 6.5); ax.set_ylim(0, 5.3); ax.axis("off")
    cols = [
        ("Rescue allele 1", "the truncated one", [
            ("Translational readthrough", 0), ("NMD inhibition", 0),
            ("Gene / ASO / trans-splicing", 0)]),
        ("Rescue allele 2", "the missense one", [
            ("Chaperone, HSP90", 0), ("Degradation, SIRT2 / NAD+", 0),
            ("Proteasome inhibition", 0)]),
        ("Target BubR1 itself", "make it, or bind it", [
            ("Direct small-molecule binding", 0)]),
        ("Rebalance downstream", "where both alleles meet", [
            ("Activate PP2A directly", 0), ("Restrain APC/C", 0),
            ("Lower Aurora B", 1)]),
    ]
    W, H = 3.14, 2.52
    for i, (head, sub, items) in enumerate(cols):
        x = 0.08 + (i % 2) * (W + 0.14)
        y = 2.68 - (i // 2) * (H + 0.12)
        live = any(st for _, st in items)
        ax.add_patch(FancyBboxPatch((x, y), W, H,
            boxstyle="round,pad=0,rounding_size=0.08",
            fc="#F7FBF8" if live else "#FBFBFA",
            ec=GREEN if live else "#D8DCE0", lw=2.0 if live else 1.3))
        ax.text(x + W / 2, y + H - 0.26, head, ha="center", fontsize=12,
                fontweight="bold", color=GREEN if live else NAVY)
        ax.text(x + W / 2, y + H - 0.50, sub, ha="center", fontsize=9.5,
                color=GREY, style="italic")
        yy = y + H - 0.74
        for name, st in items:
            ax.add_patch(FancyBboxPatch((x + 0.12, yy - 0.42), W - 0.24, 0.40,
                boxstyle="round,pad=0,rounding_size=0.05",
                fc="#ECF7EE" if st else "white",
                ec=GREEN if st else "#DCE0E4", lw=1.4 if st else 1.0))
            ax.text(x + W / 2, yy - 0.22, name, ha="center", va="center",
                    fontsize=9.5, color="#222" if st else "#6E767D",
                    fontweight="bold" if st else "normal")
            if not st:
                ax.plot([x + 0.24, x + W - 0.24], [yy - 0.22, yy - 0.22],
                        color="#C3C9CF", lw=1.2)
            yy -= 0.50
        ax.text(x + W / 2, y + 0.18, "SURVIVES" if live else "closed on exposure",
                ha="center", fontsize=10.5 if live else 9.5,
                fontweight="bold" if live else "normal",
                color=GREEN if live else GREY)
    fig.savefig(f"{OUT}/fig_themes.png", bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


# ------------------------------------------------------ 3 the evidence base
def evidence():
    fig, ax = plt.subplots(figsize=(12.4, 1.75), dpi=200)
    ax.set_xlim(0, 12.4); ax.set_ylim(0, 1.75); ax.axis("off")
    items = [("54", "primary papers\nread, not cited", BLUE),
             ("5", "drug-target\ndatabases", BLUE),
             ("4", "experimental\nstructures", BLUE),
             ("2,536", "alleles scored\nin our atlas", BLUE),
             ("51", "numbered corrections\nto our own work", ORANGE),
             ("0", "claims resting on\na single paper", GREEN)]
    w = 1.92
    x = 0.14
    for big, lab, col in items:
        ax.add_patch(FancyBboxPatch((x, 0.12), w, 1.50,
            boxstyle="round,pad=0,rounding_size=0.10", fc=PALE if col == BLUE else
            ("#FDF3E9" if col == ORANGE else "#ECF7EE"), ec=col, lw=1.8))
        ax.text(x + w / 2, 1.14, big, ha="center", fontsize=23, fontweight="bold",
                color=col)
        ax.text(x + w / 2, 0.55, lab, ha="center", va="center", fontsize=9.5,
                color="#333", linespacing=1.45)
        x += w + 0.14
    fig.savefig(f"{OUT}/fig_evidence.png", bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)


for f in (mechanism, themes, evidence):
    f(); print("ok", f.__name__)
