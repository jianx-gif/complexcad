import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-30))
w1=cq.Workplane('XY',origin=(0,0,-33))
r=w0.workplane(offset=60/2).cylinder(60,43).union(w0.sketch().circle(36).circle(35,mode='s').finalize().extrude(63)).union(w1.sketch().circle(19).circle(11,mode='s').finalize().extrude(2))
