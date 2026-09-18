import cadquery as cq
w0=cq.Workplane('XY',origin=(-71,-100,-72))
r=w0.sketch().segment((-71,76),(-29,97)).arc((-51,90),(-71,76)).assemble().reset().face(w0.sketch().segment((-28,97),(29,100)).arc((3,100),(-21,97)).close().assemble()).reset().face(w0.sketch().arc((29,-97),(51,-90),(71,-76)).close().assemble()).finalize().extrude(144)