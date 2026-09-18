import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-100,-10))
w1=cq.Workplane('XY',origin=(-100,-100,-10))
r=w0.sketch().segment((32,-57),(32,-56)).arc((30,-53),(32,-50)).segment((32,-49)).arc((29,-53),(32,-57)).assemble().finalize().extrude(110).union(w1.sketch().face(w1.sketch().segment((0,0),(200,0)).segment((200,0),(200,200)).segment((200,200),(0,200)).segment((0,200),(0,0)).assemble()).finalize().extrude(-20))