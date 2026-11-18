import svgkit as k, math
from svgkit import *
W,H=1320,1000
f=Fig(W,H,bg="#FBFCFE")
M=22
def inhibit(f,x1,y1,x2,y2,color,sw=3):
    ang=math.atan2(y2-y1,x2-x1); f.line(x1,y1,x2,y2,color=color,sw=sw)
    bx,by=math.cos(ang+math.pi/2),math.sin(ang+math.pi/2)
    f.line(x2-8*bx,y2-8*by,x2+8*bx,y2+8*by,color=color,sw=sw)

# ============ A : nanocarrier toolbox ============
ax,ay,aw,ah=M,M,628,300
panel(f,ax,ay,aw,ah); panel_tag(f,ax+22,ay+34,"A","The nanocarrier toolbox",title_color=INK)
carriers=[(np_polymeric,"Polymeric\nPLGA · PCL",BLUE,"50–200 nm"),
          (np_liposome,"Liposome",PINK,"80–160 nm"),
          (np_micelle,"Polymeric micelle",VIOLET,"10–60 nm"),
          (np_sln,"SLN / NLC",TEAL,"100–300 nm"),
          (np_droplet,"Nanoemulsion",ORANGE,"10–200 nm"),
          (np_gold,"Metal / theranostic",AMBER,"5–60 nm")]
cols=3; cw=(aw-60)/cols
for i,(fn,lab,col,sz) in enumerate(carriers):
    r=i//cols; cC=i%cols
    cx=ax+40+cC*cw+cw/2; cy=ay+90+r*118
    if fn in (np_gold,np_sln): fn(f,cx,cy,30)
    else: fn(f,cx,cy,30, shell=col)
    for j,ln in enumerate(lab.split("\n")):
        f.text(cx, cy+46+j*15, ln, size=12 if j==0 else 11, color=INK if j==0 else MUTED, weight=700 if j==0 else 400, anchor="middle")

# ============ B : delivery journey & barriers ============
bx,by,bw,bh=M+aw+18,M,W-(M+aw+18)-M,300
panel(f,bx,by,bw,bh); panel_tag(f,bx+22,by+34,"B","From dose to tumor: the barriers in between",title_color=INK)
stages=[("absorption",AMBER),("first pass",ORANGE),("circulation",BLUE),("RES uptake",VIOLET),("extravasation",TEAL)]
sx=bx+40; sy=by+78; sw_=(bw-150)/len(stages); shh=40
for i,(lab,col) in enumerate(stages):
    chip(f, sx+i*sw_, sy, sw_-10, shh, lab, tint(col,0.82), text_color=shade(col,0.15), tsize=11.5, stroke=tint(col,0.5))
chip(f, sx+len(stages)*sw_, sy, 92, shh, "tumor", PINK, tsize=12)
# routes entering at different stages
routes=[("oral",0,AMBER,by+160),("i.v.",2,BLUE,by+200),("intratumoral",5,PINK,by+240)]
for lab,idx,col,ry in routes:
    tx = sx+idx*sw_+ (sw_-10)/2 if idx<5 else sx+len(stages)*sw_+46
    f.circle(bx+46, ry, 7, fill=col, stroke="#fff", sw=1.4)
    f.text(bx+58, ry, lab, size=12, color=col, weight=700, anchor="start")
    f.path(f"M {bx+120} {ry} L {tx} {ry} L {tx} {sy+shh+4}", stroke=col, sw=2.4)
    f.arrow(tx, ry+6, tx, sy+shh+2, color=col, sw=2.4, head=True, headsize=9)
f.text(bx+bw/2, by+bh-22, "EPR is heterogeneous; up to ~97% of uptake is cell-mediated, not paracellular",
       size=11.5, color=MUTED, italic=True, anchor="middle")

# ============ C : phytochemical targets in the prostate cancer cell ============
cx0,cy0,cw0,ch0=M,M+300+18,628,640
panel(f,cx0,cy0,cw0,ch0); panel_tag(f,cx0+22,cy0+34,"C","Molecular targets of natural products in prostate cancer",title_color=INK)
cellcx,cellcy=cx0+cw0/2, cy0+ch0/2+40
f.ellipse(cellcx,cellcy, cw0/2-46, ch0/2-96, fill="#EFF4FB", stroke=tint(BLUE,0.4), sw=2.2, shadow=True)
# membrane receptor (top)
rx,ry=cellcx-120, cy0+160
circ_node(f, rx, ry, 26, "RTK", TEAL, tsize=13)
# small pill node helper
def pnode(px,py,txt,col,w=78,h=36,ts=14): pill(f,px,py,w,h,txt,col,tsize=ts)
pi3k=(cellcx-120, cy0+260); akt=(cellcx-120, cy0+350)
nfkb=(cellcx+10, cy0+210)
pnode(*pi3k,"PI3K",BLUE); pnode(*akt,"AKT",INDIGO); pnode(*nfkb,"NF-κB",ORANGE,88)
# nucleus (lower right)
nuccx,nuccy=cellcx+120, cy0+430
f.ellipse(nuccx,nuccy, 160, 120, fill=tint(VIOLET,0.84), stroke=VIOLET, sw=2.0)
f.text(nuccx+116, nuccy-96, "nucleus", size=12, color=VIOLET, italic=True, anchor="middle")
pill(f, nuccx-28, nuccy-18, 86, 40, "AR", VIOLET2, tsize=18)
pill(f, nuccx+66, nuccy+36, 118, 34, "proliferation", PINK, tsize=12)
dht=(nuccx-28, nuccy-96); pnode(*dht,"DHT",AMBER,70,30,13)
# cascades
f.arrow(rx, ry+26, pi3k[0], pi3k[1]-20, color=TEAL, sw=3)
f.arrow(pi3k[0], pi3k[1]+20, akt[0], akt[1]-20, color=BLUE, sw=3)
f.arrow(akt[0]+42, akt[1]-4, nuccx-72, nuccy-16, color=INDIGO, sw=2.8, curve=24)
f.arrow(nfkb[0], nfkb[1]+20, nuccx-6, nuccy-40, color=ORANGE, sw=2.8, curve=-26)
f.arrow(dht[0], dht[1]+16, nuccx-28, nuccy-40, color=AMBER, sw=2.8)
f.arrow(nuccx+16, nuccy-10, nuccx+36, nuccy+18, color=VIOLET, sw=2.6)
# phytochemical inhibition chips (local, non-crossing)
def phychip(px,py,lab,col,tgt,anchor_side):
    chip(f, px-48, py-15, 96, 30, lab, col, tsize=12)
    sx = px+48 if anchor_side=="r" else px-48
    inhibit(f, sx, py, tgt[0], tgt[1], shade(col,0.05), sw=2.4)
phychip(cx0+78, cy0+210, "curcumin", ORANGE, nfkb, "r")
phychip(cx0+78, cy0+350, "resveratrol", TEAL, akt, "r")
phychip(cx0+78, cy0+470, "quercetin", VIOLET, pi3k, "r")
phychip(cx0+cw0-84, cy0+430-18, "EGCG", BLUE, (nuccx-28,nuccy-18), "l")
phychip(cx0+cw0-84, cy0+520, "apigenin", PINK, (nuccx-28,nuccy-18), "l")
phychip(cx0+cw0-84, cy0+600-30, "genistein", GREEN, (nuccx+66,nuccy+36), "l")
f.text(cellcx, cy0+ch0-16, "bar-ended lines denote inhibition", size=11, color=MUTED, italic=True, anchor="middle")

# ============ D : steroidogenesis in the standard steroid scheme ============
dx,dy,dw,dh=M+628+18,M+300+18,W-(M+628+18)-M,640
panel(f,dx,dy,dw,dh); panel_tag(f,dx+22,dy+34,"D","Androgen synthesis and the steroidogenic intervention point",title_color=INK)
scx=dx+150                       # skeleton center x
names=["Cholesterol","Pregnenolone","DHEA","Androstenedione","Testosterone"]
decos=[None,None,"O","O","OH"]
ys=[dy+108,dy+214,dy+320,dy+426,dy+532]
enzymes=[("CYP11A1",TEAL),("CYP17A1",PINK),("3β-HSD",TEAL),("17β-HSD",TEAL)]
for i,(nm,yy,deco) in enumerate(zip(names,ys,decos)):
    p=steroid(f, scx, yy, a=14)
    if deco=="OH": f.text(p['c17'][0]+5,p['c17'][1]-6,"OH",size=10,color=RED,weight=700,anchor="start")
    if deco=="O": f.text(p['c3'][0]-7,p['c3'][1],"O",size=10.5,color=RED,weight=700,anchor="end")
    if i==4:
        f.text(scx, yy+44, nm, size=12, color=INK, weight=700, anchor="middle")
    else:
        f.text(scx+64, yy-4, nm, size=12, color=INK, weight=600, anchor="start")
    if i<4:
        y2=ys[i+1]; f.arrow(scx, yy+22, scx, y2-48, color=shade(AMBER,0.08), sw=2.8)
        en,ec=enzymes[i]; chip(f, scx-56, (yy+22+y2-48)/2-12, 104, 24, en, ec, tsize=10.5)
# DHT branch from testosterone
p=steroid(f, scx+210, ys[4], a=14); f.text(p['c17'][0]+5,p['c17'][1]-6,"OH",size=10,color=RED,weight=700,anchor="start")
f.text(scx+210, ys[4]+44, "DHT → AR", size=12, color=INK, weight=700, anchor="middle")
f.arrow(scx+64, ys[4], scx+176, ys[4], color=shade(AMBER,0.08), sw=2.8)
chip(f, scx+74, ys[4]-13, 96, 24, "5α-reductase", VIOLET, tsize=10)
# intervention callout on CYP17A1
icx,icy=dx+dw-140, dy+214
f.rrect(icx-16, icy-56, 150, 118, r=12, fill=PINK_BG, stroke=tint(PINK,0.45), sw=1.5)
f.text(icx+59, icy-36, "Intervention", size=12.5, color=PINK, weight=700, anchor="middle")
f.textblock(icx-6, icy-14, ["curcumin–piperine","nanoparticles modulate","CYP17A1 / CYP21A2","and steroid output"], size=10.3, color=INK2, lh=1.32)
inhibit(f, icx-16, icy, scx+52, (ys[1]+22+ys[2]-48)/2, PINK, sw=2.6)
f.text(dx+dw/2, dy+dh-16, "abiraterone validates CYP17A1 as a clinical target", size=11, color=MUTED, italic=True, anchor="middle")
open("Figure2.svg","w").write(f.finish()); print("fig2 ok")
