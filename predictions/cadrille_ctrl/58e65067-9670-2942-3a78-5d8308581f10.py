import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,38))
w1=cq.Workplane('XY',origin=(0,0,35))
r=w0.sketch().circle(48).circle(45,mode='s').finalize().extrude(-76).union(w0.sketch().circle(15).circle(12,mode='s').finalize().extrude(13)).union(w1.sketch().circle(45).circle(44,mode='s').finalize().extrude(-73))
