import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-17,-8))
r=w0.sketch().segment((29,-58),(33,-58)).segment((33,-55)).arc((31,-56),(29,-58)).assemble().finalize().extrude(-28).union(w0.sketch().push([(31,0)]).circle(29).circle(19,mode='s').finalize().extrude(16)).union(w0.workplane(offset=108/2).moveTo(31,0).cylinder(108,2))