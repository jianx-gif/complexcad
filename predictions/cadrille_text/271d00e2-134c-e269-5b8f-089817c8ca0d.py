import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,0,-100))
r=w0.sketch().segment((28,-58),(32,-58)).segment((32,-48)).arc((30,-53),(28,-58)).assemble().finalize().extrude(190).union(w0.sketch().push([(0,1)]).circle(20).circle(18,mode='s').finalize().extrude(200))