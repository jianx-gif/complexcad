import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,13,0))
w1=cq.Workplane('XY',origin=(0,0,-61))
r=w0.sketch().circle(100).circle(83,mode='s').finalize().extrude(-27).union(w1.sketch().arc((-60,12),(0,-9),(60,12)).segment((38,12)).arc((0,-3),(-38,12)).close().assemble().finalize().extrude(137))