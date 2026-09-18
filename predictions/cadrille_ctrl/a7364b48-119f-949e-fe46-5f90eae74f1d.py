import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
r=w0.sketch().segment((-40,-20),(-33,-20)).arc((-36,-17),(-40,-14)).close().assemble().finalize().extrude(-10).union(w0.sketch().segment((-40,-19),(-33,-19)).arc((-36,-17),(-40,-14)).close().assemble().reset().face(w0.sketch().segment((-39,10),(-33,10)).arc((-36,13),(-39,16)).close().assemble()).reset().face(w0.sketch().segment((19,-25),(40,-25)).segment((40,25)).segment((19,25)).arc((21,0),(19,-25)).assemble()).finalize().extrude(-8)).union(w0.sketch().push([(27,0)]).circle(14).circle(13,mode='s').finalize().extrude(-8))
