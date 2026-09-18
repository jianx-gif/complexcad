import cadquery as cq
w0=cq.Workplane('ZX',origin=(-100,14,0))
w1=cq.Workplane('ZX',origin=(-100,14,0))
r=w0.sketch().segment((91,-58),(91,58)).arc((39,0),(91,-58)).assemble().finalize().extrude(-28).union(w1.sketch().face(w1.sketch().arc((0,-1),(1,-2),(3,-2)).segment((3,-1)).close().assemble()).finalize().extrude(-28))