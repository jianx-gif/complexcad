import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,96,0))
w1=cq.Workplane('ZX',origin=(0,38,0))
r=w0.sketch().arc((-57,48),(18,33),(78,-11)).arc((80,1),(80,13)).arc((82,28),(77,43)).arc((10,78),(-57,48)).assemble().finalize().extrude(-152).union(w1.sketch().arc((-100,-83),(-1,1),(100,-83)).segment((100,83)).segment((-100,83)).close().assemble().finalize().extrude(-138))