import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((92,-29),(195,-29)).segment((195,-29),(200,50)).segment((200,50),(92,50)).close().assemble().finalize().extrude(100)