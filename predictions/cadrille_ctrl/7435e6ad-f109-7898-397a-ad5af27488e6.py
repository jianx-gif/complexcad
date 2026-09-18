import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,13))
r=w0.sketch().segment((-30,-12),(-21,-21)).segment((-17,-18)).arc((-23,-14),(-27,-8)).close().assemble().reset().face(w0.sketch().arc((1,11),(16,-2),(20,-20)).segment((30,-10)).segment((10,8)).close().assemble()).finalize().extrude(-13).union(w0.sketch().segment((-24,14),(-17,25)).segment((-18,25)).close().assemble().finalize().extrude(-12)).union(w0.sketch().segment((-18,10),(14,-27)).segment((30,-14)).segment((14,4)).segment((28,19)).segment((17,20)).segment((16,15)).close().assemble().finalize().extrude(-12))
