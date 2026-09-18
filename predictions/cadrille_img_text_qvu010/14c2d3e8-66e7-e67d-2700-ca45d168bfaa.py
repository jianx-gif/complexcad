import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,34,0))
w1=cq.Workplane('ZX',origin=(0,91,0))
r=w0.sketch().rect(200,194).circle(91,mode='s').finalize().extrude(-34).union(w1.sketch().circle(53).circle(35,mode='s').finalize().extrude(-182))