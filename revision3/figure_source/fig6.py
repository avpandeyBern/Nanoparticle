import svgkit as k, math
from svgkit import *
W,H=1280,740
f=Fig(W,H,bg="#FBFCFE"); M=22
# A : reporting audit heatmap
ax,ay,aw,ah=M,M,760,360
panel(f,ax,ay,aw,ah); panel_tag(f,ax+22,ay+34,"A","Reporting audit of the four full-text comparisons",title_color=INK)
rows=["EGCG, targeted","catechin nanoemulsion","curcumin, aptamer liposome","curcumin, lipid carrier"]
cols=["dose\nunits","route\nstated","endpoint\nday","variance\ntype","animal\nnumber","vehicle\nmatched","formulation\ntable"]
Mx=[[0,0,2,0,2,1,2],[0,2,2,1,2,2,2],[2,2,0,2,0,0,2],[2,2,2,0,0,1,0]]
cmap={2:(mark_check,GREEN),1:(mark_dot,AMBER),0:(mark_cross,RED)}
heat_grid(f, ax+28, ay+66, 80, 48, Mx, rows, cols, cmap, rowlab_w=186, collab_h=48, lab_size=11)
legend_key(f, ax+210, ay+ah-26, [(GREEN,"consistent"),(AMBER,"unclear"),(RED,"conflicting / missing")], cols=3, box_w=185, gap=0, tsize=11.5)
# B : six conditions for pooling
bx,by,bw,bh=M+760+18,M,W-(M+760+18)-M,360
panel(f,bx,by,bw,bh); panel_tag(f,bx+22,by+34,"B","Six conditions before pooling",title_color=INK)
conds=[("same active\nmoiety",BLUE),("matched\nroute",TEAL),("common\nendpoint",VIOLET),
       ("reported\nvariance",AMBER),("animal-level\nreplication",ORANGE),("independent\ncomparator",PINK)]
for i,(lab,col) in enumerate(conds):
    r=i//2; c=i%2
    ccx=bx+90+c*180; ccy=by+112+r*90
    circ_node(f, ccx, ccy, 25, str(i+1), col, tsize=18)
    for j,ln in enumerate(lab.split("\n")):
        f.text(ccx, ccy+40+j*13, ln, size=10.5, color=shade(col,0.1), weight=600, anchor="middle")
# C : within-study ratios + no pooled estimate
cx,cy,cw,ch=M,M+360+18,760,344
panel(f,cx,cy,cw,ch); panel_tag(f,cx+22,cy+34,"C","Within-study ratios are shown; no pooled estimate is justified",title_color=INK)
groups=[("EGCG",BLUE,[0.828,0.603,0.420,0.649,0.566]),("curcumin",ORANGE,[0.753,0.332,0.674]),("catechin",TEAL,[0.717,0.475])]
fx,fy,fw,fh=cx+120,cy+80,cw-220,150
dot_forest(f, fx, fy, fw, fh, groups, 0.3,1.2,[0.3,0.5,0.7,0.9,1.1], ref=1.0, xlab="formulated / free ratio of tumor burden")
f.text(fx+fw*0.18, cy+66, "favors formulation", size=10.5, color=MUTED, anchor="middle")
f.text(fx+fw*0.92, cy+66, "favors free", size=10.5, color=MUTED, anchor="middle")
# empty dashed diamond with X in the right margin (ratio>1 region, no data there)
dmx,dmy=fx+fw*0.80, fy+fh*0.5
pts=[(dmx-40,dmy),(dmx,dmy-15),(dmx+40,dmy),(dmx,dmy+15)]
f.poly(pts, fill="none", stroke=MUTED, sw=1.6)
f.body[-1]=f.body[-1].replace('/>',' stroke-dasharray="5 4"/>')
f.line(dmx-26,dmy-10,dmx+26,dmy+10,color=RED,sw=2.6); f.line(dmx-26,dmy+10,dmx+26,dmy-10,color=RED,sw=2.6)
f.text(dmx, dmy-26, "no pooled", size=11.5, color=RED, weight=700, anchor="middle")
f.text(dmx, dmy+28, "estimate", size=11.5, color=RED, weight=700, anchor="middle")
# D : estimator + pitfalls
dx,dy,dw,dh=M+760+18,M+360+18,W-(M+760+18)-M,344
panel(f,dx,dy,dw,dh); panel_tag(f,dx+22,dy+34,"D","The estimator, and what breaks it",title_color=INK)
f.rrect(dx+24,dy+64,dw-48,66,r=12,fill=INDIGO_BG,stroke=tint(INDIGO,0.4),sw=1.3)
f.text(dx+dw/2, dy+90, "lnRR = ln( mean nano / mean free )", size=15, color=INDIGO, weight=700, anchor="middle")
f.text(dx+dw/2, dy+114, "var ≈ SD²/(n·mean²) for each arm", size=12, color=INK2, anchor="middle")
pit=[("shared control arms are not independent",PINK),
     ("multiple tumors per mouse are not replicates",ORANGE),
     ("SEM must be converted to SD using the true n",VIOLET)]
for i,(lab,col) in enumerate(pit):
    yy=dy+156+i*44
    f.rrect(dx+24,yy,dw-48,34,r=9,fill=tint(col,0.86),stroke=tint(col,0.42),sw=1.2)
    mark_cross(f, dx+42, yy+17, 10, col); f.text(dx+60, yy+17, lab, size=11.5, color=INK2, anchor="start")
open("Figure6.svg","w").write(f.finish()); print("fig6 ok")
