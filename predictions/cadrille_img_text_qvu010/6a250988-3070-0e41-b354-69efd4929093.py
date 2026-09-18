import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-67,0))
r=w0.sketch().circle(100).reset().face(w0.sketch().arc((-19,12),(-39,-31),(11,-25)).arc((37,29),(-19,12)).assemble(),mode='s').finalize().extrude(-33).union(w0.sketch().arc((-100,-1),(0,-100),(100,-1)).segment((87,-1)).arc((0,-87),(-87,-1)).close().assemble().finalize().extrude(167))