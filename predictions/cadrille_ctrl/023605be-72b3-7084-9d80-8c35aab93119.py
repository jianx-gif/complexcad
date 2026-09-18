import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
r=w0.sketch().segment((-40,-25),(-21,-25)).arc((-31,-20),(-40,-13)).close().assemble().finalize().extrude(-11).union(w0.sketch().segment((-40,-11),(-33,-11)).arc((-31,-17),(-28,-22)).segment((-28,-11)).segment((6,-11)).segment((6,-25)).segment((40,-25)).segment((40,25)).segment((-40,25)).close().assemble().reset().face(w0.sketch().arc((-24,-25),(0,-35),(24,-25)).close().assemble()).reset().face(w0.sketch().segment((-24,25),(24,25)).arc((0,35),(-24,25)).assemble()).finalize().extrude(-10))
