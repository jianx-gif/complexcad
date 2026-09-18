import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,47))
w1=cq.Workplane('XY',origin=(0,0,13))
r=w0.sketch().circle(94).circle(81,mode='s').finalize().extrude(-94).union(w0.sketch().circle(93).circle(91,mode='s').finalize().extrude(-83)).union(w1.workplane(offset=-32/2).cylinder(32,100))