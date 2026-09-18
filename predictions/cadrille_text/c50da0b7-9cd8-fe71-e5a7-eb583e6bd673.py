import cadquery as cq
w0=cq.Workplane('XY',origin=(-20,-25,-100))
r=w0.sketch().segment((24,-58),(24,-57)).segment((27,-57)).arc((20,-52),(24,-58)).assemble().finalize().extrude(200)