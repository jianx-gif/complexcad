import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,11,0))
w1=cq.Workplane('ZX',origin=(0,36,0))
r=w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(23).union(w1.sketch().circle(71).circle(45,mode='s').finalize().extrude(-107))