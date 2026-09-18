import cadquery as cq
w0=cq.Workplane('XY',origin=(-30,-30,-100))
r=w0.sketch().segment((-30,29),(-30,30)).arc((-32,30),(-30,29)).assemble().reset().face(w0.sketch().arc((-29,29),(-27,30),(-29,30)).close().assemble()).finalize().extrude(200)