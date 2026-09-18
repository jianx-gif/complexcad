import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-40))
r=w0.workplane(offset=-3/2).cylinder(3,24).union(w0.sketch().circle(33).circle(30,mode='s').finalize().extrude(80))