import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,99,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().arc((-68,32),(-29,-10),(25,-26)).segment((25,-19)).segment((32,-19)).close().assemble().finalize().extrude(-139).union(w1.sketch().segment((-96,-62),(-68,-62)).arc((-10,-91),(50,-62)).segment((78,-62)).segment((78,43)).segment((50,43)).arc((-10,72),(-68,43)).segment((-96,43)).close().assemble().finalize().extrude(200))