import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-11))
r=w0.sketch().segment((29,-58),(33,-58)).segment((33,-42)).arc((31,-50),(29,-58)).assemble().finalize().extrude(-39).union(w0.workplane(offset=111/2).moveTo(0,5).cylinder(111,2)).union(w0.workplane(offset=111/2).moveTo(0,5).cylinder(111,3))