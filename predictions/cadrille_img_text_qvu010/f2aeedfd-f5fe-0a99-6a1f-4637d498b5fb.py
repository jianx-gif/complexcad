import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-77,-19),(19,77)).arc((-1,72),(-19,64)).segment((-19,32)).segment((-44,32)).arc((-58,13),(-77,1)).close().assemble().reset().face(w0.sketch().arc((-19,-77),(1,-72),(19,-64)).segment((19,-32)).segment((44,-32)).segment((77,-1)).segment((-19,-77)).close().assemble()).finalize().extrude(-200)