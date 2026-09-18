import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-58,0))
r=w0.sketch().push([(6,7)]).circle(94).circle(92,mode='s').finalize().extrude(-2).union(w0.sketch().arc((1,5),(16,2),(29,-5)).arc((30,28),(1,5)).assemble().finalize().extrude(118))