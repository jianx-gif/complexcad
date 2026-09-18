import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-51))
r=w0.sketch().segment((-100,19),(-99,19)).segment((-99,21)).close().assemble().reset().face(w0.sketch().segment((99,-21),(100,-19)).segment((99,-19)).close().assemble()).finalize().extrude(102)