import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('XY',origin=(0,0,72))
r=w0.sketch().circle(38).circle(37,mode='s').circle(3).finalize().extrude(-100).union(w1.workplane(offset=-72/2).cylinder(72,32))
