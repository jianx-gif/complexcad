import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-11))
w1=cq.Workplane('XY',origin=(-100,-50,-11))
r=w0.sketch().segment((92,-50),(100,-50)).segment((100,-47)).close().assemble().finalize().extrude(28).union(w1.sketch().face(w1.sketch().segment((0,0),(200,0)).segment((200,0),(0,100)).close().assemble()).finalize().extrude(23))