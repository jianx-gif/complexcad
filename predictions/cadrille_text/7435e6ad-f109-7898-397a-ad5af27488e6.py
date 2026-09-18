import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-21,-21))
r=w0.sketch().segment((29,-58),(33,-58)).segment((33,-55)).arc((31,-56),(29,-58)).assemble().finalize().extrude(-20).union(w0.sketch().push([(31,-20)]).circle(2).push([(95,-20)]).rect(10,2).finalize().extrude(101))