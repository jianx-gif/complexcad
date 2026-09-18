import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-17))
r=w0.sketch().segment((-100,49),(-99,49)).segment((-99,50)).close().assemble().reset().face(w0.sketch().segment((99,-50),(100,-49)).segment((99,-49)).close().assemble()).finalize().extrude(-73).union(w0.workplane(offset=117/2).cylinder(117,3))