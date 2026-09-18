import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('XY',origin=(0,0,58))
r=w0.sketch().circle(32).circle(30,mode='s').finalize().extrude(30).union(w0.workplane(offset=70/2).cylinder(70,32)).union(w1.sketch().circle(47).circle(11,mode='s').finalize().extrude(14))
