import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,2))
r=w0.sketch().circle(100).circle(6,mode='s').finalize().extrude(-7).union(w0.workplane(offset=3/2).moveTo(33,-1).cylinder(3,2))