import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-10,-10))
r=w0.sketch().segment((-100,9),(-99,9)).segment((-99,11)).close().assemble().reset().face(w0.sketch().segment((99,-11),(100,-9)).segment((99,-9)).close().assemble()).finalize().extrude(-29).union(w0.workplane(offset=48/2).box(200,20,48))