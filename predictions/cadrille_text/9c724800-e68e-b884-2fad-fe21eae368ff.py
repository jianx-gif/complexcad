import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-100,-100))
r=w0.sketch().segment((-100,99),(-99,99)).segment((-99,100)).close().assemble().reset().face(w0.sketch().segment((99,-100),(100,-99)).segment((99,-99)).close().assemble()).finalize().extrude(200)