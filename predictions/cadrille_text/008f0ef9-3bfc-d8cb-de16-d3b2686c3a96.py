import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-10,-7))
w1=cq.Workplane('XY',origin=(-100,-10,-7))
r=w0.sketch().segment((-97,10),(-97,12)).arc((-98,11),(-97,10)).assemble().finalize().extrude(10).union(w1.sketch().face(w1.sketch().segment((0,0),(200,0)).segment((200,0),(200,20)).segment((200,20),(0,20)).segment((0,20),(0,0)).assemble()).finalize().extrude(15))