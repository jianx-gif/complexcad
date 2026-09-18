import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,60))
r=w0.sketch().circle(94).circle(32,mode='s').finalize().extrude(-153).union(w0.sketch().circle(100).circle(94,mode='s').finalize().extrude(-147)).union(w0.sketch().circle(30).circle(24,mode='s').finalize().extrude(33))