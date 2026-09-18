import cadquery as cq
w0=cq.Workplane('XY').r = 0, 100).cylinder(100,90).union(w0.sketch().circle(93).circle(90,mode='s').finalize().extrude(-200))