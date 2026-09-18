import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-51))
r=w0.sketch().segment((26,-58),(26,-57)).segment((28,-57)).arc((33,-53),(37,-57)).segment((39,-57)).arc((33,-52),(26,-58)).assemble().finalize().extrude(81).union(w0.sketch().push([(0,9)]).circle(3).circle(2,mode='s').finalize().extrude(102)).union(w0.workplane(offset=103/2).moveTo(0,9).cylinder(103,3))