import cadquery as cq
w0=cq.Workplane('XY',origin=(-50,0,-100))
r=w0.sketch().segment((-50,15),(-50,19)).arc((-49,17),(-47,15)).close().assemble().reset().face(w0.sketch().arc((47,-19),(49,-17),(50,-15)).segment((50,-15)).arc((49,-17),(47,-19)).assemble()).finalize().extrude(200)