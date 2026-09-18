import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-11,0))
w1=cq.Workplane('XY',origin=(0,0,71))
r=w0.sketch().segment((-100,-72),(100,-72)).segment((100,72)).segment((92,72)).arc((88,67),(84,72)).segment((-100,72)).close().assemble().finalize().extrude(-4).union(w0.sketch().arc((-79,-12),(0,-80),(79,-12)).segment((53,-12)).arc((0,-55),(-53,-12)).close().assemble().finalize().extrude(103)).union(w1.sketch().arc((-3,-94),(1,-91),(5,-87)).segment((-3,-87)).close().assemble().finalize().extrude(-142))