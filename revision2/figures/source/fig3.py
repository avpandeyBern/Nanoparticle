import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *

CTRL, FREE, NANO, TGT = "#9AA7B6", ORANGE, BLUE, VIOLET

fig = plt.figure(figsize=(7.0, 6.2))
gs = fig.add_gridspec(2, 2, left=0.085, right=0.985, top=0.925, bottom=0.045,
                      wspace=0.30, hspace=0.34)

# ---- A  i.v. liposomes: baseline and endpoint --------------------------
axA = fig.add_subplot(gs[0, 0])
labels = ["blank\ncarrier", "free", "untargeted", "targeted"]
d1  = np.array([129, 131, 126, 131], float); e1 = np.array([26, 22, 28, 31], float)
d10 = np.array([659, 365, 275, 121], float); e10 = np.array([136, 156, 135, 72], float)
cols = [CTRL, FREE, NANO, TGT]
x = np.arange(4); w = 0.34
for i in range(4):
    axA.add_patch(FancyBboxPatch((x[i]-w-0.02, 0), w, d1[i],
                                 boxstyle="round,pad=0,rounding_size=0",
                                 facecolor=tint(cols[i], .55), edgecolor=cols[i],
                                 lw=1.1, hatch="////"))
    axA.errorbar(x[i]-w/2-0.02, d1[i], yerr=e1[i], fmt="none", ecolor=INK2,
                 elinewidth=0.9, capsize=2.4, capthick=0.9, zorder=5)
    axA.add_patch(FancyBboxPatch((x[i]+0.02, 0), w, d10[i],
                                 boxstyle="round,pad=0,rounding_size=0",
                                 facecolor=cols[i], edgecolor="white", lw=1.4))
    axA.errorbar(x[i]+w/2+0.02, d10[i], yerr=e10[i], fmt="none", ecolor=INK2,
                 elinewidth=1.0, capsize=2.8, capthick=1.0, zorder=5)
    axA.text(x[i]+w/2+0.02, d10[i]+e10[i]+22, f"{d10[i]:.0f}", ha="center",
             va="bottom", fontsize=7.2, color=INK, fontweight="semibold")
axA.axhline(d1.mean(), color=PINK, lw=1.2, ls=(0, (4, 3)), zorder=3)
axA.text(3.68, d1.mean()+16, "baseline", fontsize=6.8, color=PINK, ha="right",
         va="bottom", fontweight="semibold")
axA.set_ylim(0, 1010); axA.set_xlim(-0.72, 3.72)
axA.set_ylabel("tumor volume (mm$^3$)", fontsize=8.3)
axA.set_xticks(x); axA.set_xticklabels(labels, fontsize=7.4)
axA.yaxis.grid(True, color=GRID, lw=0.8); axA.set_axisbelow(True)
for sp in ("top", "right"): axA.spines[sp].set_visible(False)
axA.add_patch(FancyBboxPatch((-0.60, 915), 0.17, 50,
                             boxstyle="round,pad=0,rounding_size=0",
                             facecolor=tint(INK2, .55), edgecolor=INK2, lw=1.0,
                             hatch="////"))
axA.text(-0.36, 940, "day 1", fontsize=6.9, color=INK2, va="center")
axA.add_patch(FancyBboxPatch((0.86, 915), 0.17, 50,
                             boxstyle="round,pad=0,rounding_size=0",
                             facecolor=INK2, edgecolor="white", lw=1.0))
axA.text(1.10, 940, "endpoint", fontsize=6.9, color=INK2, va="center")
axA.annotate("mean ± s.d.", xy=(0.5, 0), xycoords="axes fraction",
             xytext=(0, -30), textcoords="offset points", ha="center", va="top",
             fontsize=7.2, color=MUTED, style="italic")

# ---- B  i.v. nanostructured lipid carrier, full arm set -----------------
axB = fig.add_subplot(gs[0, 1])
bars(axB, ["control", "blank\ncarrier", "free", "lipid\ncarrier"],
     [1412.0, 1375.2, 1155.1, 778.4], [CTRL, tint(TEAL, .45), FREE, TEAL],
     label_size=7.2)
axB.set_ylabel("tumor volume (mm$^3$)", fontsize=8.3)
axB.set_ylim(0, 1412*1.36)
axB.text(3, 778.4 + 255, "0.67×", ha="center", va="bottom", fontsize=8.2,
         color=TEAL, fontweight="bold")
axB.annotate("variance not recovered", xy=(0.5, 0), xycoords="axes fraction",
             xytext=(0, -30), textcoords="offset points", ha="center", va="top",
             fontsize=7.2, color=MUTED, style="italic")

# ---- C  route strata ----------------------------------------------------
axC = canvas(fig.add_subplot(gs[1, 0]))
stages = [("absorption", AMBER), ("first\npass", ORANGE),
          ("circulation", BLUE), ("extra-\nvasation", TEAL)]
x0, w, gp = 0.045, 0.180, 0.012
cy0, ch = 0.645, 0.175
for i, (lab, c) in enumerate(stages):
    x = x0 + i*(w + gp)
    card(axC, x, cy0, w, ch, tint(c, .70), ec=c, r=0.026, lw=1.3)
    axC.text(x + w/2, cy0 + ch/2, lab, ha="center", va="center", fontsize=6.2,
             color=c, fontweight="semibold")
tx = x0 + 4*(w + gp)
card(axC, tx, cy0, 0.155, ch, PINK, r=0.026)
axC.text(tx + 0.0775, cy0 + ch/2, "tumor", ha="center", va="center",
         fontsize=6.9, color="white", fontweight="semibold")
axC.text(0.5, 0.90, "barriers between dose and tumor", ha="center",
         fontsize=7.6, color=MUTED, style="italic")

for lab, xt, c, y in [("oral", x0 + w/2, AMBER, 0.46),
                      ("i.v.", x0 + 2*(w + gp) + w/2, BLUE, 0.29),
                      ("intratumoral", tx + 0.0775, PINK, 0.12)]:
    axC.plot([0.035, xt], [y, y], color=c, lw=2.1, solid_capstyle="round", zorder=3)
    arrow(axC, (xt, y), (xt, cy0 - 0.012), color=c, lw=2.1, ms=9, z=3)
    axC.add_patch(Circle((0.035, y), 0.018, facecolor=c, edgecolor="white",
                         lw=1.0, zorder=4))
    axC.text(0.058, y - 0.030, lab, ha="left", va="top", fontsize=7.4,
             color=c, fontweight="semibold")

# ---- D ------------------------------------------------------------------
axD = canvas(fig.add_subplot(gs[1, 1]))
items = [("cancer-cell\nproliferation", GREEN, "down"),
         ("tumor\nburden",             GREY,  "flat"),
         ("body\nweight",               GREY,  "flat"),
         ("liver\nweight",              RED,   "up")]
bw2, g2 = 0.205, 0.028
for i, (lab, c, d) in enumerate(items):
    x = 0.035 + i*(bw2 + g2)
    card(axD, x, 0.345, bw2, 0.40, tint(c, .78), ec=tint(c, .45), r=0.03, lw=1.2)
    cx, cy = x + bw2/2, 0.545
    if d == "down":
        arrow(axD, (cx, cy + 0.085), (cx, cy - 0.085), color=c, lw=3.0, ms=14, z=5)
    elif d == "up":
        arrow(axD, (cx, cy - 0.085), (cx, cy + 0.085), color=c, lw=3.0, ms=14, z=5)
    else:
        axD.plot([cx - 0.055, cx + 0.055], [cy, cy], color=c, lw=3.0,
                 solid_capstyle="round", zorder=5)
    axD.text(cx, 0.295, lab, ha="center", va="top", fontsize=7.1, color=INK)
axD.text(0.5, 0.90, "dietary nanoparticle curcumin, no free-drug arm",
         ha="center", fontsize=7.6, color=MUTED, style="italic")

panel_letter(fig, 0.010, 0.985, "A")
panel_letter(fig, 0.510, 0.985, "B")
panel_letter(fig, 0.010, 0.470, "C")
panel_letter(fig, 0.510, 0.470, "D")
save(fig, "Figure3.png")
