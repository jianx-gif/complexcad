import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-11))
r=w0.sketch().segment((29,-58),(33,-58)).segment((33,-55)).arc((31,-56),(29,-58)).assemble().finalize().extrude(-33).union(w0.sketch().push([(31,-5)]).circle(2).push([(31,-5.5)]).rect(2,3,mode='s').finalize().extrude(65)).union(w0.workplane(offset=111/2).moveTo(31,-5).cylinder(111,2))