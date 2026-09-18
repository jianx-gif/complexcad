import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-67,-67))
r=w0.sketch().segment((29,-57),(33,-57)).segment((33,-54)).arc((31,-56),(29,-57)).assemble().finalize().extrude(109).union(w0.sketch().push([(0,6)]).circle(3).circle(2,mode='s').finalize().extrude(134)).union(w0.workplane(offset=134/2).moveTo(0,6).cylinder(134,3))