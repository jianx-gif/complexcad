import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,38,0))
w1=cq.Workplane('ZX',origin=(0,89,0))
r=w0.sketch().arc((-96,26),(-73,-46),(-10,-83)).segment((-10,-96)).segment((10,-96)).segment((10,-83)).arc((73,-46),(96,26)).close().assemble().finalize().extrude(-102).union(w1.sketch().arc((-1,-1),(1,-1),(3,0)).arc((1,2),(3,3)).arc((2,5),(0,6)).arc((1,3),(-1,1)).close().assemble().finalize().extrude(-179))