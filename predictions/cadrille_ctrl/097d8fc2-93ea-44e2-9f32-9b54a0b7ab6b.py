import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
w1=cq.Workplane('XY',origin=(0,0,3))
r=w0.sketch().circle(40).circle(33,mode='s').finalize().extrude(-10).union(w0.workplane(offset=-7/2).cylinder(7,22)).union(w1.sketch().circle(40).circle(27,mode='s').finalize().extrude(5))
