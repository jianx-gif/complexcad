import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-86,0))
r=w0.workplane(offset=18/2).cylinder(18,100).union(w0.sketch().arc((-81,-19),(0,-82),(81,-19)).segment((77,-19)).arc((0,-79),(-77,-19)).close().assemble().reset().face(w0.sketch().segment((-81,19),(-77,19)).arc((0,79),(77,19)).segment((81,19)).arc((0,82),(-81,19)).assemble()).finalize().extrude(186))