import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-10,-17))
r=w0.sketch().segment((28,-58),(32,-58)).segment((32,-48)).arc((30,-53),(28,-58)).assemble().finalize().extrude(-24).union(w0.sketch().segment((28,-48),(28,-46)).segment((32,-46)).arc((10,-12),(28,-48)).assemble().finalize().extrude(33)).union(w0.workplane(offset=39/2).moveTo(0,-1).cylinder(39,3))