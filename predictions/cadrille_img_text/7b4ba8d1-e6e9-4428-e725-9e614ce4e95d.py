import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,96,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().arc((-35,22),(-19,-2),(9,-13)).close().assemble().finalize().extrude(-109).union(w1.sketch().arc((-99,-96),(0,-60),(99,-96)).segment((99,-59)).arc((0,-67),(-99,-59)).close().assemble().finalize().extrude(200))