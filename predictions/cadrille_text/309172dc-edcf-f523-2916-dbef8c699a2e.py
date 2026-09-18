import cadquery as cq
w0=cq.Workplane('XY',origin=(-33,-33,-100))
w1=cq.Workplane('XY',origin=(-33,-33,-100))
r=w0.sketch().circle(33).circle(29,mode='s').finalize().extrude(200).union(w1.workplane(offset=190/2).cylinder(190,5))