import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-59,0))
w1=cq.Workplane('XY',origin=(0,0,59))
r=w0.sketch().segment((-62,-57),(-62,-10)).arc((-64,0),(-62,10)).segment((-62,57)).arc((-84,0),(-62,-57)).assemble().reset().face(w0.sketch().arc((62,-57),(84,0),(62,57)).segment((62,10)).arc((64,0),(62,-10)).close().assemble()).finalize().extrude(149).union(w1.sketch().segment((-73,-46),(-73,46)).arc((-84,0),(-73,-46)).assemble().finalize().extrude(-139))