import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-25,-11))
r=w0.sketch().segment((29,-58),(33,-58)).segment((33,-47)).arc((31,-53),(29,-58)).assemble().finalize().extrude(-3).union(w0.sketch().push([(31,0)]).circle(3).circle(2,mode='s').finalize().extrude(23)).union(w0.sketch().push([(31,0)]).circle(69).circle(67,mode='s').finalize().extrude(27))