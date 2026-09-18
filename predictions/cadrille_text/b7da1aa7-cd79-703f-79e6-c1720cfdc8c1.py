import cadquery as cq
w0=cq.Workplane('XY',origin=(-60,-11,-100))
w1=cq.Workplane('XY',origin=(-60,-11,-100))
r=w0.sketch().circle(45).circle(35,mode='s').finalize().extrude(200).union(w1.workplane(offset=190/2).box(120,22,190))