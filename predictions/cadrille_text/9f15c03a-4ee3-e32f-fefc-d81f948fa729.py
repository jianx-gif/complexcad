import cadquery as cq
w0=cq.Workplane('XY',origin=(-50,-100,-50))
r=w0.sketch().segment((-50,100),(-45,88)).segment((-45,100)).close().assemble().reset().face(w0.sketch().segment((45,-100),(50,-100)).segment((50,-88)).close().assemble()).finalize().extrude(100)