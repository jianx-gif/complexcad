import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,60))
r=w0.sketch().circle(40).circle(12,mode='s').finalize().extrude(-120).union(w0.sketch().circle(69).circle(12,mode='s').finalize().extrude(-67)).union(w0.sketch().circle(100).circle(53,mode='s').finalize().extrude(-53))