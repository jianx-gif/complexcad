import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-14,0))
w1=cq.Workplane('XY',origin=(0,0,-75))
r=w0.sketch().push([(0,13)]).rect(194,172).circle(87,mode='s').circle(18).push([(63,13)]).circle(15,mode='s').push([(63,-17)]).circle(13,mode='s').push([(63,36)]).circle(13,mode='s').finalize().extrude(20).union(w1.sketch().arc((-89,19),(-88,17),(-87,15)).arc((-11,79),(85,42)).arc((87,43),(89,43)).arc((-11,82),(-89,19)).assemble().finalize().extrude(175))