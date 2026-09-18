import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-10))
r=w0.sketch().segment((-100,90),(-99,90)).segment((-99,92)).close().assemble().finalize().extrude(-80).union(w0.sketch().segment((92,-9),(92,-7)).arc((96,-11),(94,-5)).segment((94,-9)).close().assemble().finalize().extrude(100))