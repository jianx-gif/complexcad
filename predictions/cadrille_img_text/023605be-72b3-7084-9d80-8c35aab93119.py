import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,90,0))
w1=cq.Workplane('YZ',origin=(-68,0,0))
r=w0.sketch().segment((-32,18),(-28,14)).arc((-24,17),(-20,19)).segment((-24,23)).close().assemble().reset().face(w0.sketch().segment((20,-19),(24,-23)).segment((32,-18)).segment((28,-14)).arc((24,-17),(20,-19)).assemble()).finalize().extrude(-109).union(w1.sketch().arc((-89,-86),(-57,-91),(-26,-100)).segment((26,-100)).arc((57,0),(26,100)).segment((-26,100)).arc((-57,91),(-89,86)).segment((-89,86),(-89,84)).segment((-89,84),(-89,-84)).close().assemble().finalize().extrude(168))