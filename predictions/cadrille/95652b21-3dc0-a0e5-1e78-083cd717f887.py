import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.workplane(offset=-16/2).cylinder(16,55).union(w0.sketch().circle(100).circle(25,mode='s').finalize().extrude(16))