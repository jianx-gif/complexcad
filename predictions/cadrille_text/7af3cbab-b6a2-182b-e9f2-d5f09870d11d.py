import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
w1=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().circle(50).circle(4,mode='s').finalize().extrude(100).union(w1.sketch().face(w1.sketch().segment((0,0),(200,0)).segment((200,0),(200,100)).segment((200,100),(0,100)).segment((0,100),(0,0)).assemble()).finalize().extrude(100))