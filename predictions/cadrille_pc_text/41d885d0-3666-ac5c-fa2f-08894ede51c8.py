import cadquery as cq
w0=cq.Workplane('YZ',origin=(-51,0,0))
w1=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().segment((-62,-11),(-42,-11)).arc((-53,0),(-42,11)).segment((-62,11)).close().assemble().finalize().extrude(109).union(w1.sketch().arc((-63,-11),(-62,-10),(-61,-11)).segment((-24,-11)).arc((-21,-4),(-17,-11)).segment((61,-11)).arc((62,-10),(62,-11)).segment((63,-11)).segment((63,1)).segment((-63,1)).close().assemble().finalize().extrude(200))