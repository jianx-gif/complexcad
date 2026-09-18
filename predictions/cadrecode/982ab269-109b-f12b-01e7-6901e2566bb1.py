import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,79))
w1=cq.Workplane('XY',origin=(0,0,53))
r=w0.sketch().circle(68).circle(64,mode='s').finalize().extrude(-158).union(w0.workplane(offset=-4/2).cylinder(4,100)).union(w1.sketch().circle(64).circle(32,mode='s').finalize().extrude(-127))