import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,76))
r=w0.sketch().circle(86).circle(72,mode='s').finalize().extrude(-152).union(w0.sketch().circle(100).circle(6,mode='s').finalize().extrude(-23))