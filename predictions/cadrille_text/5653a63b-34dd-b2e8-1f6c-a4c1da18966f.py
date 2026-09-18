import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-1,-10))
r=w0.sketch().segment((28,-58),(30,-58)).segment((30,-57)).arc((29,-57),(28,-58)).assemble().finalize().extrude(-80).union(w0.sketch().push([(29,-1)]).circle(3).circle(2,mode='s').finalize().extrude(65)).union(w0.sketch().push([(29,-1)]).circle(3).circle(2,mode='s').finalize().extrude(110))