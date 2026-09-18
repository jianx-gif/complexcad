import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('ZX',origin=(0,90,0))
r=w0.sketch().segment((-95,-36),(-87,-41)).arc((-77,-66),(-57,-83)).segment((-57,-95)).segment((-36,-95)).arc((53,85),(-95,-36)).assemble().circle(95,mode='s').finalize().extrude(-100).union(w1.sketch().circle(100).circle(60,mode='s').finalize().extrude(-180))