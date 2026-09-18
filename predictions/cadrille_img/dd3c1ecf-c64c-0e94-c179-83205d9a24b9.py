import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-14,0))
w1=cq.Workplane('XY',origin=(0,0,-79))
r=w0.sketch().push([(-6.5,30.5)]).rect(187,139).push([(-61,29)]).circle(21,mode='s').reset().face(w0.sketch().segment((-44,-36),(59,-54)).segment((76,51)).segment((-27,69)).close().assemble(),mode='s').push([(83,-11)]).circle(16,mode='s').finalize().extrude(-21).union(w0.sketch().push([(8,71)]).circle(18).circle(16,mode='s').finalize().extrude(29)).union(w1.sketch().arc((-79,-19),(0,-52),(79,-19)).segment((78,-19)).arc((0,-51),(-78,-19)).close().assemble().finalize().extrude(179))