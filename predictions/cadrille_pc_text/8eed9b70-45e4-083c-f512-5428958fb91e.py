import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,34))
r=w0.sketch().circle(95).circle(89,mode='s').finalize().extrude(-67).union(w0.sketch().circle(100).circle(50,mode='s').finalize().extrude(-6))