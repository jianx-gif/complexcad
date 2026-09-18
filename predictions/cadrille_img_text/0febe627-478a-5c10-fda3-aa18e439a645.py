import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-35,0))
w1=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().segment((-22,-57),(22,-57)).segment((22,-35)).arc((0,-41),(-22,-35)).close().assemble().reset().face(w0.sketch().arc((-22,35),(0,41),(22,35)).segment((22,57)).segment((-22,57)).close().assemble()).finalize().extrude(120).union(w1.sketch().arc((-87,-52),(-63,-77),(-33,-95)).segment((-33,-81)).arc((-60,-72),(-80,-52)).close().assemble().reset().face(w1.sketch().arc((-80,81),(-60,72),(-33,81)).segment((-33,95)).arc((-63,77),(-80,52)).close().assemble()).finalize().extrude(200))