import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-100))
w1=cq.Workplane('XY',origin=(-100,-17,-100))
r=w0.sketch().circle(4).circle(3,mode='s').finalize().extrude(200).union(w1.sketch().circle(17).circle(12,mode='s').finalize().extrude(117))