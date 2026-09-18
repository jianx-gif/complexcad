import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-7))
r=w0.sketch().segment((-50,-96),(49,-100)).segment((50,-67)).segment((-49,-57)).close().assemble().reset().face(w0.sketch().segment((-50,-41),(49,-51)).segment((50,96)).segment((-49,100)).close().assemble()).finalize().extrude(14)