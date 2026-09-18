import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,39,0))
w1=cq.Workplane('ZX',origin=(0,77,0))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-52,33),(-33,23)).arc((-27,37),(-15,47)).segment((-34,57)).close().assemble(),mode='s').reset().face(w0.sketch().segment((15,-47),(34,-57)).segment((52,-33)).segment((33,-23)).arc((27,-37),(15,-47)).assemble(),mode='s').finalize().extrude(-58).union(w1.sketch().arc((-2,-4),(2,-3),(2,1)).arc((-1,1),(-2,-2)).segment((-2,-1)).segment((0,-1)).segment((0,-3)).close().assemble().finalize().extrude(-154))