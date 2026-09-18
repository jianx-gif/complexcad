import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,6))
r=w0.sketch().segment((-40,-15),(-33,-15)).segment((-33,-10)).arc((-36,-12),(-40,-15)).close().assemble().finalize().extrude(-11).union(w0.sketch().segment((-40,-15),(-33,-15)).segment((-33,-10)).arc((-36,-12),(-40,-15)).assemble().reset().face(w0.sketch().segment((-31,15),(-22,15)).segment((-31,16)).close().assemble()).reset().face(w0.sketch().segment((15,-15),(24,-16)).segment((25,-15)).close().assemble()).reset().face(w0.sketch().segment((21,15),(30,14)).segment((21,15)).close().assemble()).finalize().extrude(-6))
