import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-25,-25))
r=w0.sketch().segment((-100,25),(-99,25)).segment((-99,27)).close().assemble().reset().face(w0.sketch().segment((99,-27),(100,-25)).segment((99,-25)).close().assemble()).finalize().extrude(50)