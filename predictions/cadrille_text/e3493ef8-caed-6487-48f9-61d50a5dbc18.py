import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,0,-100))
r=w0.sketch().segment((-53,17),(-53,19)).arc((-54,18),(-53,17)).assemble().reset().face(w0.sketch().arc((-52,17),(-51,18),(-52,19)).close().assemble()).finalize().extrude(200)