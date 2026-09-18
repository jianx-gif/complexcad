import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,0,-100))
w1=cq.Workplane('XY',origin=(-25,0,-100))
r=w0.sketch().face(w0.sketch().segment((91,-19),(97,-19)).segment((97,-16)).close().assemble()).finalize().extrude(200).union(w1.sketch().face(w1.sketch().segment((0,0),(0,25)).arc((-1,1),(15,-18)).segment((15,-25)).segment((25,-25)).arc((40,-27),(54,-25)).segment((57,-25)).segment((57,-23)).arc((57,19),(15,25)).segment((15,0)).close().assemble()).finalize().extrude(110))