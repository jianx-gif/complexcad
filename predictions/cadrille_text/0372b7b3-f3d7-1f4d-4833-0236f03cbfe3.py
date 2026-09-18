import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-40,-40))
r=w0.sketch().segment((29,-58),(33,-58)).segment((33,-55)).arc((31,-56),(29,-58)).assemble().finalize().extrude(80).union(w0.workplane(offset=80/2).moveTo(0,1).cylinder(80,3)).union(w0.workplane(offset=81/2).moveTo(0,1).box(200,2,81))