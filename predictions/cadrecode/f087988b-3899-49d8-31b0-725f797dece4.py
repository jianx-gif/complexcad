import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-22))
r=w0.sketch().segment((-32,-95),(-30,-95)).arc((0,-100),(30,-95)).segment((32,-95)).segment((32,-94)).arc((100,0),(32,94)).segment((32,95)).segment((30,95)).arc((0,100),(-30,95)).segment((-32,95)).segment((-32,94)).arc((-100,0),(-32,-94)).close().assemble().finalize().extrude(25).union(w0.workplane(offset=45/2).cylinder(45,38))