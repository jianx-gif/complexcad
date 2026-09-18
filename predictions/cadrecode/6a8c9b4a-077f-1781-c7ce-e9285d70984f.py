import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-23))
w1=cq.Workplane('XY',origin=(0,0,23))
r=w0.sketch().circle(96).circle(34,mode='s').finalize().extrude(-9).union(w0.sketch().circle(100).circle(91,mode='s').finalize().extrude(36)).union(w1.workplane(offset=9/2).cylinder(9,91))