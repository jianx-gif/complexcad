import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,4))
r=w0.sketch().segment((-40,-30),(-30,-30)).arc((-36,-20),(-40,-9)).close().assemble().reset().face(w0.sketch().arc((-40,9),(-36,20),(-30,30)).segment((-40,30)).close().assemble()).reset().face(w0.sketch().segment((30,-30),(40,-30)).segment((40,-9)).arc((36,-20),(30,-30)).assemble()).finalize().extrude(-4).union(w0.sketch().segment((-10,-18),(10,-18)).segment((10,18)).segment((-10,18)).segment((-10,15)).arc((-8,13),(-10,12)).close().assemble().finalize().extrude(-4)).union(w0.workplane(offset=3/2).box(20,40,3))
