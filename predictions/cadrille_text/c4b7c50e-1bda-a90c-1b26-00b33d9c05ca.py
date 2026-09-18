import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-13,-13))
w1=cq.Workplane('YZ',origin=(-100,-13,-13))
r=w0.sketch().face(w0.sketch().segment((0,0),(200,-2)).segment((200,-2),(200,2)).segment((200,2),(0,2)).segment((0,2),(0,0)).assemble()).finalize().extrude(29).union(w1.sketch().face(w1.sketch().segment((0,0),(1,0)).segment((1,0),(1,1)).segment((1,1),(2,1)).segment((2,1),(2,0)).segment((2,0),(3,0)).segment((3,0),(3,2)).segment((3,2),(0,2)).segment((0,2),(0,0)).assemble()).finalize().extrude(200))