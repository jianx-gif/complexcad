import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,60))
r=w0.sketch().circle(20).circle(15,mode='s').finalize().extrude(-60).union(w0.sketch().circle(30).circle(24,mode='s').finalize().extrude(-15))
