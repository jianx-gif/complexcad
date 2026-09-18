import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-33))
r=w0.sketch().segment((29,-58),(33,-58)).segment((33,-55)).arc((31,-56),(29,-58)).assemble().finalize().extrude(-36).union(w0.sketch().push([(31,0)]).circle(3).circle(2,mode='s').finalize().extrude(103)).union(w0.workplane(offset=133/2).moveTo(31,0).cylinder(133,2))