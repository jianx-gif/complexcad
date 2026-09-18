import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,20))
w1=cq.Workplane('ZX',origin=(0,-59,0))
r=w0.workplane(offset=-20/2).moveTo(57,-59).cylinder(20,33).union(w1.sketch().circle(100).circle(93,mode='s').finalize().extrude(151))