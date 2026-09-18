import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,1,0))
w1=cq.Workplane('ZX',origin=(0,39,0))
r=w0.sketch().circle(100).circle(83,mode='s').finalize().extrude(-19).union(w1.sketch().circle(81).circle(79,mode='s').finalize().extrude(-79))