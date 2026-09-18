import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-37))
r=w0.sketch().segment((-100,4),(-99,4)).segment((-99,6)).close().assemble().reset().face(w0.sketch().segment((99,-6),(100,-4)).segment((99,-4)).close().assemble()).finalize().extrude(74)