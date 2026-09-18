import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-22))
r=w0.sketch().segment((28,-58),(28,-57)).segment((30,-57)).arc((29,-56),(28,-58)).assemble().finalize().extrude(-28).union(w0.sketch().push([(100,0)]).circle(100).circle(5,mode='s').finalize().extrude(48)).union(w0.workplane(offset=112/2).moveTo(100,0).cylinder(112,2))