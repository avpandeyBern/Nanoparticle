import svgkit as k
from svgkit import *
W,H=1280,726
f=Fig(W,H,bg="#FBFCFE")
def P(x,y,w,h): panel(f,x,y,w,h)
M=22
# ---------------- A : equal carrier mass != equal active dose ----------------
ax,ay,aw,ah=M,M,610,250
P(ax,ay,aw,ah); panel_tag(f,ax+22,ay+34,"A","Equal carrier mass is not equal active dose",title_color=INK)
free_drug(f, ax+120, ay+120, 30, ORANGE, seed=3, n=11, spread=1.5)
np_polymeric(f, ax+300, ay+120, 42, shell=BLUE, core=ORANGE, seed=4)
f.text(ax+210, ay+120, "=", size=34, color=INK, weight=800, anchor="middle")
f.text(ax+120, ay+180, "free compound", size=13, color=INK2, anchor="middle")
f.text(ax+300, ay+180, "loaded carrier", size=13, color=INK2, anchor="middle")
# loading bar
bx,by,bw=ax+400,ay+95,180
f.rrect(bx,by,bw,22, r=8, fill=tint(BLUE,0.7))
f.rrect(bx,by,bw*0.04,22, r=6, fill=ORANGE)
f.text(bx+bw, by-10, "carrier mass  100 mg kg⁻¹", size=12, color=BLUE, weight=700, anchor="end")
f.line(bx+bw*0.04, by+22, bx+bw*0.04, by+44, color=ORANGE, sw=1.6)
f.text(bx+bw*0.04+6, by+52, "active equivalent", size=12, color=ORANGE, weight=700, anchor="start")
f.text(bx+bw*0.04+6, by+70, "2 mg kg⁻¹  (2% loading)", size=11.5, color=MUTED, anchor="start")
# ---------------- B : four estimands ----------------
bx2,by2,bw2,bh2=M+aw+22,M,W-(M+aw+22)-M,250
P(bx2,by2,bw2,bh2); panel_tag(f,bx2+22,by2+34,"B","One contrast, four possible questions",title_color=INK)
rows=[("equal administered dose","delivery gain",BLUE),
      ("lower formulated dose","dose sparing",TEAL),
      ("equal exposure","altered action",VIOLET),
      ("equal tumor control","therapeutic index",PINK)]
yy=by2+70
for lhs,rhs,c in rows:
    chip(f, bx2+24, yy, 200, 32, lhs, c, tsize=12)
    f.arrow(bx2+232, yy+16, bx2+268, yy+16, color=c, sw=3)
    chip(f, bx2+276, yy, 180, 32, rhs, tint(c,0.82), text_color=c, tsize=12, stroke=tint(c,0.5))
    yy+=42
# ---------------- C : causal structure ----------------
cx,cy,cw,ch=M,M+250+18,610,330
P(cx,cy,cw,ch); panel_tag(f,cx+22,cy+34,"C","Formulation acts through two routes; four factors confound both",title_color=INK, tsize=19)
# nodes
def node(nx,ny,txt,col): chip(f,nx-78,ny-22,156,44,txt,col,tsize=13)
nF=(cx+140,cy+110); nE=(cx+cw-150,cy+110); nC=(cx+140,cy+250); nR=(cx+cw-150,cy+250)
f.arrow(nF[0]+80,nF[1], nE[0]-80,nE[1], color=TEAL, sw=3.4)
f.arrow(nF[0],nF[1]+24, nC[0],nC[1]-24, color=VIOLET, sw=3.4)
f.arrow(nE[0],nE[1]+24, nR[0],nR[1]-24, color=PINK, sw=3.4)
f.arrow(nC[0]+80,nC[1], nR[0]-80,nR[1], color=PINK, sw=3.4)
node(*nF,"formulation",BLUE); node(*nE,"tumor exposure",TEAL)
node(*nC,"carrier action",VIOLET); node(*nR,"tumor response",PINK)
# confounder cluster center
ccx,ccy=cx+cw/2, cy+180
f.rrect(ccx-104,ccy-30,208,60, r=14, fill=AMBER_BG, stroke=tint(AMBER,0.45), sw=1.5)
f.text(ccx,ccy-9,"dose · route",size=13,color=shade(AMBER,0.1),weight=700,anchor="middle")
f.text(ccx,ccy+11,"vehicle · schedule",size=13,color=shade(AMBER,0.1),weight=700,anchor="middle")
for tx,ty in [(nF[0]+40,nF[1]+10),(nE[0]-40,nE[1]+10),(nC[0]+40,nC[1]-10),(nR[0]-40,nR[1]-10)]:
    f.arrow(ccx,ccy, tx,ty, color=tint(AMBER,0.2), sw=1.8, head=True, headsize=9)
# ---------------- D : claim ladder ----------------
dx,dy,dw,dh=M+aw+22,M+250+18,W-(M+aw+22)-M,330
P(dx,dy,dw,dh); panel_tag(f,dx+22,dy+34,"D","Claims ranked by evidential burden",title_color=INK)
steps=[("uptake",BLUE),("exposure",TEAL),("efficacy",AMBER),("benefit–harm",PINK)]
base_y=dy+dh-56; maxh=180; bw3=70; gap=(dw-80-bw3*4)/3
for i,(lab,c) in enumerate(steps):
    hgt=70+i*(maxh-70)/3
    xx=dx+40+i*(bw3+gap)
    g=f.lin(tint(c,0.2),c)
    f.rrect(xx,base_y-hgt,bw3,hgt, r=10, fill=f"url(#{g})", stroke="#fff", sw=1.4, shadow=True)
    f.text(xx+bw3/2, base_y-hgt-14, lab, size=12.5, color=c, weight=700, anchor="middle")
    for j in range(i+1):
        f.circle(xx+bw3/2+(j-i/2)*14, base_y-22, 4.5, fill="#fff", opacity=0.9)
f.arrow(dx+34, base_y+16, dx+dw-30, base_y+16, color=MUTED, sw=2.6)
f.text(dx+dw/2, base_y+36, "more independent measurements required", size=12, color=MUTED, italic=True, anchor="middle")
# ---------------- E : fair-comparison checklist strip ----------------
ex,ey,ew,eh=M,M+250+18+330+18,W-2*M,66
f.rrect(ex,ey,ew,eh, r=14, fill="#FFFFFF", stroke=BORDER, sw=1.4, shadow=True)
panel_tag(f,ex+22,ey+22,"E","A fair formulation comparison requires:", title_color=INK, tsize=17)
items=["same active moiety","matched dose","matched route","matched vehicle","matched schedule","established tumor","animal as unit"]
n=len(items); step=(ew-60)/n
for i,it in enumerate(items):
    xx=ex+40+i*step+step/2
    mark_check(f, xx-62, ey+46, 10, GREEN)
    f.text(xx-46, ey+46, it, size=11.5, color=INK2, anchor="start")
open("Figure1.svg","w").write(f.finish()); print("fig1 ok", W, H)
