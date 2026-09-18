import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-10))
w1=cq.Workplane('XY',origin=(-100,-50,-10))
r=w0.sketch().segment((91,-42),(100,-42)).segment((100,-37)).close().assemble().finalize().extrude(20).union(w1.sketch().face(w1.sketch().segment((0,0),(200,0)).segment((200,0),(200,100)).segment((200,100),(0,100)).segment((0,100),(0,0)).assemble()).finalize().extrude(20))