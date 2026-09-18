import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,98,0))
w1=cq.Workplane('ZX',origin=(0,93,0))
r=w0.sketch().arc((-99,-36),(0,-91),(99,-36)).segment((88,-36)).arc((0,-90),(-88,-36)).close().assemble().reset().face(w0.sketch().segment((-99,36),(-88,36)).arc((0,90),(88,36)).segment((99,36)).arc((0,91),(-99,36)).assemble()).finalize().extrude(-194).union(w1.sketch().arc((-100,-15),(-77,1),(-51,15)).segment((-100,15)).close().assemble().finalize().extrude(-182))