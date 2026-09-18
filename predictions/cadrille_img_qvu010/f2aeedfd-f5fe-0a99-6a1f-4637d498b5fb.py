import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('ZX',origin=(0,-20,0))
r=w0.sketch().segment((-77,-19),(-44,-19)).arc((-4,-59),(46,-34)).segment((46,-19)).segment((47,-19)).arc((38,18),(14,47)).segment((14,69)).arc((-3,66),(-19,62)).arc((-12,59),(-6,55)).segment((-11,55)).arc((-43,25),(-77,1)).close().assemble().finalize().extrude(-200).union(w1.sketch().arc((84,13),(92,1),(97,-12)).arc((96,6),(84,19)).close().assemble().finalize().extrude(29))