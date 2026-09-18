import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,20))
w1=cq.Workplane('XY',origin=(0,0,5))
r=w0.sketch().circle(69).circle(50,mode='s').finalize().extrude(-45).union(w1.sketch().circle(100).circle(88,mode='s').finalize().extrude(20))