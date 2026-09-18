import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-35,-25))
r=w0.sketch().segment((-97,25),(-96,25)).segment((-96,28)).close().assemble().reset().face(w0.sketch().segment((96,-28),(97,-25)).segment((96,-25)).close().assemble()).finalize().extrude(50).union(w0.workplane(offset=51/2).cylinder(51,8))