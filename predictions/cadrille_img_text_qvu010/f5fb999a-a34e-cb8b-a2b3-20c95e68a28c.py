import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-70,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().arc((-41,-29),(3,-44),(41,-17)).close().assemble().reset().face(w0.sketch().segment((-39,29),(42,17)).arc((7,44),(-39,29)).assemble()).finalize().extrude(145).union(w1.sketch().circle(100).push([(-56,-11)]).circle(13,mode='s').push([(11,10)]).circle(15,mode='s').finalize().extrude(129))