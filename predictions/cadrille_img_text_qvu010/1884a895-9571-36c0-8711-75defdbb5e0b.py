import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('ZX',origin=(0,-58,0))
r=w0.sketch().segment((-100,-59),(-88,-59)).arc((-96,-5),(-88,49)).segment((-100,49)).close().assemble().reset().face(w0.sketch().segment((88,-59),(100,-59)).segment((100,49)).segment((88,49)).arc((96,-5),(88,-59)).assemble()).finalize().extrude(-200).union(w1.sketch().arc((84,-68),(98,-5),(84,58)).segment((84,38)).arc((93,-5),(84,-48)).close().assemble().finalize().extrude(158))