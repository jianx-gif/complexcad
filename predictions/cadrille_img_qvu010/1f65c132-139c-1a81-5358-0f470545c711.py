import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-6,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().arc((-96,29),(-92,26),(-88,23)).segment((-88,29)).close().assemble().reset().face(w0.sketch().arc((-79,19),(10,-19),(100,19)).segment((88,19)).arc((10,-17),(-68,19)).close().assemble()).finalize().extrude(-80).union(w1.sketch().segment((-97,-5),(97,-5)).segment((97,22)).arc((0,87),(-97,22)).close().assemble().finalize().extrude(200))