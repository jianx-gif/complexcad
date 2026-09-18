import cadquery as cq
w0=cq.Workplane('XY',origin=(-75,-50,-100))
r=w0.sketch().segment((-7,-10),(-7,10)).arc((-10,0),(-7,-10)).assemble().reset().face(w0.sketch().arc((7,-10),(10,0),(7,10)).close().assemble()).finalize().extrude(200)