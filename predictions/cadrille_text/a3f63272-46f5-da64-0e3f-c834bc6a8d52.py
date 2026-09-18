import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-27))
r=w0.sketch().segment((-100,11),(-99,11)).segment((-99,13)).close().assemble().reset().face(w0.sketch().segment((99,-13),(100,-11)).segment((99,-11)).close().assemble()).finalize().extrude(54)