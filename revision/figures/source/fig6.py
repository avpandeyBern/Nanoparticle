import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *

fig = plt.figure(figsize=(7.0, 6.3))
gs = fig.add_gridspec(2, 2, left=0.025, right=0.985, top=0.945, bottom=0.025,
                      wspace=0.10, hspace=0.16)

# ---------------- A : the arms ------------------------------------------
axA = canvas(fig.add_subplot(gs[0, 0]))
arms = [("vehicle", MUTED), ("free drug", ORANGE), ("blank carrier", TEAL),
        ("loaded carrier", BLUE), ("untargeted vs\ntargeted", VIOLET)]
n = len(arms)
hh, gg = 0.145, 0.032
for i, (lab, c) in enumerate(arms):
    y = 0.975 - i*(hh + gg) - hh
    card(axA, 0.055, y, 0.90, hh, tint(c, .86), ec=tint(c, .55), r=0.028, lw=1.2)
    gx, gy = 0.145, y + hh/2
    if i == 0:
        axA.add_patch(Circle((gx, gy), 0.040, facecolor=tint(c, .45),
                             edgecolor=c, lw=1.2, zorder=4))
    elif i == 1:
        free_drug(axA, gx, gy, 0.026, ORANGE, n=6, seed=21, spread=1.5)
    elif i == 2:
        nanoparticle(axA, gx, gy, 0.045, TEAL, "none", n=0, seed=22, lw=1.5)
    elif i == 3:
        nanoparticle(axA, gx, gy, 0.045, BLUE, ORANGE, n=6, seed=23, lw=1.5)
    else:
        nanoparticle(axA, gx - 0.038, gy, 0.034, VIOLET, ORANGE, n=4, seed=24,
                     lw=1.3, corona=False)
        nanoparticle(axA, gx + 0.050, gy, 0.034, VIOLET, ORANGE, n=4, seed=25, lw=1.3)
    axA.text(0.265, gy, lab, ha="left", va="center", fontsize=8.0, color=c,
             fontweight="semibold")
    axA.text(0.925, gy, str(i + 1), ha="right", va="center", fontsize=8.4,
             color=tint(c, .35), fontweight="bold")
axA.text(0.5, 0.030, "matched active dose, route and schedule", ha="center",
         fontsize=7.4, color=MUTED, style="italic")

# ---------------- B : which contrast answers what -----------------------
axB = canvas(fig.add_subplot(gs[0, 1]))
rows = [("loaded  vs  free",        "delivery gain",   BLUE),
        ("loaded  vs  blank",       "carrier action",  TEAL),
        ("targeted vs untargeted",  "targeting",       VIOLET),
        ("co-loaded vs free mix",   "combination",     ORANGE),
        ("tumor  vs  toxicity",    "benefit–harm",    PINK)]
hh, gg = 0.145, 0.032
for i, (lhs, rhs, c) in enumerate(rows):
    y = 0.975 - i*(hh + gg) - hh
    chip(axB, 0.02, y, 0.52, hh, lhs, c, fs=7.5)
    arrow(axB, (0.555, y + hh/2), (0.625, y + hh/2), color=c, lw=1.9, ms=8)
    chip(axB, 0.645, y, 0.335, hh, rhs, tint(c, .80), tc=c, fs=7.5,
         ec=tint(c, .50))
axB.text(0.5, 0.030, "each question needs its own pair", ha="center",
         fontsize=7.4, color=MUTED, style="italic")

# ---------------- C : prespecified sequence -----------------------------
axC = canvas(fig.add_subplot(gs[1, 0]))
steps = [("implant", TEAL), ("randomize at\nset tumor size", BLUE),
         ("blinded\nmeasurement", VIOLET), ("exposure +\ntarget assay", AMBER),
         ("recovery\ninterval", PINK)]
ybase = 0.56
axC.plot([0.085, 0.935], [ybase, ybase], color=tint(MUTED, .50), lw=3.2,
         solid_capstyle="round", zorder=1)
for i, (lab, c) in enumerate(steps):
    x = 0.085 + i*0.2125
    axC.add_patch(Circle((x, ybase), 0.043, facecolor=c, edgecolor="white",
                         lw=2.2, zorder=4))
    axC.text(x, ybase, str(i + 1), ha="center", va="center", fontsize=7.6,
             color="white", fontweight="bold", zorder=5)
    up = (i % 2 == 0)
    ty = ybase + 0.095 if up else ybase - 0.095
    axC.text(x, ty, lab, ha="center", va="bottom" if up else "top",
             fontsize=6.9, color=c, fontweight="semibold")
arrow(axC, (0.935, ybase), (0.965, ybase), color=tint(MUTED, .30), lw=3.2, ms=10, z=1)
for mx, mc in [(0.215, MUTED), (0.500, ORANGE), (0.785, BLUE)]:
    mouse(axC, mx, 0.185, 0.072, tumor=0.40, tcolor=mc)
axC.text(0.5, 0.045, "equal starting tumor burden across arms", ha="center",
         fontsize=7.2, color=MUTED, style="italic")
axC.text(0.5, 0.905, "treat established disease, not engraftment",
         ha="center", fontsize=7.4, color=MUTED, style="italic")

# ---------------- D : replication and translation -----------------------
axD = canvas(fig.add_subplot(gs[1, 1]))
tiers = [("second AR-driven model", BLUE),
         ("resistant phenotype",    TEAL),
         ("orthotopic / PDX / GEM", VIOLET),
         ("animal-level data release", PINK)]
for i, (lab, c) in enumerate(tiers):
    w = 0.52 + i*0.145
    x = 0.05
    y = 0.165 + i*0.195
    card(axD, x, y, w, 0.145, c, r=0.026)
    axD.text(x + 0.035, y + 0.0725, lab, ha="left", va="center", fontsize=7.4,
             color="white", fontweight="semibold")
    axD.add_patch(Circle((x + w - 0.045, y + 0.0725), 0.028,
                         facecolor="white", edgecolor="none", zorder=5))
    axD.text(x + w - 0.045, y + 0.0725, str(i + 1), ha="center", va="center",
             fontsize=7.0, color=c, fontweight="bold", zorder=6)
arrow(axD, (0.028, 0.155), (0.028, 0.915), color=tint(MUTED, .40), lw=2.4, ms=10)
axD.text(0.5, 0.075, "progression toward translational claim", ha="center",
         fontsize=7.4, color=MUTED, style="italic")

panel_letter(fig, 0.008, 0.990, "A")
panel_letter(fig, 0.508, 0.990, "B")
panel_letter(fig, 0.008, 0.505, "C")
panel_letter(fig, 0.508, 0.505, "D")
save(fig, "Figure6.png")
