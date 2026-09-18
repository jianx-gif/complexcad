import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,15,0))
w1=cq.Workplane('YZ',origin=(-42,0,0))
r=w0.sketch().segment((-100,-48),(-100,48)).arc((-100,0),(-100,-48)).assemble().reset().face(w0.sketch().arc((100,-87),(100,-86),(100,34)).close().assemble()).finalize().extrude(-26).union(w1.sketch().arc((-79,-82),(-4,-31),(79,-34)).arc((73,18),(48,66)).arc((-11,19),(-79,34)).close().assemble().finalize().extrude(110))