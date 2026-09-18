import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-42,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().arc((-28,-20),(28,21),(-28,62)).close().assemble().push([(1,21)]).circle(19,mode='s').finalize().extrude(128).union(w1.sketch().segment((-100,-99),(100,-99)).segment((100,99)).segment((24,99)).arc((0,95),(-24,99)).segment((-100,99)).close().assemble().push([(-81,83)]).circle(17,mode='s').push([(0,0)]).circle(53,mode='s').push([(81,-55)]).circle(18,mode='s').finalize().extrude(109))