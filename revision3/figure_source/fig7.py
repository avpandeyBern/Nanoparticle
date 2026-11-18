import svgkit as k
from svgkit import *
W,H=1280,760
f=Fig(W,H,bg="#FBFCFE"); M=22
# A : core arms
ax,ay,aw,ah=M,M,560,360
panel(f,ax,ay,aw,ah); panel_tag(f,ax+22,ay+34,"A","Core arms at matched dose, route, schedule",title_color=INK)
arms=[("vehicle",GREY,"veh"),("free drug",ORANGE,"free"),("blank carrier",TEAL,"blank"),
      ("loaded carrier",BLUE,"load"),("targeted vs untargeted",VIOLET,"targ")]
for i,(lab,col,kind) in enumerate(arms):
    yy=ay+84+i*52
    f.rrect(ax+30,yy-20,aw-60,42,r=12,fill=tint(col,0.9),stroke=tint(col,0.4),sw=1.3)
    gx=ax+58
    if kind=="veh": f.circle(gx,yy,15,fill=tint(GREY,0.5),stroke=GREY,sw=1.4)
    elif kind=="free": free_drug(f,gx,yy,13,ORANGE,seed=20,n=6)
    elif kind=="blank": np_polymeric(f,gx,yy,16,shell=TEAL,core="none",payload=0,seed=21)
    elif kind=="load": np_polymeric(f,gx,yy,16,shell=BLUE,seed=22)
    else:
        np_polymeric(f,gx-6,yy,13,shell=VIOLET,seed=23,corona=False); np_polymeric(f,gx+20,yy,13,shell=VIOLET,seed=24)
    f.text(ax+100, yy, lab, size=13, color=INK, weight=600, anchor="start")
    f.text(ax+aw-40, yy, str(i+1), size=14, color=tint(col,0.2), weight=800, anchor="end")
f.text(ax+aw/2, ay+ah-16, "add a dose- and ratio-matched free mixture for combinations", size=11, color=MUTED, italic=True, anchor="middle")
# B : contrast -> question
bx,by,bw,bh=M+560+18,M,W-(M+560+18)-M,360
panel(f,bx,by,bw,bh); panel_tag(f,bx+22,by+34,"B","Each question needs its own prespecified contrast",title_color=INK)
pairs=[("loaded vs free","delivery gain",BLUE),("loaded vs blank","carrier action",TEAL),
       ("targeted vs untargeted","targeting",VIOLET),("co-loaded vs free mix","combination",ORANGE),
       ("tumor vs toxicity","benefit–harm",PINK)]
for i,(lhs,rhs,col) in enumerate(pairs):
    yy=by+84+i*52
    chip(f, bx+30, yy-18, 230, 36, lhs, col, tsize=12.5)
    f.arrow(bx+268, yy, bx+306, yy, color=col, sw=3)
    chip(f, bx+314, yy-18, 200, 36, rhs, tint(col,0.82), text_color=col, tsize=12.5, stroke=tint(col,0.5))
# C : timeline
cx,cy,cw,ch=M,M+360+18,W-2*M,170
f.rrect(cx,cy,cw,ch,r=14,fill="#fff",stroke=BORDER,sw=1.4,shadow=True)
panel_tag(f,cx+22,cy+30,"C","A prespecified sequence that treats established disease",title_color=INK,tsize=17)
steps=[("implant",TEAL),("randomize at\nset tumor size",BLUE),("blinded\nmeasurement",VIOLET),
       ("exposure +\ntarget assay",AMBER),("recovery\ninterval",PINK)]
ty=cy+96; x0=cx+90; x1=cx+cw-90
f.line(x0,ty,x1,ty,color=tint(MUTED,0.4),sw=3.2)
f.arrow(x1-6,ty,x1+8,ty,color=tint(MUTED,0.3),sw=3.2)
for i,(lab,col) in enumerate(steps):
    xx=x0+(x1-x0)*i/(len(steps)-1)
    circ_node(f, xx, ty, 20, str(i+1), col, tsize=15)
    up = i%2==0
    for j,ln in enumerate(lab.split("\n")):
        f.text(xx, (ty-44 if up else ty+30)+j*14, ln, size=11, color=shade(col,0.1), weight=600, anchor="middle")
# D : replication & reporting ladder + benchmark
dx,dy,dw,dh=M,M+360+18+170+18,W-2*M,54+120
# place as bottom strip with 4 tiers + benchmark note
dx,dy,dw,dh=M,cy+ch+18,W-2*M,120
f.rrect(dx,dy,dw,dh,r=14,fill="#fff",stroke=BORDER,sw=1.4,shadow=True)
panel_tag(f,dx+22,dy+30,"D","Replication and auditable reporting before any translational claim",title_color=INK,tsize=17)
tiers=[("second AR-driven model",BLUE),("resistant phenotype",TEAL),("orthotopic / PDX / GEM",VIOLET),("animal-level data release",PINK)]
step=(dw-280)/len(tiers)
for i,(lab,col) in enumerate(tiers):
    xx=dx+40+i*step
    chip(f, xx, dy+56, step-20, 40, lab, col, tsize=12)
    if i<len(tiers)-1: f.arrow(xx+step-18, dy+76, xx+step-2, dy+76, color=MUTED, sw=2.4)
chip(f, dx+dw-230, dy+56, 210, 40, "benchmark vs docetaxel", AMBER, tsize=12)
open("Figure7.svg","w").write(f.finish()); print("fig7 ok")
