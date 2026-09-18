import cadquery as cq
w0=cq.Workplane('XY',origin=(-60,-60,-100))
r=w0.sketch().segment((26,-58),(26,-57)).segment((28,-57)).arc((24,-54),(26,-58)).assemble().finalize().extrude(183).union(w0.workplane(offset=200/2).moveTo(0,60).cylinder(200,4))