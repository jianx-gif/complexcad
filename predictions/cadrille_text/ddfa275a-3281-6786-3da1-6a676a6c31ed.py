import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-25,-3))
r=w0.sketch().segment((29,-58),(33,-58)).segment((33,-55)).arc((31,-56),(29,-58)).assemble().finalize().extrude(-31).union(w0.sketch().push([(31,-24)]).circle(2).push([(31,-24.5)]).rect(2,3,mode='s').finalize().extrude(38)).union(w0.workplane(offset=38/2).moveTo(31,-24).cylinder(38,2))