import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-25,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().push([(13,13)]).circle(87).circle(69,mode='s').finalize().extrude(50).union(w1.sketch().circle(100).push([(-14,64)]).circle(16,mode='s').finalize().extrude(200))