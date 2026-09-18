import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('ZX',origin=(0,-30,0))
r=w0.sketch().arc((-79,-49),(-23,-67),(33,-49)).close().assemble().reset().face(w0.sketch().segment((-79,49),(33,49)).arc((-23,67),(-79,49)).assemble()).finalize().extrude(200).union(w1.sketch().arc((-64,11),(-39,23),(-12,28)).arc((-39,28),(-64,11)).assemble().finalize().extrude(120))