import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-1,-1))
r=w0.sketch().segment((28,-58),(28,-57)).segment((30,-57)).arc((34,-54),(38,-57)).segment((40,-57)).arc((34,-52),(28,-58)).assemble().finalize().extrude(-40).union(w0.sketch().push([(100,-1)]).circle(2).push([(99.5,-1)]).rect(3,2,mode='s').finalize().extrude(101))