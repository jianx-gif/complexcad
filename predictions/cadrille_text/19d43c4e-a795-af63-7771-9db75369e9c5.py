import cadquery as cq
w0=cq.Workplane('ZX',origin=(-100,33,-1))
w1=cq.Workplane('ZX',origin=(-100,33,-1))
r=w0.sketch().segment((91,-58),(95,-58)).segment((95,-55)).close().assemble().finalize().extrude(-120).union(w1.sketch().face(w1.sketch().segment((0,27),(0,33)).arc((-2,35),(0,37)).segment((0,43)).arc((-2,35),(0,27)).assemble()).finalize().extrude(-67))