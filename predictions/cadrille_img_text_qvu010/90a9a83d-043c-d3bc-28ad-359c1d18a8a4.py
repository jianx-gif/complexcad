import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,35,0))
w1=cq.Workplane('ZX',origin=(0,79,0))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-100,-1),(-87,-15)).arc((-77,33),(-38,63)).segment((-51,77)).close().assemble(),mode='s').circle(52,mode='s').finalize().extrude(-70).union(w1.sketch().arc((-1,-1),(0,1),(1,-1)).segment((1,1)).segment((-1,1)).close().assemble().finalize().extrude(-158))