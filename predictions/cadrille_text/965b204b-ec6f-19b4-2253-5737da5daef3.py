import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-33,-33))
r=w0.sketch().segment((-100,33),(-99,28)).segment((-99,33)).close().assemble().reset().face(w0.sketch().segment((-98,33),(-97,33)).segment((-97,35)).close().assemble()).reset().face(w0.sketch().segment((97,-35),(98,-33)).segment((97,-33)).close().assemble()).finalize().extrude(67)