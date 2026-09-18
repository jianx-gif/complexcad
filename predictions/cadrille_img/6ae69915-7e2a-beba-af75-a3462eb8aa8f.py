import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,39,0))
w1=cq.Workplane('ZX',origin=(0,29,0))
r=w0.sketch().arc((-42,69),(48,1),(-35,-73)).arc((96,8),(-42,69)).assemble().finalize().extrude(-79).union(w0.sketch().segment((-38,54),(-29,48)).arc((-28,51),(-26,54)).segment((-35,60)).close().assemble().reset().face(w0.sketch().segment((53,-34),(62,-40)).segment((72,-24)).segment((63,-18)).arc((61,-26),(53,-34)).assemble()).finalize().extrude(21)).union(w1.workplane(offset=-69/2).moveTo(17,12).cylinder(69,83))