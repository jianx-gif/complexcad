import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,-100,-5))
r=w0.sketch().segment((-53,100),(-48,96)).segment((-48,100)).close().assemble().reset().face(w0.sketch().segment((24,-58),(53,-100)).segment((53,-58)).close().assemble()).finalize().extrude(11)