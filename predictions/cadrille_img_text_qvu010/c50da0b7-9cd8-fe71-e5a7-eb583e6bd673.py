import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-100,0))
w1=cq.Workplane('ZX',origin=(0,-58,0))
r=w0.sketch().segment((-83,-40),(-62,-77)).segment((-19,-53)).arc((-47,-52),(-70,-40)).close().assemble().finalize().extrude(200).union(w1.sketch().arc((12,77),(18,-18),(68,62)).arc((40,75),(12,77)).assemble().push([(1,1)]).circle(15,mode='s').push([(42,47)]).circle(18,mode='s').finalize().extrude(-42))