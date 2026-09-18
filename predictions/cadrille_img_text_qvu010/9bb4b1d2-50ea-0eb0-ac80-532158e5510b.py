import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-25,0))
w1=cq.Workplane('ZX',origin=(0,-94,0))
r=w0.sketch().segment((-100,-62),(-84,-62)).arc((-98,17),(-54,86)).segment((-100,98)).close().assemble().finalize().extrude(49).union(w1.sketch().arc((-59,-66),(11,-93),(81,-62)).segment((100,-62)).segment((100,62)).segment((81,62)).arc((11,93),(-59,62)).segment((-78,62)).segment((-78,-62)).segment((-73,-62)).arc((-80,-64),(-59,-66)).assemble().push([(85,-59)]).circle(16,mode='s').finalize().extrude(188))