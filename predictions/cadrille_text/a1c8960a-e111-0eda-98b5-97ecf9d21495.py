import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((-100,40),(-99,37)).segment((-99,41)).close().assemble().reset().face(w0.sketch().segment((-98,41),(-97,41)).segment((-97,42)).close().assemble()).reset().face(w0.sketch().segment((97,-42),(98,-41)).segment((97,-37)).close().assemble()).finalize().extrude(100)