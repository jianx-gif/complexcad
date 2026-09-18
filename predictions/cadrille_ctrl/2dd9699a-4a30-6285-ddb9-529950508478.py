import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
r=w0.sketch().segment((-40,-30),(40,-30)).segment((40,30)).segment((-40,30)).segment((-40,18)).segment((-32,18)).segment((-32,12)).segment((-40,12)).close().assemble().push([(32,20)]).circle(3,mode='s').finalize().extrude(-8).union(w0.sketch().segment((-3,-15),(3,-15)).segment((3,-1)).arc((0,-2),(-3,-1)).close().assemble().finalize().extrude(-8)).union(w0.sketch().segment((-3,39),(3,39)).arc((0,40),(-3,39)).assemble().reset().face(w0.sketch().arc((3,-15),(16,12),(3,39)).close().assemble()).finalize().extrude(6))
