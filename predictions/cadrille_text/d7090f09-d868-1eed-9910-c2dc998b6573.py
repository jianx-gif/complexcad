import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-71))
r=w0.sketch().segment((28,-58),(33,-58)).segment((33,-57)).arc((30,-57),(28,-58)).assemble().finalize().extrude(119).union(w0.sketch().segment((-100,40),(-99,37)).segment((-99,41)).close().assemble().reset().face(w0.sketch().segment((99,-41),(100,-40)).segment((99,-37)).close().assemble()).finalize().extrude(142))