import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().arc((-95,-18),(-73,-57),(-37,-86)).segment((-37,-58)).close().assemble().reset().face(w0.sketch().arc((-13,86),(11,72),(29,52)).segment((37,52)).arc((19,76),(-13,86)).assemble()).reset().face(w0.sketch().arc((37,-86),(47,-63),(52,-38)).arc((46,-43),(37,-47)).close().assemble()).finalize().extrude(-200)