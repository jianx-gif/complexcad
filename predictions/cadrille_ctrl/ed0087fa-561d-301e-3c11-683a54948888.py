import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-10))
r=w0.sketch().circle(37).circle(28,mode='s').finalize().extrude(-5).union(w0.sketch().circle(45).circle(15,mode='s').finalize().extrude(25))
