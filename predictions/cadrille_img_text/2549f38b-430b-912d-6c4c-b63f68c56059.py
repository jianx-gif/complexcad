import cadquery as cq
w0=cq.Workplane('YZ',origin=(-47,0,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-35,-45),(0,-53),(35,-45)).close().assemble().reset().face(w0.sketch().segment((-35,80),(35,80)).arc((0,88),(-35,80)).assemble()).reset().face(w0.sketch().arc((37,-44),(53,17),(37,78)).close().assemble()).finalize().extrude(125).union(w1.sketch().arc((-89,-58),(0,-88),(89,-58)).close().assemble().finalize().extrude(-192))