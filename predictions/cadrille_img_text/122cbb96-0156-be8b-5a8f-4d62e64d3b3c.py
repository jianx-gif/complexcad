import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,90,0))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.workplane(offset=-156/2).moveTo(26,19).cylinder(156,51).union(w1.sketch().arc((-100,-75),(-90,-74),(-80,-73)).segment((100,-73)).segment((100,68)).arc((90,70),(80,72)).arc((26,95),(-33,96)).arc((-67,98),(-100,100)).close().assemble().push([(-73,83)]).circle(13,mode='s').push([(26,19)]).circle(62,mode='s').finalize().extrude(-100))