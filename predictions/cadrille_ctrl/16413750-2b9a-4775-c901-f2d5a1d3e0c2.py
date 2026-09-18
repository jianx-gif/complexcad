import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,60))
r=w0.sketch().circle(30).circle(27,mode='s').finalize().extrude(-60).union(w0.sketch().circle(27).circle(23,mode='s').finalize().extrude(-10))
