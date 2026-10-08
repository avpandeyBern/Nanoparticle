import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *

fig = plt.figure(figsize=(7.0, 6.4))
gs = fig.add_gridspec(2, 2, left=0.145, right=0.985, top=0.905, bottom=0.055,
                      height_ratios=[1.0, 1.12], wspace=0.34, hspace=0.46)

# ---- A  extraction barriers --------------------------------------------
axA = fig.add_subplot(gs[0, :])
rows = ["EGCG, targeted", "catechin nanoemulsion",
        "curcumin, aptamer liposome", "curcumin, lipid carrier"]
cols = ["dose\nunits", "route\nstated", "endpoint\nday", "variance\ntype",
        "animal\nnumber", "treatment\ncount", "formulation\ntable"]
#  0 = conflicting / missing, 1 = unclear, 2 = consistent as reported
M = np.array([[0, 0, 2, 0, 1, 2, 2],
              [0, 2, 2, 1, 2, 0, 2],
              [2, 2, 0, 1, 1, 1, 2],
              [2, 2, 2, 0, 0, 2, 0]])
cmap = {2: GREEN, 1: AMBER, 0: RED}
nr, nc = M.shape
for i in range(nr):
    for j in range(nc):
        c = cmap[M[i, j]]
        axA.add_patch(FancyBboxPatch((j + 0.08, nr - 1 - i + 0.08), 0.84, 0.84,
                                     boxstyle="round,pad=0,rounding_size=0.16",
                                     facecolor=tint(c, .72), edgecolor=c, lw=1.2))
        cx, cy = j + 0.5, nr - 1 - i + 0.5
        if M[i, j] == 2:
            axA.plot([cx - .17, cx - .05, cx + .19], [cy + .01, cy - .14, cy + .16],
                     color=c, lw=1.9, solid_capstyle="round", solid_joinstyle="round")
        elif M[i, j] == 1:
            axA.plot([cx], [cy], marker="o", ms=5.0, color=c)
        else:
            axA.plot([cx - .15, cx + .15], [cy - .15, cy + .15], color=c, lw=1.9,
                     solid_capstyle="round")
            axA.plot([cx - .15, cx + .15], [cy + .15, cy - .15], color=c, lw=1.9,
                     solid_capstyle="round")
axA.set_xlim(0, nc); axA.set_ylim(0, nr)
axA.set_xticks(np.arange(nc) + 0.5); axA.set_xticklabels(cols, fontsize=6.6, color=INK2)
axA.set_yticks(np.arange(nr) + 0.5); axA.set_yticklabels(rows[::-1], fontsize=7.4, color=INK)
axA.xaxis.set_ticks_position("top"); axA.xaxis.set_label_position("top")
axA.tick_params(length=0, pad=4)
for sp in axA.spines.values():
    sp.set_visible(False)
for k, (c, lab) in enumerate([(GREEN, "consistent"), (AMBER, "unclear"),
                              (RED, "conflicting or missing")]):
    axA.add_patch(Ellipse((0.22 + k*2.05, -0.62), 0.22, 0.30, facecolor=tint(c, .60),
                         edgecolor=c, lw=1.2, clip_on=False))
    axA.text(0.40 + k*2.05, -0.62, lab, fontsize=7.0, color=INK2, va="center",
             ha="left", clip_on=False)

# ---- B  conditions for a pooled contrast -------------------------------
axB = canvas(fig.add_subplot(gs[1, 0]))
reqs = [("same active\nmoiety", BLUE), ("matched\nroute", TEAL),
        ("common\nendpoint", VIOLET), ("reported\nvariance", AMBER),
        ("animal-level\nreplication", ORANGE), ("independent\ncomparator", PINK)]
for k, (lab, c) in enumerate(reqs):
    cx = 0.175 + (k % 3)*0.325
    cy = 0.78 - (k // 3)*0.42
    axB.add_patch(Circle((cx, cy), 0.088, facecolor=tint(c, .45),
                         edgecolor="white", lw=2.0, zorder=3))
    axB.add_patch(Circle((cx, cy), 0.118, facecolor="none", edgecolor=tint(c, .62),
                         lw=1.6, zorder=2))
    axB.text(cx, cy, str(k + 1), ha="center", va="center", fontsize=9.0,
             color="white", fontweight="bold", zorder=4)
    axB.text(cx, cy - 0.145, lab, ha="center", va="top", fontsize=6.9, color=c,
             fontweight="semibold")
axB.text(0.5, 0.015, "all six required before pooling", ha="center",
         fontsize=7.4, color=MUTED, style="italic")

# ---- C  descriptive within-study ratios, no pooled estimate ------------
axC = fig.add_subplot(gs[1, 1])
pts = [("EGCG",     [0.828, 0.603, 0.420, 0.649, 0.566], BLUE),
       ("curcumin", [0.753, 0.332, 0.674],               ORANGE),
       ("catechin", [0.717, 0.475],                      TEAL)]
y = 0
yt, ylab = [], []
for name, vals, c in pts:
    ys = [y + 0.5]*len(vals)
    axC.scatter(vals, ys, s=58, c=c, edgecolors="white", linewidths=1.3, zorder=4)
    yt.append(y + 0.5); ylab.append(name)
    y += 1
axC.axvline(1.0, color=INK2, lw=1.2, ls=(0, (4, 3)), zorder=2)
axC.set_xticks([0.3, 0.5, 0.7, 0.9, 1.1])
axC.set_xticklabels(["0.3", "0.5", "0.7", "0.9", "1.1"], fontsize=7.6)
axC.set_xlim(0.24, 1.30)
axC.set_yticks(yt); axC.set_yticklabels(ylab, fontsize=7.8, color=INK)
axC.set_ylim(-1.15, 3.05)
axC.set_xlabel("formulated / free ratio of tumor burden", fontsize=7.8)
axC.xaxis.grid(True, color=GRID, lw=0.8); axC.set_axisbelow(True)
axC.tick_params(axis="y", length=0)
for sp in ("top", "right", "left"):
    axC.spines[sp].set_visible(False)
# where a pooled diamond would go - explicitly absent
d = np.array([[0.50, -0.52], [0.64, -0.30], [0.78, -0.52], [0.64, -0.74]])
axC.add_patch(Polygon(d, closed=True, facecolor="none", edgecolor=MUTED,
                      lw=1.3, ls=(0, (3, 2)), zorder=3))
for dx, dy in [(1, 1), (1, -1)]:
    axC.plot([0.64 - 0.055*dx, 0.64 + 0.055*dx],
             [-0.52 - 0.145*dy, -0.52 + 0.145*dy], color=RED, lw=2.0,
             zorder=5, solid_capstyle="round")
axC.text(0.64, -0.80, "no pooled estimate", fontsize=7.0, color=RED,
         va="top", ha="center", fontweight="semibold")
axC.text(1.045, 2.72, "favors\nfree", fontsize=6.6, color=MUTED, ha="left",
         va="center")
axC.text(0.955, 2.72, "favors\nformulation", fontsize=6.6, color=MUTED,
         ha="right", va="center")

panel_letter(fig, 0.010, 0.985, "A")
panel_letter(fig, 0.010, 0.460, "B")
panel_letter(fig, 0.510, 0.460, "C")
save(fig, "Figure5.png")
