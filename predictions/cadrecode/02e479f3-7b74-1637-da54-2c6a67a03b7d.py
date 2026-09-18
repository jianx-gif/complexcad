import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-37))
w1=cq.Workplane('XY',origin=(0,0,11))
r=w0.workplane(offset=10/2).cylinder(10,100).union(w0.sketch().circle(77).circle(67,mode='s').finalize().extrude(74)).union(w1.workplane(offset=11/2).cylinder(11,67))