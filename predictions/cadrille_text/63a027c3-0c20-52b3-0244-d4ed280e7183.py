import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-25,-25))
r=w0.sketch().segment((28,-58),(28,-57)).segment((30,-57)).arc((33,-56),(36,-57)).segment((38,-57)).arc((33,-54),(28,-58)).assemble().finalize().extrude(50).union(w0.sketch().push([(0,17)]).circle(10).push([(0,16.5)]).rect(14,11,mode='s').finalize().extrude(50))