import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-21,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-10,61),(-7,50),(-4,39)).segment((-2,39)).segment((-2,36)).arc((-1,35),(0,34)).segment((-2,34)).segment((-2,-63)).segment((10,-63)).segment((10,39)).segment((8,39)).arc((1,50),(-10,61)).assemble().finalize().extrude(45).union(w1.sketch().arc((-79,1),(1,-1),(28,77)).arc((1,71),(-25,75)).arc((-52,43),(-79,10)).close().assemble().finalize().extrude(-200))