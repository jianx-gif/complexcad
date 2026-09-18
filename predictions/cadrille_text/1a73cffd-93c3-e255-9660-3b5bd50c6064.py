import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((-50,19),(-50,22)).segment((-46,22)).segment((-46,20)).segment((-49,19)).close().assemble().reset().face(w0.sketch().segment((46,-22),(49,-22)).segment((50,-19)).segment((46,-19)).close().assemble()).finalize().extrude(100).union(w0.workplane(offset=100/2).box(10,20,100))