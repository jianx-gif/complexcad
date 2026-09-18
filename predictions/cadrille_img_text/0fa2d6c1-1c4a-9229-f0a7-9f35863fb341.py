import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,96,0))
w1=cq.Workplane('ZX',origin=(0,90,0))
r=w0.sketch().arc((-10,-86),(10,-84),(29,-86)).arc((100,0),(29,86)).arc((-97,25),(-10,-86)).assemble().finalize().extrude(-162).union(w1.sketch().push([(6,0)]).circle(94).circle(79,mode='s').finalize().extrude(-187))