import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-1,-1))
r=w0.sketch().segment((-100,1),(-99,-2)).segment((-99,1)).close().assemble().reset().face(w0.sketch().segment((-99,1),(-97,1)).segment((-97,3)).close().assemble()).reset().face(w0.sketch().segment((97,-3),(100,-1)).segment((99,2)).close().assemble()).finalize().extrude(10).union(w0.workplane(offset=10/2).cylinder(10,8))