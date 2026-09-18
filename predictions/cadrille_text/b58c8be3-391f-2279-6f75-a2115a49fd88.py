import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-40))
r=w0.sketch().segment((26,-58),(26,-57)).segment((28,-57)).arc((24,-50),(26,-58)).assemble().finalize().extrude(80).union(w0.sketch().push([(0,4)]).circle(4).circle(3,mode='s').finalize().extrude(80)).union(w0.workplane(offset=81/2).moveTo(0,4).cylinder(81,3))