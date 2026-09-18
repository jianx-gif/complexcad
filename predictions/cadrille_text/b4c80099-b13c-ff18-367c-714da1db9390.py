import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((29,-58),(33,-58)).segment((33,-50)).arc((31,-50),(29,-51)).close().assemble().finalize().extrude(99).union(w0.sketch().push([(31,-50)]).circle(2).push([(98,-50)]).rect(4,2).finalize().extrude(100))