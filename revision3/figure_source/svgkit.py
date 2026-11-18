# -*- coding: utf-8 -*-
"""SVG toolkit for publication-grade molecular/biology figures (Cell / Nat Commun style).
Canvas units are arbitrary; render width sets final pixels (vector, crisp at any size)."""
import math, html

FONT = "Inter, 'Liberation Sans', Arial, sans-serif"

# ---- palette ------------------------------------------------------------
INK   = "#1A2230"; INK2 = "#51607A"; MUTED = "#8B97A8"
BORDER= "#DBE2EC"; GRID = "#E7ECF3"
TEAL="#0E9594"; TEAL2="#13B3A6"; TEAL_BG="#E4F5F2"
BLUE="#2E6FD6"; BLUE2="#4C8DF0"; BLUE_BG="#E8F0FC"
VIOLET="#7C4DD1"; VIOLET2="#9B6BE8"; VIOLET_BG="#F0E9FB"
PINK="#D6457E"; PINK2="#EC6AA0"; PINK_BG="#FBE7F0"
AMBER="#E08521"; AMBER2="#F2A33D"; AMBER_BG="#FCF0DC"
GREEN="#2E9E5B"; GREEN2="#46BC76"; GREEN_BG="#E4F4EA"
RED="#D64545"; RED2="#E96A6A"; RED_BG="#FBE7E7"
GREY="#8A97A8"; GREY2="#AAB4C2"; GREY_BG="#EEF1F6"
ORANGE="#E8622A"; ORANGE2="#F2824F"; ORANGE_BG="#FCE8DE"
INDIGO="#3F4FB0"; INDIGO_BG="#E8EAF7"

def tint(hexc, f):
    hexc=hexc.lstrip('#'); r,g,b=(int(hexc[i:i+2],16) for i in (0,2,4))
    r=int(r+(255-r)*f); g=int(g+(255-g)*f); b=int(b+(255-b)*f)
    return f"#{r:02x}{g:02x}{b:02x}"
def shade(hexc, f):  # darken
    hexc=hexc.lstrip('#'); r,g,b=(int(hexc[i:i+2],16) for i in (0,2,4))
    r=int(r*(1-f)); g=int(g*(1-f)); b=int(b*(1-f))
    return f"#{r:02x}{g:02x}{b:02x}"
def esc(s): return html.escape(str(s), quote=True)

class Fig:
    def __init__(self, w, h, bg="#FFFFFF"):
        self.w=w; self.h=h; self.defs=[]; self.body=[]; self._ids=0; self._reg={}
        if bg: self.body.append(f'<rect x="0" y="0" width="{w}" height="{h}" fill="{bg}"/>')
    def uid(self, p="g"):
        self._ids+=1; return f"{p}{self._ids}"
    # gradients (cached by key)
    def lin(self, c0, c1, vertical=True):
        key=("lin",c0,c1,vertical)
        if key in self._reg: return self._reg[key]
        i=self.uid("lg"); x2,y2=(0,1) if vertical else (1,0)
        self.defs.append(f'<linearGradient id="{i}" x1="0" y1="0" x2="{x2}" y2="{y2}">'
                         f'<stop offset="0" stop-color="{c0}"/><stop offset="1" stop-color="{c1}"/></linearGradient>')
        self._reg[key]=i; return i
    def rad(self, c0, c1, cx=0.38, cy=0.34):
        key=("rad",c0,c1,cx,cy)
        if key in self._reg: return self._reg[key]
        i=self.uid("rg")
        self.defs.append(f'<radialGradient id="{i}" cx="{cx}" cy="{cy}" r="0.72">'
                         f'<stop offset="0" stop-color="{c0}"/><stop offset="1" stop-color="{c1}"/></radialGradient>')
        self._reg[key]=i; return i
    def shadow(self, dy=1.3, blur=2.6, op=0.22):
        key=("sh",dy,blur,op)
        if key in self._reg: return self._reg[key]
        i=self.uid("sh")
        self.defs.append(f'<filter id="{i}" x="-30%" y="-30%" width="160%" height="160%">'
                         f'<feDropShadow dx="0" dy="{dy}" stdDeviation="{blur}" flood-color="#1A2230" flood-opacity="{op}"/></filter>')
        self._reg[key]=i; return i
    def soft(self, blur=3):
        key=("blur",blur)
        if key in self._reg: return self._reg[key]
        i=self.uid("bl")
        self.defs.append(f'<filter id="{i}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{blur}"/></filter>')
        self._reg[key]=i; return i
    def add(self, s): self.body.append(s); return self
    # ---------- text ----------
    def text(self, x, y, s, size=13, color=INK, weight=400, anchor="start",
             italic=False, spacing=None, family=FONT, opacity=None):
        sty=f'font-family:{family};font-size:{size}px;font-weight:{weight};fill:{color}'
        if italic: sty+=';font-style:italic'
        if spacing is not None: sty+=f';letter-spacing:{spacing}px'
        if opacity is not None: sty+=f';opacity:{opacity}'
        self.body.append(f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}" '
                         f'dominant-baseline="middle" style="{sty}">{esc(s)}</text>')
        return self
    def textblock(self, x, y, lines, size=12, color=INK2, weight=400, lh=1.32, anchor="start", **kw):
        for i,ln in enumerate(lines):
            self.text(x, y+i*size*lh, ln, size=size, color=color, weight=weight, anchor=anchor, **kw)
        return self
    # ---------- shapes ----------
    def rrect(self, x, y, w, h, r=12, fill="#fff", stroke=None, sw=1.4, shadow=False, dash=None, opacity=None):
        extra=""
        if shadow: extra+=f' filter="url(#{self.shadow()})"'
        if stroke: extra+=f' stroke="{stroke}" stroke-width="{sw}"'
        if dash: extra+=f' stroke-dasharray="{dash}"'
        if opacity is not None: extra+=f' opacity="{opacity}"'
        self.body.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{r}" ry="{r}" fill="{fill}"{extra}/>')
        return self
    def circle(self, cx, cy, r, fill="#fff", stroke=None, sw=1.4, shadow=False, opacity=None):
        extra=""
        if shadow: extra+=f' filter="url(#{self.shadow()})"'
        if stroke: extra+=f' stroke="{stroke}" stroke-width="{sw}"'
        if opacity is not None: extra+=f' opacity="{opacity}"'
        self.body.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{fill}"{extra}/>')
        return self
    def ellipse(self, cx, cy, rx, ry, fill="#fff", stroke=None, sw=1.4, shadow=False, rot=0, opacity=None):
        extra=""
        if shadow: extra+=f' filter="url(#{self.shadow()})"'
        if stroke: extra+=f' stroke="{stroke}" stroke-width="{sw}"'
        if opacity is not None: extra+=f' opacity="{opacity}"'
        tr=f' transform="rotate({rot} {cx:.2f} {cy:.2f})"' if rot else ""
        self.body.append(f'<ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="{rx:.2f}" ry="{ry:.2f}" fill="{fill}"{extra}{tr}/>')
        return self
    def path(self, d, fill="none", stroke=None, sw=1.6, dash=None, cap="round", join="round", opacity=None, shadow=False):
        extra=""
        if stroke: extra+=f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}" stroke-linejoin="{join}"'
        if dash: extra+=f' stroke-dasharray="{dash}"'
        if opacity is not None: extra+=f' opacity="{opacity}"'
        if shadow: extra+=f' filter="url(#{self.shadow()})"'
        self.body.append(f'<path d="{d}" fill="{fill}"{extra}/>')
        return self
    def line(self, x1,y1,x2,y2, color=INK2, sw=1.6, dash=None, cap="round", opacity=None):
        extra=f' stroke-dasharray="{dash}"' if dash else ""
        if opacity is not None: extra+=f' opacity="{opacity}"'
        self.body.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{color}" stroke-width="{sw}" stroke-linecap="{cap}"{extra}/>')
        return self
    def poly(self, pts, fill="#fff", stroke=None, sw=1.4, closed=True, opacity=None):
        p=" ".join(f"{x:.2f},{y:.2f}" for x,y in pts)
        extra=""
        if stroke: extra+=f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"'
        if opacity is not None: extra+=f' opacity="{opacity}"'
        tag="polygon" if closed else "polyline"
        if not closed and fill=="#fff": fill="none"
        self.body.append(f'<{tag} points="{p}" fill="{fill}"{extra}/>')
        return self
    # ---------- composite: arrow ----------
    def arrow(self, x1,y1,x2,y2, color=INK2, sw=3.0, dash=None, curve=0.0, head=True, headsize=None, double=False, opacity=None):
        hs = headsize if headsize else max(7, sw*2.6)
        # shorten end for head
        ang=math.atan2(y2-y1, x2-x1)
        ex,ey=x2,y2
        if head:
            ex=x2-hs*0.86*math.cos(ang); ey=y2-hs*0.86*math.sin(ang)
        sx,sy=x1,y1
        if double:
            sx=x1+hs*0.86*math.cos(ang); sy=y1+hs*0.86*math.sin(ang)
        if abs(curve)<1e-6:
            d=f"M {sx:.2f} {sy:.2f} L {ex:.2f} {ey:.2f}"
        else:
            mx,my=(sx+ex)/2,(sy+ey)/2
            nx,ny=-(ey-sy),(ex-sx); nlen=math.hypot(nx,ny) or 1
            cx,cy=mx+nx/nlen*curve, my+ny/nlen*curve
            d=f"M {sx:.2f} {sy:.2f} Q {cx:.2f} {cy:.2f} {ex:.2f} {ey:.2f}"
        op=f' opacity="{opacity}"' if opacity is not None else ""
        extra=f' stroke-dasharray="{dash}"' if dash else ""
        self.body.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"{extra}{op}/>')
        def headtri(px,py,a):
            b=hs*0.62
            p1=(px,py)
            p2=(px-hs*math.cos(a)+b*math.cos(a+math.pi/2), py-hs*math.sin(a)+b*math.sin(a+math.pi/2))
            p3=(px-hs*math.cos(a)-b*math.cos(a+math.pi/2), py-hs*math.sin(a)-b*math.sin(a+math.pi/2))
            self.poly([p1,p2,p3], fill=color, opacity=opacity)
        if head: headtri(x2,y2,ang)
        if double: headtri(x1,y1,ang+math.pi)
        return self
    def finish(self, title=None):
        defs=f'<defs>{"".join(self.defs)}</defs>' if self.defs else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}">{defs}{"".join(self.body)}</svg>')

# ======================================================================
# higher-level components
# ======================================================================
def panel(f, x, y, w, h, fill="#FFFFFF", stroke=BORDER, r=14, shadow=True):
    f.rrect(x,y,w,h, r=r, fill=fill, stroke=stroke, sw=1.4, shadow=shadow)

def panel_tag(f, x, y, letter, title=None, color=INK, tsize=19, title_color=None):
    """Panel letter + optional short header, examples style."""
    f.text(x, y, letter, size=tsize, color=color, weight=800, anchor="start")
    if title:
        f.text(x+tsize*1.05, y, title, size=tsize*0.82, color=title_color or INK, weight=700, anchor="start")

def subbox(f, x, y, w, h, title, accent, body_bg=None, r=12):
    """Pastel sub-panel with a colored header strip and title (like 'Microsomal CYP450 system')."""
    bg = body_bg if body_bg else tint(accent, 0.9)
    f.rrect(x,y,w,h, r=r, fill=bg, stroke=tint(accent,0.45), sw=1.5)
    f.rrect(x,y,w,26, r=r, fill=accent)
    f.rrect(x,y+13,w,13, r=0, fill=accent)  # square off bottom of header
    f.text(x+w/2, y+13, title, size=12.5, color="#fff", weight=700, anchor="middle")
    return (x, y+26, w, h-26)  # inner content region

def pill(f, cx, cy, w, h, text, base, text_color="#fff", tsize=None, bold=True, stroke=None):
    g=f.rad(tint(base,0.35), base)
    f.rrect(cx-w/2, cy-h/2, w, h, r=h/2, fill=f"url(#{g})", stroke=stroke or shade(base,0.12), sw=1.3, shadow=True)
    # glossy highlight
    f.ellipse(cx, cy-h*0.22, w*0.40, h*0.20, fill="#ffffff", opacity=0.22)
    f.text(cx, cy, text, size=tsize or h*0.46, color=text_color, weight=700 if bold else 500, anchor="middle")

def chip(f, x, y, w, h, text, fill, text_color="#fff", r=None, tsize=12.5, weight=700, stroke=None, anchor="middle", shadow=False):
    r = h/2 if r is None else r
    f.rrect(x,y,w,h, r=r, fill=fill, stroke=stroke, sw=1.3, shadow=shadow)
    tx = x+w/2 if anchor=="middle" else x+10
    f.text(tx, y+h/2, text, size=tsize, color=text_color, weight=weight, anchor=anchor)

def circ_node(f, cx, cy, r, text, base, text_color="#fff", tsize=None, outline=True):
    g=f.rad(tint(base,0.4), base)
    f.circle(cx,cy,r, fill=f"url(#{g})", stroke=shade(base,0.12) if outline else None, sw=1.4, shadow=True)
    f.ellipse(cx, cy-r*0.34, r*0.5, r*0.28, fill="#fff", opacity=0.25)
    if text: f.text(cx,cy,text, size=tsize or r*0.8, color=text_color, weight=700, anchor="middle")

# ---- membrane (phospholipid bilayer) ----
def membrane(f, x, y, w, head_color="#9FB6E6", tail_color="#C4CFE4", hr=7.2, th=30, n=None):
    """Horizontal bilayer centered vertically on y, thickness th."""
    sp=hr*2.15
    n = n or int(w/sp)
    y_top_head=y-th/2+hr; y_bot_head=y+th/2-hr
    for i in range(n):
        px=x+hr+ i*sp + (w-n*sp)/2
        # tails
        f.line(px, y_top_head+hr*0.5, px, y-1.5, color=tail_color, sw=2.0)
        f.line(px+2.2, y_top_head+hr*0.5, px+2.2, y-1.5, color=tail_color, sw=2.0)
        f.line(px, y_bot_head-hr*0.5, px, y+1.5, color=tail_color, sw=2.0)
        f.line(px+2.2, y_bot_head-hr*0.5, px+2.2, y+1.5, color=tail_color, sw=2.0)
    for i in range(n):
        px=x+hr+ i*sp + (w-n*sp)/2
        f.circle(px+1.1, y_top_head, hr, fill=head_color, stroke=shade(head_color,0.18), sw=1.0)
        f.circle(px+1.1, y_bot_head, hr, fill=head_color, stroke=shade(head_color,0.18), sw=1.0)

# ---- nanoparticle variants ----
import random
def _seed(s): return random.Random(s)

def np_polymeric(f, cx, cy, r, shell=BLUE, core=ORANGE, seed=1, corona=True, payload=9):
    rng=_seed(seed)
    if corona:
        for a in [i*2*math.pi/20 for i in range(20)]:
            f.line(cx+r*math.cos(a), cy+r*math.sin(a), cx+r*1.26*math.cos(a), cy+r*1.26*math.sin(a),
                   color=tint(shell,0.35), sw=max(1.2,r*0.05))
    g=f.rad(tint(shell,0.5), shell)
    f.circle(cx,cy,r, fill=f"url(#{g})", stroke=shade(shell,0.12), sw=max(1.4,r*0.06), shadow=True)
    for _ in range(payload):
        a=rng.uniform(0,2*math.pi); rr=r*0.66*math.sqrt(rng.uniform(0.02,1))
        f.circle(cx+rr*math.cos(a), cy+rr*math.sin(a), r*0.14, fill=core, stroke="#fff", sw=max(0.6,r*0.02))

def np_liposome(f, cx, cy, r, shell=PINK, core=AMBER, seed=2, payload=7):
    rng=_seed(seed)
    g=f.rad(tint(shell,0.75), tint(shell,0.5))
    f.circle(cx,cy,r, fill=f"url(#{g})", stroke=shade(shell,0.08), sw=max(2.2,r*0.1), shadow=True)
    f.circle(cx,cy,r*0.82, fill="#ffffff", opacity=0.55)
    f.circle(cx,cy,r*0.82, fill="none", stroke=tint(shell,0.3), sw=max(1.6,r*0.07))
    for _ in range(payload):
        a=rng.uniform(0,2*math.pi); rr=r*0.6*math.sqrt(rng.uniform(0.02,1))
        f.circle(cx+rr*math.cos(a), cy+rr*math.sin(a), r*0.13, fill=core, stroke="#fff", sw=0.6)

def np_micelle(f, cx, cy, r, shell=VIOLET, core=AMBER, seed=3, n=18):
    g=f.rad(tint(core,0.4), core)
    f.circle(cx,cy,r*0.5, fill=f"url(#{g})")
    for i in range(n):
        a=i*2*math.pi/n
        f.line(cx+r*0.48*math.cos(a), cy+r*0.48*math.sin(a), cx+r*math.cos(a), cy+r*math.sin(a),
               color=tint(shell,0.2), sw=max(1.6,r*0.08))
        f.circle(cx+r*math.cos(a), cy+r*math.sin(a), r*0.12, fill=shell, stroke="#fff", sw=0.5)

def np_sln(f, cx, cy, r, shell=TEAL, core=None, seed=4):
    g=f.rad(tint(shell,0.55), shade(shell,0.05))
    f.circle(cx,cy,r, fill=f"url(#{g})", stroke=shade(shell,0.15), sw=max(1.4,r*0.06), shadow=True)
    # crystalline lattice hint
    for dx in (-0.4,0,0.4):
        f.line(cx+dx*r, cy-0.7*r, cx+dx*r, cy+0.7*r, color="#ffffff", sw=1.2, opacity=0.35)
    for dy in (-0.4,0,0.4):
        f.line(cx-0.7*r, cy+dy*r, cx+0.7*r, cy+dy*r, color="#ffffff", sw=1.2, opacity=0.35)

def np_gold(f, cx, cy, r, seed=5):
    g=f.rad("#FFE9A8", "#C9941E")
    f.circle(cx,cy,r, fill=f"url(#{g})", stroke="#9A6E12", sw=max(1.4,r*0.06), shadow=True)
    f.ellipse(cx-r*0.25,cy-r*0.3, r*0.3,r*0.18, fill="#fff", opacity=0.5)

def np_droplet(f, cx, cy, r, shell=ORANGE, core=AMBER, seed=6):
    g=f.rad(tint(shell,0.5), shell)
    f.circle(cx,cy,r, fill=f"url(#{g})", stroke=shade(shell,0.12), sw=max(1.4,r*0.06), shadow=True)
    f.ellipse(cx-r*0.28,cy-r*0.32, r*0.34,r*0.2, fill="#fff", opacity=0.45)

def free_drug(f, cx, cy, r, color=ORANGE, seed=7, n=9, spread=1.3):
    rng=_seed(seed)
    for _ in range(n):
        a=rng.uniform(0,2*math.pi); rr=r*spread*math.sqrt(rng.uniform(0.05,1))
        f.circle(cx+rr*math.cos(a), cy+rr*math.sin(a), r*0.3, fill=color, stroke="#fff", sw=0.6)

# ---- cell & tumor ----
def cell(f, cx, cy, r, fill="#E8F0FC", stroke=BLUE, nuc=VIOLET):
    f.circle(cx,cy,r, fill=fill, stroke=stroke, sw=1.6, shadow=True)
    f.circle(cx+r*0.12, cy+r*0.05, r*0.42, fill=tint(nuc,0.55), stroke=nuc, sw=1.3)

def tumor_mass(f, cx, cy, r, color=PINK, seed=11, lobes=11):
    rng=_seed(seed)
    pts=[]
    for i in range(lobes*2):
        a=i*math.pi/lobes
        rad=r*(0.86 if i%2 else 1.0)*rng.uniform(0.94,1.08)
        pts.append((cx+rad*math.cos(a), cy+rad*math.sin(a)))
    # smooth-ish blob via polygon
    g=f.rad(tint(color,0.45), color)
    d="M "+" L ".join(f"{x:.1f} {y:.1f}" for x,y in pts)+" Z"
    f.path(d, fill=f"url(#{g})", stroke=shade(color,0.1), sw=1.6, shadow=True)
    # cell nuclei texture
    for _ in range(int(lobes*2.2)):
        a=rng.uniform(0,2*math.pi); rr=r*0.7*math.sqrt(rng.uniform(0,1))
        f.circle(cx+rr*math.cos(a), cy+rr*math.sin(a), r*0.07, fill="#fff", opacity=0.5)

def mouse(f, cx, cy, s, body="#E7ECF3", stroke="#9AA6B6", tumor=None, tumor_color=PINK):
    f.ellipse(cx, cy, 2.1*s, 1.2*s, fill=body, stroke=stroke, sw=1.6, shadow=True)
    f.circle(cx+1.55*s, cy-0.12*s, 0.72*s, fill=body, stroke=stroke, sw=1.5)
    f.circle(cx+2.0*s, cy-0.52*s, 0.26*s, fill=body, stroke=stroke, sw=1.3)  # ear
    f.circle(cx+2.08*s, cy-0.05*s, 0.08*s, fill=INK)  # eye
    f.path(f"M {cx-2.0*s:.1f} {cy+0.1*s:.1f} q {-0.9*s:.1f} {-0.1*s:.1f} {-1.0*s:.1f} {0.7*s:.1f}",
           stroke=stroke, sw=1.5)  # tail
    if tumor:
        f.circle(cx-0.95*s, cy+0.75*s, tumor*s, fill=tint(tumor_color,0.35), stroke=tumor_color, sw=1.6)

# ---- bar chart ----
def bars(f, x, y, w, h, values, labels, colors, ymax=None, ylab=None,
         value_fmt="{:,.0f}", vsize=12.5, lab_size=12, grid_n=4, bar_frac=0.62,
         err=None, baseline_label=None):
    ymax = ymax or max(values)*1.18
    n=len(values); slot=w/n; bw=slot*bar_frac
    # gridlines
    for i in range(grid_n+1):
        gy=y+h - h*i/grid_n
        f.line(x, gy, x+w, gy, color=GRID, sw=1.2)
    # axis
    f.line(x, y, x, y+h, color="#C7D0DC", sw=1.4)
    f.line(x, y+h, x+w, y+h, color="#C7D0DC", sw=1.4)
    for i,(v,lb,c) in enumerate(zip(values,labels,colors)):
        bx=x+slot*i+(slot-bw)/2
        bh=h*v/ymax
        g=f.lin(tint(c,0.18), c)
        f.rrect(bx, y+h-bh, bw, bh, r=min(6,bw*0.16), fill=f"url(#{g})", stroke="#ffffff", sw=1.4)
        f.rrect(bx, y+h-bh, bw, min(bh,10), r=min(6,bw*0.16), fill="#ffffff", opacity=0.18)
        ev=err[i] if err else 0
        if ev:
            ey=y+h-bh; f.line(bx+bw/2, ey-h*ev/ymax, bx+bw/2, ey+h*ev/ymax, color=INK2, sw=1.6)
            f.line(bx+bw*0.3, ey-h*ev/ymax, bx+bw*0.7, ey-h*ev/ymax, color=INK2, sw=1.6)
            f.line(bx+bw*0.3, ey+h*ev/ymax, bx+bw*0.7, ey+h*ev/ymax, color=INK2, sw=1.6)
        if value_fmt:
            f.text(bx+bw/2, y+h-bh-(h*ev/ymax)-vsize*0.8, value_fmt.format(v), size=vsize, color=INK, weight=700, anchor="middle")
        for j,line in enumerate(str(lb).split("\n")):
            f.text(bx+bw/2, y+h+lab_size*1.1*(j+1), line, size=lab_size, color=INK2, anchor="middle")
    if ylab:
        f.body.append(f'<text x="{x-vsize*2.6:.1f}" y="{y+h/2:.1f}" text-anchor="middle" '
                      f'transform="rotate(-90 {x-vsize*2.6:.1f} {y+h/2:.1f})" '
                      f'style="font-family:{FONT};font-size:{lab_size}px;font-weight:600;fill:{INK2}">{esc(ylab)}</text>')
    return ymax

def legend_key(f, x, y, items, box_w=None, title=None, sw_r=7, gap=22, cols=1, tsize=12):
    """items: list of (color, label). Simple key row/box."""
    if title:
        f.text(x, y, title, size=tsize+0.5, color=INK, weight=700); y+=gap
    for i,(c,lab) in enumerate(items):
        yy=y+(i//cols)*gap; xx=x+(i%cols)*(box_w or 150)
        f.circle(xx+sw_r, yy, sw_r, fill=tint(c,0.45), stroke=c, sw=1.5)
        f.text(xx+sw_r*2+6, yy, lab, size=tsize, color=INK2, anchor="start")

# ---- steroid nucleus (cyclopentanoperhydrophenanthrene, standard orientation) ----
def steroid(f, cx, cy, a=22, color="#2C3440", sw=None, fill="#FFFFFF", scale=1.0):
    """Steran skeleton: rings A,B,C (cyclohexane) + D (cyclopentane), textbook staircase.
    (cx,cy) ~ center of ring A. a = bond length. Returns attachment dict."""
    import math as _m
    a*=scale; sw = sw or 2.3*scale
    def hexc(ctr):
        px,py=ctr; return [(px+a*_m.cos(_m.radians(60*k+30)), py-a*_m.sin(_m.radians(60*k+30))) for k in range(6)]
    A=(cx,cy)
    B=(cx+a*_m.sqrt(3)*_m.cos(_m.radians(60)), cy-a*_m.sqrt(3)*_m.sin(_m.radians(60)))
    C=(B[0]+a*_m.sqrt(3)*_m.cos(_m.radians(-60)), B[1]-a*_m.sqrt(3)*_m.sin(_m.radians(-60)))
    Ah,Bh,Ch=hexc(A),hexc(B),hexc(C)
    # pentagon D shares ring C upper-right edge (C vertices index 0 at 30deg, index 5 at -30 -> use 0 and 1)
    p=Ch[0]; q=Ch[1]  # an edge of C (30deg and 90deg vertices)
    # regular pentagon on edge p-q, outward
    ex,ey=q[0]-p[0], q[1]-p[1]; L=_m.hypot(ex,ey); ux,uy=ex/L,ey/L
    nx,ny=uy,-ux  # outward normal (points away from C center)
    # ensure normal points away from C
    midx,midy=(p[0]+q[0])/2,(p[1]+q[1])/2
    if (midx-C[0])*nx+(midy-C[1])*ny < 0: nx,ny=-nx,-ny
    R=L/(2*_m.sin(_m.pi/5))  # circumradius
    pcx=midx+ny*0 ; # pentagon center along normal from edge midpoint
    apo=L/(2*_m.tan(_m.pi/5))
    pcx=midx+nx*apo; pcy=midy+ny*apo
    ang0=_m.atan2(p[1]-pcy, p[0]-pcx)
    D=[(pcx+R*_m.cos(ang0+2*_m.pi*k/5), pcy+R*_m.sin(ang0+2*_m.pi*k/5)) for k in range(5)]
    for ring in (Ah,Bh,Ch):
        d="M "+" L ".join(f"{px:.1f} {py:.1f}" for px,py in ring)+" Z"
        f.path(d, fill=fill, stroke=color, sw=sw)
    dD="M "+" L ".join(f"{px:.1f} {py:.1f}" for px,py in D)+" Z"
    f.path(dD, fill=fill, stroke=color, sw=sw)
    return dict(A=Ah,B=Bh,C=Ch,D=D,
                c3=(Ah[3][0], Ah[3][1]),          # lower-left (A ring, 3-position region)
                c17=(D[2][0], D[2][1]),            # upper-right tip (D ring, 17-position)
                top=(B[0], B[1]-a))

def mark_check(f, cx, cy, r, color=GREEN):
    f.circle(cx,cy,r, fill=tint(color,0.74), stroke=color, sw=1.6)
    f.path(f"M {cx-r*0.42:.1f} {cy+0.02*r:.1f} L {cx-r*0.08:.1f} {cy+r*0.38:.1f} L {cx+r*0.5:.1f} {cy-r*0.4:.1f}",
           stroke=color, sw=max(2.2,r*0.26))
def mark_cross(f, cx, cy, r, color=RED):
    f.circle(cx,cy,r, fill=tint(color,0.74), stroke=color, sw=1.6)
    f.line(cx-r*0.4,cy-r*0.4, cx+r*0.4,cy+r*0.4, color=color, sw=max(2.2,r*0.26))
    f.line(cx-r*0.4,cy+r*0.4, cx+r*0.4,cy-r*0.4, color=color, sw=max(2.2,r*0.26))
def mark_dot(f, cx, cy, r, color=AMBER):
    f.circle(cx,cy,r, fill=tint(color,0.74), stroke=color, sw=1.6)
    f.circle(cx,cy,r*0.3, fill=color)

def heat_grid(f, x, y, cw, ch, M, rows, cols, cmap, rowlab_w=140, collab_h=46, lab_size=12):
    """M: 2D list of state codes; cmap: dict code->(mark_fn,color). Marks drawn in each cell."""
    nr=len(M); nc=len(M[0])
    for j,c in enumerate(cols):
        for line_i,line in enumerate(str(c).split("\n")):
            f.text(x+rowlab_w+cw*j+cw/2, y+collab_h-collab_h+12+line_i*13, line, size=lab_size, color=INK2, anchor="middle")
    for i,r in enumerate(rows):
        f.text(x+rowlab_w-8, y+collab_h+ch*i+ch/2, r, size=lab_size+0.5, color=INK, anchor="end", weight=600)
        for j in range(nc):
            code=M[i][j]; fn,col=cmap[code]
            cellx=x+rowlab_w+cw*j; celly=y+collab_h+ch*i
            f.rrect(cellx+3, celly+3, cw-6, ch-6, r=9, fill=tint(col,0.78), stroke=tint(col,0.4), sw=1.3)
            fn(f, cellx+cw/2, celly+ch/2, min(cw,ch)*0.26, color=col)

def dot_forest(f, x, y, w, h, groups, xmin, xmax, xticks, ref=1.0, xlab=None, logscale=False):
    """groups: list of (label,color,[values]). Dots on a shared axis with a reference line."""
    import math as _m
    def X(v):
        if logscale:
            return x+w*(_m.log(v)-_m.log(xmin))/(_m.log(xmax)-_m.log(xmin))
        return x+w*(v-xmin)/(xmax-xmin)
    n=len(groups); rh=h/n
    for t in xticks:
        gx=X(t); f.line(gx, y, gx, y+h, color=GRID, sw=1.2)
        f.text(gx, y+h+16, (f"{t:g}"), size=11.5, color=INK2, anchor="middle")
    f.line(X(ref), y, X(ref), y+h, color=INK2, sw=1.5, dash="6 5")
    for i,(lab,col,vals) in enumerate(groups):
        cy=y+rh*i+rh/2
        f.text(x-12, cy, lab, size=13, color=INK, anchor="end", weight=600)
        for v in vals:
            f.circle(X(v), cy, 8, fill=tint(col,0.3), stroke=col, sw=2.0)
    f.line(x, y+h, x+w, y+h, color="#C7D0DC", sw=1.4)
    if xlab: f.text(x+w/2, y+h+40, xlab, size=12.5, color=INK2, anchor="middle", weight=600)
