#!/usr/bin/env python3
"""Add Aurora B and its substrate to the Bloom & North KC-MT panel.

The source panel shows PP2A-B56 delivery only; Aurora B is not in it. Our
additions are drawn in orange and declared on the slide and in FIGURE-CREDITS.
"""
import sys, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch
from PIL import Image

OUT = sys.argv[1] if len(sys.argv) > 1 else "img"
ORANGE, RED, GREY = "#E8820C", "#C0392B", "#5C5C5C"
im = Image.open(f"{OUT}/pap_kcmt.png")
W, H = im.size
# widen the canvas downward so the annotation does not cover the source panel
PAD = int(H * 0.21)
canvas = Image.new("RGB", (W, H + PAD), "white")
canvas.paste(im, (0, 0))

fig, ax = plt.subplots(figsize=(W / 100, (H + PAD) / 100), dpi=200)
ax.imshow(canvas); ax.set_xlim(0, W); ax.set_ylim(H + PAD, 0); ax.axis("off")
plt.rcParams["font.family"] = "Liberation Sans"

# the grip: where the green microtubule meets the yellow kinetochore
GX, GY = int(W * 0.745), int(H * 0.552)
ax.add_patch(Circle((GX, GY), int(W * 0.052), fc="none", ec=RED, lw=3.0, zorder=5))

# Aurora B, drawn by us, below the kinetochore
AX, AY = int(W * 0.21), int(H + PAD * 0.42)
ax.add_patch(Circle((AX, AY), int(W * 0.125), fc=ORANGE, ec="white", lw=2.0, zorder=6))
ax.text(AX, AY, "Aurora\nB", ha="center", va="center", fontsize=13,
        fontweight="bold", color="white", linespacing=1.0, zorder=7)
ax.add_patch(FancyArrowPatch((AX + W * 0.10, AY - PAD * 0.26),
                             (GX - W * 0.065, GY + H * 0.040),
                             arrowstyle="-|>", mutation_scale=20, color=ORANGE,
                             lw=3.0, zorder=6,
                             connectionstyle="arc3,rad=-0.22"))
ax.text(GX + W * 0.085, GY - H * 0.030, "P", ha="center", va="center", fontsize=15,
        fontweight="bold", color=RED, zorder=7)
ax.text(W * 0.46, H + PAD * 0.40, "Aurora B\nadded by us",
        ha="left", va="center", fontsize=13, fontweight="bold", color=ORANGE, linespacing=1.3)
fig.savefig(f"{OUT}/pap_kcmt_annot.png", bbox_inches="tight", pad_inches=0.02)
print("ok pap_kcmt_annot")
