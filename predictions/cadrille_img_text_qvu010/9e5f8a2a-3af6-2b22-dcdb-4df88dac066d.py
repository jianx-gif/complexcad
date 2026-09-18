import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,19,0))
w1=cq.Workplane('ZX',origin=(0,96,0))
r=w0.sketch().segment((-100,-83),(100,-83)).segment((100,83)).segment((-100,83)).segment((-100,82)).segment((-97,82)).segment((-97,78)).segment((-100,78)).close().assemble().finalize().extrude(-38).union(w1.sketch().arc((-2,-5),(2,4),(2,-5)).segment((2,5)).segment((-2,5)).close().assemble().finalize().extrude(-193))