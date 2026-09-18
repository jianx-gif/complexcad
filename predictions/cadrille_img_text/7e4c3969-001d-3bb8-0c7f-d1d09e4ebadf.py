import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,1,0))
w1=cq.Workplane('ZX',origin=(0,39,0))
r=w0.sketch().push([(13,13)]).circle(87).circle(82,mode='s').finalize().extrude(-10).union(w1.sketch().push([(13,13)]).circle(87).circle(68,mode='s').finalize().extrude(-78))