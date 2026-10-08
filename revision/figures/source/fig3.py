import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *

CTRL, FREE, NANO, TGT = "#9AA7B6", ORANGE, BLUE, VIOLET

fig = plt.figure(figsize=(7.0, 6.2))
gs = fig.add_gridspec(2, 2, left=0.085, right=0.985, top=0.925, bottom=0.045,
                      wspace=0.30, hspace=0.34)

# ---- A ------------------------------------------------------------------
axA = fig.add_subplot(gs[0, 0])
v = [659, 365, 275, 121]; e = [136, 156, 135, 72]
bars(axA, ["blank\ncarrier", "free", "untargeted", "targeted"], v,
     [CTRL, FREE, NANO, TGT], errs=e, label_size=7.4)
axA.set_ylabel("tumor volume (mm$^3$)", fontsize=8.3)
axA.set_ylim(0, 1080)
axA.text(2, 560, "0.75×", ha="center", fontsize=8.2, color=NANO, fontweight="bold")
axA.text(3, 340, "0.33×", ha="center", fontsize=8.2, color=TGT, fontweight="bold")
axA.annotate("mean ± s.d.", xy=(0.5, 0), xycoords="axes fraction",
             xytext=(0, -30), textcoords="offset points", ha="center", va="top",
             fontsize=7.2, color=MUTED, style="italic")

# ---- B ------------------------------------------------------------------
axB = fig.add_subplot(gs[0, 1])
bars(axB, ["free", "lipid carrier"], [1155.1, 778.4], [FREE, TEAL],
     width=0.46, label_size=8.0)
axB.set_ylabel("tumor volume (mm$^3$)", fontsize=8.3)
axB.set_ylim(0, 1620); axB.set_xlim(-0.75, 1.75)
axB.annotate("", xy=(1, 1330), xytext=(0, 1330),
             arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.5,
                             shrinkA=2, shrinkB=2))
axB.text(0.5, 1385, "0.67×", ha="center", fontsize=9.0, color=TEAL,
         fontweight="bold")
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
