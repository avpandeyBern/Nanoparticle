import svgkit as k, math
from svgkit import *
W,H=1280,730
f=Fig(W,H,bg="#FBFCFE"); M=22; GREYB="#9AA6B6"
# A : tumor vs plasma AUC
ax,ay,aw,ah=M,M,628,330
panel(f,ax,ay,aw,ah); panel_tag(f,ax+22,ay+34,"A","Tumor exposure rises while plasma exposure falls",title_color=INK)
labels=["free","untargeted","targeted"]; cols=[ORANGE,BLUE,VIOLET]
tum=[1032,1484,4356]; pla=[2306,1834,1475]; ymax=5000
px,py,pw,ph=ax+92,ay+70,aw-170,200
for i in range(6):
    gy=py+ph-ph*i/5; f.line(px,gy,px+pw,gy,color=GRID,sw=1.2); f.text(px-8,gy,f"{i*1000}",size=10,color=MUTED,anchor="end")
f.line(px,py,px,py+ph,color="#C7D0DC",sw=1.4); f.line(px,py+ph,px+pw,py+ph,color="#C7D0DC",sw=1.4)
slot=pw/3
for i in range(3):
    bw2=slot*0.3; bx1=px+slot*i+slot/2-bw2-3
    for val,xo,fill,light in [(tum[i],bx1,cols[i],False),(pla[i],bx1+bw2+6,cols[i],True)]:
        bh2=ph*val/ymax; g=f.lin(tint(fill,0.55 if light else 0.15),tint(fill,0.4) if light else fill)
        f.rrect(xo,py+ph-bh2,bw2,bh2,r=4,fill=f"url(#{g})",stroke=fill if light else "#fff",sw=1.3)
        f.text(xo+bw2/2,py+ph-bh2-9,f"{val:,}",size=10,color=INK,weight=700,anchor="middle")
    f.text(px+slot*i+slot/2,py+ph+16,labels[i],size=12,color=INK2,anchor="middle")
f.body.append(f'<text x="{px-52:.0f}" y="{py+ph/2:.0f}" text-anchor="middle" transform="rotate(-90 {px-52:.0f} {py+ph/2:.0f})" style="font-family:{FONT};font-size:12px;font-weight:600;fill:{INK2}">AUC₀–₁₂ₕ (ng·h g⁻¹)</text>')
legend_key(f, ax+aw-150, ay+70, [(INK2,"tumor"),(GREY,"plasma")], gap=18, tsize=11)
f.text(ax+aw/2, ay+ah-16, "4.22× tumor AUC with lower plasma AUC — redistribution, not more drug", size=11.5, color=MUTED, italic=True, anchor="middle")
# B : analyte compartments
bx,by,bw,bh=M+628+18,M,W-(M+628+18)-M,330
panel(f,bx,by,bw,bh); panel_tag(f,bx+22,by+34,"B","Three distinct analytes across three compartments",title_color=INK)
comp=[("plasma",BLUE,by+96),("tumor tissue",TEAL,by+172),("tumor cell",PINK,by+248)]
for lab,col,yy in comp:
    f.rrect(bx+30,yy-30,bw-60,58,r=12,fill=tint(col,0.86),stroke=tint(col,0.45),sw=1.3)
    f.text(bx+44,yy,lab,size=12,color=shade(col,0.1),weight=700,anchor="start")
np_polymeric(f,bx+220,by+96,20,shell=BLUE,seed=11,corona=False)
np_polymeric(f,bx+220,by+172,20,shell=BLUE,seed=12,corona=False)
free_drug(f,bx+330,by+172,16,ORANGE,seed=13,n=6)
free_drug(f,bx+300,by+248,16,ORANGE,seed=14,n=5)
free_drug(f,bx+420,by+248,14,GREY,seed=15,n=5)
for y1,y2 in [(by+120,by+146),(by+196,by+222)]:
    f.arrow(bx+250,y1,bx+250,y2,color=MUTED,sw=2.2)
legend_key(f, bx+30, by+bh-40, [(BLUE,"carrier-bound"),(ORANGE,"released parent"),(GREY,"metabolite")], cols=3, box_w=165, gap=0, tsize=11)
# C : payload vs carrier decomposition
cx,cy,cw,ch=M,M+330+18,628,334
panel(f,cx,cy,cw,ch); panel_tag(f,cx+22,cy+34,"C","Carrier is not always inert: apigenin–selenium example",title_color=INK)
bars(f, cx+92, cy+74, cw-180, 190, [44.3,31.4,9.8],
     ["loaded\ncarrier","blank\ncarrier","free\ndrug"], [PINK,VIOLET,ORANGE],
     ylab="apoptosis (%)", value_fmt="{:.1f}")
f.text(cx+cw/2, cy+ch-16, "the blank selenium carrier alone drives most of the effect", size=11.5, color=MUTED, italic=True, anchor="middle")
# D : exposure measurement wheel
dx,dy,dw,dh=M+628+18,M+330+18,W-(M+628+18)-M,334
panel(f,dx,dy,dw,dh); panel_tag(f,dx+22,dy+34,"D","Minimum exposure evidence set",title_color=INK)
wcx,wcy=dx+dw/2, dy+dh/2+26; R=116; r0=46
segs=[("plasma\nAUC",BLUE),("tumor\nAUC",TEAL),("tumor:plasma",VIOLET),("organ\ndistribution",AMBER),("unbound\nparent",ORANGE),("target\nengagement",PINK)]
for i,(lab,col) in enumerate(segs):
    a0=math.radians(90-i*60-54); a1=math.radians(90-i*60-6)
    x0o,y0o=wcx+R*math.cos(a0),wcy-R*math.sin(a0); x1o,y1o=wcx+R*math.cos(a1),wcy-R*math.sin(a1)
    x0i,y0i=wcx+r0*math.cos(a0),wcy-r0*math.sin(a0); x1i,y1i=wcx+r0*math.cos(a1),wcy-r0*math.sin(a1)
    d=f"M {x0i:.1f} {y0i:.1f} L {x0o:.1f} {y0o:.1f} A {R} {R} 0 0 1 {x1o:.1f} {y1o:.1f} L {x1i:.1f} {y1i:.1f} A {r0} {r0} 0 0 0 {x0i:.1f} {y0i:.1f} Z"
    f.path(d, fill=tint(col,0.38), stroke="#fff", sw=2.2)
    am=(a0+a1)/2; lx,ly=wcx+(R+22)*math.cos(am), wcy-(R+22)*math.sin(am)
    anchor="middle"
    for j,ln in enumerate(lab.split("\n")):
        f.text(lx, ly-6+j*13, ln, size=10.5, color=shade(col,0.1), weight=600, anchor=anchor)
f.circle(wcx,wcy,r0-6,fill="#fff",stroke=BORDER,sw=1.3)
f.text(wcx,wcy-6,"exposure",size=12,color=INK,weight=700,anchor="middle"); f.text(wcx,wcy+10,"evidence",size=12,color=INK,weight=700,anchor="middle")
open("Figure5.svg","w").write(f.finish()); print("fig5 ok")
