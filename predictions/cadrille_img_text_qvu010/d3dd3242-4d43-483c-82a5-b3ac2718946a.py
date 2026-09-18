import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-94,-67),(-77,-67)).arc((0,-99),(77,-67)).segment((94,-67)).segment((94,-62)).segment((-94,-62)).close().assemble().reset().face(w0.sketch().segment((-94,62),(94,62)).segment((94,67)).segment((77,67)).arc((0,99),(-77,67)).segment((-94,67)).close().assemble()).finalize().extrude(-200)