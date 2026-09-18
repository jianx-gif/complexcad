import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,79))
r=w0.sketch().circle(90).circle(85,mode='s').finalize().extrude(-158).union(w0.sketch().circle(100).circle(92,mode='s').finalize().extrude(-9))