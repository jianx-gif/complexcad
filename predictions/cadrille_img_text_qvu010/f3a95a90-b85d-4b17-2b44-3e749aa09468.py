import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-68))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().arc((-81,-1),(-21,-39),(40,-10)).segment((35,-10)).arc((-21,-36),(-77,-1)).close().assemble().reset().face(w0.sketch().segment((-81,39),(-77,39)).arc((-21,65),(35,39)).segment((40,39)).arc((-21,81),(-81,39)).assemble()).finalize().extrude(168).union(w1.sketch().segment((-35,-5),(81,-5)).segment((81,5)).segment((77,5)).segment((77,3)).segment((74,3)).segment((74,5)).segment((-35,5)).close().assemble().finalize().extrude(158))