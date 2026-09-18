import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-11))
r=w0.sketch().segment((-100,40),(-99,37)).segment((-99,41)).close().assemble().reset().face(w0.sketch().segment((99,-41),(100,-40)).segment((99,-37)).close().assemble()).finalize().extrude(-39).union(w0.workplane(offset=111/2).cylinder(111,4))