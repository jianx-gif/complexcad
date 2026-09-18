import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-66,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().segment((-60,60),(-58,56)).arc((-57,58),(-55,60)).segment((-57,63)).close().assemble().reset().face(w0.sketch().segment((-54,48),(-37,17)).arc((-35,15),(-33,13)).segment((60,-48)).segment((87,-4)).segment((-47,73)).segment((-54,62)).close().assemble()).finalize().extrude(131).union(w1.sketch().arc((-100,20),(-57,33),(-14,35)).arc((-13,35),(-12,34)).arc((46,23),(87,-19)).arc((93,-17),(100,-15)).arc((1,35),(-100,20)).assemble().finalize().extrude(200))