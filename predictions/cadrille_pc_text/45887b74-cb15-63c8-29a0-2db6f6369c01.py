import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-15))
r=w0.sketch().segment((-100,-75),(100,-75)).segment((100,-50)).segment((-75,-50)).segment((-75,-10)).segment((-88,-67)).segment((-100,-65)).close().assemble().reset().face(w0.sketch().segment((-95,-46),(-75,-13)).segment((-75,75)).arc((-83,28),(-95,-19)).close().assemble()).finalize().extrude(30)