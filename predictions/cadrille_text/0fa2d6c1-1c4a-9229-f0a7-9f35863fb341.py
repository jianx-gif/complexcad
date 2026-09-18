import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((29,-58),(33,-58)).segment((33,-55)).arc((31,-56),(29,-58)).assemble().finalize().extrude(99).union(w0.sketch().push([(31,-50)]).circle(2).push([(31,-50.5)]).rect(2,3,mode='s').finalize().extrude(100))