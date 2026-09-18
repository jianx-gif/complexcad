import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,0,-100))
r=w0.sketch().segment((-53,12),(-53,14)).arc((-54,13),(-53,12)).assemble().reset().face(w0.sketch().arc((23,-58),(37,-48),(53,-42)).segment((53,-12)).segment((23,-12)).close().assemble()).finalize().extrude(200)