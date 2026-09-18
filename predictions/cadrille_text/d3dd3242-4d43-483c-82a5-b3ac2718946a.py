import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
w1=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().face(w0.sketch().segment((91,-50),(100,-50)).segment((100,-42)).arc((96,-46),(91,-50)).assemble()).finalize().extrude(100).union(w1.sketch().face(w1.sketch().segment((0,0),(200,0)).segment((200,0),(200,100)).segment((200,100),(0,100)).segment((0,100),(0,0)).assemble()).finalize().extrude(100))