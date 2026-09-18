import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,70))
r=w0.sketch().circle(40).circle(34,mode='s').finalize().extrude(-70).union(w0.workplane(offset=10/2).cylinder(10,50))