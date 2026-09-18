import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-31,-21))
r=w0.sketch().segment((29,-58),(31,-58)).segment((31,-57)).arc((30,-57),(29,-58)).assemble().finalize().extrude(-14).union(w0.sketch().push([(30,-30)]).circle(3).push([(30,-30.5)]).rect(4,3,mode='s').finalize().extrude(49)).union(w0.workplane(offset=96/2).moveTo(30,-30).cylinder(96,2))