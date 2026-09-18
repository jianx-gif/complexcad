import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-100,0))
w1=cq.Workplane('ZX',origin=(0,-45,0))
r=w0.sketch().circle(67).reset().face(w0.sketch().segment((-18,10),(14,-14)).segment((18,-10)).segment((-14,14)).close().assemble(),mode='s').push([(39,40)]).circle(10,mode='s').finalize().extrude(199).union(w1.sketch().arc((-99,-35),(-45,-21),(-60,-75)).arc((80,60),(-99,-35)).assemble().finalize().extrude(145))