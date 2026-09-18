import cadquery as cq
w0=cq.Workplane('XY',origin=(-50,-2,-100))
w1=cq.Workplane('XY',origin=(-50,-2,-100))
r=w0.sketch().circle(50).circle(4,mode='s').finalize().extrude(200).union(w1.workplane(offset=190/2).box(100,4,190))