import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,0,-100))
r=w0.sketch().segment((-53,16),(-53,19)).arc((-54,17),(-53,16)).assemble().reset().face(w0.sketch().arc((-52,15),(-49,12),(-45,15)).close().assemble()).reset().face(w0.sketch().segment((-52,17),(-45,17)).arc((-49,20),(-52,17)).assemble()).finalize().extrude(200)