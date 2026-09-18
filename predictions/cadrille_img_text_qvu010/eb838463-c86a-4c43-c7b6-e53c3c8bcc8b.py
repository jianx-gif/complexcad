import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-17,0))
w1=cq.Workplane('ZX',origin=(0,-77,0))
r=w0.sketch().segment((-99,-22),(-98,-22)).arc((0,-100),(98,-22)).segment((99,-22)).segment((99,-18)).arc((100,0),(99,18)).segment((99,22)).segment((98,22)).arc((0,100),(-98,22)).segment((-99,22)).segment((-99,18)).arc((-100,0),(-99,-18)).close().assemble().finalize().extrude(34).union(w1.sketch().arc((-78,-18),(0,79),(78,-18)).segment((78,18)).segment((28,18)).arc((0,30),(-28,18)).segment((-78,18)).close().assemble().finalize().extrude(154))