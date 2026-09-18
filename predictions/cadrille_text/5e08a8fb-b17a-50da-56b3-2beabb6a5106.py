import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-33,-27))
r=w0.sketch().segment((29,-58),(33,-58)).segment((33,-42)).arc((31,-43),(29,-42)).close().assemble().finalize().extrude(54).union(w0.sketch().push([(31,-31)]).circle(2).push([(95,-31)]).rect(10,28).finalize().extrude(55))