import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-25,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().segment((-2,-85),(2,-85)).segment((2,-84)).arc((84,0),(2,84)).segment((2,85)).segment((-2,85)).segment((-2,84)).arc((-84,0),(-2,-84)).close().assemble().finalize().extrude(45).union(w1.sketch().arc((35,33),(38,37),(41,40)).arc((-39,-37),(44,38)).arc((42,35),(38,33)).close().assemble().finalize().extrude(200))