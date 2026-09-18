import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-25,-25))
r=w0.sketch().segment((-100,12),(-99,12)).segment((-99,14)).close().assemble().reset().face(w0.sketch().segment((99,-14),(100,-12)).segment((99,-12)).close().assemble()).finalize().extrude(50)