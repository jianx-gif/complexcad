import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-59,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().segment((-29,-34),(57,-34)).segment((57,68)).segment((-29,68)).segment((-29,43)).segment((54,43)).segment((54,-11)).segment((-29,-11)).close().assemble().finalize().extrude(10).union(w1.sketch().segment((-100,-91),(-73,-91)).arc((0,-100),(73,-91)).segment((100,-91)).segment((100,91)).segment((73,91)).arc((0,100),(-73,91)).segment((-100,91)).close().assemble().finalize().extrude(200))