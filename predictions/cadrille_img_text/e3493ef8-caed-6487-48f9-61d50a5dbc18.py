import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,77,0))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().arc((-41,72),(-12,3),(1,-72)).segment((41,-72)).segment((41,72)).close().assemble().finalize().extrude(-142).union(w1.sketch().segment((-100,-89),(-41,-89)).arc((0,-94),(41,-89)).segment((100,-89)).segment((100,89)).segment((41,89)).arc((0,94),(-41,89)).segment((-100,89)).close().assemble().push([(-71,68)]).circle(14,mode='s').push([(-51,-33)]).circle(15,mode='s').push([(51,-60)]).circle(23,mode='s').finalize().extrude(-200))