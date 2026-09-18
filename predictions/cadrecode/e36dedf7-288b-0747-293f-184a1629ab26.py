import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-16))
w1=cq.Workplane('XY',origin=(0,0,20))
r=w0.sketch().circle(100).circle(83,mode='s').finalize().extrude(-6).union(w0.sketch().circle(83).circle(73,mode='s').finalize().extrude(48)).union(w1.sketch().circle(83).circle(6,mode='s').finalize().extrude(-52))