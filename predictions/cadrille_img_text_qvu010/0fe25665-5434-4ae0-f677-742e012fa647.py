import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-83,0))
r=w0.sketch().rect(200,200).circle(89,mode='s').finalize().extrude(166).union(w0.sketch().arc((-88,-40),(0,-92),(88,-40)).segment((87,-40)).arc((0,-91),(-87,-40)).close().assemble().reset().face(w0.sketch().segment((-88,40),(-87,40)).arc((0,91),(87,40)).segment((88,40)).arc((0,92),(-88,40)).assemble()).finalize().extrude(185))