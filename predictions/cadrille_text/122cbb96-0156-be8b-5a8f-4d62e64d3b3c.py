import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-50))
r=w0.sketch().segment((-100,8),(-99,8)).segment((-99,10)).close().assemble().reset().face(w0.sketch().segment((99,-10),(100,-8)).segment((99,-8)).close().assemble()).finalize().extrude(100).union(w0.workplane(offset=100/2).cylinder(100,5))