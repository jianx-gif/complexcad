import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-20,0))
w1=cq.Workplane('ZX',origin=(0,-18,0))
r=w0.sketch().circle(100).circle(31,mode='s').finalize().extrude(18).union(w1.sketch().circle(71).circle(27,mode='s').finalize().extrude(97))