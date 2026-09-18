import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-100,-1))
w1=cq.Workplane('XY',origin=(-100,-100,-1))
r=w0.sketch().circle(8).circle(7,mode='s').finalize().extrude(200).union(w1.sketch().face(w1.sketch().segment((0,0),(200,0)).segment((200,0),(200,200)).segment((200,200),(0,200)).segment((0,200),(0,0)).assemble()).finalize().extrude(-1))