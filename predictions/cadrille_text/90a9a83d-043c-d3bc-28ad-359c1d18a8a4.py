import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((29,-58),(33,-58)).segment((33,-55)).arc((31,-56),(29,-58)).assemble().finalize().extrude(100).union(w0.sketch().push([(31,-5)]).circle(2).push([(98,-5)]).rect(4,2).finalize().extrude(100))