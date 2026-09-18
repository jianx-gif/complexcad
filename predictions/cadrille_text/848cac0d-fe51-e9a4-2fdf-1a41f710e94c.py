import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-67,-67))
r=w0.sketch().segment((28,-58),(28,-57)).segment((30,-57)).arc((34,-54),(38,-57)).segment((40,-57)).arc((34,-52),(28,-58)).assemble().finalize().extrude(134).union(w0.sketch().push([(0,6)]).circle(33).circle(27,mode='s').finalize().extrude(134))