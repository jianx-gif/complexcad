import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-61,0))
w1=cq.Workplane('ZX',origin=(0,-86,0))
r=w0.sketch().push([(0,-1)]).circle(25).circle(23,mode='s').finalize().extrude(-39).union(w0.sketch().arc((-11,-19),(-10,-15),(-10,-19)).arc((1,20),(-11,-19)).assemble().finalize().extrude(161)).union(w1.sketch().push([(0,-1)]).circle(23).circle(12,mode='s').finalize().extrude(18))