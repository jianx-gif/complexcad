import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-50))
r=w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(60).union(w0.workplane(offset=100/2).cylinder(100,60))