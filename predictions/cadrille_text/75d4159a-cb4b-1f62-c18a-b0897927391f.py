import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,0,-100))
r=w0.sketch().segment((-53,18),(-18,18)).arc((-36,23),(-53,18)).assemble().reset().face(w0.sketch().arc((18,-87),(29,-54),(18,-21)).close().assemble()).finalize().extrude(200)