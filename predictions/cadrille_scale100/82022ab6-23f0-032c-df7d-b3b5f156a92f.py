import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,72,0))
r=w0.sketch().circle(20).circle(12,mode='s').finalize().extrude(-72).union(w0.sketch().circle(60).circle(12,mode='s').finalize().extrude(8))