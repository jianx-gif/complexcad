import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,0,0))
r=w0.sketch().circle(38).circle(33,mode='s').finalize().extrude(-100).union(w0.sketch().circle(25).circle(20,mode='s').finalize().extrude(100))