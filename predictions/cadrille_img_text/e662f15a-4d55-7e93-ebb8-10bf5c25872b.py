import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('ZX',origin=(0,9,0))
r=w0.sketch().arc((-92,-56),(0,-88),(92,-56)).close().assemble().reset().face(w0.sketch().segment((-92,56),(92,56)).arc((0,88),(-92,56)).assemble()).finalize().extrude(200).union(w1.sketch().push([(0,0.5)]).rect(180,131).push([(0,1)]).circle(33,mode='s').finalize().extrude(-41))