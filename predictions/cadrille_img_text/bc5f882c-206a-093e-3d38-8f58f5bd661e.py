import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,88,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().arc((-92,1),(-88,15),(-81,28)).segment((-92,28)).close().assemble().reset().face(w0.sketch().arc((-60,28),(34,-1),(100,-68)).segment((100,-28)).segment((92,-28)).arc((90,-15),(85,-1)).segment((92,-1)).segment((92,28)).segment((60,28)).arc((0,68),(-60,28)).assemble()).finalize().extrude(-79).union(w1.sketch().arc((-59,-68),(68,0),(-59,68)).segment((-59,67)).arc((67,0),(-59,-67)).close().assemble().finalize().extrude(195))