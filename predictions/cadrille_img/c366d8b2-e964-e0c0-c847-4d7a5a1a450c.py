import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-34,0))
w1=cq.Workplane('YZ',origin=(71,0,0))
r=w0.sketch().arc((-100,-19),(-10,42),(89,-19)).segment((89,-16)).arc((91,-10),(89,-4)).segment((89,19)).segment((-100,19)).close().assemble().finalize().extrude(104).union(w1.sketch().arc((-79,-91),(59,-51),(37,86)).arc((29,79),(20,74)).arc((19,-47),(-79,-91)).assemble().finalize().extrude(-121))