import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,25,0))
w1=cq.Workplane('ZX',origin=(0,60,0))
r=w0.sketch().segment((-82,-30),(-79,-35)).segment((10,91)).segment((7,92)).close().assemble().finalize().extrude(-45).union(w0.sketch().segment((-29,1),(-26,-1)).arc((-24,3),(-22,6)).close().assemble().reset().face(w0.sketch().segment((22,-91),(29,-87)).segment((26,-84)).arc((24,-87),(22,-91)).assemble()).finalize().extrude(45)).union(w1.sketch().push([(15,-56)]).circle(44).circle(23,mode='s').finalize().extrude(-120))