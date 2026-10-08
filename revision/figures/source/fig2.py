import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *

CTRL, FREE, NANO, TGT = "#9AA7B6", ORANGE, BLUE, VIOLET

fig = plt.figure(figsize=(7.0, 6.2))
gs = fig.add_gridspec(2, 2, left=0.085, right=0.985, top=0.925, bottom=0.075,
                      wspace=0.30, hspace=0.52)

def dose_row(ax, doses, colors, caption):
    for i, (d, c) in enumerate(zip(doses, colors)):
        if d:
            ax.annotate(d, xy=(i, 0), xycoords=("data", "axes fraction"),
                        xytext=(0, -19), textcoords="offset points",
                        ha="center", va="top", fontsize=7.4, color=c,
                        fontweight="semibold")
    ax.annotate(caption, xy=(0.5, 0), xycoords="axes fraction",
                xytext=(0, -34), textcoords="offset points",
                ha="center", va="top", fontsize=7.2, color=MUTED, style="italic")

def ratio_tag(ax, x, ytop, span, text, color):
    ax.text(x, ytop + span*0.105, text, ha="center", va="bottom",
            fontsize=8.0, color=color, fontweight="bold")

# ---- A ------------------------------------------------------------------
axA = fig.add_subplot(gs[0, 0])
v = [1242, 854, 707]
bars(axA, ["control", "free", "nano"], v, [CTRL, FREE, NANO])
dose_row(axA, ["", "1 mg", "100 µg"], [CTRL, FREE, NANO], "dose per mouse")
axA.set_ylabel("tumor volume (mm$^3$)", fontsize=8.3)
axA.set_ylim(0, 1242*1.34)
ratio_tag(axA, 2, 707 + 95, 1242, "0.83×", NANO)

# ---- B ------------------------------------------------------------------
axB = fig.add_subplot(gs[0, 1])
v = [1200, 514, 310, 216]
bars(axB, ["control", "free", "nano", "nano"], v,
     [CTRL, FREE, tint(NANO, .35), NANO])
dose_row(axB, ["", "40", "3", "6"], [CTRL, FREE, NANO, NANO],
         "dose (mg kg$^{-1}$)")
axB.set_ylabel("tumor volume (mm$^3$)", fontsize=8.3)
axB.set_ylim(0, 1200*1.34)
ratio_tag(axB, 2, 310 + 95, 1200, "0.60×", NANO)
ratio_tag(axB, 3, 216 + 95, 1200, "0.42×", NANO)

# ---- C ------------------------------------------------------------------
axC = fig.add_subplot(gs[1, 0])
v = [2685, 1895, 1230, 1073]
bars(axC, ["control", "free", "untargeted", "targeted"], v,
     [CTRL, FREE, NANO, TGT], label_size=7.4)
axC.set_ylabel("tumor volume (mm$^3$)", fontsize=8.3)
axC.set_ylim(0, 2685*1.34)
ratio_tag(axC, 2, 1230 + 200, 2685, "0.65×", NANO)
ratio_tag(axC, 3, 1073 + 200, 2685, "0.57×", TGT)
axC.annotate("", xy=(3, 2360), xytext=(2, 2360),
             arrowprops=dict(arrowstyle="-|>", color=TGT, lw=1.3,
                             shrinkA=1, shrinkB=1))
axC.text(2.5, 2420, "0.87×", ha="center", va="bottom", fontsize=7.8,
         color=TGT, fontweight="bold")

# ---- D ------------------------------------------------------------------
axD = fig.add_subplot(gs[1, 1])
cols = ["dose\nmatched", "route\nmatched", "variance\nrecovered",
        "established\ntumor", "animal\nas unit"]
rows = ["i.p.", "oral", "targeted"]
M = np.array([[0, 2, 0, 1, 2],
              [0, 2, 0, 0, 0],
              [2, 0, 0, 1, 1]])
cmap = {2: GREEN, 1: AMBER, 0: RED}
for i in range(3):
    for j in range(5):
        c = cmap[M[i, j]]
        axD.add_patch(FancyBboxPatch((j + 0.09, 2 - i + 0.09), 0.82, 0.82,
                                     boxstyle="round,pad=0,rounding_size=0.16",
                                     facecolor=tint(c, .72), edgecolor=c, lw=1.3))
        cx, cy = j + 0.5, 2 - i + 0.5
        if M[i, j] == 2:
            axD.plot([cx - .18, cx - .05, cx + .20], [cy + .02, cy - .15, cy + .17],
                     color=c, lw=2.1, solid_capstyle="round", solid_joinstyle="round")
        elif M[i, j] == 1:
            axD.plot([cx], [cy], marker="o", ms=5.5, color=c)
        else:
            axD.plot([cx - .16, cx + .16], [cy - .16, cy + .16], color=c, lw=2.1,
                     solid_capstyle="round")
            axD.plot([cx - .16, cx + .16], [cy + .16, cy - .16], color=c, lw=2.1,
                     solid_capstyle="round")
axD.set_xlim(0, 5); axD.set_ylim(0, 3)
axD.set_aspect("equal")
axD.set_xticks(np.arange(5) + 0.5)
axD.set_xticklabels(cols, fontsize=6.8, color=INK2)
axD.set_yticks(np.arange(3) + 0.5)
axD.set_yticklabels(rows[::-1], fontsize=8.2, color=INK)
axD.tick_params(length=0)
for sp in axD.spines.values():
    sp.set_visible(False)
for k, (c, lab) in enumerate([(GREEN, "met"), (AMBER, "unclear"), (RED, "not met")]):
    axD.add_patch(Circle((0.30 + k*1.65, -1.30), 0.155, facecolor=tint(c, .60),
                         edgecolor=c, lw=1.2, clip_on=False))
    axD.text(0.56 + k*1.65, -1.30, lab, fontsize=7.4, color=INK2,
             va="center", ha="left", clip_on=False)

panel_letter(fig, 0.010, 0.985, "A")
panel_letter(fig, 0.510, 0.985, "B")
panel_letter(fig, 0.010, 0.500, "C")
panel_letter(fig, 0.510, 0.500, "D")
save(fig, "Figure2.png")
