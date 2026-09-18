import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('XY',origin=(0,0,63))
r=w0.sketch().arc((-35,-92),(33,-18),(35,78)).close().assemble().finalize().extrude(-185).union(w1.sketch().arc((-78,80),(12,18),(26,-78)).arc((69,55),(-78,80)).assemble().finalize().extrude(-127))