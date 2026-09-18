import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-10,-10))
r=w0.sketch().segment((-100,10),(-99,8)).segment((-99,11)).close().assemble().reset().face(w0.sketch().segment((99,-11),(100,-10)).segment((99,-8)).close().assemble()).finalize().extrude(-8).union(w0.workplane(offset=28/2).cylinder(28,3))