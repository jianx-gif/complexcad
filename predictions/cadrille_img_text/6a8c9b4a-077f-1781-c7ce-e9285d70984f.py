import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,38,0))
w1=cq.Workplane('ZX',origin=(0,87,0))
r=w0.sketch().segment((-74,-45),(-74,-44)).segment((-61,-44)).segment((-61,-56)).arc((70,72),(-74,-45)).assemble().finalize().extrude(-77).union(w1.sketch().arc((1,-15),(14,0),(1,15)).close().assemble().finalize().extrude(-174))