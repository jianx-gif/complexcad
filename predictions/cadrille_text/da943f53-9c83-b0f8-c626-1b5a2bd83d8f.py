import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((28,-58),(32,-58)).segment((32,-48)).arc((30,-53),(28,-58)).assemble().finalize().extrude(99).union(w0.sketch().push([(0,50)]).circle(5).push([(0,49.5)]).rect(6,7,mode='s').finalize().extrude(100)).union(w0.workplane(offset=100/2).moveTo(0,50).cylinder(100,2))