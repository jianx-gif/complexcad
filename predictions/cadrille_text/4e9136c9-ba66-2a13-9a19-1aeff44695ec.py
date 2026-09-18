import cadquery as cq
w0=cq.Workplane('XY',origin=(-50,-50,-100))
w1=cq.Workplane('XY',origin=(-50,-50,-50))
r=w0.sketch().segment((24,-58),(24,-57)).arc((22,-54),(24,-51)).segment((24,-50)).segment((26,-50)).segment((26,-51)).arc((28,-54),(26,-57)).segment((26,-58)).close().assemble().finalize().extrude(200).union(w1.workplane(offset=150/2).moveTo(0,50).cylinder(150,3))