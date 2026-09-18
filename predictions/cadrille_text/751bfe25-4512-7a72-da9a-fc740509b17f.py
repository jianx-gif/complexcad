import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-10,-10))
r=w0.sketch().segment((29,-58),(33,-58)).segment((33,-42)).arc((31,-50),(29,-58)).assemble().finalize().extrude(-8).union(w0.sketch().push([(31,0)]).circle(31).push([(31.5,0)]).rect(3,44,mode='s').finalize().extrude(10)).union(w0.workplane(offset=27/2).moveTo(31,0).cylinder(27,2))