import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-25,-25))
w1=cq.Workplane('XY',origin=(-100,-25,-25))
r=w0.sketch().segment((92,-25),(100,-25)).segment((100,-18)).close().assemble().finalize().extrude(51).union(w1.workplane(offset=51/2).moveTo(0,25).cylinder(51,2))