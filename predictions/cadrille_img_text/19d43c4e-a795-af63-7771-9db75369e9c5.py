import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-36,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().arc((-26,-12),(-19,-22),(-8,-28)).close().assemble().reset().face(w0.sketch().segment((-1,28),(26,12)).arc((19,22),(-1,28)).assemble()).finalize().extrude(123).union(w1.sketch().arc((-100,-42),(0,-83),(100,-42)).segment((100,-28)).arc((0,-80),(-100,-28)).close().assemble().reset().face(w1.sketch().arc((-100,28),(0,80),(100,28)).segment((100,42)).arc((0,83),(-100,42)).close().assemble()).finalize().extrude(200))