import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,48,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().arc((-98,-14),(-64,-2),(-33,14)).segment((-98,14)).close().assemble().finalize().extrude(-82).union(w0.sketch().segment((-56,-68),(40,-68)).segment((-56,68)).close().assemble().reset().face(w0.sketch().segment((-40,68),(56,-68)).segment((56,68)).close().assemble()).finalize().extrude(42)).union(w1.sketch().arc((10,82),(28,53),(35,21)).arc((37,54),(10,82)).assemble().finalize().extrude(200))