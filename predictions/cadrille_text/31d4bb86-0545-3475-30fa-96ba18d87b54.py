import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-10))
w1=cq.Workplane('XY',origin=(69,40,-10))
r=w0.sketch().segment((96,-50),(96,50)).arc((20,0),(96,-50)).assemble().finalize().extrude(20).union(w1.sketch().face(w1.sketch().arc((96,-50),(100,0),(96,50)).close().assemble()).finalize().extrude(20))