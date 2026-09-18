import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,95))
r=w0.sketch().circle(59).circle(57,mode='s').finalize().extrude(-190).union(w0.sketch().circle(100).circle(18,mode='s').finalize().extrude(-17))