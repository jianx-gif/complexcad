import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('ZX',origin=(0,24,0))
r=w0.sketch().segment((-79,10),(28,68)).arc((11,72),(-6,76)).arc((-41,58),(-79,44)).close().assemble().finalize().extrude(200).union(w1.sketch().arc((-10,38),(-4,50),(-1,62)).arc((-4,51),(-10,41)).close().assemble().finalize().extrude(-46))