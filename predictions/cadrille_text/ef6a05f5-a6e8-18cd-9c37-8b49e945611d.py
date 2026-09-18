import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-67,-67))
w1=cq.Workplane('XY',origin=(-100,-67,-67))
r=w0.sketch().segment((26,-57),(26,-56)).arc((24,-61),(28,-57)).close().assemble().finalize().extrude(134).union(w1.sketch().face(w1.sketch().segment((0,0),(200,0)).segment((200,0),(200,134)).segment((200,134),(0,134)).segment((0,134),(0,0)).assemble()).finalize().extrude(134))