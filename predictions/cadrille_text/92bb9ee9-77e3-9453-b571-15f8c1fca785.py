import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-40,-40))
r=w0.sketch().segment((28,-58),(28,-57)).segment((30,-57)).arc((33,-56),(36,-57)).segment((38,-57)).arc((33,-54),(28,-58)).assemble().finalize().extrude(79).union(w0.sketch().push([(0,40)]).circle(4).push([(0,39.5)]).rect(4,5,mode='s').finalize().extrude(80)).union(w0.workplane(offset=80/2).moveTo(0,40).cylinder(80,2))