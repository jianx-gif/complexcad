import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-51))
r=w0.sketch().segment((28,-58),(30,-58)).segment((30,-57)).arc((29,-57),(28,-58)).assemble().finalize().extrude(91).union(w0.sketch().push([(0,5)]).circle(5).circle(4,mode='s').finalize().extrude(102)).union(w0.workplane(offset=103/2).moveTo(0,5).cylinder(103,3))