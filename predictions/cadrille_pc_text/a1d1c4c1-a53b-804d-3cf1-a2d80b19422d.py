import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-3))
r=w0.sketch().circle(100).circle(92,mode='s').finalize().extrude(-2).union(w0.workplane(offset=7/2).moveTo(40,-51).cylinder(7,10))