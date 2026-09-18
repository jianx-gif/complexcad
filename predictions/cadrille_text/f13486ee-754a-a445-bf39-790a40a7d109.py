import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-21))
r=w0.sketch().segment((28,-58),(32,-58)).segment((32,-57)).arc((30,-57),(28,-58)).assemble().finalize().extrude(-79).union(w0.sketch().segment((28,-57),(28,-56)).segment((29,-56)).arc((25,-54),(28,-57)).assemble().finalize().extrude(100)).union(w0.workplane(offset=121/2).moveTo(29,-10).cylinder(121,2))