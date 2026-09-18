import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-14,0))
w1=cq.Workplane('ZX',origin=(0,-60,0))
r=w0.sketch().push([(12,13)]).circle(87).reset().face(w0.sketch().segment((-1,21),(4,11)).segment((24,21)).segment((19,31)).close().assemble(),mode='s').finalize().extrude(11).union(w0.sketch().segment((-100,1),(-85,1)).arc((100,-11),(-85,11)).segment((-100,11)).close().assemble().push([(10,1)]).circle(87,mode='s').finalize().extrude(29)).union(w1.sketch().push([(12,13)]).circle(87).circle(82,mode='s').finalize().extrude(121))