import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,87,0))
w1=cq.Workplane('YZ',origin=(-87,0,0))
r=w0.sketch().segment((-45,-86),(45,-86)).segment((45,45)).arc((0,-78),(-45,45)).close().assemble().finalize().extrude(-100).union(w1.sketch().arc((-87,-19),(-55,-18),(-25,-26)).segment((-25,-100)).segment((25,-100)).segment((25,-10)).arc((55,18),(87,45)).segment((87,100)).segment((-87,100)).close().assemble().finalize().extrude(187))