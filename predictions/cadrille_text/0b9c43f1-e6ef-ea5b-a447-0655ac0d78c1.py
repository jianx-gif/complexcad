import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-17,-17))
r=w0.sketch().segment((29,-58),(33,-58)).segment((33,-55)).arc((31,-56),(29,-58)).assemble().finalize().extrude(-22).union(w0.sketch().push([(31,-15)]).circle(3).push([(31,-14.5)]).rect(4,3,mode='s').finalize().extrude(43)).union(w0.sketch().push([(31,-15)]).circle(3).push([(31,-14.5)]).rect(4,3,mode='s').finalize().extrude(117))