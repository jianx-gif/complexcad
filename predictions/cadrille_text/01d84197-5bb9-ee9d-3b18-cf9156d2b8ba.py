import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-33))
r=w0.sketch().segment((28,-58),(33,-58)).segment((33,-47)).arc((31,-53),(28,-58)).assemble().finalize().extrude(-33).union(w0.workplane(offset=67/2).moveTo(31,-5).cylinder(67,29)).union(w0.sketch().push([(31,-5)]).circle(2).push([(98,-5)]).rect(4,54).finalize().extrude(133))