import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-19,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-70,-72),(70,-72)).segment((70,-17)).arc((0,-71),(-70,-17)).close().assemble().reset().face(w0.sketch().arc((-70,17),(0,71),(70,17)).segment((70,72)).segment((-70,72)).close().assemble()).circle(53).finalize().extrude(-10).union(w1.sketch().segment((-100,-19),(-96,-19)).arc((0,-98),(96,-19)).segment((100,-19)).segment((100,19)).segment((96,19)).arc((0,98),(-96,19)).segment((-100,19)).close().assemble().finalize().extrude(-200))