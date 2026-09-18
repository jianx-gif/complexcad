import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-100))
w1=cq.Workplane('XY',origin=(-100,-50,-100))
r=w0.sketch().segment((92,-50),(100,-50)).segment((100,-43)).close().assemble().finalize().extrude(200).union(w1.sketch().face(w1.sketch().segment((0,0),(0,100)).arc((-100,50),(0,0)).assemble()).finalize().extrude(110))