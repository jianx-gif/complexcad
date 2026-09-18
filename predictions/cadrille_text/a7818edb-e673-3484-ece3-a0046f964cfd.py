import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-10,-10))
w1=cq.Workplane('XY',origin=(60,-10,-10))
r=w0.sketch().face(w0.sketch().segment((0,0),(200,0)).segment((200,0),(0,20)).close().assemble()).finalize().extrude(20).union(w1.sketch().face(w1.sketch().segment((0,0),(40,0)).segment((40,0),(40,20)).segment((40,20),(0,20)).segment((0,20),(0,0)).assemble()).finalize().extrude(20))