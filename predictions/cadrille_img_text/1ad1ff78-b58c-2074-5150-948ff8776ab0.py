import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,89,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-78,75),(-6,10)).segment((-6,68)).segment((-67,98)).close().assemble().reset().face(w0.sketch().segment((6,-68),(67,-98)).segment((78,-75)).segment((6,-10)).close().assemble()).finalize().extrude(-50).union(w1.sketch().arc((-98,-57),(0,-68),(98,-57)).segment((98,57)).segment((9,57)).arc((0,68),(-9,78)).segment((-9,57)).segment((-58,57)).arc((-77,46),(-98,42)).close().assemble().finalize().extrude(-200))