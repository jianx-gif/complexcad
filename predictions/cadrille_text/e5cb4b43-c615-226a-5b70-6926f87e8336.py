import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-25,-10))
r=w0.sketch().segment((29,-58),(33,-58)).segment((33,-57)).arc((31,-57),(29,-58)).assemble().finalize().extrude(-8).union(w0.sketch().push([(31,-25)]).circle(2).push([(31,-24.5)]).rect(2,3,mode='s').finalize().extrude(25)).union(w0.sketch().push([(31,-25)]).circle(2).push([(95,-25)]).circle(5).finalize().extrude(28))