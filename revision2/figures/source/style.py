import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Ellipse, Rectangle, Wedge, Polygon
from matplotlib.path import Path
import matplotlib.patheffects as pe
import numpy as np

# ---- validated categorical palette -------------------------------------
BLUE   = "#2563C9"
ORANGE = "#E85A2A"
TEAL   = "#0E9594"
VIOLET = "#7B4FD1"
AMBER  = "#C98A09"
PINK   = "#D6336C"
CAT = [BLUE, ORANGE, TEAL, VIOLET, AMBER, PINK]

# tints for fills / backgrounds
def tint(hexc, f):
    hexc = hexc.lstrip("#")
    r, g, b = (int(hexc[i:i+2], 16) for i in (0, 2, 4))
    r = r + (255 - r) * f
    g = g + (255 - g) * f
    b = b + (255 - b) * f
    return "#%02x%02x%02x" % (int(r), int(g), int(b))

INK   = "#17202A"
INK2  = "#49566B"
MUTED = "#8A97A8"
GRID  = "#E3E8EF"
SURF  = "#FFFFFF"
PANEL = "#F6F8FB"

GREEN = "#1F9D55"   # status: favourable
RED   = "#D62839"   # status: adverse
GREY  = "#9AA7B6"   # status: unchanged

plt.rcParams.update({
    "font.family": "Inter",
    "font.size": 8.5,
    "text.color": INK,
    "axes.labelcolor": INK,
    "axes.edgecolor": "#C7D0DC",
    "xtick.color": INK2,
    "ytick.color": INK2,
    "axes.linewidth": 0.9,
    "xtick.major.width": 0.9,
    "ytick.major.width": 0.9,
    "xtick.major.size": 3,
    "ytick.major.size": 3,
    "savefig.dpi": 600,
    "figure.dpi": 150,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
})

def panel_letter(fig, x, y, letter):
    fig.text(x, y, letter, fontsize=13, fontweight="bold", color=INK,
             ha="left", va="top")

def canvas(ax):
    """Turn an axes into a blank 0-1 drawing canvas."""
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis("off")
    return ax

def card(ax, x, y, w, h, fc, ec=None, r=0.022, lw=1.2, alpha=1.0, z=1):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0,rounding_size={r}",
                       facecolor=fc, edgecolor=ec if ec else "none",
                       linewidth=lw, alpha=alpha, zorder=z,
                       transform=ax.transData, mutation_aspect=1)
    ax.add_patch(p)
    return p

def arrow(ax, p0, p1, color=MUTED, lw=1.6, style="-|>", ms=8, rad=0.0, z=3, ls="-"):
    a = FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms,
                        color=color, linewidth=lw, zorder=z,
                        connectionstyle=f"arc3,rad={rad}",
                        shrinkA=0, shrinkB=0, linestyle=ls,
                        joinstyle="round", capstyle="round")
    ax.add_patch(a)
    return a

def nanoparticle(ax, cx, cy, r, shell, core, n=9, seed=0, lw=1.8, corona=True):
    """Draw a vibrant nanoparticle glyph: corona ring, shell, payload dots."""
    rng = np.random.default_rng(seed)
    if corona:
        ax.add_patch(Circle((cx, cy), r*1.34, facecolor=tint(shell, .86),
                            edgecolor="none", zorder=1))
    ax.add_patch(Circle((cx, cy), r, facecolor=tint(shell, .55),
                        edgecolor=shell, linewidth=lw, zorder=2))
    ang = rng.uniform(0, 2*np.pi, n)
    rad = r*0.68*np.sqrt(rng.uniform(0.02, 1, n))
    ax.scatter(cx + rad*np.cos(ang), cy + rad*np.sin(ang),
               s=r*1300, c=core, edgecolors="white", linewidths=0.6, zorder=3)
    # PEG corona bristles
    if corona:
        th = np.linspace(0, 2*np.pi, 17, endpoint=False)
        for t in th:
            ax.plot([cx + r*np.cos(t), cx + r*1.3*np.cos(t)],
                    [cy + r*np.sin(t), cy + r*1.3*np.sin(t)],
                    color=shell, lw=0.9, alpha=.75, zorder=1,
                    solid_capstyle="round")

def free_drug(ax, cx, cy, r, color, n=9, seed=1, spread=1.25):
    rng = np.random.default_rng(seed)
    ang = rng.uniform(0, 2*np.pi, n)
    rad = r*spread*np.sqrt(rng.uniform(0.05, 1, n))
    ax.scatter(cx + rad*np.cos(ang), cy + rad*np.sin(ang),
               s=r*1300, c=color, edgecolors="white", linewidths=0.6, zorder=3)

def mouse(ax, cx, cy, s, body=tint(MUTED,.55), ec=MUTED, tumor=None, tcolor=ORANGE):
    """Simple side-view mouse glyph; optional flank tumor."""
    ax.add_patch(Ellipse((cx, cy), 2.1*s, 1.25*s, facecolor=body, edgecolor=ec,
                         linewidth=1.1, zorder=2))
    ax.add_patch(Circle((cx + 1.0*s, cy + 0.18*s), 0.44*s, facecolor=body,
                        edgecolor=ec, linewidth=1.1, zorder=3))
    ax.add_patch(Circle((cx + 1.08*s, cy + 0.52*s), 0.17*s, facecolor=body,
                        edgecolor=ec, linewidth=1.0, zorder=3))
    ax.plot([cx - 1.05*s, cx - 1.6*s], [cy - 0.1*s, cy + 0.3*s],
            color=ec, lw=1.1, zorder=2, solid_capstyle="round")
    if tumor:
        ax.add_patch(Circle((cx - 0.70*s, cy - 0.42*s), tumor*s,
                            facecolor=tint(tcolor, .30), edgecolor=tcolor,
                            linewidth=1.3, zorder=4))

def bars(ax, labels, values, colors, errs=None, width=0.62, vfmt="{:,.0f}",
         vsize=8.0, gap_ring=True, label_rot=0, label_size=8.0):
    x = np.arange(len(values))
    for i, (xx, v, c) in enumerate(zip(x, values, colors)):
        ax.add_patch(FancyBboxPatch(
            (xx - width/2, 0), width, v,
            boxstyle="round,pad=0,rounding_size=0.0",
            facecolor=c, edgecolor="white", linewidth=1.6, zorder=2,
            mutation_aspect=1))
    if errs is not None:
        for xx, v, e, c in zip(x, values, errs, colors):
            if e and e > 0:
                ax.errorbar(xx, v, yerr=e, fmt="none", ecolor=INK2,
                            elinewidth=1.1, capsize=3.2, capthick=1.1, zorder=4)
    top = max(v + (errs[i] if errs is not None and errs[i] else 0)
              for i, v in enumerate(values))
    for xx, v, e in zip(x, values, (errs if errs is not None else [0]*len(values))):
        ax.text(xx, v + (e or 0) + top*0.035, vfmt.format(v), ha="center",
                va="bottom", fontsize=vsize, color=INK, fontweight="semibold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=label_size, rotation=label_rot,
                       ha="center" if label_rot == 0 else "right", color=INK)
    ax.set_ylim(0, top*1.22)
    ax.set_xlim(-0.62, len(values) - 0.38)
    ax.yaxis.grid(True, color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.spines["left"].set_color("#C7D0DC")
    ax.spines["bottom"].set_color("#C7D0DC")
    return x

def rounded_cap_bars(ax, *a, **k):
    return bars(ax, *a, **k)

def chip(ax, x, y, w, h, text, fc, tc="white", fs=8.0, weight="semibold", r=0.03, ec=None):
    card(ax, x, y, w, h, fc, ec=ec, r=r, lw=1.2)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center",
            fontsize=fs, color=tc, fontweight=weight, zorder=5)

def save(fig, path):
    # Resolve relative names against this file's directory so the scripts can be
    # run from any working directory without scattering output.
    import os
    path = str(path)
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    fig.savefig(path, dpi=600, facecolor="white", bbox_inches="tight",
                pad_inches=0.06)
    fig.savefig(path.replace(".png", ".pdf"), facecolor="white",
                bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    print("wrote", path)
