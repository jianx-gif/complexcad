import cadquery as cq
w0=cq.Workplane('XY',origin=(-75,-25,-100))
r=w0.sketch().segment((69,-25),(69,25)).arc((33,0),(69,-25)).assemble().finalize().extrude(200)