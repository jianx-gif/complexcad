import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-39,0))
w1=cq.Workplane('ZX',origin=(0,-97,0))
r=w0.sketch().circle(100).circle(17,mode='s').finalize().extrude(10).union(w0.sketch().arc((-100,-12),(0,-100),(100,-12)).segment((94,-12)).arc((0,-95),(-94,-12)).close().assemble().reset().face(w0.sketch().segment((-100,12),(-94,12)).arc((0,95),(94,12)).segment((100,12)).arc((0,100),(-100,12)).assemble()).finalize().extrude(115)).union(w1.sketch().segment((-14,-14),(14,-14)).segment((14,-12)).arc((10,-10),(14,-8)).segment((14,14)).segment((-14,14)).close().assemble().finalize().extrude(174))