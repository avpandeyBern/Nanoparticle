import svgkit as k
from svgkit import *
W,H=1280,730
f=Fig(W,H,bg="#FBFCFE")
M=22; GREYB="#9AA6B6"
# A : Ma i.v. liposomes, baseline vs endpoint
ax,ay,aw,ah=M,M,628,330
panel(f,ax,ay,aw,ah); panel_tag(f,ax+22,ay+34,"A","Intravenous curcumin liposomes, DU145 (mean ± s.d.)",title_color=INK)
labels=["blank\ncarrier","free","untargeted","targeted"]; cols=[GREYB,ORANGE,BLUE,VIOLET]
d1=[129,131,126,131]; e1=[26,22,28,31]; d10=[659,365,275,121]; e10=[136,156,135,72]
px,py,pw,ph=ax+84,ay+70,aw-150,200; ymax=860
for i in range(5):
    gy=py+ph-ph*i/4*(860/860)/1*1; gy=py+ph-ph*(i*215)/ymax
    f.line(px,gy,px+pw,gy,color=GRID,sw=1.2); f.text(px-8,gy,f"{i*215}",size=10.5,color=MUTED,anchor="end")
f.line(px,py,px,py+ph,color="#C7D0DC",sw=1.4); f.line(px,py+ph,px+pw,py+ph,color="#C7D0DC",sw=1.4)
slot=pw/4
for i in range(4):
    bw2=slot*0.3; bx1=px+slot*i+slot/2-bw2-3
    # day1 (hatched/light) and endpoint
    for val,err,xo,fill,light in [(d1[i],e1[i],bx1,cols[i],True),(d10[i],e10[i],bx1+bw2+6,cols[i],False)]:
        bh2=ph*val/ymax; g=f.lin(tint(fill,0.6 if light else 0.15),tint(fill,0.4) if light else fill)
        f.rrect(xo,py+ph-bh2,bw2,bh2,r=4,fill=f"url(#{g})",stroke=fill if light else "#fff",sw=1.3)
        ey=py+ph-bh2
        f.line(xo+bw2/2,ey-ph*err/ymax,xo+bw2/2,ey+ph*err/ymax,color=INK2,sw=1.4)
        if not light: f.text(xo+bw2/2,ey-ph*err/ymax-10,f"{val}",size=10.5,color=INK,weight=700,anchor="middle")
    f.text(px+slot*i+slot/2,py+ph+ (14 if "\n" not in labels[i] else 14), labels[i].split("\n")[0], size=11.5,color=INK2,anchor="middle")
    if "\n" in labels[i]: f.text(px+slot*i+slot/2,py+ph+28, labels[i].split("\n")[1], size=11.5,color=INK2,anchor="middle")
# baseline line
by0=py+ph-ph*129/ymax
f.line(px,by0,px+pw,by0,color=PINK,sw=1.6,dash="7 5"); f.text(px+pw,by0-8,"baseline",size=10.5,color=PINK,weight=700,anchor="end")
f.body.append(f'<text x="{px-42:.0f}" y="{py+ph/2:.0f}" text-anchor="middle" transform="rotate(-90 {px-42:.0f} {py+ph/2:.0f})" style="font-family:{FONT};font-size:12px;font-weight:600;fill:{INK2}">tumor volume (mm³)</text>')
legend_key(f, ax+aw-150, ay+70, [(GREY,"day 1"),(INK2,"endpoint")], gap=18, tsize=11)
f.text(ax+aw/2, ay+ah-16, "only the targeted arm ends below its own baseline (regression)", size=11.5, color=MUTED, italic=True, anchor="middle")
# B : Akanda NLC
bx,by,bw,bh=M+628+18,M,W-(M+628+18)-M,330
panel(f,bx,by,bw,bh); panel_tag(f,bx+22,by+34,"B","Intravenous curcumin NLC, LNCaP, ~4 weeks",title_color=INK)
bars(f, bx+84, by+70, bw-150, 196, [1412,1375,1155,778],
     ["control","blank\ncarrier","free","lipid\ncarrier"], [GREYB,tint(TEAL,0.4),ORANGE,TEAL], ylab="tumor volume (mm³)")
f.text(bx+bw/2, by+bh-16, "blank carrier ≈ control: the carrier is inert here", size=11.5, color=MUTED, italic=True, anchor="middle")
# C : route strata
cx,cy,cw,ch=M,M+330+18,628,334
panel(f,cx,cy,cw,ch); panel_tag(f,cx+22,cy+34,"C","Administration route sets what a result can claim",title_color=INK)
stages=[("absorption",AMBER),("circulation",BLUE),("extravasation",TEAL)]
sx=cx+150; sy=cy+92; sw_=(cw-200)/len(stages)
for i,(lab,col) in enumerate(stages):
    chip(f, sx+i*sw_, sy, sw_-12, 38, lab, tint(col,0.82), text_color=shade(col,0.15), tsize=11.5, stroke=tint(col,0.5))
chip(f, sx+len(stages)*sw_, sy, 84, 38, "tumor", PINK, tsize=12)
routes=[("oral",0,AMBER,cy+170),("i.v.",1,BLUE,cy+212),("intratumoral",3,PINK,cy+254)]
for lab,idx,col,ry in routes:
    tx= sx+idx*sw_+(sw_-12)/2 if idx<3 else sx+len(stages)*sw_+42
    f.circle(cx+50,ry,7,fill=col,stroke="#fff",sw=1.4); f.text(cx+62,ry,lab,size=12,color=col,weight=700,anchor="start")
    f.path(f"M {cx+130} {ry} L {tx} {ry} L {tx} {sy+40}", stroke=col, sw=2.4); f.arrow(tx,ry+4,tx,sy+38,color=col,sw=2.4,headsize=9)
f.text(cx+cw/2, cy+ch-18, "intratumoral curcumin cannot speak to oral bioavailability or systemic targeting", size=11.5, color=MUTED, italic=True, anchor="middle")
# D : Pten divergent readouts
dx,dy,dw,dh=M+628+18,M+330+18,W-(M+628+18)-M,334
panel(f,dx,dy,dw,dh); panel_tag(f,dx+22,dy+34,"D","Dietary nanoparticle curcumin, Pten-deficient mice",title_color=INK)
items=[("cancer-cell\nproliferation",GREEN,"down"),("tumor\nburden",GREY,"flat"),("body\nweight",GREY,"flat"),("liver\nweight",RED,"up")]
n=len(items); step=(dw-60)/n
for i,(lab,c,d) in enumerate(items):
    xx=dx+40+i*step+step/2; cyy=dy+150
    f.rrect(xx-step/2+10, dy+96, step-20, 150, r=12, fill=tint(c,0.84), stroke=tint(c,0.45), sw=1.4)
    if d=="down": f.arrow(xx,cyy-30,xx,cyy+34,color=c,sw=5,headsize=20)
    elif d=="up": f.arrow(xx,cyy+30,xx,cyy-34,color=c,sw=5,headsize=20)
    else: f.line(xx-22,cyy,xx+22,cyy,color=c,sw=5)
    for j,ln in enumerate(lab.split("\n")): f.text(xx, dy+262+j*15, ln, size=11.5, color=INK, anchor="middle")
f.text(dx+dw/2, dy+dh-14, "a favorable marker with no tumor benefit and an organ signal — and no free-drug arm", size=11, color=MUTED, italic=True, anchor="middle")
open("Figure4.svg","w").write(f.finish()); print("fig4 ok")
