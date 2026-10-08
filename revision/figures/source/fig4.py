import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *

FREE, NANO, TGT = ORANGE, BLUE, VIOLET

fig = plt.figure(figsize=(7.0, 6.2))
gs = fig.add_gridspec(2, 2, left=0.085, right=0.985, top=0.925, bottom=0.045,
                      wspace=0.30, hspace=0.34)

# ---- A  tumor AUC ------------------------------------------------------
axA = fig.add_subplot(gs[0, 0])
bars(axA, ["free", "untargeted", "targeted"], [1032.3, 1484.3, 4356.3],
     [FREE, NANO, TGT], vfmt="{:,.0f}", label_size=7.6)
axA.set_ylabel("tumor AUC$_{0-12h}$ (ng·h g$^{-1}$)", fontsize=8.1)
axA.set_ylim(0, 6000)
axA.annotate("", xy=(2, 5250), xytext=(0, 5250),
             arrowprops=dict(arrowstyle="-|>", color=TGT, lw=1.5,
                             shrinkA=2, shrinkB=2))
axA.text(1.0, 5320, "4.22×", ha="center", va="bottom", fontsize=9.0,
         color=TGT, fontweight="bold")
axA.annotate("uncertainty not recoverable", xy=(0.5, 0), xycoords="axes fraction",
             xytext=(0, -30), textcoords="offset points", ha="center", va="top",
             fontsize=7.2, color=MUTED, style="italic")

# ---- B  analytes along the compartments --------------------------------
axB = canvas(fig.add_subplot(gs[0, 1]))
comp = [("plasma", BLUE, 0.80), ("tumor tissue", TEAL, 0.50),
        ("tumor cell", PINK, 0.20)]
for lab, c, y in comp:
    card(axB, 0.05, y - 0.095, 0.90, 0.19, tint(c, .84), ec=tint(c, .50),
         r=0.028, lw=1.2)
    axB.text(0.085, y, lab, ha="left", va="center", fontsize=7.4, color=c,
             fontweight="semibold", rotation=0)
# species glyphs in each compartment
nanoparticle(axB, 0.47, 0.80, 0.045, BLUE, ORANGE, n=5, seed=11, lw=1.3)
nanoparticle(axB, 0.47, 0.50, 0.045, BLUE, ORANGE, n=5, seed=12, lw=1.3)
free_drug(axB, 0.70, 0.50, 0.030, ORANGE, n=6, seed=13, spread=1.5)
free_drug(axB, 0.58, 0.20, 0.030, ORANGE, n=5, seed=14, spread=1.5)
free_drug(axB, 0.80, 0.20, 0.028, MUTED, n=5, seed=15, spread=1.5)
for y0, y1 in [(0.705, 0.600), (0.405, 0.300)]:
    arrow(axB, (0.50, y0), (0.50, y1), color=MUTED, lw=1.6, ms=8)
leg = [(BLUE, "carrier-bound"), (ORANGE, "released parent"),
       (MUTED, "metabolite")]
for k, (c, lab) in enumerate(leg):
    axB.add_patch(Circle((0.075, 0.055 - 0*k), 0.0, facecolor="none"))
for k, (c, lab) in enumerate(leg):
    x = 0.05 + k*0.330
    axB.add_patch(Circle((x + 0.018, 0.035), 0.016, facecolor=c,
                         edgecolor="white", lw=0.8))
    axB.text(x + 0.042, 0.035, lab, fontsize=6.3, color=INK2, va="center")

# ---- C  decomposing the observed effect --------------------------------
axC = fig.add_subplot(gs[1, 0])
rows = ["loaded\ncarrier", "blank\ncarrier", "free\ndrug"]
payload = [0.58, 0.00, 0.40]
carrier = [0.34, 0.34, 0.00]
ypos = np.arange(3)[::-1]
for y, p, c in zip(ypos, payload, carrier):
    if p > 0:
        axC.add_patch(FancyBboxPatch((0, y - 0.26), p, 0.52,
                                     boxstyle="round,pad=0,rounding_size=0.0",
                                     facecolor=ORANGE, edgecolor="white", lw=1.6))
    if c > 0:
        axC.add_patch(FancyBboxPatch((p, y - 0.26), c, 0.52,
                                     boxstyle="round,pad=0,rounding_size=0.0",
                                     facecolor=VIOLET, edgecolor="white", lw=1.6))
axC.set_ylim(-1.75, 2.75); axC.set_xlim(0, 1.0)
axC.set_yticks(ypos); axC.set_yticklabels(rows, fontsize=7.6, color=INK)
axC.set_xticks([])
axC.tick_params(length=0)
for sp in axC.spines.values():
    sp.set_visible(False)
axC.annotate("", xy=(0.62, -0.72), xytext=(0.02, -0.72),
             arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.5),
             annotation_clip=False)
axC.text(0.02, -0.86, "antitumor effect", fontsize=7.8, color=MUTED,
         va="top", ha="left", style="italic")
for k, (c, lab) in enumerate([(ORANGE, "payload"), (VIOLET, "carrier")]):
    axC.add_patch(FancyBboxPatch((0.02 + k*0.40, -1.50), 0.055, 0.22,
                                 boxstyle="round,pad=0,rounding_size=0.03",
                                 facecolor=c, edgecolor="none", clip_on=False))
    axC.text(0.09 + k*0.40, -1.39, lab, fontsize=7.4, color=INK2, va="center",
             clip_on=False)

# ---- D  minimum exposure measurement set --------------------------------
axD = canvas(fig.add_subplot(gs[1, 1]))
axD.set_aspect("equal")
labels = ["plasma\nAUC", "tumor\nAUC", "tumor:plasma\nratio",
          "organ\ndistribution", "unbound\nparent", "target\nengagement"]
cols = [BLUE, TEAL, VIOLET, AMBER, ORANGE, PINK]
cx, cy, R, r0 = 0.50, 0.50, 0.30, 0.125
for i, (lab, c) in enumerate(zip(labels, cols)):
    a0, a1 = 90 - i*60 - 57, 90 - i*60 - 3
    axD.add_patch(Wedge((cx, cy), R, a0, a1, width=R - r0,
                        facecolor=tint(c, .40), edgecolor="white", lw=1.6))
    am = np.radians((a0 + a1) / 2)
    lx, ly = cx + (R + 0.105)*np.cos(am), cy + (R + 0.105)*np.sin(am)
    ha = "center"
    if np.cos(am) > 0.4: ha = "left"
    elif np.cos(am) < -0.4: ha = "right"
    axD.text(lx, ly, lab, ha=ha, va="center", fontsize=6.8, color=c,
             fontweight="semibold")
axD.add_patch(Circle((cx, cy), r0*0.92, facecolor=tint(INK2, .90),
                     edgecolor="none"))
axD.text(cx, cy + 0.022, "exposure", ha="center", va="center", fontsize=7.0,
         color=INK, fontweight="bold")
axD.text(cx, cy - 0.030, "evidence", ha="center", va="center", fontsize=7.0,
         color=INK, fontweight="bold")

panel_letter(fig, 0.010, 0.985, "A")
panel_letter(fig, 0.510, 0.985, "B")
panel_letter(fig, 0.010, 0.470, "C")
panel_letter(fig, 0.510, 0.470, "D")
save(fig, "Figure4.png")
