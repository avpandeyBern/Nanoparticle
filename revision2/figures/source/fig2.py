import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *

CTRL, FREE, NANO, TGT = "#9AA7B6", ORANGE, BLUE, VIOLET

fig = plt.figure(figsize=(7.0, 6.3))
gs = fig.add_gridspec(2, 2, left=0.085, right=0.985, top=0.925, bottom=0.075,
                      wspace=0.30, hspace=0.55)

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

# ---- A  i.p., day 45 ----------------------------------------------------
axA = fig.add_subplot(gs[0, 0])
v = [1242, 854, 707]
bars(axA, ["control", "free", "nano"], v, [CTRL, FREE, NANO])
dose_row(axA, ["", "1 mg", "100 µg"], [CTRL, FREE, NANO], "dose per mouse, i.p.")
axA.set_ylabel("tumor volume (mm$^3$)", fontsize=8.3)
axA.set_ylim(0, 1242*1.34)
axA.text(2, 707 + 175, "0.83×", ha="center", va="bottom", fontsize=8.2,
         color=NANO, fontweight="bold")

# ---- B  oral, day 32 ----------------------------------------------------
axB = fig.add_subplot(gs[0, 1])
v = [1200, 514, 310, 216]
bars(axB, ["control", "free", "nano", "nano"], v,
     [CTRL, FREE, tint(NANO, .35), NANO])
dose_row(axB, ["", "40", "3", "6"], [CTRL, FREE, NANO, NANO],
         "dose (mg kg$^{-1}$), oral")
axB.set_ylabel("tumor volume (mm$^3$)", fontsize=8.3)
axB.set_ylim(0, 1200*1.34)
axB.text(2, 310 + 165, "0.60×", ha="center", va="bottom", fontsize=8.2,
         color=NANO, fontweight="bold")
axB.text(3, 216 + 165, "0.42×", ha="center", va="bottom", fontsize=8.2,
         color=NANO, fontweight="bold")

# ---- C  targeted vs untargeted: two endpoints, one scale ---------------
axC = fig.add_subplot(gs[1, 0])
labels = ["control", "free", "untargeted", "targeted"]
vol = np.array([2685, 1895, 1230, 1073], float)
wt  = np.array([3.0, 2.1, 1.3, 1.1], float)
volp = 100*vol/vol[0]
wtp  = 100*wt/wt[0]
cols = [CTRL, FREE, NANO, TGT]
x = np.arange(4); w = 0.34
for i in range(4):
    axC.add_patch(FancyBboxPatch((x[i] - w - 0.02, 0), w, volp[i],
                                 boxstyle="round,pad=0,rounding_size=0",
                                 facecolor=cols[i], edgecolor="white", lw=1.4))
    axC.text(x[i] - w/2 - 0.02, volp[i] + 2.6, f"{volp[i]:.0f}", ha="center",
             va="bottom", fontsize=7.0, color=INK, fontweight="semibold")
    axC.add_patch(FancyBboxPatch((x[i] + 0.02, 0), w, wtp[i],
                                 boxstyle="round,pad=0,rounding_size=0",
                                 facecolor=tint(cols[i], .50),
                                 edgecolor=cols[i], lw=1.2, hatch="////"))
    axC.text(x[i] + w/2 + 0.02, wtp[i] + 2.6, f"{wtp[i]:.0f}", ha="center",
             va="bottom", fontsize=7.0, color=INK2)
axC.set_ylim(0, 128); axC.set_xlim(-0.72, 3.72)
axC.set_ylabel("endpoint, % of control", fontsize=8.3)
axC.set_xticks(x); axC.set_xticklabels(labels, fontsize=7.4)
axC.yaxis.grid(True, color=GRID, lw=0.8); axC.set_axisbelow(True)
for sp in ("top", "right"): axC.spines[sp].set_visible(False)
axC.add_patch(FancyBboxPatch((-0.60, 117.5), 0.17, 7.0,
                             boxstyle="round,pad=0,rounding_size=0",
                             facecolor=INK2, edgecolor="white", lw=1.0))
axC.text(-0.36, 121.0, "volume", fontsize=7.0, color=INK2, va="center")
axC.add_patch(FancyBboxPatch((0.86, 117.5), 0.17, 7.0,
                             boxstyle="round,pad=0,rounding_size=0",
                             facecolor=tint(INK2, .50), edgecolor=INK2,
                             lw=1.0, hatch="////"))
axC.text(1.10, 121.0, "weight", fontsize=7.0, color=INK2, va="center")

# ---- D  verification status of the three experiments -------------------
axD = fig.add_subplot(gs[1, 1])
cols2 = ["dose\nmatched", "route\nstated", "variance\nrecovered",
         "established\ntumor", "animal\nas unit"]
rows = ["i.p.", "oral", "targeted"]
#  2 = met, 1 = unclear, 0 = not met
M = np.array([[0, 2, 1, 1, 2],
              [0, 2, 1, 0, 0],
              [2, 0, 0, 0, 2]])
cmap = {2: GREEN, 1: AMBER, 0: RED}
for i in range(3):
    for j in range(5):
        c = cmap[M[i, j]]
        axD.add_patch(FancyBboxPatch((j + 0.09, 2 - i + 0.09), 0.82, 0.82,
                                     boxstyle="round,pad=0,rounding_size=0.16",
                                     facecolor=tint(c, .72), edgecolor=c, lw=1.3))
        cx, cy = j + 0.5, 2 - i + 0.5
        if M[i, j] == 2:
            axD.plot([cx-.18, cx-.05, cx+.20], [cy+.02, cy-.15, cy+.17], color=c,
                     lw=2.1, solid_capstyle="round", solid_joinstyle="round")
        elif M[i, j] == 1:
            axD.plot([cx], [cy], marker="o", ms=5.5, color=c)
        else:
            axD.plot([cx-.16, cx+.16], [cy-.16, cy+.16], color=c, lw=2.1, solid_capstyle="round")
            axD.plot([cx-.16, cx+.16], [cy+.16, cy-.16], color=c, lw=2.1, solid_capstyle="round")
axD.set_xlim(0, 5); axD.set_ylim(0, 3); axD.set_aspect("equal")
axD.set_xticks(np.arange(5) + 0.5); axD.set_xticklabels(cols2, fontsize=6.8, color=INK2)
axD.set_yticks(np.arange(3) + 0.5); axD.set_yticklabels(rows[::-1], fontsize=8.2, color=INK)
axD.tick_params(length=0)
for sp in axD.spines.values(): sp.set_visible(False)
for k, (c, lab) in enumerate([(GREEN, "met"), (AMBER, "unclear"), (RED, "not met")]):
    axD.add_patch(Circle((0.30 + k*1.65, -1.30), 0.155, facecolor=tint(c, .60),
                         edgecolor=c, lw=1.2, clip_on=False))
    axD.text(0.56 + k*1.65, -1.30, lab, fontsize=7.4, color=INK2, va="center",
             ha="left", clip_on=False)

panel_letter(fig, 0.010, 0.985, "A")
panel_letter(fig, 0.510, 0.985, "B")
panel_letter(fig, 0.010, 0.495, "C")
panel_letter(fig, 0.510, 0.495, "D")
save(fig, "Figure2.png")
