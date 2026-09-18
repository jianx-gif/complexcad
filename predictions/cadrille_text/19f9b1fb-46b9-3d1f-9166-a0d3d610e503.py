import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-100,-100))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().face(w0.sketch().segment((92,-100),(100,-100)).segment((100,-97)).close().assemble()).finalize().extrude(200).union(w1.sketch().face(w1.sketch().segment((0,0),(0,200)).arc((-8,10),(92,0)).close().assemble()).finalize().extrude(100))