import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,75))
w1=cq.Workplane('XY',origin=(0,0,25))
r=w0.sketch().circle(60).circle(27,mode='s').finalize().extrude(-150).union(w1.sketch().circle(100).circle(27,mode='s').finalize().extrude(50))