import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.workplane(offset=-15/2).moveTo(0,-1).cylinder(15,9).union(w0.sketch().segment((-20,3),(-15,-15)).segment((20,-3)).segment((15,15)).close().assemble().finalize().extrude(16)).union(w0.sketch().segment((-21,3),(-16,-1)).arc((-10,-14),(4,-19)).segment((4,-16)).arc((-11,-10),(-16,6)).segment((-17,6)).close().assemble().reset().face(w0.sketch().arc((-4,16),(11,10),(16,-6)).segment((17,-6)).segment((21,-3)).segment((16,1)).arc((10,14),(-4,19)).close().assemble()).finalize().extrude(60))
