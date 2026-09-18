import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,91,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-14,-29),(14,3),(-14,35)).segment((-14,29)).arc((10,3),(-14,-23)).close().assemble().finalize().extrude(-100).union(w1.sketch().arc((-99,-49),(0,-91),(99,-49)).segment((68,-49)).arc((0,-84),(-68,-49)).close().assemble().finalize().extrude(-200))