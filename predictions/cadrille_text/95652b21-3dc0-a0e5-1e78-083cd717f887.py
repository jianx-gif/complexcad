import cadquery as cq
w0=cq.Workplane('XY',origin=(-87,0,-16))
r=w0.sketch().segment((29,-58),(33,-58)).segment((33,-48)).arc((31,-53),(29,-58)).assemble().finalize().extrude(-2).union(w0.sketch().push([(31,0)]).circle(2).circle(1,mode='s').finalize().extrude(24)).union(w0.workplane(offset=32/2).moveTo(31,0).cylinder(32,2))