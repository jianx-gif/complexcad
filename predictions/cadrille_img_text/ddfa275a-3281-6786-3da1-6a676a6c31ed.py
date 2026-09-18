import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-100,0))
w1=cq.Workplane('ZX',origin=(0,-78,0))
r=w0.sketch().arc((-59,-48),(0,-73),(59,-48)).segment((47,-48)).arc((0,-68),(-47,-48)).close().assemble().reset().face(w0.sketch().segment((-59,48),(-47,48)).arc((0,68),(47,48)).segment((59,48)).arc((0,73),(-59,48)).assemble()).finalize().extrude(200).union(w1.sketch().push([(8,10)]).circle(88).circle(87,mode='s').finalize().extrude(129))