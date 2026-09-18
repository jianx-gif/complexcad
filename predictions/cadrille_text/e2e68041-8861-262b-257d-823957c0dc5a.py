import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-100))
w1=cq.Workplane('XY',origin=(-100,-1,-100))
r=w0.sketch().face(w0.sketch().segment((96,-1),(96,1)).segment((97,1)).arc((93,0),(97,-1)).close().assemble()).finalize().extrude(200).union(w1.sketch().face(w1.sketch().segment((0,0),(0,1)).segment((3,1)).arc((-2,2),(0,0)).assemble()).finalize().extrude(180))