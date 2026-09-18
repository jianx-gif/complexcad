import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-100,-100))
w1=cq.Workplane('XY',origin=(-100,-100,-100))
r=w0.sketch().segment((26,-58),(26,-57)).arc((24,-56),(26,-54)).segment((26,-53)).segment((28,-53)).arc((32,-52),(35,-53)).segment((37,-53)).segment((37,-54)).arc((38,-56),(37,-57)).segment((37,-58)).segment((35,-58)).arc((32,-59),(28,-58)).close().assemble().finalize().extrude(200).union(w1.sketch().face(w1.sketch().segment((0,0),(0,200)).segment((0,200),(200,200)).segment((200,200),(200,0)).segment((200,0),(0,0)).assemble()).finalize().extrude(200))