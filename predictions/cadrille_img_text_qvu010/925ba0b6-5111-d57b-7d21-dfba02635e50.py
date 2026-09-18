import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-30,0))
w1=cq.Workplane('ZX',origin=(0,-87,0))
r=w0.sketch().arc((-100,10),(-3,-100),(100,10)).segment((73,10)).arc((-3,-74),(-79,10)).close().assemble().reset().face(w0.sketch().segment((-100,32),(-79,32)).arc((-3,74),(73,32)).segment((100,32)).arc((-3,100),(-100,32)).assemble()).finalize().extrude(23).union(w1.sketch().arc((-2,-8),(0,-7),(2,-8)).segment((2,8)).segment((-2,8)).close().assemble().finalize().extrude(174))