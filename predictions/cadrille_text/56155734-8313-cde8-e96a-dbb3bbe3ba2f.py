import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-40,-40))
r=w0.sketch().segment((26,-58),(26,-57)).segment((28,-57)).arc((29,-56),(30,-57)).segment((32,-57)).arc((28,-54),(26,-58)).assemble().finalize().extrude(80).union(w0.sketch().push([(0,1)]).circle(5).circle(4,mode='s').finalize().extrude(80)).union(w0.sketch().push([(0,1)]).circle(3).circle(2,mode='s').finalize().extrude(80))