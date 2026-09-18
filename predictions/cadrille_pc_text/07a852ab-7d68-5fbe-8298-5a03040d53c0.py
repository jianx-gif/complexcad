import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,25))
r=w0.sketch().circle(100).circle(88,mode='s').finalize().extrude(-50).union(w0.workplane(offset=-35/2).moveTo(-90,0).cylinder(35,3))