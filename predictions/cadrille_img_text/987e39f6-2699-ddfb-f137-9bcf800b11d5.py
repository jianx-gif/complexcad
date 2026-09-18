import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,28,0))
w1=cq.Workplane('ZX',origin=(0,60,0))
r=w0.sketch().circle(100).circle(87,mode='s').finalize().extrude(-57).union(w1.sketch().push([(0,2)]).rect(24,168).push([(0,0)]).rect(12,12,mode='s').finalize().extrude(-120))