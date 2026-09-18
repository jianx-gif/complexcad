import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-50))
r=w0.sketch().segment((-100,19),(-99,19)).segment((-99,17)).segment((-96,17)).segment((-96,19)).segment((100,19)).segment((100,25)).segment((-100,25)).close().assemble().finalize().extrude(100).union(w0.sketch().segment((29,-58),(32,-58)).segment((32,-55)).arc((30,-56),(29,-58)).assemble().finalize().extrude(100))