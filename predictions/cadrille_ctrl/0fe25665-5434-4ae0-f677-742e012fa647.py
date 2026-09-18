import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,45))
r=w0.sketch().circle(30).circle(25,mode='s').finalize().extrude(-45).union(w0.workplane(offset=8/2).cylinder(8,35))
