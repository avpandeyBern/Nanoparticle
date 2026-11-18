import svgkit as k
from svgkit import *
W,H=1280,720
f=Fig(W,H,bg="#FBFCFE")
M=22; GREYB="#9AA6B6"
# A : Siddiqui i.p.
ax,ay,aw,ah=M,M,610,320
panel(f,ax,ay,aw,ah); panel_tag(f,ax+22,ay+34,"A","Intraperitoneal nano-EGCG, 22Rv1, day 45",title_color=INK)
bars(f, ax+80, ay+70, 300, 180, [1242,854,707], ["control","free","nano"], [GREYB,ORANGE,BLUE], ylab="tumor volume (mm³)")
# dose schematic
f.text(ax+470, ay+86, "dose per mouse", size=12, color=INK2, weight=700, anchor="middle")
free_drug(f, ax+430, ay+150, 20, ORANGE, seed=3, n=9); f.text(ax+430, ay+192, "free  1 mg", size=12, color=ORANGE, weight=700, anchor="middle")
np_polymeric(f, ax+520, ay+150, 26, shell=BLUE, seed=4); f.text(ax+520, ay+192, "nano  100 µg", size=12, color=BLUE, weight=700, anchor="middle")
chip(f, ax+430, ay+215, 160, 30, "10× lower dose", TEAL, tsize=12)
f.text(ax+230, ay+ah-18, "0.83× of free at one-tenth the dose", size=12, color=INK2, italic=True, anchor="middle")
# B : Khan oral
bx,by,bw,bh=M+610+18,M,W-(M+610+18)-M,320
panel(f,bx,by,bw,bh); panel_tag(f,bx+22,by+34,"B","Oral chitosan-EGCG, 22Rv1, day 32",title_color=INK)
bars(f, bx+80, by+70, bw-150, 180, [1200,514,310,216], ["control","free\n40","nano\n3","nano\n6"],
     [GREYB,ORANGE,tint(BLUE,0.35),BLUE], ylab="tumor volume (mm³)")
f.text(bx+bw/2, by+bh-18, "dose in mg kg⁻¹ · treatment began 1 day after implantation", size=11.5, color=MUTED, italic=True, anchor="middle")
# C : Sanna targeted, volume & weight as % control
cx,cy,cw,ch=M,M+320+18,610,342
panel(f,cx,cy,cw,ch); panel_tag(f,cx+22,cy+34,"C","Targeted vs untargeted EGCG: two endpoints agree",title_color=INK)
labels=["control","free","untargeted","targeted"]; cols=[GREYB,ORANGE,BLUE,VIOLET]
vol=[100,71,46,40]; wt=[100,70,43,37]
px,py,pw,ph=cx+80,cy+76,cw-150,196; ymax=120
for i in range(5): 
    gy=py+ph-ph*i/4; f.line(px,gy,px+pw,gy,color=GRID,sw=1.2)
    f.text(px-8, gy, f"{i*30}", size=11, color=MUTED, anchor="end")
f.line(px,py,px,py+ph,color="#C7D0DC",sw=1.4); f.line(px,py+ph,px+pw,py+ph,color="#C7D0DC",sw=1.4)
slot=pw/4
for i in range(4):
    bw2=slot*0.3
    bx1=px+slot*i+slot/2-bw2-3
    for val,xo,fill,hatch in [(vol[i],bx1,cols[i],False),(wt[i],bx1+bw2+6,tint(cols[i],0.5),True)]:
        bh2=ph*val/ymax; g=f.lin(tint(fill,0.15),fill)
        f.rrect(xo, py+ph-bh2, bw2, bh2, r=4, fill=f"url(#{g})", stroke=cols[i] if hatch else "#fff", sw=1.3)
        f.text(xo+bw2/2, py+ph-bh2-10, f"{val}", size=10.5, color=INK, weight=700, anchor="middle")
    f.text(px+slot*i+slot/2, py+ph+18, labels[i], size=12, color=INK2, anchor="middle")
f.text(px-ph*0+ -46, py+ph/2, "", size=1)
f.body.append(f'<text x="{px-40:.0f}" y="{py+ph/2:.0f}" text-anchor="middle" transform="rotate(-90 {px-40:.0f} {py+ph/2:.0f})" style="font-family:{FONT};font-size:12px;font-weight:600;fill:{INK2}">endpoint, % of control</text>')
legend_key(f, cx+cw-180, cy+76, [(INK2,"tumor volume"),(GREY,"tumor weight")], gap=20, tsize=11.5)
# D : audit / context
dx,dy,dw,dh=M+610+18,M+320+18,W-(M+610+18)-M,342
panel(f,dx,dy,dw,dh); panel_tag(f,dx+22,dy+34,"D","Interpretation checks and chemoprevention context",title_color=INK)
rows=["i.p. (A)","oral (B)","targeted (C)"]
cols2=["dose\nmatched","route\nstated","established\ntumor","variance\nrecovered","animal\nas unit"]
# 2 met,1 unclear,0 not
Mx=[[0,2,1,0,2],[0,2,0,1,0],[2,0,0,0,2]]
cmap={2:(mark_check,GREEN),1:(mark_dot,AMBER),0:(mark_cross,RED)}
heat_grid(f, dx+24, dy+64, 64, 44, Mx, rows, cols2, cmap, rowlab_w=96, collab_h=44, lab_size=10.5)
legend_key(f, dx+30, dy+260, [(GREEN,"met"),(AMBER,"unclear"),(RED,"not met")], cols=3, box_w=120, gap=0, tsize=11.5)
f.rrect(dx+24, dy+290, dw-48, 36, r=10, fill=TEAL_BG, stroke=tint(TEAL,0.4), sw=1.3)
f.text(dx+dw/2, dy+308, "Green-tea catechins cut progression in a 1-year HG-PIN prevention trial", size=11.5, color=shade(TEAL,0.1), weight=600, anchor="middle")
open("Figure3.svg","w").write(f.finish()); print("fig3 ok")
