import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
w1=cq.Workplane('XY',origin=(0,0,4))
r=w0.sketch().segment((-40,-25),(-18,-25)).arc((-30,-20),(-40,-11)).close().assemble().reset().face(w0.sketch().arc((-40,11),(-30,20),(-18,25)).segment((-40,25)).close().assemble()).reset().face(w0.sketch().segment((18,-25),(40,-25)).segment((40,-11)).arc((30,-20),(18,-25)).assemble()).reset().face(w0.sketch().arc((18,25),(30,20),(40,11)).segment((40,25)).close().assemble()).finalize().extrude(-12).union(w1.sketch().push([(12,0)]).circle(25).push([(12.5,0)]).rect(29,12,mode='s').finalize().extrude(-4))
