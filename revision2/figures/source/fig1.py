import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *

fig = plt.figure(figsize=(7.0, 6.1))
gs = fig.add_gridspec(2, 2, left=0.045, right=0.985, top=0.945, bottom=0.035,
                      wspace=0.13, hspace=0.18)

# ---------------- A : equal active dose, not equal carrier mass ----------
axA = canvas(fig.add_subplot(gs[0, 0]))
free_drug(axA, 0.24, 0.75, 0.085, ORANGE, n=10, seed=3, spread=1.5)
nanoparticle(axA, 0.72, 0.75, 0.115, BLUE, ORANGE, n=10, seed=4)
axA.text(0.48, 0.75, "=", ha="center", va="center", fontsize=18,
         color=INK, fontweight="bold")
axA.text(0.24, 0.555, "free", ha="center", va="center", fontsize=8.5, color=INK2)
axA.text(0.72, 0.555, "loaded carrier", ha="center", va="center", fontsize=8.5, color=INK2)

y0, bw = 0.30, 0.84
card(axA, 0.08, y0, bw, 0.085, tint(BLUE, .70), r=0.016)
card(axA, 0.08, y0, bw*0.02, 0.085, ORANGE, r=0.003)
axA.text(0.08 + bw, y0 + 0.115, "carrier mass  100 mg kg$^{-1}$", fontsize=8.0,
         color=BLUE, fontweight="semibold", va="bottom", ha="right")
# leader from the 2 % sliver down to its label
arrow(axA, (0.088, y0 - 0.008), (0.088, y0 - 0.085), color=ORANGE, lw=1.2,
      style="-", z=6)
arrow(axA, (0.088, y0 - 0.085), (0.145, y0 - 0.085), color=ORANGE, lw=1.2,
      style="-", z=6)
axA.text(0.155, y0 - 0.085, "active equivalent  2 mg kg$^{-1}$", fontsize=8.0,
         color=ORANGE, fontweight="semibold", va="center", ha="left")
axA.text(0.08 + bw, y0 - 0.175, "2 % loading", fontsize=7.8, color=MUTED,
         va="center", ha="right", style="italic")

# ---------------- B : four matched conditions -> four estimands ----------
axB = canvas(fig.add_subplot(gs[0, 1]))
rows = [("equal dose",          "delivery gain",     BLUE),
        ("lower dose",          "dose sparing",      TEAL),
        ("equal exposure",      "altered action",    VIOLET),
        ("equal tumor control", "therapeutic index", PINK)]
h, g = 0.155, 0.065
for i, (lhs, rhs, c) in enumerate(rows):
    y = 0.86 - i*(h + g) - h
    chip(axB, 0.03, y, 0.40, h, lhs, c, fs=8.2)
    arrow(axB, (0.455, y + h/2), (0.545, y + h/2), color=c, lw=2.0, ms=9)
    chip(axB, 0.57, y, 0.40, h, rhs, tint(c, .80), tc=c, fs=8.2, ec=tint(c, .50))

# ---------------- C : causal sequence ------------------------------------
axC = canvas(fig.add_subplot(gs[1, 0]))
nodes = {"F": (0.25, 0.82, "formulation",     BLUE),
         "E": (0.75, 0.82, "tumor exposure", TEAL),
         "C": (0.25, 0.22, "carrier action",  VIOLET),
         "R": (0.75, 0.22, "tumor response", PINK)}
for k, (x, y, lab, c) in nodes.items():
    chip(axC, x - 0.215, y - 0.082, 0.43, 0.164, lab, c, fs=8.2)
arrow(axC, (0.47, 0.82), (0.527, 0.82), color=TEAL, lw=2.0, ms=9)
arrow(axC, (0.25, 0.732), (0.25, 0.308), color=VIOLET, lw=2.0, ms=9)
arrow(axC, (0.75, 0.732), (0.75, 0.308), color=PINK, lw=2.0, ms=9)
arrow(axC, (0.47, 0.22), (0.527, 0.22), color=PINK, lw=2.0, ms=9)
# confounder cluster, radiating outward only
card(axC, 0.325, 0.445, 0.35, 0.155, tint(ORANGE, .88), ec=tint(ORANGE, .45),
     r=0.03, lw=1.3)
axC.text(0.50, 0.555, "dose · route", ha="center", va="center", fontsize=7.8,
         color=ORANGE, fontweight="semibold")
axC.text(0.50, 0.488, "vehicle · schedule", ha="center", va="center",
         fontsize=7.8, color=ORANGE, fontweight="semibold")
for (sx, sy, ex, ey) in [(0.325, 0.60, 0.255, 0.675),
                         (0.675, 0.60, 0.745, 0.675),
                         (0.325, 0.445, 0.255, 0.368),
                         (0.675, 0.445, 0.745, 0.368)]:
    arrow(axC, (sx, sy), (ex, ey), color=tint(ORANGE, .20), lw=1.4, ms=7, z=2)

# ---------------- D : claim ladder ---------------------------------------
axD = canvas(fig.add_subplot(gs[1, 1]))
steps = [("uptake", BLUE), ("exposure", TEAL), ("efficacy", AMBER),
         ("benefit–harm", PINK)]
bw2 = 0.205
for i, (lab, c) in enumerate(steps):
    x = 0.045 + i*0.235
    hgt = 0.24 + i*0.135
    card(axD, x, 0.22, bw2, hgt, c, r=0.022)
    axD.text(x + bw2/2, 0.22 + hgt + 0.035, lab, ha="center", va="bottom",
             fontsize=8.2, color=c, fontweight="semibold")
    # dot row = number of independent measurements the claim needs
    for j in range(i + 1):
        axD.add_patch(Circle((x + bw2/2 + (j - i/2)*0.044, 0.30), 0.0155,
                             facecolor="white", edgecolor="none", zorder=6))
arrow(axD, (0.045, 0.155), (0.955, 0.155), color=MUTED, lw=1.8, ms=9)
axD.text(0.50, 0.085, "increasing evidential burden", ha="center", va="center",
         fontsize=7.8, color=MUTED, style="italic")

panel_letter(fig, 0.010, 0.985, "A")
panel_letter(fig, 0.510, 0.985, "B")
panel_letter(fig, 0.010, 0.500, "C")
panel_letter(fig, 0.510, 0.500, "D")
save(fig, "Figure1.png")
