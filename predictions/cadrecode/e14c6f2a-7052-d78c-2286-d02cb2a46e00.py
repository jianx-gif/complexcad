import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-78))
w1=cq.Workplane('XY',origin=(0,0,-94))
r=w0.workplane(offset=167/2).cylinder(167,61).union(w0.sketch().arc((-66,-10),(66,10),(-66,10)).arc((-61,0),(-66,-10)).assemble().circle(59,mode='s').finalize().extrude(173)).union(w1.workplane(offset=11/2).cylinder(11,100))