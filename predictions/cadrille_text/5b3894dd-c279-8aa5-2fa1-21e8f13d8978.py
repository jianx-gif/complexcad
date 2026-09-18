import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-19,-19))
r=w0.sketch().segment((28,-58),(30,-58)).segment((30,-57)).arc((29,-57),(28,-58)).assemble().finalize().extrude(-71).union(w0.sketch().push([(100,-19)]).circle(3).push([(99.5,-19)]).rect(3,4,mode='s').finalize().extrude(119))