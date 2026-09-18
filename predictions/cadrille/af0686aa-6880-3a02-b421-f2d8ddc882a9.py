import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-57,0))
w1=cq.Workplane('XY',origin=(0,0,45))
r=w0.sketch().arc((-55,-18),(55,-2),(-55,18)).close().assemble().finalize().extrude(-12).union(w0.sketch().push([(16,44)]).circle(42).circle(37,mode='s').finalize().extrude(103)).union(w0.workplane(offset=157/2).moveTo(16,44).cylinder(157,32)).union(w1.sketch().push([(0,-1)]).circle(99).circle(52,mode='s').finalize().extrude(-65))