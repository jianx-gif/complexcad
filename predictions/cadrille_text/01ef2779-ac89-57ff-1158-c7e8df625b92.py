import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-100,-100))
w1=cq.Workplane('XY',origin=(-100,-100,-50))
r=w0.sketch().face(w0.sketch().segment((90,-99),(100,-99)).segment((100,-97)).close().assemble()).finalize().extrude(200).union(w1.sketch().face(w1.sketch().segment((0,0),(200,0)).segment((200,10)).segment((198,10)).segment((198,6)).segment((195,6)).segment((195,10)).segment((0,10)).close().assemble()).finalize().extrude(150))