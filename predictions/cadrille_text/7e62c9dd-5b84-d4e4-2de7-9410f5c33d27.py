import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-11,-11))
r=w0.sketch().segment((28,-58),(28,-57)).segment((30,-57)).arc((33,-56),(36,-57)).segment((38,-57)).arc((33,-54),(28,-58)).assemble().finalize().extrude(-30).union(w0.workplane(offset=111/2).moveTo(0,-11).cylinder(111,2))