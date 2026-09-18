import cadquery as cq
w0=cq.Workplane('XY',origin=(-67,-33,-100))
r=w0.sketch().segment((-67,33),(-67,37)).arc((-68,35),(-67,33)).assemble().reset().face(w0.sketch().arc((27,-58),(33,-33),(27,-8)).close().assemble()).finalize().extrude(200)