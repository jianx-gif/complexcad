import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-19,0))
w1=cq.Workplane('ZX',origin=(0,-29,0))
r=w0.sketch().segment((-10,-10),(10,-10)).arc((0,-11),(-10,-10)).assemble().finalize().extrude(-68).union(w0.sketch().arc((-1,-1),(0,0),(1,-1)).segment((1,1)).segment((-1,1)).close().assemble().finalize().extrude(106)).union(w1.workplane(offset=10/2).cylinder(10,96))